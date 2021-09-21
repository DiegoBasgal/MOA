import unittest
import datetime
from unittest.mock import MagicMock
from src.abstracao_usina import Usina


def Decimal(value):
    return float(value)


class TesteComportamentoPotencia(unittest.TestCase):

    def get_base_mocks(self):
        cfg = dict(UG1_slave_ip='192.168.70.10', UG1_slave_porta=502, UG2_slave_ip='192.168.70.13',
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
                   nv_minimo=643.0, nv_alvo=643.25, nv_maximo=643.5, nv_religamento=643.25,
                   pot_maxima_usina=5.2, pot_maxima_alvo=5.0, pot_minima=1.0, margem_pot_critica=1.0,
                   pot_maxima_ug=2.6, kp=-2.0, ki=-0.015, kd=-10, kie=0.08, saida_ie_inicial=0.0)

        clp_mock = MagicMock()
        clp_mock.is_online.return_value = True
        clp_mock.write_to_single.return_value = True
        clp_mock.read_sequential.return_value = [0] * 1000

        db_mock = MagicMock()
        db_mock.get_parametros_usina.return_value = dict(id=1, modo_autonomo=1, status_moa=7, emergencia_acionada=0,
                                                         timestamp=datetime.datetime(2021, 9, 17, 10, 18, 40),
                                                         aguardando_reservatorio=0, clp_online=1, clp_ip='localhost',
                                                         clp_porta=5002, modbus_server_ip='localhost',
                                                         modbus_server_porta=5003, kp=Decimal('-5.0000000000'),
                                                         ki=Decimal('0.0000120000'), kd=Decimal('0E-10'),
                                                         kie=Decimal('0.0000120000'),
                                                         margem_pot_critica=Decimal('0.50000'), n_movel_L=15,
                                                         n_movel_R=5, nv_alvo=Decimal('643.250'),
                                                         nv_maximo=Decimal('643.500'), nv_minimo=Decimal('643.000'),
                                                         nv_montante=Decimal('643.270'),
                                                         nv_religamento=Decimal('643.150'),
                                                         pot_minima=Decimal('1.00000'), pot_nominal=Decimal('5.00000'),
                                                         pot_nominal_ug=Decimal('2.50000'), pot_disp=Decimal('5.20000'),
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
        return cfg, clp_mock, db_mock

    def test_distribuir_pot_caso_max(self):
        cfg, clp_mock, db_mock = self.get_base_mocks()
        usina = Usina(cfg=cfg, clp=clp_mock, db=db_mock)
        for _ in range(10):
            usina.distribuir_potencia(cfg['pot_maxima_alvo'])
        self.assertEqual(usina.ug1.setpoint + usina.ug2.setpoint, cfg['pot_maxima_alvo'])

    def test_distribuir_pot_caso_acima(self):
        cfg, clp_mock, db_mock = self.get_base_mocks()
        usina = Usina(cfg=cfg, clp=clp_mock, db=db_mock)
        usina.pot_medidor = cfg['pot_maxima_alvo']*2
        usina.ug1.potencia = cfg['pot_maxima_ug']*2
        usina.ug2.potencia = cfg['pot_maxima_ug']*2
        for _ in range(10):
            usina.distribuir_potencia(cfg['pot_maxima_alvo'])
            usina.pot_medidor = usina.ug1.setpoint + usina.ug2.setpoint
        self.assertEqual(usina.pot_medidor, cfg['pot_maxima_alvo'])

    def test_divisao_pot_caso_zero(self):
        cfg, clp_mock, db_mock = self.get_base_mocks()
        usina = Usina(cfg=cfg, clp=clp_mock, db=db_mock)
        pot = cfg['pot_minima']*0.9
        for _ in range(10):
            usina.distribuir_potencia(pot)
            usina.pot_medidor = usina.ug1.setpoint + usina.ug2.setpoint
            self.assertEqual(usina.ug1.setpoint, 0)
            self.assertEqual(usina.ug2.setpoint, 0)

    def test_divisao_pot_caso_A(self):
        # Caso A:   Potencia abaixo do range de uma ug
        #           Abaixo da margem critica
        #           Sem erro significativo no nivel.
        # Resultado esperado: Nenhuma uma UG deve partir
        cfg, clp_mock, db_mock = self.get_base_mocks()
        usina = Usina(cfg=cfg, clp=clp_mock, db=db_mock)
        usina.erro_nv = 0
        pot = cfg['pot_maxima_ug']
        for _ in range(10):
            usina.distribuir_potencia(pot)
            usina.pot_medidor = usina.ug1.setpoint + usina.ug2.setpoint
            self.assertEqual(usina.ug1.setpoint, pot)
            self.assertEqual(usina.ug2.setpoint, 0)

    def test_divisao_pot_caso_B(self):
        # Caso B:   Potencia fora do range de uma ug
        #           Abaixo da margem critica
        #           Sem erro significativo no nivel.
        # Resultado esperado: Apenas uma UG deve partir
        cfg, clp_mock, db_mock = self.get_base_mocks()
        usina = Usina(cfg=cfg, clp=clp_mock, db=db_mock)
        usina.erro_nv = 1
        pot = cfg['pot_maxima_ug']+cfg['margem_pot_critica']*0.9
        for _ in range(10):
            usina.distribuir_potencia(pot)
            usina.pot_medidor = usina.ug1.setpoint + usina.ug2.setpoint
            self.assertEqual(usina.ug1.setpoint, cfg['pot_maxima_ug'])
            self.assertEqual(usina.ug2.setpoint, 0)

    def test_divisao_pot_caso_C(self):
        # Caso C:   Potencia acima do range de uma ug
        #           Acima da margem critica
        #           Sem erro significativo no nivel.
        # Resultado esperado: Apenas uma UG deve partir
        cfg, clp_mock, db_mock = self.get_base_mocks()
        usina = Usina(cfg=cfg, clp=clp_mock, db=db_mock)
        usina.erro_nv = 0
        pot = cfg['pot_maxima_ug']+cfg['margem_pot_critica']*1.1
        for _ in range(10):
            usina.distribuir_potencia(pot)
            usina.pot_medidor = usina.ug1.setpoint + usina.ug2.setpoint
            self.assertEqual(usina.ug1.setpoint, cfg['pot_maxima_ug'])
            self.assertEqual(usina.ug2.setpoint, 0)

    def test_divisao_pot_caso_D(self):
        # Caso D:   Potencia acima do range de uma ug
        #           Acima da margem critica
        #           Com erro significativo no nivel.
        # Resultado esperado: Ambas as UGs devem partir
        cfg, clp_mock, db_mock = self.get_base_mocks()
        usina = Usina(cfg=cfg, clp=clp_mock, db=db_mock)
        usina.erro_nv = 1
        pot = cfg['pot_maxima_ug']+cfg['margem_pot_critica']*1.1
        for _ in range(10):
            usina.distribuir_potencia(pot)
            usina.pot_medidor = usina.ug1.setpoint + usina.ug2.setpoint
            self.assertEqual(usina.ug1.setpoint, pot/2)
            self.assertEqual(usina.ug2.setpoint, pot/2)

    def test_divisao_pot_caso_E(self):
        # Caso E:   Potencia maxima
        #           UG1 restrita por flag
        # Resultado esperado: Apenas a UG2 deve partir
        cfg, clp_mock, db_mock = self.get_base_mocks()
        usina = Usina(cfg=cfg, clp=clp_mock, db=db_mock)
        usina.ug1.flag = 1
        for ug in usina.ugs:
            ug.atualizar_estado()
        pot = cfg['pot_maxima_alvo']
        for _ in range(10):
            usina.distribuir_potencia(pot)
            usina.pot_medidor = usina.ug1.setpoint + usina.ug2.setpoint
            self.assertEqual(usina.ug1.setpoint, 0)
            self.assertTrue(usina.ug1.flag)
            self.assertEqual(usina.ug2.setpoint, cfg['pot_maxima_ug'])

if __name__ == '__main__':
    unittest.main()
