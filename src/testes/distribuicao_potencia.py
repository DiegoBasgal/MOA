import logging
import unittest

from decimal import Decimal
from datetime import datetime
from unittest.mock import MagicMock, patch

from usina import Usina
from conectores.servidores import Servidores

CICLOS = 50

class TestDistribuicaoPotencia(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logging.disable(logging.INFO)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        logging.disable(logging.NOTSET)
        return super().tearDownClass()

    def setUp(self) -> None:

        self.db_mock = MagicMock()

        self.db_mock.get_parametros_usina.return_value = dict(
            id=1,
            timestamp=datetime(2023, 9, 11, 10, 50, 0),
            modo_autonomo=1,
            emergencia_acionada=0,
            aguardando_reservatorio=0,
            modo_de_escolha_das_ugs=0,
            tda_offline=0,
            clp_online=1,
            clp_ug1_ip="10.101.2.215",
            clp_ug1_porta=502,
            clp_ug2_ip="10.101.2.215",
            clp_ug2_porta=502,
            clp_ug3_ip="10.101.2.215",
            clp_ug3_porta=502,
            clp_sa_ip="10.101.2.215",
            clp_sa_porta=502,
            clp_tda_ip="10.101.2.215",
            clp_tda_porta=502,
            clp_moa_ip="0.0.0.0",
            clp_moa_porta=502,
            nv_alvo=405,
            nv_maximo=Decimal("405.150"),
            nv_minimo=Decimal("404.750"),
            nv_montante=Decimal("405.000"),
            nv_religamento=Decimal("405.850"),
            kp=Decimal("2.5"),
            ki=Decimal("0.05"),
            kd=Decimal("0.0"),
            kie=Decimal("0.1"),
            cx_kp=Decimal("2.0"),
            cx_ki=Decimal("0.1"),
            cx_kie=Decimal("0.0"),
            press_cx_alvo=Decimal("16.3"),
            valor_ie_inicial=Decimal("0.1"),
            pot_minima=Decimal("1360.0"),
            pot_nominal=Decimal("3600.0"),
            pot_nominal_ug=Decimal("3600.0"),
            margem_pot_critica=Decimal("0.06"),
            ug1_pot=Decimal("0.0"),
            ug1_setpot=Decimal("0.0"),
            ug1_prioridade=0,
            ug1_ultimo_estado=1,
            alerta_caixa_espiral_ug1=Decimal("16.0"),
            limite_caixa_espiral_ug1=Decimal("15.5"),
            alerta_temperatura_fase_r_ug1=Decimal("100.0"),
            alerta_temperatura_fase_s_ug1=Decimal("100.0"),
            alerta_temperatura_fase_t_ug1=Decimal("100.0"),
            alerta_temperatura_nucleo_estator_ug1=Decimal("100.0"),
            alerta_temperatura_mancal_rad_dia_1_ug1=Decimal("100.0"),
            alerta_temperatura_mancal_rad_dia_2_ug1=Decimal("100.0"),
            alerta_temperatura_mancal_rad_tra_1_ug1=Decimal("100.0"),
            alerta_temperatura_mancal_rad_tra_2_ug1=Decimal("100.0"),
            alerta_temperatura_saida_de_ar_ug1=Decimal("100.0"),
            alerta_temperatura_mancal_guia_escora_ug1=Decimal("100.0"),
            alerta_temperatura_mancal_guia_radial_ug1=Decimal("100.0"),
            alerta_temperatura_mancal_guia_contra_ug1=Decimal("100.0"),
            limite_temperatura_fase_r_ug1=Decimal("200.0"),
            limite_temperatura_fase_s_ug1=Decimal("200.0"),
            limite_temperatura_fase_t_ug1=Decimal("200.0"),
            limite_temperatura_nucleo_estator_ug1=Decimal("200.0"),
            limite_temperatura_mancal_rad_dia_1_ug1=Decimal("200.0"),
            limite_temperatura_mancal_rad_dia_2_ug1=Decimal("200.0"),
            limite_temperatura_mancal_rad_tra_1_ug1=Decimal("200.0"),
            limite_temperatura_mancal_rad_tra_2_ug1=Decimal("200.0"),
            limite_temperatura_saida_de_ar_ug1=Decimal("200.0"),
            limite_temperatura_mancal_guia_escora_ug1=Decimal("200.0"),
            limite_temperatura_mancal_guia_radial_ug1=Decimal("200.0"),
            limite_temperatura_mancal_guia_contra_ug1=Decimal("200.0"),
            ug2_pot=Decimal("0.0"),
            ug2_setpot=Decimal("0.0"),
            ug2_prioridade=0,
            ug2_ultimo_estado=1,
            alerta_caixa_espiral_ug2=Decimal("16.0"),
            limite_caixa_espiral_ug2=Decimal("15.5"),
            alerta_temperatura_fase_r_ug2=Decimal("100.0"),
            alerta_temperatura_fase_s_ug2=Decimal("100.0"),
            alerta_temperatura_fase_t_ug2=Decimal("100.0"),
            alerta_temperatura_nucleo_estator_ug2=Decimal("100.0"),
            alerta_temperatura_mancal_rad_dia_1_ug2=Decimal("100.0"),
            alerta_temperatura_mancal_rad_dia_2_ug2=Decimal("100.0"),
            alerta_temperatura_mancal_rad_tra_1_ug2=Decimal("100.0"),
            alerta_temperatura_mancal_rad_tra_2_ug2=Decimal("100.0"),
            alerta_temperatura_saida_de_ar_ug2=Decimal("100.0"),
            alerta_temperatura_mancal_guia_escora_ug2=Decimal("100.0"),
            alerta_temperatura_mancal_guia_radial_ug2=Decimal("100.0"),
            alerta_temperatura_mancal_guia_contra_ug2=Decimal("100.0"),
            limite_temperatura_fase_r_ug2=Decimal("200.0"),
            limite_temperatura_fase_s_ug2=Decimal("200.0"),
            limite_temperatura_fase_t_ug2=Decimal("200.0"),
            limite_temperatura_nucleo_estator_ug2=Decimal("200.0"),
            limite_temperatura_mancal_rad_dia_1_ug2=Decimal("200.0"),
            limite_temperatura_mancal_rad_dia_2_ug2=Decimal("200.0"),
            limite_temperatura_mancal_rad_tra_1_ug2=Decimal("200.0"),
            limite_temperatura_mancal_rad_tra_2_ug2=Decimal("200.0"),
            limite_temperatura_saida_de_ar_ug2=Decimal("200.0"),
            limite_temperatura_mancal_guia_escora_ug2=Decimal("200.0"),
            limite_temperatura_mancal_guia_radial_ug2=Decimal("200.0"),
            limite_temperatura_mancal_guia_contra_ug2=Decimal("200.0"),
            ug3_pot=Decimal("0.0"),
            ug3_setpot=Decimal("0.0"),
            ug3_prioridade=0,
            ug3_ultimo_estado=1,
            alerta_caixa_espiral_ug3=Decimal("16.0"),
            limite_caixa_espiral_ug3=Decimal("15.5"),
            alerta_temperatura_fase_r_ug3=Decimal("100.0"),
            alerta_temperatura_fase_s_ug3=Decimal("100.0"),
            alerta_temperatura_fase_t_ug3=Decimal("100.0"),
            alerta_temperatura_nucleo_estator_ug3=Decimal("100.0"),
            alerta_temperatura_mancal_rad_dia_1_ug3=Decimal("100.0"),
            alerta_temperatura_mancal_rad_dia_2_ug3=Decimal("100.0"),
            alerta_temperatura_mancal_rad_tra_1_ug3=Decimal("100.0"),
            alerta_temperatura_mancal_rad_tra_2_ug3=Decimal("100.0"),
            alerta_temperatura_saida_de_ar_ug3=Decimal("100.0"),
            alerta_temperatura_mancal_guia_escora_ug3=Decimal("100.0"),
            alerta_temperatura_mancal_guia_radial_ug3=Decimal("100.0"),
            alerta_temperatura_mancal_guia_contra_ug3=Decimal("100.0"),
            limite_temperatura_fase_r_ug3=Decimal("200.0"),
            limite_temperatura_fase_s_ug3=Decimal("200.0"),
            limite_temperatura_fase_t_ug3=Decimal("200.0"),
            limite_temperatura_nucleo_estator_ug3=Decimal("200.0"),
            limite_temperatura_mancal_rad_dia_1_ug3=Decimal("200.0"),
            limite_temperatura_mancal_rad_dia_2_ug3=Decimal("200.0"),
            limite_temperatura_mancal_rad_tra_1_ug3=Decimal("200.0"),
            limite_temperatura_mancal_rad_tra_2_ug3=Decimal("200.0"),
            limite_temperatura_saida_de_ar_ug3=Decimal("200.0"),
            limite_temperatura_mancal_guia_escora_ug3=Decimal("200.0"),
            limite_temperatura_mancal_guia_radial_ug3=Decimal("200.0"),
            limite_temperatura_mancal_guia_contra_ug3=Decimal("200.0"),
        )

        self.cfg = {
            "nv_alvo": 405.0,
            "nv_minimo": 404.75,
            "nv_maximo": 405.15,
            "nv_maximorum": 407.5,
            "nv_fundo_reservatorio": 404.6,
            "pot_minima": 1360,
            "pot_maxima_ug": 3550.0,
            "pot_maxima_ug1": 3600.0,
            "pot_maxima_ug2": 3600.0,
            "pot_maxima_ug3": 3600.0,
            "pot_maxima_alvo": 9800.0,
            "pot_maxima_usina": 10650.0,
            "pot_limpeza_grade": 500.0,
            "margem_pot_critica": 0.06,
            "kp": 2.5,
            "ki": 0.05,
            "kd": 0.0,
            "kie": 0.1,
            "cx_kp": 2.0,
            "cx_ki": 0.1,
            "cx_kie": 0.0,
            "press_cx_alvo": 16.3,
            "saida_ie_inicial": 0.1
        }

        Servidores.clp = MagicMock()

        self.usina = Usina(cfg=self.cfg, db=self.db_mock)

        self.usina.clp = MagicMock()
        self.usina.oco = MagicMock()
        self.usina.agn = MagicMock()

        self.usina.__potencia_ativa_kW = MagicMock()
        self.usina.__tensao_rs = MagicMock()
        self.usina.__tensao_st = MagicMock()
        self.usina.__tensao_tr = MagicMock()
        self.usina._nv_montante = MagicMock()

        self.usina.__potencia_ativa_kW.valor = 0
        self.usina.__tensao_rs.valor = 68000
        self.usina.__tensao_st.valor = 68000
        self.usina.__tensao_tr.valor = 68000
        self.usina._nv_montante.valor = 405

        for ug in self.usina.ugs:
            ug.oco = MagicMock()

            ug.__potencia_ativa_kW = MagicMock()
            ug.__leitura_pressao_uhrv = MagicMock()
            ug.__leitura_rotacao = MagicMock()
            ug.__leitura_horimetro_hora = MagicMock()
            ug.__leitura_horimetro_min = MagicMock()
            ug.__leitura_etapa_atual = MagicMock()
            ug._leitura_potencia = MagicMock()
            ug._leitura_horimetro = MagicMock()

            ug.__potencia_ativa_kW.valor = 0
            ug.__leitura_pressao_uhrv.valor = 0
            ug.__leitura_rotacao.valor = 0
            ug.__leitura_horimetro_hora.valor = 0
            ug.__leitura_horimetro_min.valor = 0
            ug.__leitura_etapa_atual.valor = 0
            ug._leitura_potencia.valor = 0
            ug._leitura_horimetro.valor = 0

        return super().setUp()

    def test_distribuir_pot_max(self):

        pot_alvo = self.cfg["pot_maxima_usina"]

        self.usina.__potencia_ativa_kW.valor = 0

        self.usina.ug1.__leitura_etapa_atual.valor = 4
        self.usina.ug1._leitura_potencia.valor = 0
        self.usina.ug1.setpoint = self.cfg["pot_minima"]

        self.usina.ug2.__leitura_etapa_atual.valor = 4
        self.usina.ug2._leitura_potencia.valor = 0
        self.usina.ug2.setpoint = self.cfg["pot_minima"]

        for _ in range(CICLOS):
            pot_alvo = self.usina.distribuir_potencia(pot_alvo)
            for ug in self.usina.ugs:
                ug.__leitura_etapa_atual.valor = 4 if ug.setpoint > self.cfg["pot_minima"] else 0

            self.usina.__potencia_ativa_kW.valor = sum(ug.setpoint for ug in self.usina.ugs)

        for ug in self.usina.ugs:
            self.assertEqual(ug.setpoint, 3600)


if __name__ == "__main__":
    unittest.main()