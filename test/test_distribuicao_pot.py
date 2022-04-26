import datetime
import logging
import unittest
from decimal import Decimal
from unittest import mock
from unittest.mock import MagicMock, patch

from src.abstracao_usina import Usina

N_CICLOS_CONTROLE = 100


class TestDistribuicaoPotencia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

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
            "pot_maxima_usina": 1100,
            "pot_maxima_alvo": 1000,
            "pot_minima": 250,
            "margem_pot_critica": 200,
            "pot_maxima_ug": 500,
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
            nv_alvo=Decimal("820.98"),
            nv_maximo=Decimal("821.0"),
            nv_minimo=Decimal("820.0"),
            nv_montante=Decimal("821.99"),
            nv_religamento=Decimal("821.98"),
            pot_minima=Decimal("0.50000"),
            pot_nominal=Decimal("1.00000"),
            pot_nominal_ug=Decimal("0.50000"),
            pot_disp=Decimal("1.10000"),
            timer_erro=30,
            ug1_disp=Decimal("0.5"),
            ug1_pot=Decimal("0.0"),
            ug1_setpot=Decimal("0.0"),
            ug1_sinc=0,
            ug1_tempo=12,
            ug1_prioridade=0,
            ug2_disp=Decimal("0.5"),
            ug2_pot=Decimal("0.5"),
            ug2_setpot=Decimal("0.5"),
            ug2_sinc=1,
            ug2_tempo=17,
            ug2_prioridade=0,
            valor_ie_inicial=Decimal("0.00000"),
            modo_de_escolha_das_ugs=1,
            tolerancia_pot_maxima=Decimal("1.02500"),
            ug1_perda_grade=Decimal("0.000"),
            ug1_perda_grade_maxima=Decimal("2.000"),
            ug1_temp_mancal=Decimal("25.20"),
            ug1_temp_maxima=Decimal("90.00"),
            ug2_perda_grade=Decimal("0.000"),
            ug2_perda_grade_maxima=Decimal("2.000"),
            ug2_temp_mancal=Decimal("25.00"),
            ug2_temp_maxima=Decimal("90.00"),
            pot_maxima_alvo=Decimal("1.00000"),
            ug1_perda_grade_alerta=Decimal("1.000"),
            ug1_temp_alerta=Decimal("75.00"),
            ug2_perda_grade_alerta=Decimal("1.000"),
            ug2_temp_alerta=Decimal("75.00"),
        )
        self.usina = Usina(
            cfg=self.cfg,
            db=self.db_mock,
            con=MagicMock(),
            leituras=MagicMock(autospec=True),
        )

        self.usina.leituras.dj52L_aberto = MagicMock()
        self.usina.leituras.dj52L_condicao_de_fechamento = MagicMock()
        self.usina.leituras.dj52L_falha_fechamento = MagicMock()
        self.usina.leituras.dj52L_falta_vcc = MagicMock()
        self.usina.leituras.dj52L_fechado = MagicMock()
        self.usina.leituras.dj52L_inconsistente = MagicMock()
        self.usina.leituras.dj52L_mola_carregada = MagicMock()
        self.usina.leituras.dj52L_trip = MagicMock()
        self.usina.leituras.nv_canal_aducao = MagicMock()
        self.usina.leituras.nv_montante = MagicMock()
        self.usina.leituras.potencia_ativa_kW = MagicMock()
        self.usina.leituras.tensao_rs = MagicMock()
        self.usina.leituras.tensao_st = MagicMock()
        self.usina.leituras.tensao_tr = MagicMock()
        self.usina.leituras.dj52L_aberto.valor = 0
        self.usina.leituras.dj52L_condicao_de_fechamento.valor = 1
        self.usina.leituras.dj52L_falha_fechamento.valor = 0
        self.usina.leituras.dj52L_falta_vcc.valor = 0
        self.usina.leituras.dj52L_fechado.valor = 1
        self.usina.leituras.dj52L_inconsistente.valor = 0
        self.usina.leituras.dj52L_mola_carregada.valor = 1
        self.usina.leituras.dj52L_trip.valor = 0
        self.usina.leituras.nv_canal_aducao.valor = 643.29
        self.usina.leituras.nv_montante.valor = 643.31
        self.usina.leituras.potencia_ativa_kW.valor = 0
        self.usina.leituras.tensao_rs.valor = 36500
        self.usina.leituras.tensao_st.valor = 36500
        self.usina.leituras.tensao_tr.valor = 36500

        for ug in self.usina.ugs:
            ug.leitura_Operacao_EtapaAlvo = MagicMock()
            ug.leitura_Operacao_EtapaAtual = MagicMock()
            ug.leitura_dispositivo_de_sobrevelocidade_mecanico_atuado = MagicMock()
            ug.leitura_emergencia_supervisorio_pressionada = MagicMock()
            ug.leitura_horimetro = MagicMock()
            ug.leitura_pcp_botao_de_emergencia_pressionado = MagicMock()
            ug.leitura_perda_na_grade = MagicMock()
            ug.leitura_potencia = MagicMock()
            ug.leitura_q49_botao_de_emergencia_pressionado = MagicMock()
            ug.leitura_reg_tensao_trip = MagicMock()
            ug.leitura_reg_velocidade_trip = MagicMock()
            ug.leitura_rele_de_bloqueio_86e_trip_atuado = MagicMock()
            ug.leitura_rele_de_bloqueio_86e_trip_atuado_pelo_clp = MagicMock()
            ug.leitura_rele_de_bloqueio_86e_trip_atuado_temporizado = MagicMock()
            ug.leitura_rele_de_bloqueio_86h_trip_atuado = MagicMock()
            ug.leitura_rele_de_bloqueio_86h_trip_atuado_pelo_clp = MagicMock()
            ug.leitura_rele_de_bloqueio_86m_trip_atuado = MagicMock()
            ug.leitura_rele_de_bloqueio_86m_trip_atuado_pelo_clp = MagicMock()
            ug.leitura_rele_de_bloqueio_86m_trip_atuado_temporizado = MagicMock()
            ug.leitura_rele_de_protecao_do_gerador_trip_atuado = MagicMock()
            ug.leitura_temperatura_enrolamento_fase_r = MagicMock()
            ug.leitura_temperatura_enrolamento_fase_s = MagicMock()
            ug.leitura_temperatura_enrolamento_fase_t = MagicMock()
            ug.leitura_temperatura_mancal_la_casquilho = MagicMock()
            ug.leitura_temperatura_mancal_la_contra_escora_1 = MagicMock()
            ug.leitura_temperatura_mancal_la_contra_escora_2 = MagicMock()
            ug.leitura_temperatura_mancal_la_escora_1 = MagicMock()
            ug.leitura_temperatura_mancal_la_escora_2 = MagicMock()
            ug.leitura_temperatura_mancal_lna_casquilho = MagicMock()
            ug.leitura_Operacao_EtapaAlvo.valor = 0
            ug.leitura_Operacao_EtapaAtual.valor = 0
            ug.leitura_dispositivo_de_sobrevelocidade_mecanico_atuado.valor = 0
            ug.leitura_emergencia_supervisorio_pressionada.valor = 0
            ug.leitura_horimetro.valor = 0
            ug.leitura_pcp_botao_de_emergencia_pressionado.valor = 0
            ug.leitura_perda_na_grade.valor = 0
            ug.leitura_potencia.valor = 0
            ug.leitura_q49_botao_de_emergencia_pressionado.valor = 0
            ug.leitura_reg_tensao_trip.valor = 0
            ug.leitura_reg_velocidade_trip.valor = 0
            ug.leitura_rele_de_bloqueio_86e_trip_atuado.valor = 0
            ug.leitura_rele_de_bloqueio_86e_trip_atuado_pelo_clp.valor = 0
            ug.leitura_rele_de_bloqueio_86e_trip_atuado_temporizado.valor = 0
            ug.leitura_rele_de_bloqueio_86h_trip_atuado.valor = 0
            ug.leitura_rele_de_bloqueio_86h_trip_atuado_pelo_clp.valor = 0
            ug.leitura_rele_de_bloqueio_86m_trip_atuado.valor = 0
            ug.leitura_rele_de_bloqueio_86m_trip_atuado_pelo_clp.valor = 0
            ug.leitura_rele_de_bloqueio_86m_trip_atuado_temporizado.valor = 0
            ug.leitura_rele_de_protecao_do_gerador_trip_atuado.valor = 0
            ug.leitura_temperatura_enrolamento_fase_r.valor = 0
            ug.leitura_temperatura_enrolamento_fase_s.valor = 0
            ug.leitura_temperatura_enrolamento_fase_t.valor = 0
            ug.leitura_temperatura_mancal_la_casquilho.valor = 0
            ug.leitura_temperatura_mancal_la_contra_escora_1.valor = 0
            ug.leitura_temperatura_mancal_la_contra_escora_2.valor = 0
            ug.leitura_temperatura_mancal_la_escora_1.valor = 0
            ug.leitura_temperatura_mancal_la_escora_2.valor = 0
            ug.leitura_temperatura_mancal_lna_casquilho.valor = 0

    def tearDown(self):
        pass

    def test_divisao_pot_caso_zero(self):
        # Teste:            test_divisao_pot_caso_zero
        # Objetivo:         Verificar distribuição de potência zero (Desligar UGs)
        # Resposta:         setpoint das UGs deve ser 0

        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        pot_alvo = 0  # Pot alvo
        self.usina.leituras.potencia_ativa_kW.valor = 0  # Potência no MP
        # == UG1 ==
        self.usina.ug1.leitura_Operacao_EtapaAlvo.valor = 4  # Etapa alvo UG1
        self.usina.ug1.leitura_Operacao_EtapaAtual.valor = 4  # Etapa atual UG1
        self.usina.ug1.leitura_potencia.valor = 0  # Potência UG1
        self.usina.ug1.setpoint = self.cfg["pot_minima"]  # Setpoint UG1
        # == UG2 ==
        self.usina.ug2.leitura_Operacao_EtapaAlvo.valor = 4  # Etapa alvo UG2
        self.usina.ug2.leitura_Operacao_EtapaAtual.valor = 4  # Etapa atual UG2
        self.usina.ug2.leitura_potencia.valor = 0  # Potência UG2
        self.usina.ug2.setpoint = self.cfg["pot_minima"]  # Setpoint UG2
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        for _ in range(N_CICLOS_CONTROLE):
            pot_alvo = self.usina.distribuir_potencia(pot_alvo)
            for ug in self.usina.ugs:
                ug.leitura_Operacao_EtapaAlvo.valor = (
                    4 if ug.setpoint > self.cfg["pot_minima"] else 0
                )
                ug.leitura_Operacao_EtapaAtual.valor = (
                    ug.leitura_Operacao_EtapaAlvo.valor
                )
            self.usina.leituras.potencia_ativa_kW.valor = sum(
                [ug.setpoint for ug in self.usina.ugs]
            )
        # FIM CICLOS DE CONTROLE -----------------------------------------------
        
        # INICIO DA VERIFICAÇÕES -----------------------------------------------
        for ug in self.usina.ugs:
            self.assertEqual(ug.setpoint, pot_alvo)
        # FIM DA VERIFICAÇÕES --------------------------------------------------

    def test_distribuir_pot_caso_max(self):
        # Teste:            test_distribuir_pot_caso_max
        # Objetivo:         Verificar distribuição de potência máxima
        # Resposta:         Soma dos setpoints deve ser a potência nominal da usina

        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        pot_alvo = self.cfg["pot_maxima_alvo"]  # Pot alvo
        self.usina.leituras.potencia_ativa_kW.valor = 0  # Potência no MP
        # == UG1 ==
        self.usina.ug1.leitura_Operacao_EtapaAlvo.valor = 4  # Etapa alvo UG1
        self.usina.ug1.leitura_Operacao_EtapaAtual.valor = 4  # Etapa atual UG1
        self.usina.ug1.leitura_potencia.valor = 0  # Potência UG1
        self.usina.ug1.setpoint = 0  # Setpoint UG1
        # == UG2 ==
        self.usina.ug2.leitura_Operacao_EtapaAlvo.valor = 4  # Etapa alvo UG2
        self.usina.ug2.leitura_Operacao_EtapaAtual.valor = 4  # Etapa atual UG2
        self.usina.ug2.leitura_potencia.valor = 0  # Potência UG2
        self.usina.ug2.setpoint = 0  # Setpoint UG2
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        for _ in range(N_CICLOS_CONTROLE):
            pot_alvo = self.usina.distribuir_potencia(pot_alvo)
            for ug in self.usina.ugs:
                ug.leitura_Operacao_EtapaAlvo.valor = (
                    4 if ug.setpoint > self.cfg["pot_minima"] else 0
                )
                ug.leitura_Operacao_EtapaAtual.valor = (
                    ug.leitura_Operacao_EtapaAlvo.valor
                )
            self.usina.leituras.potencia_ativa_kW.valor = sum(
                [ug.setpoint for ug in self.usina.ugs]
            )
        # FIM CICLOS DE CONTROLE -----------------------------------------------

        # INICIO DA VERIFICAÇÕES -----------------------------------------------
        for ug in self.usina.ugs:
            self.assertEqual(
                self.usina.ug1.setpoint + self.usina.ug2.setpoint,
                self.cfg["pot_maxima_alvo"],
            )
        # FIM DA VERIFICAÇÕES --------------------------------------------------

    def test_distribuir_pot_caso_acima(self):
        # Teste:            test_distribuir_pot_caso_acima
        # Objetivo:         Verificar distribuição de potência caso algo esteja acima do permitido, seja medidor ou UG
        # Resposta:         Potência no medidor deve ser a potência nominal da usina

        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        aux = 2 * self.cfg["pot_maxima_alvo"]
        pot_alvo = aux  # Pot alvo
        self.usina.leituras.potencia_ativa_kW.valor = aux  # Potência no MP
        # == UG1 ==
        self.usina.ug1.leitura_Operacao_EtapaAlvo.valor = 4  # Etapa alvo UG1
        self.usina.ug1.leitura_Operacao_EtapaAtual.valor = 4  # Etapa atual UG1
        self.usina.ug1.leitura_potencia.valor = aux  # Potência UG1
        self.usina.ug1.setpoint = aux  # Setpoint UG1
        # == UG2 ==
        self.usina.ug2.leitura_Operacao_EtapaAlvo.valor = 4  # Etapa alvo UG2
        self.usina.ug2.leitura_Operacao_EtapaAtual.valor = 4  # Etapa atual UG2
        self.usina.ug2.leitura_potencia.valor = aux  # Potência UG2
        self.usina.ug2.setpoint = aux  # Setpoint UG2
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        for _ in range(N_CICLOS_CONTROLE):
            pot_alvo = self.usina.distribuir_potencia(pot_alvo)
            for ug in self.usina.ugs:
                ug.leitura_Operacao_EtapaAlvo.valor = (
                    4 if ug.setpoint > self.cfg["pot_minima"] else 0
                )
                ug.leitura_Operacao_EtapaAtual.valor = (
                    ug.leitura_Operacao_EtapaAlvo.valor
                )
            self.usina.leituras.potencia_ativa_kW.valor = sum(
                [ug.setpoint for ug in self.usina.ugs]
            )
        # FIM CICLOS DE CONTROLE -----------------------------------------------

        # INICIO DA VERIFICAÇÕES -----------------------------------------------
        for ug in self.usina.ugs:
            self.assertEqual(
                self.usina.leituras.potencia_ativa_kW.valor, self.cfg["pot_maxima_alvo"]
            )
        # FIM DA VERIFICAÇÕES --------------------------------------------------

    def test_divisao_pot_caso_B(self):
        # Teste:            test_divisao_pot_caso_B
        # Objetivo:         Comprovar divisão adequada da carga entre as UGs
        # Estado inicial:   Máximo de uma UG < Alvo < (Máximo de uma UG + Margem crítica),
        #                   UGs Não sincronizadas
        # Resposta:         setpoint da primeira UG == Máximo da UG, setpoint das demais = 0

        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        pot_alvo = self.cfg["pot_maxima_ug"] + self.cfg["margem_pot_critica"] * 0.9
        # Pot alvo
        self.usina.leituras.potencia_ativa_kW.valor = 0  # Potência no MP
        # == UG1 ==
        self.usina.ug1.leitura_Operacao_EtapaAlvo.valor = 0  # Etapa alvo UG1
        self.usina.ug1.leitura_Operacao_EtapaAtual.valor = 0  # Etapa atual UG1
        self.usina.ug1.leitura_potencia.valor = 0  # Potência UG1
        self.usina.ug1.setpoint = 0  # Setpoint UG1
        # == UG2 ==
        self.usina.ug2.leitura_Operacao_EtapaAlvo.valor = 0  # Etapa alvo UG2
        self.usina.ug2.leitura_Operacao_EtapaAtual.valor = 0  # Etapa atual UG2
        self.usina.ug2.leitura_potencia.valor = 0  # Potência UG2
        self.usina.ug2.setpoint = 0  # Setpoint UG2
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        for _ in range(N_CICLOS_CONTROLE):
            pot_alvo = self.usina.distribuir_potencia(pot_alvo)
            for ug in self.usina.ugs:
                ug.leitura_Operacao_EtapaAlvo.valor = (
                    4 if ug.setpoint > self.cfg["pot_minima"] else 0
                )
                ug.leitura_Operacao_EtapaAtual.valor = (
                    ug.leitura_Operacao_EtapaAlvo.valor
                )
            self.usina.leituras.potencia_ativa_kW.valor = sum(
                [ug.setpoint for ug in self.usina.ugs]
            )
        # FIM CICLOS DE CONTROLE -----------------------------------------------

        # INICIO DA VERIFICAÇÕES -----------------------------------------------
        self.assertEqual(self.usina.ugs[0].setpoint, self.cfg["pot_maxima_ug"])
        for ug in self.usina.ugs[1:]:
            self.assertEqual(ug.setpoint, 0)
        # FIM DA VERIFICAÇÕES --------------------------------------------------

    def test_divisao_pot_caso_C(self):
        # Teste:            test_divisao_pot_caso_C
        # Objetivo:         Comprovar divisão adequada da carga entre as UGs
        # Estado inicial:   Alvo > (Máximo de uma UG + Margem crítica),
        #                   Nível alvo atingido
        #                   UGs sincronizadas
        # Resposta:         setpoint igual nas duas a metade do alvo

        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        pot_alvo = self.cfg["pot_maxima_ug"] + self.cfg["margem_pot_critica"] * 1.1
        # Pot alvo
        self.usina.leituras.potencia_ativa_kW.valor = 0  # Potência no MP
        # == UG1 ==
        self.usina.ug1.leitura_Operacao_EtapaAlvo.valor = 4  # Etapa alvo UG
        self.usina.ug1.leitura_Operacao_EtapaAtual.valor = 4  # Etapa atual UG1
        self.usina.ug1.leitura_potencia.valor = 0  # Potência UG1
        self.usina.ug1.setpoint = 0  # Setpoint UG1
        # == UG2 ==
        self.usina.ug2.leitura_Operacao_EtapaAlvo.valor = 4  # Etapa alvo UG2
        self.usina.ug2.leitura_Operacao_EtapaAtual.valor = 4  # Etapa atual UG2
        self.usina.ug2.leitura_potencia.valor = 0  # Potência UG2
        self.usina.ug2.setpoint = 0  # Setpoint UG2
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        for _ in range(N_CICLOS_CONTROLE):
            pot_alvo = self.usina.distribuir_potencia(pot_alvo)
            for ug in self.usina.ugs:
                ug.leitura_Operacao_EtapaAlvo.valor = (
                    4 if ug.setpoint > self.cfg["pot_minima"] else 0
                )
                ug.leitura_Operacao_EtapaAtual.valor = (
                    ug.leitura_Operacao_EtapaAlvo.valor
                )
            self.usina.leituras.potencia_ativa_kW.valor = sum(
                [ug.setpoint for ug in self.usina.ugs]
            )
        # FIM CICLOS DE CONTROLE -----------------------------------------------

        # INICIO DA VERIFICAÇÕES -----------------------------------------------
        for ug in self.usina.ugs:
            self.assertEqual(ug.setpoint, pot_alvo / len(self.usina.ugs))
        # FIM DA VERIFICAÇÕES --------------------------------------------------

    def test_divisao_pot_caso_E(self):
        # Teste:            test_divisao_pot_caso_E
        # Estado inicial:   Alvo > (Máximo de uma UG + Margem crítica),
        #                   Nível alvo não atingido,
        #                   UGs Não Sincronizadas
        # Resposta:         setpoint da UGs == alvo/Numero de UGs

        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        pot_alvo = self.cfg["pot_maxima_ug"] + self.cfg["margem_pot_critica"] * 1.1
        # Pot alvo
        self.usina.leituras.potencia_ativa_kW.valor = 0  # Potência no MP
        # == UG1 ==
        self.usina.ug1.leitura_Operacao_EtapaAlvo.valor = 0  # Etapa alvo UG
        self.usina.ug1.leitura_Operacao_EtapaAtual.valor = 0  # Etapa atual UG1
        self.usina.ug1.leitura_potencia.valor = 0  # Potência UG1
        self.usina.ug1.setpoint = 0  # Setpoint UG1
        # == UG2 ==
        self.usina.ug2.leitura_Operacao_EtapaAlvo.valor = 0  # Etapa alvo UG2
        self.usina.ug2.leitura_Operacao_EtapaAtual.valor = 0  # Etapa atual UG2
        self.usina.ug2.leitura_potencia.valor = 0  # Potência UG2
        self.usina.ug2.setpoint = 0  # Setpoint UG2
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        for _ in range(N_CICLOS_CONTROLE):
            pot_alvo = self.usina.distribuir_potencia(pot_alvo)
            for ug in self.usina.ugs:
                ug.leitura_Operacao_EtapaAlvo.valor = (
                    4 if ug.setpoint > self.cfg["pot_minima"] else 0
                )
                ug.leitura_Operacao_EtapaAtual.valor = (
                    ug.leitura_Operacao_EtapaAlvo.valor
                )
            self.usina.leituras.potencia_ativa_kW.valor = sum(
                [ug.setpoint for ug in self.usina.ugs]
            )
        # FIM CICLOS DE CONTROLE -----------------------------------------------

        # INICIO DA VERIFICAÇÕES -----------------------------------------------
        for ug in self.usina.ugs:
            self.assertEqual(ug.setpoint, pot_alvo / len(self.usina.ugs))
        # FIM DA VERIFICAÇÕES --------------------------------------------------

    def test_divisao_pot_caso_G(self):
        # Teste:            test_divisao_pot_caso_G
        # Estado inicial:   Alvo < Minimo de uma UG
        #                   1 UG sincronizada
        # Resposta:         Uma UG -> pot, outras = 0
        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        pot_alvo = self.cfg["pot_minima"] * 0.9
        # Pot alvo
        self.usina.leituras.potencia_ativa_kW.valor = 0  # Potência no MP
        # == UG1 ==
        self.usina.ug1.leitura_Operacao_EtapaAlvo.valor = 4  # Etapa alvo UG
        self.usina.ug1.leitura_Operacao_EtapaAtual.valor = 4  # Etapa atual UG1
        self.usina.ug1.leitura_potencia.valor = 0  # Potência UG1
        self.usina.ug1.setpoint = 0  # Setpoint UG1
        # == UG2 ==
        self.usina.ug2.leitura_Operacao_EtapaAlvo.valor = 0  # Etapa alvo UG2
        self.usina.ug2.leitura_Operacao_EtapaAtual.valor = 0  # Etapa atual UG2
        self.usina.ug2.leitura_potencia.valor = 0  # Potência UG2
        self.usina.ug2.setpoint = 0  # Setpoint UG2
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        for _ in range(N_CICLOS_CONTROLE):
            pot_alvo = self.usina.distribuir_potencia(pot_alvo)
            for ug in self.usina.ugs:
                ug.leitura_Operacao_EtapaAlvo.valor = (
                    4 if ug.setpoint > self.cfg["pot_minima"] else 0
                )
                ug.leitura_Operacao_EtapaAtual.valor = (
                    ug.leitura_Operacao_EtapaAlvo.valor
                )
            self.usina.leituras.potencia_ativa_kW.valor = sum(
                [ug.setpoint for ug in self.usina.ugs]
            )
        # FIM CICLOS DE CONTROLE -----------------------------------------------

        # INICIO DA VERIFICAÇÕES -----------------------------------------------
        self.assertEqual(self.usina.ugs[0].setpoint, self.cfg["pot_minima"])
        for ug in self.usina.ugs[1:]:
            self.assertEqual(ug.setpoint, 0)
        # FIM DA VERIFICAÇÕES --------------------------------------------------

    def test_divisao_pot_caso_H(self):
        # Teste:            test_divisao_pot_caso_H
        # Estado inicial:   Alvo < Minimo de uma UG
        #                   Todas UGs sincronizadas
        # Resposta:         Uma UG -> pot, outras = 0

        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        pot_alvo = self.cfg["pot_minima"] * 0.9
        # Pot alvo
        self.usina.leituras.potencia_ativa_kW.valor = 0  # Potência no MP
        # == UG1 ==
        self.usina.ug1.leitura_Operacao_EtapaAlvo.valor = 4  # Etapa alvo UG
        self.usina.ug1.leitura_Operacao_EtapaAtual.valor = 4  # Etapa atual UG1
        self.usina.ug1.leitura_potencia.valor = 0  # Potência UG1
        self.usina.ug1.setpoint = 0  # Setpoint UG1
        # == UG2 ==
        self.usina.ug2.leitura_Operacao_EtapaAlvo.valor = 4  # Etapa alvo UG2
        self.usina.ug2.leitura_Operacao_EtapaAtual.valor = 4  # Etapa atual UG2
        self.usina.ug2.leitura_potencia.valor = 0  # Potência UG2
        self.usina.ug2.setpoint = 0  # Setpoint UG2
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        for _ in range(N_CICLOS_CONTROLE):
            pot_alvo = self.usina.distribuir_potencia(pot_alvo)
            for ug in self.usina.ugs:
                ug.leitura_Operacao_EtapaAlvo.valor = (
                    4 if ug.setpoint > self.cfg["pot_minima"] else 0
                )
                ug.leitura_Operacao_EtapaAtual.valor = (
                    ug.leitura_Operacao_EtapaAlvo.valor
                )
            self.usina.leituras.potencia_ativa_kW.valor = sum(
                [ug.setpoint for ug in self.usina.ugs]
            )
        # FIM CICLOS DE CONTROLE -----------------------------------------------

        # INICIO DA VERIFICAÇÕES -----------------------------------------------
        self.assertEqual(self.usina.ugs[0].setpoint, self.cfg["pot_minima"])
        for ug in self.usina.ugs[1:]:
            self.assertEqual(ug.setpoint, 0)
        # FIM DA VERIFICAÇÕES --------------------------------------------------

    def test_divisao_pot_caso_J(self):
        # Teste:            test_divisao_pot_caso_J
        # Estado inicial:   Max UG - margem < Alvo <= Max UG
        #                   Todas UGs sincronizadas
        # Resposta:         Uma UG -> pot, outras = 0

        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        for ug in self.usina.ugs:
            ug.setpoint = self.cfg["pot_maxima_ug"]
            ug.potencia = self.cfg["pot_maxima_ug"]
            ug.sincronizada = True
        pot_alvo = self.cfg["pot_maxima_ug"] - self.cfg["margem_pot_critica"] * 1.1
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        for _ in range(N_CICLOS_CONTROLE):
            pot_alvo = self.usina.distribuir_potencia(pot_alvo)
            for ug in self.usina.ugs:
                ug.leitura_Operacao_EtapaAlvo.valor = (
                    4 if ug.setpoint > self.cfg["pot_minima"] else 0
                )
                ug.leitura_Operacao_EtapaAtual.valor = (
                    ug.leitura_Operacao_EtapaAlvo.valor
                )
            self.usina.leituras.potencia_ativa_kW.valor = sum(
                [ug.setpoint for ug in self.usina.ugs]
            )
        # FIM CICLOS DE CONTROLE -----------------------------------------------

        # INICIO DA VERIFICAÇÕES -----------------------------------------------
        self.assertEqual(self.usina.ug1.setpoint, pot_alvo)
        for ug in self.usina.ugs[1:]:
            self.assertEqual(ug.setpoint, 0)
        # FIM DA VERIFICAÇÕES --------------------------------------------------

    def test_divisao_pot_caso_K(self):
        # Teste:            test_divisao_pot_caso_K
        # Estado inicial:   Alvo < Min UG
        #                   Todas UGs sincronizadas
        # Resposta:         Uma UG -> pot, outras = 0
        
        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        for ug in self.usina.ugs:
            ug.setpoint = self.cfg["pot_maxima_ug"]
            ug.potencia = self.cfg["pot_maxima_ug"]
            ug.sincronizada = True
        pot_alvo = self.cfg["pot_minima"] * 0.5
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        for _ in range(N_CICLOS_CONTROLE):
            pot_alvo = self.usina.distribuir_potencia(pot_alvo)
            for ug in self.usina.ugs:
                ug.leitura_Operacao_EtapaAlvo.valor = (
                    4 if ug.setpoint > self.cfg["pot_minima"] else 0
                )
                ug.leitura_Operacao_EtapaAtual.valor = (
                    ug.leitura_Operacao_EtapaAlvo.valor
                )
            self.usina.leituras.potencia_ativa_kW.valor = sum(
                [ug.setpoint for ug in self.usina.ugs]
            )
        # FIM CICLOS DE CONTROLE -----------------------------------------------
        
        # INICIO DA VERIFICAÇÕES -----------------------------------------------
        self.assertEqual(self.usina.ug1.setpoint, self.cfg["pot_minima"])
        for ug in self.usina.ugs[1:]:
            self.assertEqual(ug.setpoint, 0)
        # FIM DA VERIFICAÇÕES --------------------------------------------------

    def test_prioridade_por_tempo(self):
        # Se o modo de prioridade estiver por modo "tempo"
        # Então a maquina com menos horas deve partir

        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        self.usina.modo_de_escolha_das_ugs = 1
        for ug in self.usina.ugs:
            ug.leitura_Operacao_EtapaAtual.valor = 0
            ug.leitura_Operacao_EtapaAlvo.valor = 0
            ug.leitura_potencia.valor = 0
            ug.prioridade = 10
            ug.leitura_horimetro.valor = 100
        self.usina.ug2.leitura_horimetro.valor = 10
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        lista = self.usina.lista_de_ugs_disponiveis()
        # FIM CICLOS DE CONTROLE -----------------------------------------------

        # INICIO DA VERIFICAÇÕES -----------------------------------------------       
        self.assertIs(self.usina.ug2, lista[0])
        self.assertIsNot(self.usina.ug2, lista[1])
        # FIM DA VERIFICAÇÕES --------------------------------------------------
        

    def test_prioridade_manual(self):
        # Se o modo de prioridade estiver por modo "manual"
        # Então a maquina com prioridade

        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        self.usina.modo_de_escolha_das_ugs = 2
        for ug in self.usina.ugs:
            ug.leitura_Operacao_EtapaAtual.valor = 0
            ug.leitura_Operacao_EtapaAlvo.valor = 0
            ug.leitura_potencia.valor = 0
            ug.prioridade = 10
            ug.leitura_horimetro.valor = 100
        self.usina.ug2.prioridade = 1
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        lista = self.usina.lista_de_ugs_disponiveis()
        # FIM CICLOS DE CONTROLE -----------------------------------------------

        # INICIO DA VERIFICAÇÕES -----------------------------------------------       
        self.assertIs(self.usina.ug2, lista[0])
        self.assertIsNot(self.usina.ug2, lista[1])
        # FIM DA VERIFICAÇÕES --------------------------------------------------


    def test_prioridade_sincronismo(self):
        # A maquina sincronizando/sincronizada tem prioridade

        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        self.usina.modo_de_escolha_das_ugs = 1
        for ug in self.usina.ugs:
            ug.leitura_Operacao_EtapaAtual.valor = 0
            ug.leitura_Operacao_EtapaAlvo.valor = 0
            ug.leitura_potencia.valor = 0
            ug.prioridade = 10
            ug.leitura_horimetro.valor = 100
        self.usina.ug2.leitura_Operacao_EtapaAtual.valor = 4
        self.usina.ug2.leitura_Operacao_EtapaAlvo.valor = 4
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        lista = self.usina.lista_de_ugs_disponiveis()
        # FIM CICLOS DE CONTROLE -----------------------------------------------

        # INICIO DA VERIFICAÇÕES -----------------------------------------------       
        self.assertIs(self.usina.ug2, lista[0])
        self.assertIsNot(self.usina.ug2, lista[1])
        # FIM DA VERIFICAÇÕES --------------------------------------------------


    def test_prioridade_potencia(self):
        # A maquina com a maior potência tem prioridade

        # INICIO DECLARAÇÃO ESTADO INICIAL -------------------------------------
        self.usina.modo_de_escolha_das_ugs = 1
        for ug in self.usina.ugs:
            ug.leitura_Operacao_EtapaAtual.valor = 4
            ug.leitura_Operacao_EtapaAlvo.valor = 4
            ug.leitura_potencia.valor = 1000
            ug.prioridade = 10
            ug.leitura_horimetro.valor = 100
        self.usina.ug2.leitura_potencia.valor = 1500
        # FIM DECLARAÇÃO ESTADO INICIAL ----------------------------------------

        # INICIO CICLOS DE CONTROLE --------------------------------------------
        lista = self.usina.lista_de_ugs_disponiveis()
        # FIM CICLOS DE CONTROLE -----------------------------------------------

        # INICIO DA VERIFICAÇÕES -----------------------------------------------       
        self.assertIs(self.usina.ug2, lista[0])
        self.assertIsNot(self.usina.ug2, lista[1])
        # FIM DA VERIFICAÇÕES --------------------------------------------------


if __name__ == "__main__":
    unittest.main()
