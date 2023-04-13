from dataclasses import Field
import logging
import unittest
from datetime import datetime, timedelta
from decimal import Decimal
from unittest import mock
from unittest.mock import MagicMock, patch

from src.abstracao_usina import Usina
import MOA


class TestAgendamentos(unittest.TestCase):
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
            timestamp=datetime(2021, 9, 17, 10, 18, 40),
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

    def test_executa_agendamento_simples(self):
        # Teste:            test_executa_agendamento_simples
        # Objetivo:         Verificar se o moa executa um evento programado teste
        # Estado inicial:   1 agendamento para agora
        # Resposta:         O sm vai para o estado de tratamento de agenda e aciona e emergencia
        self.db_mock.get_agendamentos_pendentes.return_value = [
            (1, datetime.utcnow(), 0, 777, 0),
        ]
        self.usina.disparar_mensagem_teste = MagicMock()
        estado = MOA.ValoresInternosAtualizados(self.usina)
        estado = estado.run()
        self.assertIsInstance(estado, MOA.AgendamentosPendentes)
        estado = estado.run()
        self.usina.disparar_mensagem_teste.assert_called_once()

    # Se houver pelo menos 1 agendamento muito atrasado (> 5 min), ele sinaliza e aciona a emergencia
    def test_executa_agendamentos_atraso_grande(self):
        # Teste:            test_executa_agendamentos_atraso_grande
        # Objetivo:         Verificar se o moa aciona a emergência caso um agendamento atrase muito
        # Estado inicial:   1 agendamento atrasado 6 minutos
        # Resposta:         O sm vai para o estado de tratamento de agenda e executa uma emergencia na clp
        self.db_mock.get_agendamentos_pendentes.return_value = [
            (1, datetime.utcnow() - timedelta(minutes=6), 0, 777, 0),
        ]

        self.usina.acionar_emergencia = MagicMock()
        estado = MOA.ValoresInternosAtualizados(self.usina)
        estado = estado.run()
        self.assertIsInstance(estado, MOA.AgendamentosPendentes)
        estado = estado.run()
        self.usina.acionar_emergencia.assert_called_once()

    # Se houver 4 ou mais agendamentos levemente atrasados (< 5 min), ele sinaliza o erro e aciona e emergencia
    def test_executa_agendamentos_atraso_multiplo(self):
        # Teste:            test_executa_agendamentos_atraso_multiplo
        # Objetivo:         Verificar se o moa aciona a emergência caso varios agendamentos atrasados
        # Estado inicial:   5 agendamentos atrasados >1 minuto
        # Resposta:         O sm vai para o estado de tratamento de agenda e executa uma emergencia na clp
        self.db_mock.get_agendamentos_pendentes.return_value = [
            (1, datetime.utcnow() - timedelta(seconds=61), 0, 777, 0),
            (2, datetime.utcnow() - timedelta(seconds=61), 0, 777, 0),
            (3, datetime.utcnow() - timedelta(seconds=61), 0, 777, 0),
            (4, datetime.utcnow() - timedelta(seconds=61), 0, 777, 0),
            (5, datetime.utcnow() - timedelta(seconds=61), 0, 777, 0),
        ]

        self.usina.acionar_emergencia = MagicMock()
        estado = MOA.ValoresInternosAtualizados(self.usina)
        estado = estado.run()
        self.assertIsInstance(estado, MOA.AgendamentosPendentes)
        estado = estado.run()
        self.usina.acionar_emergencia.assert_called_once()


if __name__ == "__main__":
    unittest.main()
