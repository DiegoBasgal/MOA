from pathlib import Path
import sys
import threading
from math import floor
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from .gui import Ui_Form

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

    def sincro(self):
        try:
            segundos = floor(self.shared_dict['GLB']['tempo_simul'] % 60)
            minutos = floor((self.shared_dict['GLB']['tempo_simul'] / 60) % 60)
            horas = floor(self.shared_dict['GLB']['tempo_simul'] / 3600)
            self.label_tempo_simul.setText(f"{horas:02d}:{minutos:02d}:{segundos:02d}")

            self.lcdNumber_tensao_linha.display(self.shared_dict['USN']['tensao_na_linha'])
            self.lcdNumber_potencia_se.display(f"{self.shared_dict['USN']['potencia_kw_se'] / 1000:1.3f}")
            self.lcdNumber_MP.display(f"{self.shared_dict['USN']['potencia_kw_mp'] / 1000:1.3f}")
            self.lcdNumber_MR.display(f"{self.shared_dict['USN']['potencia_kw_mr'] / 1000:1.3f}")

            self.checkBox_sinal_trip_condic_usina.setChecked(self.shared_dict['USN']['trip_condic_usina'])

            self.checkBox_52L_aberto.setChecked(self.shared_dict['DJ']['dj52L_aberto'])
            self.checkBox_52L_fechado.setChecked(self.shared_dict['DJ']['dj52L_fechado'])
            self.checkBox_52L_inconsistente.setChecked(self.shared_dict['DJ']['dj52L_inconsistente'])
            self.checkBox_52L_trip.setChecked(self.shared_dict['DJ']['dj52L_trip'])
            self.checkBox_52L_mola_carregada.setChecked(self.shared_dict['DJ']['dj52L_mola_carregada'])
            self.checkBox_52L_falta_vcc.setChecked(self.shared_dict['DJ']['dj52L_falta_vcc'])
            self.checkBox_52L_condicao_fechamento.setChecked(self.shared_dict['DJ']['dj52L_condicao_de_fechamento'])

            self.lcdNumber_nv_montante.display(f"{self.shared_dict['USN']['nv_montante']:3.2f}")
            self.lcdNumber_q_alfuente.display(f"{self.shared_dict['USN']['q_alfuente']:2.3f}")
            self.lcdNumber_q_liquida.display(f"{self.shared_dict['USN']['q_liquida']:2.3f}")
            self.lcdNumber_q_sanitaria.display(f"{self.shared_dict['USN']['q_sanitaria']:2.3f}")
            self.lcdNumber_q_vertimento.display(f"{self.shared_dict['USN']['q_vertimento']:2.3f}")

            self.checkBox_sinal_trip_ug1.setChecked(self.shared_dict['UG']['trip_ug1'])
            self.checkBox_sinal_trip_condic_ug1.setChecked(self.shared_dict['UG']['trip_condic_ug1'])

            self.lcdNumber_potencia_ug1.display(f"{self.shared_dict['UG']['potencia_kw_ug1']:1.3f}")
            self.lcdNumber_setpoint_ug1.display(f"{self.shared_dict['UG']['setpoint_kw_ug1']:1.3f}")

            if self.shared_dict['UG']['etapa_alvo_ug1'] is None:
                self.lcdNumber_etapa_alvo_ug1.setHexMode()
                self.lcdNumber_etapa_alvo_ug1.display(15)

            else:
                self.lcdNumber_etapa_alvo_ug1.setDecMode()
                self.lcdNumber_etapa_alvo_ug1.display(f"{self.shared_dict['UG']['etapa_alvo_ug1']:d}")

            self.lcdNumber_etapa_atual_ug1.display(f"{self.shared_dict['UG']['etapa_atual_ug1']:d}")
            self.lcdNumber_bitsalarme_ug1.display(f"{self.shared_dict['UG']['flags_ug1']:08b}")
            self.lcdNumber_q_ug1.display(f"{self.shared_dict['UG']['q_ug1']:2.3f}")
            self.lcdNumber_pressao_turbina_ug1.display(f"{self.shared_dict['UG']['pressao_turbina_ug1']:2.2f}")
            self.lcdNumber_temperatura_ug1_fase_r.display(f"{self.shared_dict['UG']['temperatura_ug1_fase_r']:03.1f}")
            self.lcdNumber_temperatura_ug1_fase_s.display(f"{self.shared_dict['UG']['temperatura_ug1_fase_s']:03.1f}")
            self.lcdNumber_temperatura_ug1_fase_t.display(f"{self.shared_dict['UG']['temperatura_ug1_fase_t']:03.1f}")
            self.lcdNumber_temperatura_ug1_nucleo_gerador_1.display(f"{self.shared_dict['UG']['temperatura_ug1_nucleo_gerador_1']:03.1f}")
            self.lcdNumber_temperatura_ug1_mancal_guia.display(f"{self.shared_dict['UG']['temperatura_ug1_mancal_guia']:03.1f}")
            self.lcdNumber_temperatura_ug1_mancal_guia_interno_1.display(f"{self.shared_dict['UG']['temperatura_ug1_mancal_guia_interno_1']:03.1f}")
            self.lcdNumber_temperatura_ug1_mancal_guia_interno_2.display(f"{self.shared_dict['UG']['temperatura_ug1_mancal_guia_interno_2']:03.1f}")
            self.lcdNumber_temperatura_ug1_patins_mancal_comb_1.display(f"{self.shared_dict['UG']['temperatura_ug1_patins_mancal_comb_1']:03.1f}")
            self.lcdNumber_temperatura_ug1_patins_mancal_comb_2.display(f"{self.shared_dict['UG']['temperatura_ug1_patins_mancal_comb_2']:03.1f}")
            self.lcdNumber_temperatura_ug1_mancal_casq_comb.display(f"{self.shared_dict['UG']['temperatura_ug1_mancal_casq_comb']:03.1f}")
            self.lcdNumber_temperatura_ug1_mancal_con_esc_comb.display(f"{self.shared_dict['UG']['temperatura_ug1_mancal_contra_esc_comb']:03.1f}")
            self.lcdNumber_perda_na_grade_ug1.display(f"{self.shared_dict['USN']['nv_montante'] - self.shared_dict['USN']['nv_jusante_grade']:03.1f}")
            
            self.checkBox_sinal_trip_ug2.setChecked(self.shared_dict['UG']['trip_ug2'])
            self.checkBox_sinal_trip_condic_ug2.setChecked(self.shared_dict['UG']['trip_condic_ug2'])

            self.lcdNumber_potencia_ug2.display(f"{self.shared_dict['UG']['potencia_kw_ug2']:1.3f}")
            self.lcdNumber_setpoint_ug2.display(f"{self.shared_dict['UG']['setpoint_kw_ug2']:1.3f}")

            if self.shared_dict['UG']['etapa_alvo_ug2'] is None:
                self.lcdNumber_etapa_alvo_ug2.setHexMode()
                self.lcdNumber_etapa_alvo_ug2.display(15)

            else:
                self.lcdNumber_etapa_alvo_ug2.setDecMode()
                self.lcdNumber_etapa_alvo_ug2.display(f"{self.shared_dict['UG']['etapa_alvo_ug2']:d}")

            self.lcdNumber_etapa_atual_ug2.display(f"{self.shared_dict['UG']['etapa_atual_ug2']:d}")
            self.lcdNumber_bitsalarme_ug2.display(f"{self.shared_dict['UG']['flags_ug2']:08b}")
            self.lcdNumber_q_ug2.display(f"{self.shared_dict['UG']['q_ug2']:2.3f}")
            self.lcdNumber_pressao_turbina_ug2.display(f"{self.shared_dict['UG']['pressao_turbina_ug2']:2.2f}")
            self.lcdNumber_temperatura_ug2_fase_r.display(f"{self.shared_dict['UG']['temperatura_ug2_fase_r']:03.1f}")
            self.lcdNumber_temperatura_ug2_fase_s.display(f"{self.shared_dict['UG']['temperatura_ug2_fase_s']:03.1f}")
            self.lcdNumber_temperatura_ug2_fase_t.display(f"{self.shared_dict['UG']['temperatura_ug2_fase_t']:03.1f}")
            self.lcdNumber_temperatura_ug2_nucleo_gerador_1.display(f"{self.shared_dict['UG']['temperatura_ug2_nucleo_gerador_1']:03.1f}")
            self.lcdNumber_temperatura_ug2_mancal_guia.display(f"{self.shared_dict['UG']['temperatura_ug2_mancal_guia']:03.1f}")
            self.lcdNumber_temperatura_ug2_mancal_guia_interno_1.display(f"{self.shared_dict['UG']['temperatura_ug2_mancal_guia_interno_1']:03.1f}")
            self.lcdNumber_temperatura_ug2_mancal_guia_interno_2.display(f"{self.shared_dict['UG']['temperatura_ug2_mancal_guia_interno_2']:03.1f}")
            self.lcdNumber_temperatura_ug2_patins_mancal_comb_1.display(f"{self.shared_dict['UG']['temperatura_ug2_patins_mancal_comb_1']:03.1f}")
            self.lcdNumber_temperatura_ug2_patins_mancal_comb_2.display(f"{self.shared_dict['UG']['temperatura_ug2_patins_mancal_comb_2']:03.1f}")
            self.lcdNumber_temperatura_ug2_mancal_casq_comb.display(f"{self.shared_dict['UG']['temperatura_ug2_mancal_casq_comb']:03.1f}")
            self.lcdNumber_temperatura_ug2_mancal_con_esc_comb.display(f"{self.shared_dict['UG']['temperatura_ug2_mancal_contra_esc_comb']:03.1f}")
            self.lcdNumber_perda_na_grade_ug2.display(f"{self.shared_dict['USN']['nv_montante'] - self.shared_dict['USN']['nv_jusante_grade']:3.1f}")

            self.progressBar_comporta_ug1.setValue(self.shared_dict['UG']["progresso_ug1"])
            self.progressBar_comporta_ug2.setValue(self.shared_dict['UG']["progresso_ug2"])

            if self.shared_dict['UG']["limpa_grades_operando"]:
                self.lcdNumber_status_limpa_grades.display("O")
            else:
                self.lcdNumber_status_limpa_grades.display("P")

            if self.shared_dict['UG']["comporta_aberta_ug1"]:
                self.lcdNumber_status_comporta_ug1.display("A")
            elif self.shared_dict['UG']["comporta_fechada_ug1"]:
                self.lcdNumber_status_comporta_ug1.display("F")
            elif self.shared_dict['UG']["comporta_cracking_ug1"]:
                self.lcdNumber_status_comporta_ug1.display("C")
            else:
                self.lcdNumber_status_comporta_ug1.display("-")

            if self.shared_dict['UG']["comporta_aberta_ug2"]:
                self.lcdNumber_status_comporta_ug2.display("A")
            elif self.shared_dict['UG']["comporta_fechada_ug2"]:
                self.lcdNumber_status_comporta_ug2.display("F")
            elif self.shared_dict['UG']["comporta_cracking_ug2"]:
                self.lcdNumber_status_comporta_ug2.display("C")
            else:
                self.lcdNumber_status_comporta_ug2.display("-")

        except Exception as e:
            print("A", repr(e))
            pass

    def closeEvent(self, event):
        self.shared_dict['GLB']["stop_sim"] = True
        self.sinc_timer.stop()
        return super().closeEvent(event)

    def mudar_q_afluente(self):
        self.shared_dict["q_alfuente"] = (10 ** (self.horizontalSlider_q_afluente.value() / 75) - 1) * 2

    def mudar_press_turbina(self):
        if self.shared_dict['UG']["set_press_turbina_ug1"] == True:
            self.shared_dict['UG']["pressao_turbina_ug1"] = self.horizontalSlider_press_turbina.value() *0.01
            if self.shared_dict['UG']["pressao_turbina_ug1"] == 15.49:
                self.shared_dict['UG']["pressao_turbina_ug1"] = 16.2
        if self.shared_dict['UG']["set_press_turbina_ug2"] == True:
            self.shared_dict['UG']["pressao_turbina_ug2"] = self.horizontalSlider_press_turbina.value() * 0.01
            if self.shared_dict['UG']["pressao_turbina_ug2"] == 15.49:
                self.shared_dict['UG']["pressao_turbina_ug2"] = 16.2
    
    def set_trip_condic_usina(self):
        self.shared_dict['USN']["trip_condic_usina"] = True

    def reset_trip_condic_usina(self):
        self.shared_dict['USN']["trip_condic_usina"] = False
    
    def reset_geral_condic_usina(self):
        self.shared_dict['USN']["reset_geral_condic"] = True
        self.shared_dict['USN']["trip_condic_usina"] = False
        self.shared_dict['UG']["trip_condic_ug1"] = False
        self.shared_dict['UG']["trip_condic_ug2"] = False
        
        QTimer.singleShot(1000, self.aux_reset_geral_condic_usina)
    
    def aux_reset_geral_condic_usina(self):
        self.shared_dict['USN']["reset_geral_condic"] = False

    def pulse_trip_linha(self):
        self.set_trip_linha()
        QTimer.singleShot(2000, self.reset_trip_linha)
    
    def set_trip_linha(self):
        self.shared_dict['DJ']["tensao_na_linha"] = 0

    def reset_trip_linha(self):
        self.shared_dict['DJ']["tensao_na_linha"] = 23100

    def pulse_trip_52L(self):
        self.set_trip_52L()
        QTimer.singleShot(2000, self.reset_trip_52L)

    def set_trip_52L(self):
        self.shared_dict['DJ']["trip_52L"] = True

    def reset_trip_52L(self):
        self.shared_dict['DJ']["trip_52L"] = False

    # ug1
    def pulso_trip_ug1(self):
        self.set_trip_high_ug1()
        QTimer.singleShot(2000, self.set_trip_low_ug1)

    def set_trip_high_ug1(self):
        self.shared_dict['UG']["trip_ug1"] = True

    def set_trip_low_ug1(self):
        self.shared_dict['UG']["trip_ug1"] = False

    def set_trip_condic_ug1(self):
        self.shared_dict['UG']["trip_condic_ug1"] = True

    def reset_trip_condic_ug1(self):
        self.shared_dict['UG']["trip_condic_ug1"] = False

    def reconhece_reset_ug1(self):
        self.shared_dict['UG']["reconhece_reset_ug1"] = True

    def partir_ug1(self):
        self.shared_dict['UG']["debug_partir_ug1"] = True
        print("partir ug1 GUI")

    def parar_ug1(self):
        self.shared_dict['UG']["debug_parar_ug1"] = True

    def mudar_setpoint_ug1(self):
        self.shared_dict['UG']["debug_setpoint_kw_ug1"] = self.horizontalSlider_setpoint_ug1.value()

    def set_press_turbina_ug1(self):
        if self.shared_dict['UG']["set_press_turbina_ug1"] == False:
            self.horizontalSlider_press_turbina.setValue(1549)
            self.shared_dict['UG']["set_press_turbina_ug1"] = True
            self.lcdNumber_pressao_turbina_ug1.setFrameShadow(QFrame.Plain)
            self.shared_dict['UG']["set_press_turbina_ug2"] = False
            self.lcdNumber_pressao_turbina_ug2.setFrameShadow(QFrame.Sunken)
        elif self.shared_dict['UG']["set_press_turbina_ug1"] == True:
            self.shared_dict['UG']["set_press_turbina_ug1"] = False
            self.horizontalSlider_press_turbina.setValue(1549)
            self.lcdNumber_pressao_turbina_ug1.setFrameShadow(QFrame.Sunken)
    
    def set_thread_comp_aberta_ug1(self):
        self.shared_dict['UG']["thread_comp_aberta_ug1"] = True
    
    def set_thread_comp_fechada_ug1(self):
        self.shared_dict['UG']["thread_comp_fechada_ug1"] = True
    
    def set_thread_comp_cracking_ug1(self):
        self.shared_dict['UG']["thread_comp_cracking_ug1"] = True
    
    def equalizar_cracking_ug1(self):
        if self.shared_dict['UG']["comporta_cracking_ug1"]:
            self.shared_dict['UG']["equalizar_ug1"] = True
        else:
            print("Não é possível equalizar a unidade pois ela não está na posição de cracking!")

    # ug2
    def pulso_trip_ug2(self):
        self.set_trip_high_ug2()
        QTimer.singleShot(2000, self.set_trip_low_ug2)

    def set_trip_high_ug2(self):
        self.shared_dict['UG']["trip_ug2"] = True

    def set_trip_low_ug2(self):
        self.shared_dict['UG']["trip_ug2"] = False

    def set_trip_condic_ug2(self):
        self.shared_dict['UG']["trip_condic_ug2"] = True

    def reset_trip_condic_ug2(self):
        self.shared_dict['UG']["trip_condic_ug2"] = False

    def reconhece_reset_ug2(self):
        self.shared_dict['UG']["reconhece_reset_ug2"] = True

    def partir_ug2(self):
        self.shared_dict['UG']["debug_partir_ug2"] = True
        print("partir ug2 GUI")

    def parar_ug2(self):
        self.shared_dict['UG']["debug_parar_ug2"] = True

    def mudar_setpoint_ug2(self):
        self.shared_dict['UG']["debug_setpoint_kw_ug2"] = self.horizontalSlider_setpoint_ug2.value()

    def set_press_turbina_ug2(self):
        if self.shared_dict['UG']["set_press_turbina_ug2"] == False:
            self.horizontalSlider_press_turbina.setValue(1549)
            self.shared_dict['UG']["set_press_turbina_ug1"] = False
            self.lcdNumber_pressao_turbina_ug1.setFrameShadow(QFrame.Sunken)
            self.shared_dict['UG']["set_press_turbina_ug2"] = True
            self.lcdNumber_pressao_turbina_ug2.setFrameShadow(QFrame.Plain)
        elif self.shared_dict['UG']["set_press_turbina_ug2"] == True:
            self.shared_dict['UG']["set_press_turbina_ug2"] = False
            self.horizontalSlider_press_turbina.setValue(1549)
            self.lcdNumber_pressao_turbina_ug2.setFrameShadow(QFrame.Sunken)

    def set_thread_comp_aberta_ug2(self):
        self.shared_dict['UG']["thread_comp_aberta_ug2"] = True
    
    def set_thread_comp_fechada_ug2(self):
        self.shared_dict['UG']["thread_comp_fechada_ug2"] = True
    
    def set_thread_comp_cracking_ug2(self):
        self.shared_dict['UG']["thread_comp_cracking_ug2"] = True
    
    def equalizar_cracking_ug2(self):
        if self.shared_dict['UG']["comporta_cracking_ug2"]:
            self.shared_dict['UG']["equalizar_ug2"] = True
        else:
            print("Não é possível equalizar a unidade pois ela não está na posição de cracking!")

    # dj52L
    def alternar_estado_dj52L(self):
        if self.shared_dict['DJ']['dj52L_aberto']:
            self.shared_dict['DJ']["debug_dj52L_fechar"] = True
        if self.shared_dict['DJ']['dj52L_fechado']:
            self.shared_dict['DJ']["debug_dj52L_abrir"] = True

    def provocar_inconsistencia_dj52L(self):
        self.shared_dict['DJ']["debug_dj52L_abrir"] = True
        self.shared_dict['DJ']["debug_dj52L_fechar"] = True

    def reconhecer_reset_dj52L(self):
        self.shared_dict['DJ']["debug_dj52L_reconhece_reset"] = True

    # limpa grades

    def operar_limpa_grades(self):
        if self.shared_dict['UG']["comporta_operando_ug1"] == True or self.shared_dict['UG']["comporta_operando_ug2"] == True:
            print("Não é possível operar o limpa grades pois as comportas estão em operação")
        elif self.shared_dict['UG']["limpa_grades_operando"] == False:
            self.shared_dict['UG']["limpa_grades_operando"] = True
        else:
            print("O limpa grades já está em operação.")
    
    def parar_limpa_grades(self):
        if self.shared_dict['UG']["comporta_operando_ug1"] == True or self.shared_dict['UG']["comporta_operando_ug2"] == True:
            print("Não é possível parar o limpa grades pois as comportas estão em operação")
        elif self.shared_dict['UG']["limpa_grades_operando"] == True:
            self.shared_dict['UG']["limpa_grades_operando"] = False
        else:
            print("O limpa grades já está parado.")

def start_gui(shared_dict):
    app = QApplication(sys.argv)
    win = Window(shared_dict)
    win.show()
    app.exec()
