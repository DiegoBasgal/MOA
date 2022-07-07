# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'geralZbQkNA.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QGridLayout,
    QHBoxLayout,
    QLCDNumber,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSlider,
    QSplitter,
    QVBoxLayout,
    QWidget,
)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(1280, 720)
        Form.setMinimumSize(QSize(1280, 720))
        Form.setMaximumSize(QSize(1280, 720))
        self.bg = QLabel(Form)
        self.bg.setObjectName("bg")
        self.bg.setGeometry(QRect(0, 0, 1280, 720))
        font = QFont()
        font.setPointSize(10)
        self.bg.setFont(font)
        self.bg.setPixmap(QPixmap("imgs/bg.png"))
        self.bg.setScaledContents(True)
        self.label = QLabel(Form)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(0, 20, 1271, 31))
        font1 = QFont()
        font1.setPointSize(24)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)
        self.layoutWidget_3 = QWidget(Form)
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(960, 400, 177, 284))
        self.verticalLayout_52L = QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_52L.setObjectName("verticalLayout_52L")
        self.verticalLayout_52L.setContentsMargins(0, 0, 0, 0)
        self.label_52L = QLabel(self.layoutWidget_3)
        self.label_52L.setObjectName("label_52L")
        self.label_52L.setFont(font)
        self.label_52L.setAlignment(Qt.AlignCenter)

        self.verticalLayout_52L.addWidget(self.label_52L)

        self.checkBox_52L_aberto = QCheckBox(self.layoutWidget_3)
        self.checkBox_52L_aberto.setObjectName("checkBox_52L_aberto")

        self.verticalLayout_52L.addWidget(self.checkBox_52L_aberto)

        self.checkBox_52L_fechado = QCheckBox(self.layoutWidget_3)
        self.checkBox_52L_fechado.setObjectName("checkBox_52L_fechado")

        self.verticalLayout_52L.addWidget(self.checkBox_52L_fechado)

        self.checkBox_52L_inconsistente = QCheckBox(self.layoutWidget_3)
        self.checkBox_52L_inconsistente.setObjectName("checkBox_52L_inconsistente")

        self.verticalLayout_52L.addWidget(self.checkBox_52L_inconsistente)

        self.checkBox_52L_trip = QCheckBox(self.layoutWidget_3)
        self.checkBox_52L_trip.setObjectName("checkBox_52L_trip")

        self.verticalLayout_52L.addWidget(self.checkBox_52L_trip)

        self.checkBox_52L_mola_carregada = QCheckBox(self.layoutWidget_3)
        self.checkBox_52L_mola_carregada.setObjectName("checkBox_52L_mola_carregada")

        self.verticalLayout_52L.addWidget(self.checkBox_52L_mola_carregada)

        self.checkBox_52L_falta_vcc = QCheckBox(self.layoutWidget_3)
        self.checkBox_52L_falta_vcc.setObjectName("checkBox_52L_falta_vcc")

        self.verticalLayout_52L.addWidget(self.checkBox_52L_falta_vcc)

        self.checkBox_52L_condicao_fechamento = QCheckBox(self.layoutWidget_3)
        self.checkBox_52L_condicao_fechamento.setObjectName(
            "checkBox_52L_condicao_fechamento"
        )

        self.verticalLayout_52L.addWidget(self.checkBox_52L_condicao_fechamento)

        self.pushButton_52L_alternar_estado = QPushButton(self.layoutWidget_3)
        self.pushButton_52L_alternar_estado.setObjectName(
            "pushButton_52L_alternar_estado"
        )

        self.verticalLayout_52L.addWidget(self.pushButton_52L_alternar_estado)

        self.pushButton_52L_provocar_inconsistencia = QPushButton(self.layoutWidget_3)
        self.pushButton_52L_provocar_inconsistencia.setObjectName(
            "pushButton_52L_provocar_inconsistencia"
        )

        self.verticalLayout_52L.addWidget(self.pushButton_52L_provocar_inconsistencia)

        self.pushButton_52L_reconhece_reset = QPushButton(self.layoutWidget_3)
        self.pushButton_52L_reconhece_reset.setObjectName(
            "pushButton_52L_reconhece_reset"
        )

        self.verticalLayout_52L.addWidget(self.pushButton_52L_reconhece_reset)

        self.layoutWidget_15 = QWidget(Form)
        self.layoutWidget_15.setObjectName("layoutWidget_15")
        self.layoutWidget_15.setGeometry(QRect(900, 260, 96, 50))
        self.verticalLayout_SE = QVBoxLayout(self.layoutWidget_15)
        self.verticalLayout_SE.setObjectName("verticalLayout_SE")
        self.verticalLayout_SE.setContentsMargins(0, 0, 0, 0)
        self.label_se = QLabel(self.layoutWidget_15)
        self.label_se.setObjectName("label_se")
        font2 = QFont()
        font2.setPointSize(12)
        self.label_se.setFont(font2)
        self.label_se.setAlignment(Qt.AlignCenter)

        self.verticalLayout_SE.addWidget(self.label_se)

        self.lcdNumber_potencia_se = QLCDNumber(self.layoutWidget_15)
        self.lcdNumber_potencia_se.setObjectName("lcdNumber_potencia_se")
        font3 = QFont()
        font3.setBold(False)
        self.lcdNumber_potencia_se.setFont(font3)
        self.lcdNumber_potencia_se.setAutoFillBackground(True)
        self.lcdNumber_potencia_se.setSmallDecimalPoint(True)
        self.lcdNumber_potencia_se.setDigitCount(5)
        self.lcdNumber_potencia_se.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_potencia_se.setProperty("value", 1.234000000000000)

        self.verticalLayout_SE.addWidget(self.lcdNumber_potencia_se)

        self.layoutWidget_4 = QWidget(Form)
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(670, 530, 191, 151))
        self.gridLayout_ug2 = QGridLayout(self.layoutWidget_4)
        self.gridLayout_ug2.setObjectName("gridLayout_ug2")
        self.gridLayout_ug2.setContentsMargins(0, 0, 0, 0)
        self.label_potencia_ug2 = QLabel(self.layoutWidget_4)
        self.label_potencia_ug2.setObjectName("label_potencia_ug2")
        self.label_potencia_ug2.setFont(font)

        self.gridLayout_ug2.addWidget(self.label_potencia_ug2, 0, 0, 1, 1)

        self.lcdNumber_potencia_ug2 = QLCDNumber(self.layoutWidget_4)
        self.lcdNumber_potencia_ug2.setObjectName("lcdNumber_potencia_ug2")
        self.lcdNumber_potencia_ug2.setAutoFillBackground(True)
        self.lcdNumber_potencia_ug2.setSmallDecimalPoint(True)
        self.lcdNumber_potencia_ug2.setDigitCount(4)
        self.lcdNumber_potencia_ug2.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_potencia_ug2.setProperty("value", 5.123000000000000)

        self.gridLayout_ug2.addWidget(self.lcdNumber_potencia_ug2, 0, 1, 1, 1)

        self.label_setpoint_ug2 = QLabel(self.layoutWidget_4)
        self.label_setpoint_ug2.setObjectName("label_setpoint_ug2")
        self.label_setpoint_ug2.setFont(font)

        self.gridLayout_ug2.addWidget(self.label_setpoint_ug2, 1, 0, 1, 1)

        self.label_etapa_ug2 = QLabel(self.layoutWidget_4)
        self.label_etapa_ug2.setObjectName("label_etapa_ug2")
        self.label_etapa_ug2.setFont(font)

        self.gridLayout_ug2.addWidget(self.label_etapa_ug2, 2, 0, 1, 1)

        self.label_bitsalarme_ug2 = QLabel(self.layoutWidget_4)
        self.label_bitsalarme_ug2.setObjectName("label_bitsalarme_ug2")
        self.label_bitsalarme_ug2.setFont(font)

        self.gridLayout_ug2.addWidget(self.label_bitsalarme_ug2, 3, 0, 1, 1)

        self.label_q_ug2 = QLabel(self.layoutWidget_4)
        self.label_q_ug2.setObjectName("label_q_ug2")
        self.label_q_ug2.setFont(font)
        self.label_q_ug2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.gridLayout_ug2.addWidget(self.label_q_ug2, 4, 0, 1, 1)

        self.lcdNumber_setpoint_ug2 = QLCDNumber(self.layoutWidget_4)
        self.lcdNumber_setpoint_ug2.setObjectName("lcdNumber_setpoint_ug2")
        self.lcdNumber_setpoint_ug2.setAutoFillBackground(True)
        self.lcdNumber_setpoint_ug2.setSmallDecimalPoint(True)
        self.lcdNumber_setpoint_ug2.setDigitCount(4)
        self.lcdNumber_setpoint_ug2.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_setpoint_ug2.setProperty("value", 5.100000000000000)

        self.gridLayout_ug2.addWidget(self.lcdNumber_setpoint_ug2, 1, 1, 1, 1)

        self.lcdNumber_bitsalarme_ug2 = QLCDNumber(self.layoutWidget_4)
        self.lcdNumber_bitsalarme_ug2.setObjectName("lcdNumber_bitsalarme_ug2")
        self.lcdNumber_bitsalarme_ug2.setAutoFillBackground(True)
        self.lcdNumber_bitsalarme_ug2.setSmallDecimalPoint(False)
        self.lcdNumber_bitsalarme_ug2.setDigitCount(5)
        self.lcdNumber_bitsalarme_ug2.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_bitsalarme_ug2.setProperty("value", 65356.000000000000000)

        self.gridLayout_ug2.addWidget(self.lcdNumber_bitsalarme_ug2, 3, 1, 1, 1)

        self.lcdNumber_q_ug2 = QLCDNumber(self.layoutWidget_4)
        self.lcdNumber_q_ug2.setObjectName("lcdNumber_q_ug2")
        self.lcdNumber_q_ug2.setAutoFillBackground(True)
        self.lcdNumber_q_ug2.setSmallDecimalPoint(True)
        self.lcdNumber_q_ug2.setDigitCount(4)
        self.lcdNumber_q_ug2.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_q_ug2.setProperty("value", 12.340000000000000)

        self.gridLayout_ug2.addWidget(self.lcdNumber_q_ug2, 4, 1, 1, 1)

        self.splitter_2 = QSplitter(self.layoutWidget_4)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.lcdNumber_etapa_atual_ug2 = QLCDNumber(self.splitter_2)
        self.lcdNumber_etapa_atual_ug2.setObjectName("lcdNumber_etapa_atual_ug2")
        self.lcdNumber_etapa_atual_ug2.setAutoFillBackground(True)
        self.lcdNumber_etapa_atual_ug2.setSmallDecimalPoint(False)
        self.lcdNumber_etapa_atual_ug2.setDigitCount(1)
        self.lcdNumber_etapa_atual_ug2.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_etapa_atual_ug2.setProperty("value", 1.000000000000000)
        self.splitter_2.addWidget(self.lcdNumber_etapa_atual_ug2)
        self.lcdNumber_etapa_alvo_ug2 = QLCDNumber(self.splitter_2)
        self.lcdNumber_etapa_alvo_ug2.setObjectName("lcdNumber_etapa_alvo_ug2")
        self.lcdNumber_etapa_alvo_ug2.setAutoFillBackground(True)
        self.lcdNumber_etapa_alvo_ug2.setSmallDecimalPoint(False)
        self.lcdNumber_etapa_alvo_ug2.setDigitCount(1)
        self.lcdNumber_etapa_alvo_ug2.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_etapa_alvo_ug2.setProperty("value", 1.000000000000000)
        self.splitter_2.addWidget(self.lcdNumber_etapa_alvo_ug2)

        self.gridLayout_ug2.addWidget(self.splitter_2, 2, 1, 1, 1)

        self.layoutWidget = QWidget(Form)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(1060, 110, 151, 52))
        self.horizontalLayout_MPMR = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_MPMR.setObjectName("horizontalLayout_MPMR")
        self.horizontalLayout_MPMR.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_MP = QVBoxLayout()
        self.verticalLayout_MP.setObjectName("verticalLayout_MP")
        self.label_MP = QLabel(self.layoutWidget)
        self.label_MP.setObjectName("label_MP")
        self.label_MP.setFont(font2)
        self.label_MP.setAlignment(Qt.AlignCenter)

        self.verticalLayout_MP.addWidget(self.label_MP)

        self.lcdNumber_MP = QLCDNumber(self.layoutWidget)
        self.lcdNumber_MP.setObjectName("lcdNumber_MP")
        self.lcdNumber_MP.setFont(font3)
        self.lcdNumber_MP.setAutoFillBackground(True)
        self.lcdNumber_MP.setSmallDecimalPoint(True)
        self.lcdNumber_MP.setDigitCount(5)
        self.lcdNumber_MP.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_MP.setProperty("value", 1.234000000000000)

        self.verticalLayout_MP.addWidget(self.lcdNumber_MP)

        self.horizontalLayout_MPMR.addLayout(self.verticalLayout_MP)

        self.verticalLayout_MR = QVBoxLayout()
        self.verticalLayout_MR.setObjectName("verticalLayout_MR")
        self.label_MR = QLabel(self.layoutWidget)
        self.label_MR.setObjectName("label_MR")
        self.label_MR.setFont(font2)
        self.label_MR.setAlignment(Qt.AlignCenter)

        self.verticalLayout_MR.addWidget(self.label_MR)

        self.lcdNumber_MR = QLCDNumber(self.layoutWidget)
        self.lcdNumber_MR.setObjectName("lcdNumber_MR")
        self.lcdNumber_MR.setFont(font3)
        self.lcdNumber_MR.setAutoFillBackground(True)
        self.lcdNumber_MR.setSmallDecimalPoint(True)
        self.lcdNumber_MR.setDigitCount(5)
        self.lcdNumber_MR.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_MR.setProperty("value", 1.234000000000000)

        self.verticalLayout_MR.addWidget(self.lcdNumber_MR)

        self.horizontalLayout_MPMR.addLayout(self.verticalLayout_MR)

        self.layoutWidget1 = QWidget(Form)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(50, 240, 141, 83))
        self.layoutWidget1.setFont(font3)
        self.layoutWidget1.setAutoFillBackground(False)
        self.gridLayout_q = QGridLayout(self.layoutWidget1)
        self.gridLayout_q.setObjectName("gridLayout_q")
        self.gridLayout_q.setContentsMargins(0, 0, 0, 0)
        self.label_q_sanitaria = QLabel(self.layoutWidget1)
        self.label_q_sanitaria.setObjectName("label_q_sanitaria")
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        self.label_q_sanitaria.setFont(font4)
        self.label_q_sanitaria.setAutoFillBackground(False)
        self.label_q_sanitaria.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

        self.gridLayout_q.addWidget(self.label_q_sanitaria, 1, 0, 1, 1)

        self.lcdNumber_q_liquida = QLCDNumber(self.layoutWidget1)
        self.lcdNumber_q_liquida.setObjectName("lcdNumber_q_liquida")
        self.lcdNumber_q_liquida.setFont(font3)
        self.lcdNumber_q_liquida.setAutoFillBackground(True)
        self.lcdNumber_q_liquida.setSmallDecimalPoint(True)
        self.lcdNumber_q_liquida.setDigitCount(5)
        self.lcdNumber_q_liquida.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_q_liquida.setProperty("value", 12.340000000000000)

        self.gridLayout_q.addWidget(self.lcdNumber_q_liquida, 0, 1, 1, 1)

        self.lcdNumber_q_vertimento = QLCDNumber(self.layoutWidget1)
        self.lcdNumber_q_vertimento.setObjectName("lcdNumber_q_vertimento")
        self.lcdNumber_q_vertimento.setFont(font3)
        self.lcdNumber_q_vertimento.setAutoFillBackground(True)
        self.lcdNumber_q_vertimento.setSmallDecimalPoint(True)
        self.lcdNumber_q_vertimento.setDigitCount(5)
        self.lcdNumber_q_vertimento.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_q_vertimento.setProperty("value", 12.340000000000000)

        self.gridLayout_q.addWidget(self.lcdNumber_q_vertimento, 2, 1, 1, 1)

        self.label_q_liquida = QLabel(self.layoutWidget1)
        self.label_q_liquida.setObjectName("label_q_liquida")
        self.label_q_liquida.setFont(font4)
        self.label_q_liquida.setAutoFillBackground(False)
        self.label_q_liquida.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

        self.gridLayout_q.addWidget(self.label_q_liquida, 0, 0, 1, 1)

        self.label_q_vertimento = QLabel(self.layoutWidget1)
        self.label_q_vertimento.setObjectName("label_q_vertimento")
        self.label_q_vertimento.setFont(font4)
        self.label_q_vertimento.setAutoFillBackground(False)
        self.label_q_vertimento.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

        self.gridLayout_q.addWidget(self.label_q_vertimento, 2, 0, 1, 1)

        self.lcdNumber_q_sanitaria = QLCDNumber(self.layoutWidget1)
        self.lcdNumber_q_sanitaria.setObjectName("lcdNumber_q_sanitaria")
        self.lcdNumber_q_sanitaria.setFont(font3)
        self.lcdNumber_q_sanitaria.setAutoFillBackground(True)
        self.lcdNumber_q_sanitaria.setSmallDecimalPoint(True)
        self.lcdNumber_q_sanitaria.setDigitCount(5)
        self.lcdNumber_q_sanitaria.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_q_sanitaria.setProperty("value", 12.340000000000000)

        self.gridLayout_q.addWidget(self.lcdNumber_q_sanitaria, 1, 1, 1, 1)

        self.layoutWidget2 = QWidget(Form)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(50, 350, 321, 336))
        self.layoutWidget2.setFont(font)
        self.gridLayout_vars_ug = QGridLayout(self.layoutWidget2)
        self.gridLayout_vars_ug.setObjectName("gridLayout_vars_ug")
        self.gridLayout_vars_ug.setContentsMargins(0, 0, 0, 0)
        self.label_temperatura_titulo = QLabel(self.layoutWidget2)
        self.label_temperatura_titulo.setObjectName("label_temperatura_titulo")
        self.label_temperatura_titulo.setFont(font)

        self.gridLayout_vars_ug.addWidget(self.label_temperatura_titulo, 0, 0, 1, 1)

        self.label_ug1 = QLabel(self.layoutWidget2)
        self.label_ug1.setObjectName("label_ug1")
        self.label_ug1.setFont(font)
        self.label_ug1.setAlignment(Qt.AlignCenter)

        self.gridLayout_vars_ug.addWidget(self.label_ug1, 0, 1, 1, 1)

        self.label_ug2 = QLabel(self.layoutWidget2)
        self.label_ug2.setObjectName("label_ug2")
        self.label_ug2.setFont(font)
        self.label_ug2.setAlignment(Qt.AlignCenter)

        self.gridLayout_vars_ug.addWidget(self.label_ug2, 0, 2, 1, 1)

        self.label_temperatura_1 = QLabel(self.layoutWidget2)
        self.label_temperatura_1.setObjectName("label_temperatura_1")
        self.label_temperatura_1.setFont(font)

        self.gridLayout_vars_ug.addWidget(self.label_temperatura_1, 1, 0, 1, 1)

        self.lcdNumber_temperatura_ug1_fase_r = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug1_fase_r.setObjectName(
            "lcdNumber_temperatura_ug1_fase_r"
        )
        self.lcdNumber_temperatura_ug1_fase_r.setFont(font4)
        self.lcdNumber_temperatura_ug1_fase_r.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug1_fase_r.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug1_fase_r.setDigitCount(5)
        self.lcdNumber_temperatura_ug1_fase_r.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug1_fase_r.setProperty("value", 12.340000000000000)

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug1_fase_r, 1, 1, 1, 1
        )

        self.lcdNumber_temperatura_ug2_fase_r = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug2_fase_r.setObjectName(
            "lcdNumber_temperatura_ug2_fase_r"
        )
        self.lcdNumber_temperatura_ug2_fase_r.setFont(font4)
        self.lcdNumber_temperatura_ug2_fase_r.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug2_fase_r.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug2_fase_r.setDigitCount(5)
        self.lcdNumber_temperatura_ug2_fase_r.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug2_fase_r.setProperty("value", 12.340000000000000)

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug2_fase_r, 1, 2, 1, 1
        )

        self.label_temperatura_2 = QLabel(self.layoutWidget2)
        self.label_temperatura_2.setObjectName("label_temperatura_2")
        self.label_temperatura_2.setFont(font)

        self.gridLayout_vars_ug.addWidget(self.label_temperatura_2, 2, 0, 1, 1)

        self.lcdNumber_temperatura_ug1_fase_s = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug1_fase_s.setObjectName(
            "lcdNumber_temperatura_ug1_fase_s"
        )
        self.lcdNumber_temperatura_ug1_fase_s.setFont(font4)
        self.lcdNumber_temperatura_ug1_fase_s.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug1_fase_s.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug1_fase_s.setDigitCount(5)
        self.lcdNumber_temperatura_ug1_fase_s.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug1_fase_s.setProperty("value", 12.340000000000000)

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug1_fase_s, 2, 1, 1, 1
        )

        self.lcdNumber_temperatura_ug2_fase_s = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug2_fase_s.setObjectName(
            "lcdNumber_temperatura_ug2_fase_s"
        )
        self.lcdNumber_temperatura_ug2_fase_s.setFont(font4)
        self.lcdNumber_temperatura_ug2_fase_s.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug2_fase_s.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug2_fase_s.setDigitCount(5)
        self.lcdNumber_temperatura_ug2_fase_s.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug2_fase_s.setProperty("value", 12.340000000000000)

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug2_fase_s, 2, 2, 1, 1
        )

        self.label_temperatura_3 = QLabel(self.layoutWidget2)
        self.label_temperatura_3.setObjectName("label_temperatura_3")
        self.label_temperatura_3.setFont(font)

        self.gridLayout_vars_ug.addWidget(self.label_temperatura_3, 3, 0, 1, 1)

        self.lcdNumber_temperatura_ug1_fase_t = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug1_fase_t.setObjectName(
            "lcdNumber_temperatura_ug1_fase_t"
        )
        self.lcdNumber_temperatura_ug1_fase_t.setFont(font4)
        self.lcdNumber_temperatura_ug1_fase_t.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug1_fase_t.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug1_fase_t.setDigitCount(5)
        self.lcdNumber_temperatura_ug1_fase_t.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug1_fase_t.setProperty("value", 12.340000000000000)

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug1_fase_t, 3, 1, 1, 1
        )

        self.lcdNumber_temperatura_ug2_fase_t = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug2_fase_t.setObjectName(
            "lcdNumber_temperatura_ug2_fase_t"
        )
        self.lcdNumber_temperatura_ug2_fase_t.setFont(font4)
        self.lcdNumber_temperatura_ug2_fase_t.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug2_fase_t.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug2_fase_t.setDigitCount(5)
        self.lcdNumber_temperatura_ug2_fase_t.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug2_fase_t.setProperty("value", 12.340000000000000)

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug2_fase_t, 3, 2, 1, 1
        )

        self.label_temperatura_4 = QLabel(self.layoutWidget2)
        self.label_temperatura_4.setObjectName("label_temperatura_4")
        self.label_temperatura_4.setFont(font)

        self.gridLayout_vars_ug.addWidget(self.label_temperatura_4, 4, 0, 1, 1)

        self.lcdNumber_temperatura_ug1_la_casquilho = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug1_la_casquilho.setObjectName(
            "lcdNumber_temperatura_ug1_la_casquilho"
        )
        self.lcdNumber_temperatura_ug1_la_casquilho.setFont(font4)
        self.lcdNumber_temperatura_ug1_la_casquilho.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug1_la_casquilho.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug1_la_casquilho.setDigitCount(5)
        self.lcdNumber_temperatura_ug1_la_casquilho.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug1_la_casquilho.setProperty(
            "value", 12.340000000000000
        )

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug1_la_casquilho, 4, 1, 1, 1
        )

        self.lcdNumber_temperatura_ug2_la_casquilho = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug2_la_casquilho.setObjectName(
            "lcdNumber_temperatura_ug2_la_casquilho"
        )
        self.lcdNumber_temperatura_ug2_la_casquilho.setFont(font4)
        self.lcdNumber_temperatura_ug2_la_casquilho.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug2_la_casquilho.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug2_la_casquilho.setDigitCount(5)
        self.lcdNumber_temperatura_ug2_la_casquilho.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug2_la_casquilho.setProperty(
            "value", 12.340000000000000
        )

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug2_la_casquilho, 4, 2, 1, 1
        )

        self.label_temperatura_5 = QLabel(self.layoutWidget2)
        self.label_temperatura_5.setObjectName("label_temperatura_5")
        self.label_temperatura_5.setFont(font)

        self.gridLayout_vars_ug.addWidget(self.label_temperatura_5, 5, 0, 1, 1)

        self.lcdNumber_temperatura_ug1_lna_casquilho = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug1_lna_casquilho.setObjectName(
            "lcdNumber_temperatura_ug1_lna_casquilho"
        )
        self.lcdNumber_temperatura_ug1_lna_casquilho.setFont(font4)
        self.lcdNumber_temperatura_ug1_lna_casquilho.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug1_lna_casquilho.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug1_lna_casquilho.setDigitCount(5)
        self.lcdNumber_temperatura_ug1_lna_casquilho.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug1_lna_casquilho.setProperty(
            "value", 12.340000000000000
        )

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug1_lna_casquilho, 5, 1, 1, 1
        )

        self.lcdNumber_temperatura_ug2_lna_casquilho = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug2_lna_casquilho.setObjectName(
            "lcdNumber_temperatura_ug2_lna_casquilho"
        )
        self.lcdNumber_temperatura_ug2_lna_casquilho.setFont(font4)
        self.lcdNumber_temperatura_ug2_lna_casquilho.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug2_lna_casquilho.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug2_lna_casquilho.setDigitCount(5)
        self.lcdNumber_temperatura_ug2_lna_casquilho.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug2_lna_casquilho.setProperty(
            "value", 12.340000000000000
        )

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug2_lna_casquilho, 5, 2, 1, 1
        )

        self.label_temperatura_6 = QLabel(self.layoutWidget2)
        self.label_temperatura_6.setObjectName("label_temperatura_6")
        self.label_temperatura_6.setFont(font)

        self.gridLayout_vars_ug.addWidget(self.label_temperatura_6, 6, 0, 1, 1)

        self.lcdNumber_temperatura_ug1_escora_1 = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug1_escora_1.setObjectName(
            "lcdNumber_temperatura_ug1_escora_1"
        )
        self.lcdNumber_temperatura_ug1_escora_1.setFont(font4)
        self.lcdNumber_temperatura_ug1_escora_1.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug1_escora_1.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug1_escora_1.setDigitCount(5)
        self.lcdNumber_temperatura_ug1_escora_1.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug1_escora_1.setProperty("value", 12.340000000000000)

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug1_escora_1, 6, 1, 1, 1
        )

        self.lcdNumber_temperatura_ug2_escora_1 = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug2_escora_1.setObjectName(
            "lcdNumber_temperatura_ug2_escora_1"
        )
        self.lcdNumber_temperatura_ug2_escora_1.setFont(font4)
        self.lcdNumber_temperatura_ug2_escora_1.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug2_escora_1.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug2_escora_1.setDigitCount(5)
        self.lcdNumber_temperatura_ug2_escora_1.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug2_escora_1.setProperty("value", 12.340000000000000)

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug2_escora_1, 6, 2, 1, 1
        )

        self.label_temperatura_7 = QLabel(self.layoutWidget2)
        self.label_temperatura_7.setObjectName("label_temperatura_7")
        self.label_temperatura_7.setFont(font)

        self.gridLayout_vars_ug.addWidget(self.label_temperatura_7, 7, 0, 1, 1)

        self.lcdNumber_temperatura_ug1_escora_2 = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug1_escora_2.setObjectName(
            "lcdNumber_temperatura_ug1_escora_2"
        )
        self.lcdNumber_temperatura_ug1_escora_2.setFont(font4)
        self.lcdNumber_temperatura_ug1_escora_2.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug1_escora_2.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug1_escora_2.setDigitCount(5)
        self.lcdNumber_temperatura_ug1_escora_2.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug1_escora_2.setProperty("value", 12.340000000000000)

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug1_escora_2, 7, 1, 1, 1
        )

        self.lcdNumber_temperatura_ug2_escora_2 = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug2_escora_2.setObjectName(
            "lcdNumber_temperatura_ug2_escora_2"
        )
        self.lcdNumber_temperatura_ug2_escora_2.setFont(font4)
        self.lcdNumber_temperatura_ug2_escora_2.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug2_escora_2.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug2_escora_2.setDigitCount(5)
        self.lcdNumber_temperatura_ug2_escora_2.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug2_escora_2.setProperty("value", 12.340000000000000)

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug2_escora_2, 7, 2, 1, 1
        )

        self.label_temperatura_8 = QLabel(self.layoutWidget2)
        self.label_temperatura_8.setObjectName("label_temperatura_8")
        self.label_temperatura_8.setFont(font)

        self.gridLayout_vars_ug.addWidget(self.label_temperatura_8, 8, 0, 1, 1)

        self.lcdNumber_temperatura_ug1_contra_escora_1 = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug1_contra_escora_1.setObjectName(
            "lcdNumber_temperatura_ug1_contra_escora_1"
        )
        self.lcdNumber_temperatura_ug1_contra_escora_1.setFont(font4)
        self.lcdNumber_temperatura_ug1_contra_escora_1.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug1_contra_escora_1.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug1_contra_escora_1.setDigitCount(5)
        self.lcdNumber_temperatura_ug1_contra_escora_1.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug1_contra_escora_1.setProperty(
            "value", 12.340000000000000
        )

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug1_contra_escora_1, 8, 1, 1, 1
        )

        self.lcdNumber_temperatura_ug2_contra_escora_1 = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug2_contra_escora_1.setObjectName(
            "lcdNumber_temperatura_ug2_contra_escora_1"
        )
        self.lcdNumber_temperatura_ug2_contra_escora_1.setFont(font4)
        self.lcdNumber_temperatura_ug2_contra_escora_1.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug2_contra_escora_1.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug2_contra_escora_1.setDigitCount(5)
        self.lcdNumber_temperatura_ug2_contra_escora_1.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug2_contra_escora_1.setProperty(
            "value", 12.340000000000000
        )

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug2_contra_escora_1, 8, 2, 1, 1
        )

        self.label_temperatura_9 = QLabel(self.layoutWidget2)
        self.label_temperatura_9.setObjectName("label_temperatura_9")
        self.label_temperatura_9.setFont(font)

        self.gridLayout_vars_ug.addWidget(self.label_temperatura_9, 9, 0, 1, 1)

        self.lcdNumber_temperatura_ug1_contra_escora_2 = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug1_contra_escora_2.setObjectName(
            "lcdNumber_temperatura_ug1_contra_escora_2"
        )
        self.lcdNumber_temperatura_ug1_contra_escora_2.setFont(font4)
        self.lcdNumber_temperatura_ug1_contra_escora_2.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug1_contra_escora_2.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug1_contra_escora_2.setDigitCount(5)
        self.lcdNumber_temperatura_ug1_contra_escora_2.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug1_contra_escora_2.setProperty(
            "value", 12.340000000000000
        )

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug1_contra_escora_2, 9, 1, 1, 1
        )

        self.lcdNumber_temperatura_ug2_contra_escora_2 = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_temperatura_ug2_contra_escora_2.setObjectName(
            "lcdNumber_temperatura_ug2_contra_escora_2"
        )
        self.lcdNumber_temperatura_ug2_contra_escora_2.setFont(font4)
        self.lcdNumber_temperatura_ug2_contra_escora_2.setAutoFillBackground(True)
        self.lcdNumber_temperatura_ug2_contra_escora_2.setSmallDecimalPoint(True)
        self.lcdNumber_temperatura_ug2_contra_escora_2.setDigitCount(5)
        self.lcdNumber_temperatura_ug2_contra_escora_2.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_temperatura_ug2_contra_escora_2.setProperty(
            "value", 12.340000000000000
        )

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_temperatura_ug2_contra_escora_2, 9, 2, 1, 1
        )

        self.label_ug1_2 = QLabel(self.layoutWidget2)
        self.label_ug1_2.setObjectName("label_ug1_2")
        self.label_ug1_2.setFont(font)
        self.label_ug1_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_vars_ug.addWidget(self.label_ug1_2, 10, 1, 1, 1)

        self.label_ug2_2 = QLabel(self.layoutWidget2)
        self.label_ug2_2.setObjectName("label_ug2_2")
        self.label_ug2_2.setFont(font)
        self.label_ug2_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_vars_ug.addWidget(self.label_ug2_2, 10, 2, 1, 1)

        self.label_perdagrade = QLabel(self.layoutWidget2)
        self.label_perdagrade.setObjectName("label_perdagrade")
        self.label_perdagrade.setFont(font)

        self.gridLayout_vars_ug.addWidget(self.label_perdagrade, 11, 0, 1, 1)

        self.lcdNumber_perda_na_grade_ug1 = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_perda_na_grade_ug1.setObjectName("lcdNumber_perda_na_grade_ug1")
        self.lcdNumber_perda_na_grade_ug1.setFont(font4)
        self.lcdNumber_perda_na_grade_ug1.setAutoFillBackground(True)
        self.lcdNumber_perda_na_grade_ug1.setSmallDecimalPoint(True)
        self.lcdNumber_perda_na_grade_ug1.setDigitCount(5)
        self.lcdNumber_perda_na_grade_ug1.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_perda_na_grade_ug1.setProperty("value", 12.340000000000000)

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_perda_na_grade_ug1, 11, 1, 1, 1
        )

        self.lcdNumber_perda_na_grade_ug2 = QLCDNumber(self.layoutWidget2)
        self.lcdNumber_perda_na_grade_ug2.setObjectName("lcdNumber_perda_na_grade_ug2")
        self.lcdNumber_perda_na_grade_ug2.setFont(font4)
        self.lcdNumber_perda_na_grade_ug2.setAutoFillBackground(True)
        self.lcdNumber_perda_na_grade_ug2.setSmallDecimalPoint(True)
        self.lcdNumber_perda_na_grade_ug2.setDigitCount(5)
        self.lcdNumber_perda_na_grade_ug2.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_perda_na_grade_ug2.setProperty("value", 12.340000000000000)

        self.gridLayout_vars_ug.addWidget(
            self.lcdNumber_perda_na_grade_ug2, 11, 2, 1, 1
        )

        self.layoutWidget3 = QWidget(Form)
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(670, 100, 191, 151))
        self.gridLayout_ug1 = QGridLayout(self.layoutWidget3)
        self.gridLayout_ug1.setObjectName("gridLayout_ug1")
        self.gridLayout_ug1.setContentsMargins(0, 0, 0, 0)
        self.label_potencia_ug1 = QLabel(self.layoutWidget3)
        self.label_potencia_ug1.setObjectName("label_potencia_ug1")
        self.label_potencia_ug1.setFont(font)

        self.gridLayout_ug1.addWidget(self.label_potencia_ug1, 0, 0, 1, 1)

        self.lcdNumber_potencia_ug1 = QLCDNumber(self.layoutWidget3)
        self.lcdNumber_potencia_ug1.setObjectName("lcdNumber_potencia_ug1")
        self.lcdNumber_potencia_ug1.setAutoFillBackground(True)
        self.lcdNumber_potencia_ug1.setSmallDecimalPoint(True)
        self.lcdNumber_potencia_ug1.setDigitCount(4)
        self.lcdNumber_potencia_ug1.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_potencia_ug1.setProperty("value", 5.123000000000000)

        self.gridLayout_ug1.addWidget(self.lcdNumber_potencia_ug1, 0, 1, 1, 1)

        self.label_setpoint_ug1 = QLabel(self.layoutWidget3)
        self.label_setpoint_ug1.setObjectName("label_setpoint_ug1")
        self.label_setpoint_ug1.setFont(font)

        self.gridLayout_ug1.addWidget(self.label_setpoint_ug1, 1, 0, 1, 1)

        self.label_etapa_ug1 = QLabel(self.layoutWidget3)
        self.label_etapa_ug1.setObjectName("label_etapa_ug1")
        self.label_etapa_ug1.setFont(font)

        self.gridLayout_ug1.addWidget(self.label_etapa_ug1, 2, 0, 1, 1)

        self.label_bitsalarme_ug1 = QLabel(self.layoutWidget3)
        self.label_bitsalarme_ug1.setObjectName("label_bitsalarme_ug1")
        self.label_bitsalarme_ug1.setFont(font)

        self.gridLayout_ug1.addWidget(self.label_bitsalarme_ug1, 3, 0, 1, 1)

        self.label_q_ug1 = QLabel(self.layoutWidget3)
        self.label_q_ug1.setObjectName("label_q_ug1")
        self.label_q_ug1.setFont(font)
        self.label_q_ug1.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.gridLayout_ug1.addWidget(self.label_q_ug1, 4, 0, 1, 1)

        self.lcdNumber_setpoint_ug1 = QLCDNumber(self.layoutWidget3)
        self.lcdNumber_setpoint_ug1.setObjectName("lcdNumber_setpoint_ug1")
        self.lcdNumber_setpoint_ug1.setAutoFillBackground(True)
        self.lcdNumber_setpoint_ug1.setSmallDecimalPoint(True)
        self.lcdNumber_setpoint_ug1.setDigitCount(4)
        self.lcdNumber_setpoint_ug1.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_setpoint_ug1.setProperty("value", 5.100000000000000)

        self.gridLayout_ug1.addWidget(self.lcdNumber_setpoint_ug1, 1, 1, 1, 1)

        self.lcdNumber_bitsalarme_ug1 = QLCDNumber(self.layoutWidget3)
        self.lcdNumber_bitsalarme_ug1.setObjectName("lcdNumber_bitsalarme_ug1")
        self.lcdNumber_bitsalarme_ug1.setAutoFillBackground(True)
        self.lcdNumber_bitsalarme_ug1.setSmallDecimalPoint(False)
        self.lcdNumber_bitsalarme_ug1.setDigitCount(5)
        self.lcdNumber_bitsalarme_ug1.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_bitsalarme_ug1.setProperty("value", 65356.000000000000000)

        self.gridLayout_ug1.addWidget(self.lcdNumber_bitsalarme_ug1, 3, 1, 1, 1)

        self.lcdNumber_q_ug1 = QLCDNumber(self.layoutWidget3)
        self.lcdNumber_q_ug1.setObjectName("lcdNumber_q_ug1")
        self.lcdNumber_q_ug1.setAutoFillBackground(True)
        self.lcdNumber_q_ug1.setSmallDecimalPoint(True)
        self.lcdNumber_q_ug1.setDigitCount(4)
        self.lcdNumber_q_ug1.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_q_ug1.setProperty("value", 12.340000000000000)

        self.gridLayout_ug1.addWidget(self.lcdNumber_q_ug1, 4, 1, 1, 1)

        self.splitter = QSplitter(self.layoutWidget3)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.lcdNumber_etapa_atual_ug1 = QLCDNumber(self.splitter)
        self.lcdNumber_etapa_atual_ug1.setObjectName("lcdNumber_etapa_atual_ug1")
        self.lcdNumber_etapa_atual_ug1.setAutoFillBackground(True)
        self.lcdNumber_etapa_atual_ug1.setSmallDecimalPoint(False)
        self.lcdNumber_etapa_atual_ug1.setDigitCount(1)
        self.lcdNumber_etapa_atual_ug1.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_etapa_atual_ug1.setProperty("value", 1.000000000000000)
        self.splitter.addWidget(self.lcdNumber_etapa_atual_ug1)
        self.lcdNumber_etapa_alvo_ug1 = QLCDNumber(self.splitter)
        self.lcdNumber_etapa_alvo_ug1.setObjectName("lcdNumber_etapa_alvo_ug1")
        self.lcdNumber_etapa_alvo_ug1.setAutoFillBackground(True)
        self.lcdNumber_etapa_alvo_ug1.setSmallDecimalPoint(False)
        self.lcdNumber_etapa_alvo_ug1.setDigitCount(1)
        self.lcdNumber_etapa_alvo_ug1.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_etapa_alvo_ug1.setProperty("value", 1.000000000000000)
        self.splitter.addWidget(self.lcdNumber_etapa_alvo_ug1)

        self.gridLayout_ug1.addWidget(self.splitter, 2, 1, 1, 1)

        self.layoutWidget4 = QWidget(Form)
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(1150, 400, 116, 131))
        self.verticalLayout_linha = QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_linha.setObjectName("verticalLayout_linha")
        self.verticalLayout_linha.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.layoutWidget4)
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(font)

        self.verticalLayout_linha.addWidget(self.label_3)

        self.lcdNumber_tensao_linha = QLCDNumber(self.layoutWidget4)
        self.lcdNumber_tensao_linha.setObjectName("lcdNumber_tensao_linha")
        self.lcdNumber_tensao_linha.setFont(font3)
        self.lcdNumber_tensao_linha.setAutoFillBackground(True)
        self.lcdNumber_tensao_linha.setSmallDecimalPoint(False)
        self.lcdNumber_tensao_linha.setDigitCount(5)
        self.lcdNumber_tensao_linha.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_tensao_linha.setProperty("value", 1234.000000000000000)

        self.verticalLayout_linha.addWidget(self.lcdNumber_tensao_linha)

        self.pushButton_pulse_trip_linha = QPushButton(self.layoutWidget4)
        self.pushButton_pulse_trip_linha.setObjectName("pushButton_pulse_trip_linha")

        self.verticalLayout_linha.addWidget(self.pushButton_pulse_trip_linha)

        self.pushButton_set_trip_linha = QPushButton(self.layoutWidget4)
        self.pushButton_set_trip_linha.setObjectName("pushButton_set_trip_linha")

        self.verticalLayout_linha.addWidget(self.pushButton_set_trip_linha)

        self.pushButton_reset_trip_linha = QPushButton(self.layoutWidget4)
        self.pushButton_reset_trip_linha.setObjectName("pushButton_reset_trip_linha")

        self.verticalLayout_linha.addWidget(self.pushButton_reset_trip_linha)

        self.layoutWidget5 = QWidget(Form)
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.layoutWidget5.setGeometry(QRect(500, 100, 164, 151))
        self.verticalLayout_ug1 = QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_ug1.setObjectName("verticalLayout_ug1")
        self.verticalLayout_ug1.setContentsMargins(0, 0, 0, 0)
        self.checkBox_sinal_trip_ug1 = QCheckBox(self.layoutWidget5)
        self.checkBox_sinal_trip_ug1.setObjectName("checkBox_sinal_trip_ug1")

        self.verticalLayout_ug1.addWidget(self.checkBox_sinal_trip_ug1)

        self.pushButton_pulso_trip_ug1 = QPushButton(self.layoutWidget5)
        self.pushButton_pulso_trip_ug1.setObjectName("pushButton_pulso_trip_ug1")

        self.verticalLayout_ug1.addWidget(self.pushButton_pulso_trip_ug1)

        self.pushButton_set_trip_high_ug1 = QPushButton(self.layoutWidget5)
        self.pushButton_set_trip_high_ug1.setObjectName("pushButton_set_trip_high_ug1")

        self.verticalLayout_ug1.addWidget(self.pushButton_set_trip_high_ug1)

        self.pushButton_set_trip_low_ug1 = QPushButton(self.layoutWidget5)
        self.pushButton_set_trip_low_ug1.setObjectName("pushButton_set_trip_low_ug1")

        self.verticalLayout_ug1.addWidget(self.pushButton_set_trip_low_ug1)

        self.pushButton_reconhece_reset_ug1 = QPushButton(self.layoutWidget5)
        self.pushButton_reconhece_reset_ug1.setObjectName(
            "pushButton_reconhece_reset_ug1"
        )

        self.verticalLayout_ug1.addWidget(self.pushButton_reconhece_reset_ug1)

        self.layoutWidget6 = QWidget(Form)
        self.layoutWidget6.setObjectName("layoutWidget6")
        self.layoutWidget6.setGeometry(QRect(50, 50, 221, 81))
        self.gridLayout_montante = QGridLayout(self.layoutWidget6)
        self.gridLayout_montante.setObjectName("gridLayout_montante")
        self.gridLayout_montante.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_montante_2 = QGridLayout()
        self.gridLayout_montante_2.setObjectName("gridLayout_montante_2")
        self.label_q_alfuente = QLabel(self.layoutWidget6)
        self.label_q_alfuente.setObjectName("label_q_alfuente")
        self.label_q_alfuente.setFont(font)
        self.label_q_alfuente.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

        self.gridLayout_montante_2.addWidget(self.label_q_alfuente, 1, 0, 1, 1)

        self.lcdNumber_nv_montante = QLCDNumber(self.layoutWidget6)
        self.lcdNumber_nv_montante.setObjectName("lcdNumber_nv_montante")
        self.lcdNumber_nv_montante.setFont(font3)
        self.lcdNumber_nv_montante.setAutoFillBackground(True)
        self.lcdNumber_nv_montante.setSmallDecimalPoint(True)
        self.lcdNumber_nv_montante.setDigitCount(6)
        self.lcdNumber_nv_montante.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_nv_montante.setProperty("value", 123.000000000000000)
        self.lcdNumber_nv_montante.setProperty("intValue", 123)

        self.gridLayout_montante_2.addWidget(self.lcdNumber_nv_montante, 0, 1, 1, 1)

        self.lcdNumber_q_alfuente = QLCDNumber(self.layoutWidget6)
        self.lcdNumber_q_alfuente.setObjectName("lcdNumber_q_alfuente")
        self.lcdNumber_q_alfuente.setFont(font3)
        self.lcdNumber_q_alfuente.setAutoFillBackground(True)
        self.lcdNumber_q_alfuente.setSmallDecimalPoint(True)
        self.lcdNumber_q_alfuente.setDigitCount(6)
        self.lcdNumber_q_alfuente.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_q_alfuente.setProperty("value", 12.345599999999999)

        self.gridLayout_montante_2.addWidget(self.lcdNumber_q_alfuente, 1, 1, 1, 1)

        self.label_nv_montante = QLabel(self.layoutWidget6)
        self.label_nv_montante.setObjectName("label_nv_montante")
        self.label_nv_montante.setFont(font)

        self.gridLayout_montante_2.addWidget(self.label_nv_montante, 0, 0, 1, 1)

        self.gridLayout_montante.addLayout(self.gridLayout_montante_2, 0, 0, 1, 1)

        self.horizontalSlider_q_afluente = QSlider(self.layoutWidget6)
        self.horizontalSlider_q_afluente.setObjectName("horizontalSlider_q_afluente")
        self.horizontalSlider_q_afluente.setMaximum(100)
        self.horizontalSlider_q_afluente.setValue(10)
        self.horizontalSlider_q_afluente.setOrientation(Qt.Horizontal)

        self.gridLayout_montante.addWidget(self.horizontalSlider_q_afluente, 1, 0, 1, 1)

        self.layoutWidget7 = QWidget(Form)
        self.layoutWidget7.setObjectName("layoutWidget7")
        self.layoutWidget7.setGeometry(QRect(1120, 20, 91, 50))
        self.verticalLayout_tempo_simul = QVBoxLayout(self.layoutWidget7)
        self.verticalLayout_tempo_simul.setObjectName("verticalLayout_tempo_simul")
        self.verticalLayout_tempo_simul.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget7)
        self.label_2.setObjectName("label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_tempo_simul.addWidget(self.label_2)

        self.label_tempo_simul = QLabel(self.layoutWidget7)
        self.label_tempo_simul.setObjectName("label_tempo_simul")
        self.label_tempo_simul.setAlignment(Qt.AlignCenter)

        self.verticalLayout_tempo_simul.addWidget(self.label_tempo_simul)

        self.layoutWidget8 = QWidget(Form)
        self.layoutWidget8.setObjectName("layoutWidget8")
        self.layoutWidget8.setGeometry(QRect(500, 70, 361, 24))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_partir_ug1 = QPushButton(self.layoutWidget8)
        self.pushButton_partir_ug1.setObjectName("pushButton_partir_ug1")

        self.horizontalLayout.addWidget(self.pushButton_partir_ug1)

        self.pushButton_parar_ug1 = QPushButton(self.layoutWidget8)
        self.pushButton_parar_ug1.setObjectName("pushButton_parar_ug1")

        self.horizontalLayout.addWidget(self.pushButton_parar_ug1)

        self.horizontalSlider_setpoint_ug1 = QSlider(self.layoutWidget8)
        self.horizontalSlider_setpoint_ug1.setObjectName(
            "horizontalSlider_setpoint_ug1"
        )
        self.horizontalSlider_setpoint_ug1.setMaximum(2600)
        self.horizontalSlider_setpoint_ug1.setSingleStep(50)
        self.horizontalSlider_setpoint_ug1.setPageStep(100)
        self.horizontalSlider_setpoint_ug1.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.horizontalSlider_setpoint_ug1)

        self.layoutWidget_5 = QWidget(Form)
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.layoutWidget_5.setGeometry(QRect(500, 500, 361, 24))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget_5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_partir_ug2 = QPushButton(self.layoutWidget_5)
        self.pushButton_partir_ug2.setObjectName("pushButton_partir_ug2")

        self.horizontalLayout_2.addWidget(self.pushButton_partir_ug2)

        self.pushButton_parar_ug2 = QPushButton(self.layoutWidget_5)
        self.pushButton_parar_ug2.setObjectName("pushButton_parar_ug2")

        self.horizontalLayout_2.addWidget(self.pushButton_parar_ug2)

        self.horizontalSlider_setpoint_ug2 = QSlider(self.layoutWidget_5)
        self.horizontalSlider_setpoint_ug2.setObjectName(
            "horizontalSlider_setpoint_ug2"
        )
        self.horizontalSlider_setpoint_ug2.setMaximum(2600)
        self.horizontalSlider_setpoint_ug2.setSingleStep(50)
        self.horizontalSlider_setpoint_ug2.setPageStep(100)
        self.horizontalSlider_setpoint_ug2.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.horizontalSlider_setpoint_ug2)

        self.layoutWidget_6 = QWidget(Form)
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.layoutWidget_6.setGeometry(QRect(500, 530, 164, 151))
        self.verticalLayout_ug2 = QVBoxLayout(self.layoutWidget_6)
        self.verticalLayout_ug2.setObjectName("verticalLayout_ug2")
        self.verticalLayout_ug2.setContentsMargins(0, 0, 0, 0)
        self.checkBox_sinal_trip_ug2 = QCheckBox(self.layoutWidget_6)
        self.checkBox_sinal_trip_ug2.setObjectName("checkBox_sinal_trip_ug2")

        self.verticalLayout_ug2.addWidget(self.checkBox_sinal_trip_ug2)

        self.pushButton_pulso_trip_ug2 = QPushButton(self.layoutWidget_6)
        self.pushButton_pulso_trip_ug2.setObjectName("pushButton_pulso_trip_ug2")

        self.verticalLayout_ug2.addWidget(self.pushButton_pulso_trip_ug2)

        self.pushButton_set_trip_high_ug2 = QPushButton(self.layoutWidget_6)
        self.pushButton_set_trip_high_ug2.setObjectName("pushButton_set_trip_high_ug2")

        self.verticalLayout_ug2.addWidget(self.pushButton_set_trip_high_ug2)

        self.pushButton_set_trip_low_ug2 = QPushButton(self.layoutWidget_6)
        self.pushButton_set_trip_low_ug2.setObjectName("pushButton_set_trip_low_ug2")

        self.verticalLayout_ug2.addWidget(self.pushButton_set_trip_low_ug2)

        self.pushButton_reconhece_reset_ug2 = QPushButton(self.layoutWidget_6)
        self.pushButton_reconhece_reset_ug2.setObjectName(
            "pushButton_reconhece_reset_ug2"
        )

        self.verticalLayout_ug2.addWidget(self.pushButton_reconhece_reset_ug2)

        self.retranslateUi(Form)
        self.horizontalSlider_q_afluente.valueChanged.connect(Form.mudar_q_afluente)
        self.pushButton_pulse_trip_linha.clicked.connect(Form.pulse_trip_linha)
        self.pushButton_set_trip_linha.clicked.connect(Form.set_trip_linha)
        self.pushButton_reset_trip_linha.clicked.connect(Form.reset_trip_linha)
        self.pushButton_partir_ug1.clicked.connect(Form.partir_ug1)
        self.pushButton_parar_ug1.clicked.connect(Form.parar_ug1)
        self.horizontalSlider_setpoint_ug1.valueChanged.connect(Form.mudar_setpoint_ug1)
        self.pushButton_partir_ug2.clicked.connect(Form.partir_ug2)
        self.pushButton_parar_ug2.clicked.connect(Form.parar_ug2)
        self.horizontalSlider_setpoint_ug2.valueChanged.connect(Form.mudar_setpoint_ug2)
        self.pushButton_pulso_trip_ug1.clicked.connect(Form.pulso_trip_ug1)
        self.pushButton_pulso_trip_ug2.clicked.connect(Form.pulso_trip_ug2)
        self.pushButton_set_trip_high_ug1.clicked.connect(Form.set_trip_high_ug1)
        self.pushButton_set_trip_high_ug2.clicked.connect(Form.set_trip_high_ug2)
        self.pushButton_set_trip_low_ug1.clicked.connect(Form.set_trip_low_ug1)
        self.pushButton_set_trip_low_ug2.clicked.connect(Form.set_trip_low_ug2)
        self.pushButton_reconhece_reset_ug1.clicked.connect(Form.reconhece_reset_ug1)
        self.pushButton_reconhece_reset_ug2.clicked.connect(Form.reconhece_reset_ug2)
        self.pushButton_52L_alternar_estado.clicked.connect(Form.alternar_estado_dj52L)
        self.pushButton_52L_provocar_inconsistencia.clicked.connect(
            Form.provocar_inconsistencia_dj52L
        )
        self.pushButton_52L_reconhece_reset.clicked.connect(Form.reconhecer_reset_dj52L)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(
            QCoreApplication.translate("Form", "Digital Twin PCH PPN", None)
        )
        self.bg.setText("")
        self.label.setText(
            QCoreApplication.translate("Form", "Simula\u00e7\u00e3o PCH PPN", None)
        )
        self.label_52L.setText(QCoreApplication.translate("Form", "Dj 52L", None))
        self.checkBox_52L_aberto.setText(
            QCoreApplication.translate("Form", "Aberto", None)
        )
        self.checkBox_52L_fechado.setText(
            QCoreApplication.translate("Form", "Fechado", None)
        )
        self.checkBox_52L_inconsistente.setText(
            QCoreApplication.translate("Form", "Inconsistente", None)
        )
        self.checkBox_52L_trip.setText(QCoreApplication.translate("Form", "TRIP", None))
        self.checkBox_52L_mola_carregada.setText(
            QCoreApplication.translate("Form", "Mola Carregada", None)
        )
        self.checkBox_52L_falta_vcc.setText(
            QCoreApplication.translate("Form", "Falta VCC", None)
        )
        self.checkBox_52L_condicao_fechamento.setText(
            QCoreApplication.translate("Form", "C. Fechamento", None)
        )
        self.pushButton_52L_alternar_estado.setText(
            QCoreApplication.translate("Form", "Alternar estado", None)
        )
        self.pushButton_52L_provocar_inconsistencia.setText(
            QCoreApplication.translate("Form", "Provocar inconsist\u00eancia", None)
        )
        self.pushButton_52L_reconhece_reset.setText(
            QCoreApplication.translate("Form", "Reconhece Reset", None)
        )
        self.label_se.setText(
            QCoreApplication.translate("Form", "Pot\u00eancia SE", None)
        )
        self.label_potencia_ug2.setText(
            QCoreApplication.translate("Form", "Pot\u00eancia", None)
        )
        self.label_setpoint_ug2.setText(
            QCoreApplication.translate("Form", "Setpoint", None)
        )
        self.label_etapa_ug2.setText(
            QCoreApplication.translate("Form", "Etapa Atual/Alvo", None)
        )
        self.label_bitsalarme_ug2.setText(
            QCoreApplication.translate("Form", "Bits Alarme", None)
        )
        self.label_q_ug2.setText(QCoreApplication.translate("Form", "Q UG", None))
        self.label_MP.setText(QCoreApplication.translate("Form", "MP", None))
        self.label_MR.setText(QCoreApplication.translate("Form", "MR", None))
        self.label_q_sanitaria.setText(
            QCoreApplication.translate("Form", "Q Sanit", None)
        )
        self.label_q_liquida.setText(
            QCoreApplication.translate("Form", "Q L\u00edquida", None)
        )
        self.label_q_vertimento.setText(
            QCoreApplication.translate("Form", "Q Vert.", None)
        )
        self.label_temperatura_titulo.setText(
            QCoreApplication.translate("Form", "Temperaturas", None)
        )
        self.label_ug1.setText(QCoreApplication.translate("Form", "UG 1", None))
        self.label_ug2.setText(QCoreApplication.translate("Form", "UG 2", None))
        self.label_temperatura_1.setText(
            QCoreApplication.translate("Form", "Fase R", None)
        )
        self.label_temperatura_2.setText(
            QCoreApplication.translate("Form", "Fase S", None)
        )
        self.label_temperatura_3.setText(
            QCoreApplication.translate("Form", "Fase T", None)
        )
        self.label_temperatura_4.setText(
            QCoreApplication.translate("Form", "Manca L.A. Casquilho", None)
        )
        self.label_temperatura_5.setText(
            QCoreApplication.translate("Form", "Manca L.N.A. Casquilho", None)
        )
        self.label_temperatura_6.setText(
            QCoreApplication.translate("Form", "Manca L.A. Escora 1", None)
        )
        self.label_temperatura_7.setText(
            QCoreApplication.translate("Form", "Manca L.A. Escora 2", None)
        )
        self.label_temperatura_8.setText(
            QCoreApplication.translate("Form", "Manca L.A. Contra escora 1", None)
        )
        self.label_temperatura_9.setText(
            QCoreApplication.translate("Form", "Manca L.A. Contra escora 2", None)
        )
        self.label_ug1_2.setText(QCoreApplication.translate("Form", "UG 1", None))
        self.label_ug2_2.setText(QCoreApplication.translate("Form", "UG 2", None))
        self.label_perdagrade.setText(
            QCoreApplication.translate("Form", "Perda na grade", None)
        )
        self.label_potencia_ug1.setText(
            QCoreApplication.translate("Form", "Pot\u00eancia", None)
        )
        self.label_setpoint_ug1.setText(
            QCoreApplication.translate("Form", "Setpoint", None)
        )
        self.label_etapa_ug1.setText(
            QCoreApplication.translate("Form", "Etapa Atual/Alvo", None)
        )
        self.label_bitsalarme_ug1.setText(
            QCoreApplication.translate("Form", "Bits Alarme", None)
        )
        self.label_q_ug1.setText(QCoreApplication.translate("Form", "Q UG", None))
        self.label_3.setText(
            QCoreApplication.translate("Form", "Tens\u00e3o na linha", None)
        )
        self.pushButton_pulse_trip_linha.setText(
            QCoreApplication.translate("Form", "Pulsar", None)
        )
        self.pushButton_set_trip_linha.setText(
            QCoreApplication.translate("Form", "Tens\u00e3o -> 0V", None)
        )
        self.pushButton_reset_trip_linha.setText(
            QCoreApplication.translate("Form", "Tens\u00e3o -> 34,5kV", None)
        )
        self.checkBox_sinal_trip_ug1.setText(
            QCoreApplication.translate("Form", "Sinal de TRIP", None)
        )
        self.pushButton_pulso_trip_ug1.setText(
            QCoreApplication.translate("Form", "Pulso TRIP HIGH, 2s, LOW", None)
        )
        self.pushButton_set_trip_high_ug1.setText(
            QCoreApplication.translate("Form", " TRIP -> HIGH", None)
        )
        self.pushButton_set_trip_low_ug1.setText(
            QCoreApplication.translate("Form", "TRIP -> LOW", None)
        )
        self.pushButton_reconhece_reset_ug1.setText(
            QCoreApplication.translate("Form", "Reconhece Reset", None)
        )
        self.label_q_alfuente.setText(
            QCoreApplication.translate("Form", "Q Afluente", None)
        )
        self.label_nv_montante.setText(
            QCoreApplication.translate("Form", "N\u00edvel montante", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("Form", "Tempo de\n" "simula\u00e7\u00e3o", None)
        )
        self.label_tempo_simul.setText(
            QCoreApplication.translate("Form", "hhhh:mm:ss", None)
        )
        self.pushButton_partir_ug1.setText(
            QCoreApplication.translate("Form", "Partir", None)
        )
        self.pushButton_parar_ug1.setText(
            QCoreApplication.translate("Form", "Parar", None)
        )
        self.pushButton_partir_ug2.setText(
            QCoreApplication.translate("Form", "Partir", None)
        )
        self.pushButton_parar_ug2.setText(
            QCoreApplication.translate("Form", "Parar", None)
        )
        self.checkBox_sinal_trip_ug2.setText(
            QCoreApplication.translate("Form", "Sinal de TRIP", None)
        )
        self.pushButton_pulso_trip_ug2.setText(
            QCoreApplication.translate("Form", "Pulso TRIP HIGH, 2s, LOW", None)
        )
        self.pushButton_set_trip_high_ug2.setText(
            QCoreApplication.translate("Form", " TRIP -> HIGH", None)
        )
        self.pushButton_set_trip_low_ug2.setText(
            QCoreApplication.translate("Form", "TRIP -> LOW", None)
        )
        self.pushButton_reconhece_reset_ug2.setText(
            QCoreApplication.translate("Form", "Reconhece Reset", None)
        )

    # retranslateUi
