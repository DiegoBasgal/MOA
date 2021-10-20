import unittest
import datetime
from unittest.mock import MagicMock, patch
from src.abstracao_usina import Usina
import logging
from decimal import Decimal


class TestUG(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def setUp(self):
        self.cfg = dict(UG1_slave_ip='192.168.70.10', UG1_slave_porta=502, UG2_slave_ip='192.168.70.13',
                        UG2_slave_porta=502, USN_slave_ip='192.168.70.16', USN_slave_porta=502,
                        clp_A_IP='10.101.2.242', clp_A_PORT=5002,
                        clp_B_IP='10.101.2.242', clp_B_PORT=5002,
                        moa_slave_ip='0.0.0.0',
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
        
        self.usina = Usina(cfg=self.cfg, db=self.db_mock, con=self.mock_con)
        self.usina.ler_valores()
        
    def tearDown(self):
        pass

    
    def test_distribuir_pot_caso_acima(self):
        # Teste:            test_distribuir_pot_caso_acima
        # Objetivo:         Verificar distribuição de potência caso algo esteja acima do permitido, seja medidor ou UG
        # Estado inicial:   Tudo normalizado,
        #                   teste sem perda,
        #                   setpoint = 2 x Máximo UG,
        #                   pot no medidor = 2 x Nominal
        # Resposta:         Potência no medidor deve ser a potência nominal da usina
        self.usina.pot_medidor = self.cfg['pot_maxima_alvo'] * 2
        self.usina.ug1.potencia = self.cfg['pot_maxima_ug'] * 2
        self.usina.ug2.potencia = self.cfg['pot_maxima_ug'] * 2
        for _ in range(10):  # Ajuste para malha de controle
            self.usina.distribuir_potencia(self.cfg['pot_maxima_alvo'])
            self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
        self.assertEqual(self.usina.pot_medidor, self.cfg['pot_maxima_alvo'])
            
    def test_distribuir_pot_caso_max(self):
            # Teste:            test_distribuir_pot_caso_max
            # Objetivo:         Verificar distribuição de potência máxima
            # Estado inicial:   Tudo normalizado,
            #                   setpoint = 0
            # Resposta:         Soma dos setpoints deve ser a potência nominal da usina]
            for _ in range(10):  # Ajuste para malha de controle
                self.usina.distribuir_potencia(self.cfg['pot_maxima_alvo'])
                self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
            self.assertEqual(self.usina.ug1.setpoint + self.usina.ug2.setpoint, self.cfg['pot_maxima_alvo'])

    def test_divisao_pot_caso_zero(self):
        # Teste:            test_divisao_pot_caso_zero
        # Objetivo:         Verificar distribuição de potência zero (Desligar UGs)
        # Estado inicial:   Tudo normalizado
        # Resposta:         setpoint das UGs deve ser 0
        pot = 0
        for _ in range(10):  # Ajuste para malha de controle
            self.usina.distribuir_potencia(pot)
            self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
            for ug in self.usina.ugs:
                self.assertEqual(ug.setpoint, 0)

    def test_divisao_pot_caso_A(self):
        # Teste:            test_divisao_pot_caso_A
        # Objetivo:         Comprovar divisão adequada da carga entre as UGs
        # Estado inicial:   Alvo < Máximo de uma UG,
        # Resposta:         setpoint da UG1 == alvo, setpoint das demais = 0
        self.usina.erro_nv = 0
        pot = self.cfg['pot_maxima_ug']
        for _ in range(10):  # Ajuste para malha de controle
            self.usina.distribuir_potencia(pot)
            self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
            self.assertEqual(self.usina.ugs[0].setpoint, pot)
            for ug in self.usina.ugs[1:]:
                self.assertEqual(ug.setpoint, 0)

    def test_divisao_pot_caso_B(self):
        # Teste:            test_divisao_pot_caso_B
        # Objetivo:         Comprovar divisão adequada da carga entre as UGs
        # Estado inicial:   Máximo de uma UG < Alvo < (Máximo de uma UG + Margem crítica),
        #                   Nível alvo atingido
        # Resposta:         setpoint da UG1 == Máximo da UG, setpoint das demais = 0
        self.usina.erro_nv = 0
        pot = self.cfg['pot_maxima_ug'] + self.cfg['margem_pot_critica'] * 0.9
        for _ in range(10):  # Ajuste para malha de controle
            self.usina.distribuir_potencia(pot)
            self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
            self.assertEqual(self.usina.ug2.setpoint, 0)
            self.assertEqual(self.usina.ugs[0].setpoint, self.cfg['pot_maxima_ug'])
            for ug in self.usina.ugs[1:]:
                self.assertEqual(ug.setpoint, 0)

    def test_divisao_pot_caso_C(self):
        # Teste:            test_divisao_pot_caso_C
        # Objetivo:         Comprovar divisão adequada da carga entre as UGs
        # Estado inicial:   Alvo > (Máximo de uma UG + Margem crítica),
        #                   Nível alvo atingido
        # Resposta:         setpoint da UG1 == Máximo da UG, setpoint das demais = 0
        self.usina.erro_nv = 0
        pot = self.cfg['pot_maxima_ug'] + self.cfg['margem_pot_critica'] * 1.1
        for _ in range(10):  # Ajuste para malha de controle
            self.usina.distribuir_potencia(pot)
            self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
            self.assertEqual(self.usina.ugs[0].setpoint, self.cfg['pot_maxima_ug'])
            for ug in self.usina.ugs[1:]:
                self.assertEqual(ug.setpoint, 0)

    def test_divisao_pot_caso_D(self):
        # Teste:            test_divisao_pot_caso_D
        # Objetivo:         Comprovar divisão adequada da carga entre as UGs
        # Estado inicial:   Alvo > (Máximo de uma UG + Margem crítica),
        #                   Nível alvo atingido, 
        #                   UGs Sincronizadas
        # Resposta esperada: setpoint da UGs == alvo/Numero de UGs
        self.usina.erro_nv = 0
        for ug in self.usina.ugs:
            ug.sincronizada = True
        pot = self.cfg['pot_maxima_ug'] + self.cfg['margem_pot_critica'] * 1.1
        for _ in range(10):  # Ajuste para malha de controle
            self.usina.distribuir_potencia(pot)
            self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
            self.assertEqual(self.usina.ug1.setpoint, pot / len(self.usina.ugs))
            self.assertEqual(self.usina.ug2.setpoint, pot / len(self.usina.ugs))

    def test_divisao_pot_caso_E(self):
        # Teste:            test_divisao_pot_caso_E
        # Estado inicial:   Alvo > (Máximo de uma UG + Margem crítica),
        #                   Nível alvo não atingido,
        #                   UGs Não Sincronizadas
        # Resposta:         setpoint da UGs == alvo/Numero de UGs
        self.usina.erro_nv = 1
        pot = self.cfg['pot_maxima_ug'] + self.cfg['margem_pot_critica'] * 1.1
        for _ in range(10):  # Ajuste para malha de controle
            self.usina.distribuir_potencia(pot)
            self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
            self.assertEqual(self.usina.ug1.setpoint, pot / 2)
            self.assertEqual(self.usina.ug2.setpoint, pot / 2)

    def test_divisao_pot_caso_F(self):
        # Teste:            test_divisao_pot_caso_E
        # Estado inicial:   Alvo = Pot Nominal
        # Estados testados: UGs com flag (uma UG por vez, uma flag por vez)
        #                   UGs com flag (uma UG por vez, varias flag por vez)
        #                   UGs com flag (varias UGs por vez, varias flag por vez)
        # Resposta:         Não deve partir nenhuma UG com Flag

        pot = self.cfg['pot_maxima_alvo']

        # UGs com flag (uma UG por vez, uma flag por vez)
        for ug in self.usina.ugs:
            ug.setpoint = 1
            ug.flag = 0
        for ug_com_flag in range(len(self.usina.ugs)):
            for bit in range(17):
                for ug in self.usina.ugs:
                    ug.normalizar = MagicMock().return_value(True)
                    ug.flag = 0
                    ug.setpoint = 0
                    ug.atualizar_estado()
                self.usina.ugs[ug_com_flag].indisponibilizar(2 ** bit)
                self.usina.ugs[ug_com_flag].atualizar_estado()
                self.assertEqual(self.usina.ugs[ug_com_flag].flag, 2 ** bit)
                self.usina.distribuir_potencia(pot)
                self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
                for ug in self.usina.ugs:
                    if ug.flag:
                        self.assertEqual(ug.setpoint, 0,
                                         "(uma UG por vez, uma flag por vez) UG{}_FLAG{} .. {}".format(ug.id_da_ug,
                                                                                                       ug.flag,
                                                                                                       bit))
                    else:
                        self.assertGreater(ug.setpoint, 0,
                                           "(uma UG por vez, uma flag por vez) UG{}_FLAG{} .. {}".format(
                                               ug.id_da_ug, ug.flag, bit))

        # UGs com flag (uma UG por vez, varais flags por vez)
        for ug in self.usina.ugs:
            ug.setpoint = 1
            ug.flag = 0
        for ug_com_flag in range(len(self.usina.ugs)):
            for ug in self.usina.ugs:
                ug.flag = 0
            for bit in range(17):
                for ug in self.usina.ugs:
                    ug.normalizar = MagicMock()
                    ug.setpoint = 0
                    ug.atualizar_estado()
                self.usina.ugs[ug_com_flag].indisponibilizar(2 ** bit)
                self.usina.ugs[ug_com_flag].atualizar_estado()
                self.assertGreaterEqual(self.usina.ugs[ug_com_flag].flag, 2 ** bit)
                self.usina.distribuir_potencia(pot)
                self.usina.pot_medidor = sum(
                    ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
                for ug in self.usina.ugs:
                    if ug.flag:
                        self.assertEqual(ug.setpoint, 0,
                                         "(uma UG por vez, uma flag por vez) UG{}_FLAG{} .. {}".format(
                                             ug.id_da_ug, ug.flag, bit))
                    else:
                        self.assertGreater(ug.setpoint, 0,
                                           "(uma UG por vez, uma flag por vez) UG{}_FLAG{} .. {}".format(
                                               ug.id_da_ug, ug.flag, bit))

        # UGs com flag (varais UGs por vez, varais flags por vez)
        for ug in self.usina.ugs:
            ug.setpoint = 1
            ug.flag = 0
        for ug_com_flag in range(len(self.usina.ugs)):
            for bit in range(17):
                for ug in self.usina.ugs:
                    ug.normalizar = MagicMock().return_value(True)
                    ug.setpoint = 0
                    ug.atualizar_estado()
                self.usina.ugs[ug_com_flag].indisponibilizar(2 ** bit)
                self.usina.ugs[ug_com_flag].atualizar_estado()
                self.assertGreaterEqual(self.usina.ugs[ug_com_flag].flag, 2 ** bit)
                self.usina.distribuir_potencia(pot)
                self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
                for ug in self.usina.ugs:
                    if ug.flag:
                        self.assertEqual(ug.setpoint, 0,
                                         "(uma UG por vez, uma flag por vez) UG{}_FLAG{} .. {}".format(ug.id_da_ug,
                                                                                                       ug.flag, bit))
                    else:
                        self.assertGreater(ug.setpoint, 0,
                                           "(uma UG por vez, uma flag por vez) UG{}_FLAG{} .. {}".format(ug.id_da_ug,
                                                                                                         ug.flag, bit))

    def test_divisao_pot_caso_G(self):
        # Teste:            test_divisao_pot_caso_G
        # Estado inicial:   Alvo < Minimo de uma UG
        #                   1 UG sincronizada
        # Resposta:         Uma UG -> pot, outras = 0
        pot = self.cfg['pot_minima'] * 0.75
        for _ in range(10):  # Ajuste para malha de controle
            self.usina.distribuir_potencia(pot)
            self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
        self.assertEqual(self.usina.ug1.setpoint, self.cfg['pot_minima'])
        for ug in self.usina.ugs[1:]:
            self.assertEqual(ug.setpoint, 0)

    def test_divisao_pot_caso_H(self):
        # Teste:            test_divisao_pot_caso_H
        # Estado inicial:   Alvo < Minimo de uma UG
        #                   Todas UGs sincronizadas
        # Resposta:         Uma UG -> pot, outras = 0
        for ug in self.usina.ugs:
            ug.setpoint = self.cfg['pot_maxima_ug']
            ug.potencia = self.cfg['pot_maxima_ug']
            ug.sincronizada = True
        pot = self.cfg['pot_minima'] * 0.75
        for _ in range(10):  # Ajuste para malha de controle
            self.usina.distribuir_potencia(pot)
            self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
        self.assertEqual(self.usina.ug1.setpoint, self.cfg['pot_minima'])
        for ug in self.usina.ugs[1:]:
            self.assertEqual(ug.setpoint, 0)

    def test_divisao_pot_caso_I(self):
        # Teste:            test_divisao_pot_caso_I
        # Estado inicial:   Max de uma UG < Alvo <= Max + margem
        #                   Todas UGs sincronizadas
        # Resposta:         Uma UG -> pot, outras = 0
        for ug in self.usina.ugs:
            ug.setpoint = self.cfg['pot_maxima_ug']
            ug.potencia = self.cfg['pot_maxima_ug']
            ug.sincronizada = True
        pot = self.cfg['pot_maxima_ug'] + self.cfg['margem_pot_critica'] * 0.5
        for _ in range(10):  # Ajuste para malha de controle
            self.usina.distribuir_potencia(pot)
            self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
        for ug in self.usina.ugs:
            self.assertEqual(ug.setpoint, pot / len(self.usina.ugs))

    def test_divisao_pot_caso_J(self):
        # Teste:            test_divisao_pot_caso_J
        # Estado inicial:   Max UG - margem < Alvo <= Max UG
        #                   Todas UGs sincronizadas
        # Resposta:         Uma UG -> pot, outras = 0
        for ug in self.usina.ugs:
            ug.setpoint = self.cfg['pot_maxima_ug']
            ug.potencia = self.cfg['pot_maxima_ug']
            ug.sincronizada = True
        pot = self.cfg['pot_maxima_ug'] - self.cfg['margem_pot_critica'] * 1.1
        for _ in range(10):  # Ajuste para malha de controle
            self.usina.distribuir_potencia(pot)
            self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
        self.assertEqual(self.usina.ug1.setpoint, pot)
        for ug in self.usina.ugs[1:]:
            self.assertEqual(ug.setpoint, 0)

    def test_divisao_pot_caso_K(self):
        # Teste:            test_divisao_pot_caso_K
        # Estado inicial:   Alvo < Min UG
        #                   Todas UGs sincronizadas
        # Resposta:         Uma UG -> pot, outras = 0
        for ug in self.usina.ugs:
            ug.setpoint = self.cfg['pot_maxima_ug']
            ug.potencia = self.cfg['pot_maxima_ug']
            ug.sincronizada = True
        pot = self.cfg['pot_minima'] * 0.5
        for _ in range(10):  # Ajuste para malha de controle
            self.usina.distribuir_potencia(pot)
            self.usina.pot_medidor = sum(ug.setpoint for ug in self.usina.ugs)  # Ajuste para malha de controle
        self.assertEqual(self.usina.ug1.setpoint, self.cfg['pot_minima'])
        for ug in self.usina.ugs[1:]:
            self.assertEqual(ug.setpoint, 0)

    def test_prioridade_por_tempo(self):
        # Se o modo de prioridade estiver por modo "tempo"
        # Então a maquina com menos horas deve partir
        self.usina.modo_de_escolha_das_ugs = 1
        for ug in self.usina.ugs:
            for ug_aux in self.usina.ugs:
                ug_aux.horas_maquina = 1234
                ug_aux.prioridade = 345
            ug.horas_maquina = 123
            ug_aux.prioridade = 34
            lista = self.usina.lista_de_ugs_disponiveis()
            self.assertIs(ug, lista[0])
            self.assertIsNot(ug, lista[1])

    def test_prioridade_munual(self):
        # Se o modo de prioridade estiver por modo "manual"
        # Então a maquina com prioridade
        self.usina.modo_de_escolha_das_ugs = 1
        for ug in self.usina.ugs:
            for ug_aux in self.usina.ugs:
                ug_aux.horas_maquina = 1234
                ug_aux.prioridade = 345
            ug.horas_maquina = 123
            ug_aux.prioridade = 34
            lista = self.usina.lista_de_ugs_disponiveis()
            self.assertIs(ug, lista[0])
            self.assertIsNot(ug, lista[1])

    def test_zona_alerta_teperadura(self):
        # Se temperatura > alerta ent�o setpoint ug < alvo
        for ug in self.usina.ugs:
            for ug_aux in self.usina.ugs:
                ug_aux.temp_mancal_alerta = 70
                ug_aux.temp_mancal_max = 90
                ug_aux.temp_mancal = 25
            ug.temp_mancal = 80
            alvo = round(self.cfg['pot_maxima_ug'] * 0.9, 2)
            ug.mudar_setpoint(alvo)
            ug.atualizar_estado()
            self.assertLess(ug.setpoint, alvo)

    def test_zona_limite_teperadura(self):
        # Se temperatura > limite ent�o setpoint ug == 0
        for ug in self.usina.ugs:
            for ug_aux in self.usina.ugs:
                ug_aux.temp_mancal_alerta = 70
                ug_aux.temp_mancal_max = 90
                ug_aux.temp_mancal = 25
            ug.temp_mancal = 91
            alvo = round(self.cfg['pot_maxima_ug'] * 0.9, 2)
            ug.mudar_setpoint(alvo)
            ug.atualizar_estado()
            self.assertEqual(ug.setpoint, 0)

    def test_zona_alerta_perda_na_grade(self):
        # Se perda na grade > alerta ent�o setpoint ug < alvo
        for ug in self.usina.ugs:
            for ug_aux in self.usina.ugs:
                ug_aux.perda_na_grade_alerta = 2
                ug_aux.perda_na_grade_mancal_max = 3
                ug_aux.perda_na_grade_mancal = 1
            ug.perda_na_grade = 2.5
            alvo = round(self.cfg['pot_maxima_ug'] * 0.9, 2)
            ug.mudar_setpoint(alvo)
            ug.atualizar_estado()
            self.assertLess(ug.setpoint, alvo)

    def test_zona_limite_perda_na_grade(self):
        # Se perda na grade > limite ent�o setpoint ug == 0
        for ug in self.usina.ugs:
            for ug_aux in self.usina.ugs:
                ug_aux.perda_na_grade_alerta = 2
                ug_aux.perda_na_grade_mancal_max = 3
                ug_aux.perda_na_grade_mancal = 1
            ug.perda_na_grade = 3.5
            alvo = round(self.cfg['pot_maxima_ug'] * 0.9, 2)
            ug.mudar_setpoint(alvo)
            ug.atualizar_estado()
            self.assertLess(ug.setpoint, alvo)

if __name__ == '__main__':
    unittest.main()
