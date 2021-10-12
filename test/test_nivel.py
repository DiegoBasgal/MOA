import datetime
import logging
import unittest
from unittest import mock
from unittest.mock import MagicMock
from decimal import Decimal

import src.abstracao_usina
import src.operador_autonomo_sm
from src.mensageiro import voip, telegram_bot


class TestNivel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)
        voip.enviar_voz_teste = MagicMock()
        telegram_bot.enviar_a_todos = MagicMock()

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def setUp(self):
        self.cfg = dict(UG1_slave_ip='192.168.70.10', UG1_slave_porta=502, UG2_slave_ip='192.168.70.13',
                        UG2_slave_porta=502, USN_slave_ip='192.168.70.16', USN_slave_porta=502,
                        clp_ip='10.101.2.242', clp_porta=5002, moa_slave_ip='0.0.0.0',
                        moa_slave_porta=5003, ENDERECO_CLP_NV_MONATNTE=40000, ENDERECO_CLP_MEDIDOR=40001,
                        ENDERECO_CLP_COMPORTA_FLAGS=40010, ENDERECO_CLP_COMPORTA_POS=40011,
                        ENDERECO_CLP_UG1_FLAGS=40020, ENDERECO_CLP_UG1_MINUTOS=40023,
                        ENDERECO_CLP_UG1_PERGA_GRADE=40025, ENDERECO_CLP_UG1_POTENCIA=40021,
                        ENDERECO_CLP_UG1_SETPOINT=40022, ENDERECO_CLP_UG1_T_MANCAL=40024,
                        ENDERECO_CLP_UG2_FLAGS=40030, ENDERECO_CLP_UG2_MINUTOS=40033,
                        ENDERECO_CLP_UG2_PERGA_GRADE=40035, ENDERECO_CLP_UG2_POTENCIA=40031,
                        ENDERECO_CLP_UG2_SETPOINT=40032, ENDERECO_CLP_UG2_T_MANCAL=40034,
                        ENDERECO_CLP_USINA_FLAGS=40100, ENDERECO_LOCAL_NV_MONATNTE=40009,
                        ENDERECO_LOCAL_NV_ALVO=40010, ENDERECO_LOCAL_NV_RELIGAMENTO=40011,
                        ENDERECO_LOCAL_UG1_POT=40019, ENDERECO_LOCAL_UG1_SETPOINT=40020,
                        ENDERECO_LOCAL_UG1_DISP=40021, ENDERECO_LOCAL_UG2_POT=40029,
                        ENDERECO_LOCAL_UG2_SETPOINT=40030, ENDERECO_LOCAL_UG2_DISP=40031,
                        ENDERECO_LOCAL_CLP_ONLINE=40099, ENDERECO_LOCAL_STATUS_MOA=40100, timeout_padrao=5,
                        timeout_emergencia=10, timeout_normalizacao=10, n_movel_R=5, n_movel_L=30,
                        nv_fundo_reservatorio=641.25, nv_minimo=643.0, nv_alvo=643.25, nv_maximo=643.5,
                        nv_maximorum=647, nv_religamento=643.25,
                        pot_maxima_usina=5.2, pot_maxima_alvo=5.0, pot_minima=1.0, margem_pot_critica=1.0,
                        pot_maxima_ug=2.6, kp=-2.0, ki=-0.015, kd=-10, kie=0.08, saida_ie_inicial=0.0)

        self.clp_mock = MagicMock()
        self.clp_mock.is_online.return_value = True
        self.clp_mock.write_to_single.return_value = True
        self.clp_mock.read_sequential.return_value = [0] * 1000

        self.db_mock = MagicMock()
        self.db_mock.get_parametros_usina.return_value = dict(id=1, modo_autonomo=1, status_moa=7,
                                                              emergencia_acionada=0,
                                                              timestamp=datetime.datetime(2021, 9, 17, 10, 18, 40),
                                                              aguardando_reservatorio=0, clp_online=1,
                                                              clp_ip='localhost',
                                                              clp_porta=5002, modbus_server_ip='localhost',
                                                              modbus_server_porta=5003, kp=Decimal('-5.0000000000'),
                                                              ki=Decimal('0.0000120000'), kd=Decimal('0E-10'),
                                                              kie=Decimal('0.0000120000'),
                                                              margem_pot_critica=Decimal('0.50000'), n_movel_L=15,
                                                              n_movel_R=5, nv_alvo=Decimal('643.250'),
                                                              nv_maximo=Decimal('643.500'),
                                                              nv_minimo=Decimal('643.000'),
                                                              nv_montante=Decimal('643.270'),
                                                              nv_religamento=Decimal('643.150'),
                                                              pot_minima=Decimal('1.00000'),
                                                              pot_nominal=Decimal('5.00000'),
                                                              pot_nominal_ug=Decimal('2.50000'),
                                                              pot_disp=Decimal('5.20000'),
                                                              timer_erro=30, ug1_disp=Decimal('1.00000'),
                                                              ug1_pot=Decimal('0.00000'), ug1_setpot=Decimal('0.00000'),
                                                              ug1_sinc=0, ug1_tempo=12, ug1_prioridade=0,
                                                              ug2_disp=Decimal('1.00000'), ug2_pot=Decimal('2.59900'),
                                                              ug2_setpot=Decimal('2.60000'), ug2_sinc=1, ug2_tempo=17,
                                                              ug2_prioridade=0, valor_ie_inicial=Decimal('0.00000'),
                                                              modo_de_escolha_das_ugs=1, pos_comporta=0,
                                                              nv_comporta_pos_0_ant=Decimal('643.50'),
                                                              nv_comporta_pos_0_prox=Decimal('643.60'),
                                                              nv_comporta_pos_1_ant=Decimal('643.56'),
                                                              nv_comporta_pos_1_prox=Decimal('643.67'),
                                                              nv_comporta_pos_2_ant=Decimal('643.58'),
                                                              nv_comporta_pos_2_prox=Decimal('643.68'),
                                                              nv_comporta_pos_3_ant=Decimal('643.60'),
                                                              nv_comporta_pos_3_prox=Decimal('643.69'),
                                                              nv_comporta_pos_4_ant=Decimal('643.62'),
                                                              nv_comporta_pos_4_prox=Decimal('643.70'),
                                                              nv_comporta_pos_5_ant=Decimal('643.64'),
                                                              nv_comporta_pos_5_prox=Decimal('643.80'),
                                                              tolerancia_pot_maxima=Decimal('1.02500'),
                                                              ug1_perda_grade=Decimal('0.000'),
                                                              ug1_perda_grade_maxima=Decimal('2.000'),
                                                              ug1_temp_mancal=Decimal('25.20'),
                                                              ug1_temp_maxima=Decimal('90.00'),
                                                              ug2_perda_grade=Decimal('0.000'),
                                                              ug2_perda_grade_maxima=Decimal('2.000'),
                                                              ug2_temp_mancal=Decimal('25.00'),
                                                              ug2_temp_maxima=Decimal('90.00'),
                                                              pot_maxima_alvo=Decimal('5.00000'),
                                                              ug1_perda_grade_alerta=Decimal('1.000'),
                                                              ug1_temp_alerta=Decimal('75.00'),
                                                              ug2_perda_grade_alerta=Decimal('1.000'),
                                                              ug2_temp_alerta=Decimal('75.00'))

        self.usina = src.abstracao_usina.Usina(cfg=self.cfg, clp=self.clp_mock, db=self.db_mock)

    def test_nivel_abaixo_do_limite(self):
        logging.disable(logging.NOTSET)
        nv_teste = 641.24
        self.usina.acionar_emergencia = MagicMock()
        sm = src.operador_autonomo_sm.StateMachine(initial_state=src.operador_autonomo_sm.Pronto(self.usina))
        self.clp_mock.read_sequential.return_value = [int((nv_teste - 620) * 1000)] + [0]*100
        sm.exec()  # Atualiza valroes internos
        self.assertEqual(self.usina.nv_montante, nv_teste)
        sm.exec()  # Deve ter entrado no Reservatorio abaixo do normal
        self.assertIsInstance(sm.state, src.operador_autonomo_sm.ReservatorioAbaixoDoMinimo)
        sm.exec()  # Deve ter entrado no Emergencia
        self.assertIsInstance(sm.state, src.operador_autonomo_sm.Emergencia)
        self.usina.acionar_emergencia.assert_called()
        voip.enviar_voz_teste.assert_called()

    def test_nivel_acima_do_limite(self):
        logging.disable(logging.NOTSET)
        nv_teste = 647.01
        self.usina.acionar_emergencia = MagicMock()
        sm = src.operador_autonomo_sm.StateMachine(initial_state=src.operador_autonomo_sm.Pronto(self.usina))
        self.clp_mock.read_sequential.return_value = [int((nv_teste - 620) * 1000)] + [0]*100
        sm.exec()  # Atualiza valroes internos
        self.assertEqual(self.usina.nv_montante, 647.01)
        sm.exec()  # Deve ter entrado no Reservatorio abaixo do normal
        self.assertIsInstance(sm.state, src.operador_autonomo_sm.ReservatorioAcimaDoMaximo)
        sm.exec()  # Deve ter entrado no Emergencia e ligado para os resp.
        self.assertIsInstance(sm.state, src.operador_autonomo_sm.Emergencia)
        self.usina.acionar_emergencia.assert_called()
        voip.enviar_voz_teste.assert_called()

if __name__ == '__main__':
    unittest.main()
