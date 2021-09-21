import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta

import abstracao_usina

class Usina(unittest.TestCase):
    pass
"""
    def test_demo(self):
        modbus_clp_mock = MagicMock()
        modbus_clp_mock.read_holding_registers.return_value = [2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0, 2]
        database_mock = MagicMock()
        database_mock.get_parametros_usina.return_value = {
            "emergencia_acionada": 10,
            "ug1_perda_grade_alerta": 10,
            "ug1_perda_grade_maxima": 10,
            "ug1_prioridade": 20,
            "ug1_temp_alerta": 10,
            "ug1_temp_maxima": 10,
            "ug2_perda_grade_alerta": 10,
            "ug2_perda_grade_maxima": 10,
            "ug2_prioridade": 10,
            "ug2_temp_alerta": 10,
            "ug2_temp_maxima": 10,
            "modo_autonomo": 10,
            "modo_de_escolha_das_ugs": 10,
            "nv_comporta_pos_0_ant": 10,
            "nv_comporta_pos_0_prox": 10,
            "nv_comporta_pos_1_ant": 10,
            "nv_comporta_pos_1_prox": 10,
            "nv_comporta_pos_2_ant": 10,
            "nv_comporta_pos_2_prox": 10,
            "nv_comporta_pos_3_ant": 10,
            "nv_comporta_pos_3_prox": 10,
            "nv_comporta_pos_4_ant": 10,
            "nv_comporta_pos_4_prox": 10,
            "nv_comporta_pos_5_ant": 10,
            "nv_comporta_pos_5_prox": 10,
            "kp": 10,
            "ki": 10,
            "kd": 10,
            "kie": 10,
            "n_movel_L": 10,
            "n_movel_R": 10
        }
        usina = abstracao_usina.Usina(modbus_clp_mock, database_mock)
        usina.acionar_emergencia_clp()

        modbus_clp_mock.write_single_register.assert_called_once_with(100, 1)
    
    def test_demo_2(self):
        modbus_clp_mock = MagicMock()
        modbus_clp_mock.read_holding_registers.return_value = [2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0,
                                                               2,0,46,0,0,0,0,0,0,0, 2]
        database_mock = MagicMock()
        database_mock.get_agendamentos_pendentes.return_value = [[1, datetime.now() - timedelta(minutes=5), 2, 3]]
        usina = abstracao_usina.Usina(modbus_clp_mock, database_mock)
        usina.verificar_agendamentos()

        modbus_clp_mock.write_single_register.assert_called_once_with(100, 1)
"""
if __name__ == '__main__':
    unittest.main()