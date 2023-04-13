import datetime
import logging
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
from decimal import Decimal

from src.abstracao_usina import Usina
import MOA
from src.field_connector import FieldConnector
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
        self.cfg = {
            "UG1_slave_ip": "172.21.15.50",
            "UG1_slave_porta": 5002,
            "UG2_slave_ip": "172.21.15.50",
            "UG2_slave_porta": 5002,
            "USN_slave_ip": "172.21.15.50",
            "USN_slave_porta": 5002,
            "TDA_slave_ip": "172.21.15.50",
            "TDA_slave_porta": 5002,
            "moa_slave_ip": "0.0.0.0",
            "moa_slave_porta": 5004,
            "REG_MOA_OUT_STATUS": 7,
            "REG_SM_STATE": 8,
            "REG_MOA_OUT_MODE": 9,
            "REG_PAINEL_LIDO": 10,
            "REG_MOA_OUT_EMERG": 50,
            "REG_MOA_OUT_TARGET_LEVEL": 51,
            "REG_MOA_OUT_SETPOINT": 52,
            "REG_MOA_OUT_BLOCK_UG1": 60,
            "REG_MOA_OUT_BLOCK_UG2": 70,
            "REG_MOA_IN_EMERG": 12,
            "REG_MOA_IN_HABILITA_AUTO": 13,
            "REG_MOA_IN_DESABILITA_AUTO": 14,
            "timeout_padrao": 5,
            "timeout_emergencia": 10,
            "timeout_normalizacao": 10,
            "n_movel_R": 6,
            "n_movel_L": 30,
            "nv_fundo_reservatorio": 641.0,
            "nv_minimo": 643.01,
            "nv_alvo": 643.3,
            "nv_maximo": 643.5,
            "nv_maximorum": 647.0,
            "pot_maxima_usina": 5100,
            "pot_maxima_alvo": 5000,
            "pot_minima": 1250,
            "margem_pot_critica": 1000,
            "pot_maxima_ug": 2550,
            "kp": 5.0,
            "ki": 0.005,
            "kd": 1.0,
            "kie": 0.1,
            "saida_ie_inicial": "auto",
            "TENSAO_LINHA_BAIXA": 31050,
            "TENSAO_LINHA_ALTA": 36200,
        }

        self.db_mock = MagicMock()
        self.db_mock.get_parametros_usina.return_value = dict(
            id=1,
            modo_autonomo=1,
            status_moa=7,
            emergencia_acionada=0,
            timestamp=datetime.datetime(2021, 9, 17, 10, 18, 40),
            aguardando_reservatorio=0,
            clp_online=1,
            clp_ip="localhost",
            clp_porta=5002,
            modbus_server_ip="localhost",
            modbus_server_porta=5003,
            kp=Decimal("-5.0000000000"),
            ki=Decimal("0.0000120000"),
            kd=Decimal("0E-10"),
            kie=Decimal("0.0000120000"),
            margem_pot_critica=Decimal("0.50000"),
            n_movel_L=15,
            n_movel_R=5,
            nv_alvo=Decimal("643.250"),
            nv_maximo=Decimal("643.500"),
            nv_minimo=Decimal("643.000"),
            nv_montante=Decimal("643.270"),
            nv_religamento=Decimal("643.150"),
            pot_minima=Decimal("1.00000"),
            pot_nominal=Decimal("5.00000"),
            pot_nominal_ug=Decimal("2.50000"),
            pot_disp=Decimal("5.20000"),
            timer_erro=30,
            ug1_disp=Decimal("1.00000"),
            ug1_pot=Decimal("0.00000"),
            ug1_setpot=Decimal("0.00000"),
            ug1_sinc=0,
            ug1_tempo=12,
            ug1_prioridade=0,
            ug2_disp=Decimal("1.00000"),
            ug2_pot=Decimal("2.59900"),
            ug2_setpot=Decimal("2.60000"),
            ug2_sinc=1,
            ug2_tempo=17,
            ug2_prioridade=0,
            valor_ie_inicial=Decimal("0.00000"),
            modo_de_escolha_das_ugs=1,
            pos_comporta=0,
            nv_comporta_pos_0_ant=Decimal("643.50"),
            nv_comporta_pos_0_prox=Decimal("643.60"),
            nv_comporta_pos_1_ant=Decimal("643.56"),
            nv_comporta_pos_1_prox=Decimal("643.67"),
            nv_comporta_pos_2_ant=Decimal("643.58"),
            nv_comporta_pos_2_prox=Decimal("643.68"),
            nv_comporta_pos_3_ant=Decimal("643.60"),
            nv_comporta_pos_3_prox=Decimal("643.69"),
            nv_comporta_pos_4_ant=Decimal("643.62"),
            nv_comporta_pos_4_prox=Decimal("643.70"),
            nv_comporta_pos_5_ant=Decimal("643.64"),
            nv_comporta_pos_5_prox=Decimal("643.80"),
            tolerancia_pot_maxima=Decimal("1.02500"),
            ug1_perda_grade=Decimal("0.000"),
            ug1_perda_grade_maxima=Decimal("2.000"),
            ug1_temp_mancal=Decimal("25.20"),
            ug1_temp_maxima=Decimal("90.00"),
            ug2_perda_grade=Decimal("0.000"),
            ug2_perda_grade_maxima=Decimal("2.000"),
            ug2_temp_mancal=Decimal("25.00"),
            ug2_temp_maxima=Decimal("90.00"),
            pot_maxima_alvo=Decimal("5.00000"),
            ug1_perda_grade_alerta=Decimal("1.000"),
            ug1_temp_alerta=Decimal("75.00"),
            ug2_perda_grade_alerta=Decimal("1.000"),
            ug2_temp_alerta=Decimal("75.00"),
        )

        self.mock_con = MagicMock()
        self.mock_con.get_emergencia_acionada.return_value = 0
        self.mock_con.get_nv_montante.return_value = 0
        self.mock_con.get_pot_medidor.return_value = 0
        self.mock_con.get_flags_ug1.return_value = 0
        self.mock_con.get_potencia_ug1.return_value = 0
        self.mock_con.get_horas_ug1.return_value = 0
        self.mock_con.get_perda_na_grade_ug1.return_value = 0
        self.mock_con.get_temperatura_do_mancal_ug1.return_value = 0
        self.mock_con.get_flags_ug2.return_value = 0
        self.mock_con.get_potencia_ug2.return_value = 0
        self.mock_con.get_horas_ug2.return_value = 0
        self.mock_con.get_perda_na_grade_ug2.return_value = 0
        self.mock_con.get_temperatura_do_mancal_ug2.return_value = 0
        self.mock_con.set_ug1_flag.return_value = 0
        self.mock_con.set_ug1_setpoint.return_value = 0
        self.mock_con.set_ug2_flag.return_value = 0
        self.mock_con.set_ug2_setpoint.return_value = 0
        self.mock_con.set_pos_comporta.return_value = 0
        self.mock_con.acionar_emergencia.return_value = 0
        self.mock_con.normalizar_emergencia.return_value = 0

        self.usina = Usina(cfg=self.cfg, db=self.db_mock)
        self.usina.con = MagicMock()

    def test_nivel_abaixo_do_limite(self):
        nv_teste = 641.24
        self.usina.acionar_emergencia = MagicMock()
        self.usina.con.get_nv_montante.return_value = nv_teste
        logging.disable(logging.NOTSET)
        sm = MOA.StateMachine(
            initial_state=MOA.Pronto(self.usina)
        )
        sm.exec()  # Atualiza valroes internos
        self.assertEqual(self.usina.nv_montante, nv_teste)
        sm.exec()  # Deve ter entrado no Reservatorio abaixo do normal
        self.assertIsInstance(sm.state, MOA.ReservatorioAbaixoDoMinimo)
        sm.exec()  # Deve ter entrado no Emergencia
        self.assertIsInstance(sm.state, MOA.Emergencia)
        self.usina.acionar_emergencia.assert_called()
        voip.enviar_voz_teste.assert_called()

    def test_nivel_acima_do_limite(self):
        nv_teste = 647.01
        self.usina.acionar_emergencia = MagicMock()
        self.usina.con.get_nv_montante.return_value = nv_teste
        logging.disable(logging.NOTSET)
        sm = MOA.StateMachine(
            initial_state=MOA.Pronto(self.usina)
        )
        sm.exec()  # Atualiza valroes internos
        self.assertEqual(self.usina.nv_montante, 647.01)
        sm.exec()  # Deve ter entrado no Reservatorio abaixo do normal
        self.assertIsInstance(sm.state, MOA.ReservatorioAcimaDoMaximo)
        sm.exec()  # Deve ter entrado no Emergencia e ligado para os resp.
        self.assertIsInstance(sm.state, MOA.Emergencia)
        self.usina.acionar_emergencia.assert_called()
        voip.enviar_voz_teste.assert_called()


if __name__ == "__main__":
    unittest.main()
