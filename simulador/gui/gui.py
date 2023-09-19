import sys
import threading

from math import floor
from pathlib import Path
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

from .ui import Ui_Form


lock = threading.Lock()


class Window(QMainWindow, Ui_Form):
    def __init__(self, dict_comp: "dict") -> "None":
        super().__init__()
        self.setupUi(self)

        self.dict = dict_comp

        self.sinc_timer = QTimer()
        self.sinc_timer.setInterval(100)
        self.sinc_timer.timeout.connect(self.sincro)
        self.sinc_timer.start()


    def sincro(self) -> "None":
        try:
            # Temporizador
            horas = floor(self.dict["GLB"]["tempo_simul"] / 3600)
            minutos = floor((self.dict["GLB"]["tempo_simul"] / 60) % 60)
            segundos = floor(self.dict["GLB"]["tempo_simul"] % 60)
            self.label_tempo_hms.setText(f"{horas:02d}:{minutos:02d}:{segundos:02d}")

            # Serviço Auxiliar
            self.checkBox_sinal_condic_usn.setChecked(self.dict["SA"]["condicionador"])

            # Subestação
            self.lcdNumber_tensao_linha.display(f"{self.dict['SE']['tensao_linha']}")
            self.lcdNumber_MP.display(f"{(self.dict['SE']['potencia_mp'])}")
            self.lcdNumber_MR.display(f"{(self.dict['SE']['potencia_mr'])}")
            self.lcdNumber_potencia_se.display(f"{(self.dict['SE']['potencia_se'])}")

            self.checkBox_dj_trip.setChecked(self.dict["SE"]["dj_trip"])
            self.checkBox_dj_aberto.setChecked(self.dict["SE"]["dj_aberto"])
            self.checkBox_dj_fechado.setChecked(self.dict["SE"]["dj_fechado"])
            self.checkBox_dj_condicao.setChecked(self.dict["SE"]["dj_condicao"])
            self.checkBox_dj_mola.setChecked(self.dict["SE"]["dj_mola_carregada"])
            self.checkBox_dj_falta_vcc.setChecked(self.dict["SE"]["dj_falta_vcc"])
            self.checkBox_dj_inconsistente.setChecked(self.dict["SE"]["dj_inconsistente"])

            # Tomada da Água
            self.lcdNumber_montante.display(f"{self.dict['TDA']['nv_montante']:3.2f}")
            self.lcdNumber_q_liquida.display(f"{self.dict['TDA']['q_liquida']:2.3f}")
            self.lcdNumber_q_alfuente.display(f"{self.dict['TDA']['q_afluente']:2.3f}")
            self.lcdNumber_q_sanitaria.display(f"{self.dict['TDA']['q_sanitaria']:2.3f}")
            self.lcdNumber_q_vertimento.display(f"{self.dict['TDA']['q_vertimento']:2.3f}")

            # Unidades de Geração
            # UG1
            self.checkBox_sinal_trip_ug1.setChecked(self.dict["UG1"]["trip"])
            self.checkBox_sinal_condic_ug1.setChecked(self.dict["UG1"]["condicionador"])

            if self.dict["UG1"]["etapa_alvo"] is None:
                self.lcdNumber_etapa_alvo_ug1.setHexMode()
                self.lcdNumber_etapa_alvo_ug1.display(15)

            else:
                self.lcdNumber_etapa_alvo_ug1.setDecMode()
                self.lcdNumber_etapa_alvo_ug1.display(f"{self.dict['UG1']['etapa_alvo']:d}")

            self.lcdNumber_q_ug1.display(f"{self.dict['UG1']['q']:2.3f}")
            self.lcdNumber_etapa_atual_ug1.display(f"{self.dict['UG1']['etapa_atual']:d}")
            self.lcdNumber_potencia_ug1.display(f"{self.dict['UG1']['potencia']}")
            self.lcdNumber_setpoint_ug1.display(f"{self.dict['UG1']['setpoint']}")
            self.lcdNumber_perda_grade_ug1.display(f"{(self.dict['TDA']['nv_montante'] - self.dict['TDA']['nv_jusante_grade']):03.1f}")

            self.lcdNumber_pressao_cx_espiral_ug1.display(f"{self.dict['UG1']['pressao_cx_espiral']:03.1f}")

            self.lcdNumber_temp_1_ug1.display(f"{self.dict['UG1']['tmp_fase_r']:03.1f}")
            self.lcdNumber_temp_2_ug1.display(f"{self.dict['UG1']['tmp_fase_s']:03.1f}")
            self.lcdNumber_temp_3_ug1.display(f"{self.dict['UG1']['tmp_fase_t']:03.1f}")
            self.lcdNumber_temp_4_ug1.display(f"{self.dict['UG1']['tmp_nucleo_estator']:03.1f}")
            self.lcdNumber_temp_5_ug1.display(f"{self.dict['UG1']['tmp_mancal_radial_dia_1']:03.1f}")
            self.lcdNumber_temp_6_ug1.display(f"{self.dict['UG1']['tmp_mancal_radial_dia_2']:03.1f}")
            self.lcdNumber_temp_7_ug1.display(f"{self.dict['UG1']['tmp_mancal_radial_tra_1']:03.1f}")
            self.lcdNumber_temp_8_ug1.display(f"{self.dict['UG1']['tmp_mancal_radial_tra_2']:03.1f}")
            self.lcdNumber_temp_9_ug1.display(f"{self.dict['UG1']['tmp_mancal_guia_escora']:03.1f}")
            self.lcdNumber_temp_10_ug1.display(f"{self.dict['UG1']['tmp_mancal_guia_radial']:03.1f}")
            self.lcdNumber_temp_11_ug1.display(f"{self.dict['UG1']['tmp_mancal_guia_contra_escora']:03.1f}")

            # UG2
            self.checkBox_sinal_trip_ug2.setChecked(self.dict["UG2"]["trip"])
            self.checkBox_sinal_condic_ug2.setChecked(self.dict["UG2"]["condicionador"])

            if self.dict["UG2"]["etapa_alvo"] is None:
                self.lcdNumber_etapa_alvo_ug2.setHexMode()
                self.lcdNumber_etapa_alvo_ug2.display(15)

            else:
                self.lcdNumber_etapa_alvo_ug2.setDecMode()
                self.lcdNumber_etapa_alvo_ug2.display(f"{self.dict['UG2']['etapa_alvo']:d}")

            self.lcdNumber_q_ug2.display(f"{self.dict['UG2']['q']:2.3f}")
            self.lcdNumber_etapa_atual_ug2.display(f"{self.dict['UG2']['etapa_atual']:d}")
            self.lcdNumber_potencia_ug2.display(f"{self.dict['UG2']['potencia']}")
            self.lcdNumber_setpoint_ug2.display(f"{self.dict['UG2']['setpoint']}")
            self.lcdNumber_perda_grade_ug2.display(f"{(self.dict['TDA']['nv_montante'] - self.dict['TDA']['nv_jusante_grade']):03.1f}")

            self.lcdNumber_pressao_cx_espiral_ug2.display(f"{self.dict['UG2']['pressao_cx_espiral']:03.1f}")

            self.lcdNumber_temp_1_ug2.display(f"{self.dict['UG2']['tmp_fase_r']:03.1f}")
            self.lcdNumber_temp_2_ug2.display(f"{self.dict['UG2']['tmp_fase_s']:03.1f}")
            self.lcdNumber_temp_3_ug2.display(f"{self.dict['UG2']['tmp_fase_t']:03.1f}")
            self.lcdNumber_temp_4_ug2.display(f"{self.dict['UG2']['tmp_nucleo_estator']:03.1f}")
            self.lcdNumber_temp_5_ug2.display(f"{self.dict['UG2']['tmp_mancal_radial_dia_1']:03.1f}")
            self.lcdNumber_temp_6_ug2.display(f"{self.dict['UG2']['tmp_mancal_radial_dia_2']:03.1f}")
            self.lcdNumber_temp_7_ug2.display(f"{self.dict['UG2']['tmp_mancal_radial_tra_1']:03.1f}")
            self.lcdNumber_temp_8_ug2.display(f"{self.dict['UG2']['tmp_mancal_radial_tra_2']:03.1f}")
            self.lcdNumber_temp_9_ug2.display(f"{self.dict['UG2']['tmp_mancal_guia_escora']:03.1f}")
            self.lcdNumber_temp_10_ug2.display(f"{self.dict['UG2']['tmp_mancal_guia_radial']:03.1f}")
            self.lcdNumber_temp_11_ug2.display(f"{self.dict['UG2']['tmp_mancal_guia_contra_escora']:03.1f}")

            # UG3
            self.checkBox_sinal_trip_ug3.setChecked(self.dict["UG3"]["trip"])
            self.checkBox_sinal_condic_ug3.setChecked(self.dict["UG3"]["condicionador"])

            if self.dict["UG3"]["etapa_alvo"] is None:
                self.lcdNumber_etapa_alvo_ug3.setHexMode()
                self.lcdNumber_etapa_alvo_ug3.display(15)

            else:
                self.lcdNumber_etapa_alvo_ug3.setDecMode()
                self.lcdNumber_etapa_alvo_ug3.display(f"{self.dict['UG3']['etapa_alvo']:d}")

            self.lcdNumber_q_ug3.display(f"{self.dict['UG3']['q']:2.3f}")
            self.lcdNumber_etapa_atual_ug3.display(f"{self.dict['UG3']['etapa_atual']:d}")
            self.lcdNumber_potencia_ug3.display(f"{self.dict['UG3']['potencia']}")
            self.lcdNumber_setpoint_ug3.display(f"{self.dict['UG3']['setpoint']}")
            self.lcdNumber_perda_grade_ug3.display(f"{(self.dict['TDA']['nv_montante'] - self.dict['TDA']['nv_jusante_grade']):03.1f}")

            self.lcdNumber_pressao_cx_espiral_ug3.display(f"{self.dict['UG3']['pressao_cx_espiral']:03.1f}")

            self.lcdNumber_temp_1_ug3.display(f"{self.dict['UG3']['tmp_fase_r']:03.1f}")
            self.lcdNumber_temp_2_ug3.display(f"{self.dict['UG3']['tmp_fase_s']:03.1f}")
            self.lcdNumber_temp_3_ug3.display(f"{self.dict['UG3']['tmp_fase_t']:03.1f}")
            self.lcdNumber_temp_4_ug3.display(f"{self.dict['UG3']['tmp_nucleo_estator']:03.1f}")
            self.lcdNumber_temp_5_ug3.display(f"{self.dict['UG3']['tmp_mancal_radial_dia_1']:03.1f}")
            self.lcdNumber_temp_6_ug3.display(f"{self.dict['UG3']['tmp_mancal_radial_dia_2']:03.1f}")
            self.lcdNumber_temp_7_ug3.display(f"{self.dict['UG3']['tmp_mancal_radial_tra_1']:03.1f}")
            self.lcdNumber_temp_8_ug3.display(f"{self.dict['UG3']['tmp_mancal_radial_tra_2']:03.1f}")
            self.lcdNumber_temp_9_ug3.display(f"{self.dict['UG3']['tmp_mancal_guia_escora']:03.1f}")
            self.lcdNumber_temp_10_ug3.display(f"{self.dict['UG3']['tmp_mancal_guia_radial']:03.1f}")
            self.lcdNumber_temp_11_ug3.display(f"{self.dict['UG3']['tmp_mancal_guia_contra_escora']:03.1f}")


        except Exception as e:
            print(e)
            pass


    def closeEvent(self, event):
        self.dict["GLB"]["stop_sim"] = True
        self.sinc_timer.stop()
        return super().closeEvent(event)


    # tomada da Água
    def mudar_q_afluente(self):
        self.dict["TDA"]["q_afluente"] = (10 ** (self.horizontalSlider_q_afluente.value() / 75) - 1) * 2


    # Geral Usina
    def trip_condic_usina(self):
        self.dict["SA"]["condicionador"] = True


    def reset_condic_usina(self):
        self.dict["SA"]["condicionador"] = False


    def reset_geral_condics(self):
        self.dict["GLB"]["reset_condicionadores"] = True
        self.dict["SA"]["condicionador"] = False
        self.dict["UG1"]["condicionador"] = False
        self.dict["UG2"]["condicionador"] = False
        self.dict["UG3"]["condicionador"] = False

        QTimer.singleShot(1000, self.aux_reset_geral_condic_usina)


    def aux_reset_geral_condic_usina(self):
        self.dict["GLB"]["reset_condicionadores"] = False


    # Subestação
    def pulse_trip_linha(self):
        self.set_trip_linha()
        QTimer.singleShot(2000, self.reset_trip_linha)


    def set_trip_linha(self):
        self.dict["SE"]["tensao_linha"] = 0


    def reset_trip_linha(self):
        self.dict["SE"]["tensao_linha"] = 69000


    def set_trip_52L(self):
        self.dict["SE"]["dj_trip"] = True


    def reset_trip_52L(self):
        self.dict["SE"]["dj_trip"] = False


    def abrir_fechar_dj(self):
        if self.dict["SE"]["dj_aberto"]:
            self.dict["SE"]["debug_dj_abrir"] = False
            self.dict["SE"]["debug_dj_fechar"] = True

        elif self.dict["SE"]["dj_fechado"]:
            self.dict["SE"]["debug_dj_abrir"] = True
            self.dict["SE"]["debug_dj_fechar"] = False


    def inconsistencia_dj(self):
        self.dict["SE"]["debug_dj_abrir"] = True
        self.dict["SE"]["debug_dj_fechar"] = True


    def reset_dj(self):
        self.dict["SE"]["debug_dj_reconhece_reset"] = True


    # Unidades de Geração
    # UG1
    def partir_ug1(self):
        self.dict["UG1"]["debug_partir"] = True


    def parar_ug1(self):
        self.dict["UG1"]["debug_parar"] = True


    def trip_ug1(self):
        self.dict["UG1"]["trip"] = True


    def reset_ug1(self):
        self.dict["UG1"]["trip"] = False
        self.dict["UG1"]["reconhece_reset"] = True


    def trip_condic_ug1(self):
        self.dict["UG1"]["condicionador"] = True


    def reset_condic_ug1(self):
        self.dict["UG1"]["condicionador"] = False


    def mudar_setpoint_ug1(self):
        self.dict["UG1"]["debug_setpoint"] = self.horizontalSlider_setpoint_ug1.value()


    # UG2
    def partir_ug2(self):
        self.dict["UG2"]["debug_partir"] = True


    def parar_ug2(self):
        self.dict["UG2"]["debug_parar"] = True


    def trip_ug2(self):
        self.dict["UG2"]["trip"] = True


    def reset_ug2(self):
        self.dict["UG2"]["trip"] = False
        self.dict["UG2"]["reconhece_reset"] = True


    def trip_condic_ug2(self):
        self.dict["UG2"]["condicionador"] = True


    def reset_condic_ug2(self):
        self.dict["UG2"]["condicionador"] = False


    def mudar_setpoint_ug2(self):
        self.dict["UG2"]["debug_setpoint"] = self.horizontalSlider_setpoint_ug2.value()


    # UG3
    def partir_ug3(self):
        self.dict["UG3"]["debug_partir"] = True


    def parar_ug3(self):
        self.dict["UG3"]["debug_parar"] = True


    def trip_ug3(self):
        self.dict["UG3"]["trip"] = True


    def reset_ug3(self):
        self.dict["UG3"]["trip"] = False
        self.dict["UG3"]["reconhece_reset"] = True


    def trip_condic_ug3(self):
        self.dict["UG3"]["condicionador"] = True


    def reset_condic_ug3(self):
        self.dict["UG3"]["condicionador"] = False


    def mudar_setpoint_ug3(self):
        self.dict["UG3"]["debug_setpoint"] = self.horizontalSlider_setpoint_ug3.value()


def start_gui(dict_comp):
    app = QApplication(sys.argv)
    win = Window(dict_comp)
    win.show()
    app.exec()
