import json
import os
from unittest.mock import MagicMock
from src.Condicionadores import *
from src.Leituras import *
from src.LeiturasUSN import *
from src.UnidadeDeGeracao import *
from pyModbusTCP.server import DataBank, ModbusServer


class UnidadeDeGeracao1(UnidadeDeGeracao):
    def __init__(
        self,
        id,
        cfg=None,
        leituras_usina=None
    ):
        super().__init__(id)

        if not cfg or not leituras_usina:
            raise ValueError
        else:
            self.cfg = cfg
            self.leituras_usina = leituras_usina
        
        # carrega as configurações
        config_file = os.path.join(os.path.dirname(__file__), "..", "config.json")
        with open(config_file, "r") as file:
            self.cfg = json.load(file)

        self.setpoint_minimo = self.cfg["pot_minima"]
        self.setpoint_maximo = self.cfg["pot_maxima_ug"]

        self.clp_ip = self.cfg["UG1_slave_ip"]
        self.clp_port = self.cfg["UG1_slave_porta"]
        self.clp = ModbusClient(
            host=self.clp_ip,
            port=self.clp_port,
            timeout=5,
            unit_id=1,
            auto_open=True,
            auto_close=False,
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit00 01.00 - Emergência Supervisório Pressionada
        self.leitura_emergencia_supervisorio_pressionada = LeituraModbusBit(
            "Emergência Supervisório Pressionada",
            self.clp,
            REG_UG1_Alarme01,
            0,
        )
        x = self.leitura_emergencia_supervisorio_pressionada
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit01 01.01 - PCP-U1 - Botão de Emergência Pressionado
        self.leitura_pcp_botao_de_emergencia_pressionado = LeituraModbusBit(
            "PCP - Botão de Emergência Pressionado",
            self.clp,
            REG_UG1_Alarme01,
            1,
        )
        x = self.leitura_pcp_botao_de_emergencia_pressionado
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme01.Bit02 01.02 - Q49 - Botão de Emergência Pressionado
        self.leitura_q49_botao_de_emergencia_pressionado = LeituraModbusBit(
            "Q49 - Botão de Emergência Pressionado",
            self.clp,
            REG_UG1_Alarme01,
            2,
        )
        x = self.leitura_q49_botao_de_emergencia_pressionado
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit02 04.02 - Reg Velocidade - TRIP
        self.leitura_reg_velocidade_trip = LeituraModbusBit(
            "Reg Velocidade - TRIP",
            self.clp,
            REG_UG1_Alarme04,
            2,
        )
        x = self.leitura_reg_velocidade_trip
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit05 04.05 - Dispositivo de SobreVelocidade Mecânico Atuado
        self.leitura_dispositivo_de_sobrevelocidade_mecanico_atuado = LeituraModbusBit(
            "Dispositivo de SobreVelocidade Mecânico Atuado",
            self.clp,
            REG_UG1_Alarme04,
            5,
        )
        x = self.leitura_dispositivo_de_sobrevelocidade_mecanico_atuado
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme04.Bit12 04.12 - Reg Tensão - TRIP
        self.leitura_reg_tensao_trip = LeituraModbusBit(
            "Reg Tensão - TRIP",
            self.clp,
            REG_UG1_Alarme04,
            12,
        )
        x = self.leitura_reg_tensao_trip
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit06 05.06 - Relé de Bloqueio 86M Trip Atuado
        self.leitura_rele_de_bloqueio_86m_trip_atuado = LeituraModbusBit(
            "Relé de Bloqueio 86M Trip Atuado",
            self.clp,
            REG_UG1_Alarme05,
            6,
        )
        x = self.leitura_rele_de_bloqueio_86m_trip_atuado
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit07 05.07 - Relé de Bloqueio 86M Trip Atuado Temporizado
        self.leitura_rele_de_bloqueio_86m_trip_atuado_temporizado = LeituraModbusBit(
            "Relé de Bloqueio 86M Trip Atuado Temporizado",
            self.clp,
            REG_UG1_Alarme05,
            7,
        )
        x = self.leitura_rele_de_bloqueio_86m_trip_atuado_temporizado
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit08 05.08 - Relé de Bloqueio 86M Trip Atuado pelo CLP
        self.leitura_rele_de_bloqueio_86m_trip_atuado_pelo_clp = LeituraModbusBit(
            "Relé de Bloqueio 86M Trip Atuado pelo CLP",
            self.clp,
            REG_UG1_Alarme05,
            8,
        )
        x = self.leitura_rele_de_bloqueio_86m_trip_atuado_pelo_clp
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit09 05.09 - Relé de Bloqueio 86E Trip Atuado
        self.leitura_rele_de_bloqueio_86e_trip_atuado = LeituraModbusBit(
            "Relé de Bloqueio 86E Trip Atuado",
            self.clp,
            REG_UG1_Alarme05,
            9,
        )
        x = self.leitura_rele_de_bloqueio_86e_trip_atuado
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit10 05.10 - Relé de Bloqueio 86E Trip Atuado Temporizado
        self.leitura_rele_de_bloqueio_86e_trip_atuado_temporizado = LeituraModbusBit(
            "Relé de Bloqueio 86E Trip Atuado Temporizado",
            self.clp,
            REG_UG1_Alarme05,
            10,
        )
        x = self.leitura_rele_de_bloqueio_86e_trip_atuado_temporizado
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit11 05.11 - Relé de Bloqueio 86E Trip Atuado pelo CLP
        self.leitura_rele_de_bloqueio_86e_trip_atuado_pelo_clp = LeituraModbusBit(
            "Relé de Bloqueio 86E Trip Atuado pelo CLP",
            self.clp,
            REG_UG1_Alarme05,
            11,
        )
        x = self.leitura_rele_de_bloqueio_86e_trip_atuado_pelo_clp
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit12 05.12 - Relé de Bloqueio 86H Trip Atuado
        self.leitura_rele_de_bloqueio_86h_trip_atuado = LeituraModbusBit(
            "Relé de Bloqueio 86H Trip Atuado",
            self.clp,
            REG_UG1_Alarme05,
            12,
        )
        x = self.leitura_rele_de_bloqueio_86h_trip_atuado
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme05.Bit13 05.13 - Relé de Bloqueio 86H Trip Atuado pelo CLP
        self.leitura_rele_de_bloqueio_86h_trip_atuado_pelo_clp = LeituraModbusBit(
            "Relé de Bloqueio 86H Trip Atuado pelo CLP",
            self.clp,
            REG_UG1_Alarme05,
            13,
        )
        x = self.leitura_rele_de_bloqueio_86h_trip_atuado_pelo_clp
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        # PCH_Covo.Driver.UG01.Alarmes.Alarme06.Bit00 06.00 - Relé de Proteção do Gerador - Trip Atuado
        self.leitura_rele_de_protecao_do_gerador_trip_atuado = LeituraModbusBit(
            "Relé de Proteção do Gerador - Trip Atuado",
            self.clp,
            REG_UG1_Alarme06,
            0,
        )
        x = self.leitura_rele_de_protecao_do_gerador_trip_atuado
        self.condicionadores.append(
            CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x)
        )

        self.leitura_potencia = LeituraModbus(
            "ug{}_Gerador_PotenciaAtivaMedia".format(self.id),
            self.clp,
            REG_UG1_Gerador_PotenciaAtivaMedia,
        )

        self.leitura_horimetro = LeituraModbus(
            "ug{}_HorimetroEletrico_Low".format(self.id),
            self.clp,
            REG_UG1_HorimetroEletrico_Low,
        )

        self.leitura_Operacao_EtapaAtual = LeituraModbus(
            "ug{}_Operacao_EtapaAtual".format(self.id),
            self.clp,
            REG_UG1_Operacao_EtapaAtual,
        )

        self.leitura_Operacao_EtapaAlvo = LeituraModbus(
            "ug{}_Operacao_EtapaAlvo".format(self.id),
            self.clp,
            REG_UG1_Operacao_EtapaAlvo,
        )

        # Gerador - Enrolamento fase R
        self.leitura_temperatura_enrolamento_fase_r = LeituraModbus(
            "Gerador {} - Enrolamento fase R".format(self.id),
            self.clp,
            REG_UG1_Temperatura_01,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_enrolamento_fase_r
        self.condicionador_temperatura_enrolamento_fase_r = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_enrolamento_fase_r)

        # Gerador - Enrolamento Fase S
        self.leitura_temperatura_enrolamento_fase_s = LeituraModbus(
            "Gerador {} - Enrolamento Fase S".format(self.id),
            self.clp,
            REG_UG1_Temperatura_02,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_enrolamento_fase_s
        self.condicionador_temperatura_enrolamento_fase_s = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_enrolamento_fase_s)

        # Gerador - Enrolamento fase T
        self.leitura_temperatura_enrolamento_fase_t = LeituraModbus(
            "Gerador {} - Enrolamento fase T".format(self.id),
            self.clp,
            REG_UG1_Temperatura_03,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_enrolamento_fase_t
        self.condicionador_temperatura_enrolamento_fase_t = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_enrolamento_fase_t)

        # Gerador - Mancal L.A. Escora 01
        self.leitura_temperatura_mancal_la_escora_1 = LeituraModbus(
            "Gerador {} - Mancal L.A. Escora 01".format(self.id),
            self.clp,
            REG_UG1_Temperatura_04,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_la_escora_1
        self.condicionador_temperatura_mancal_la_escora_1 = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_mancal_la_escora_1)

        # Gerador - Mancal L.A. Escora 02
        self.leitura_temperatura_mancal_la_escora_2 = LeituraModbus(
            "Gerador {} - Mancal L.A. Escora 02".format(self.id),
            self.clp,
            REG_UG1_Temperatura_05,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_la_escora_2
        self.condicionador_temperatura_mancal_la_escora_2 = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_mancal_la_escora_2)

        # Gerador - Mancal L. A. Contra Escora 01
        self.leitura_temperatura_mancal_la_contra_escora_1 = LeituraModbus(
            "Gerador {} - Mancal L. A. Contra Escora 01".format(self.id),
            self.clp,
            REG_UG1_Temperatura_07,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_la_contra_escora_1
        self.condicionador_temperatura_mancal_la_contra_escora_1 = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_mancal_la_contra_escora_1)

        # Gerador - Mancal L. A. Contra Escora 02
        self.leitura_temperatura_mancal_la_contra_escora_2 = LeituraModbus(
            "Gerador {} - Mancal L. A. Contra Escora 02".format(self.id),
            self.clp,
            REG_UG1_Temperatura_09,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_la_contra_escora_2
        self.condicionador_temperatura_mancal_la_contra_escora_2 = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_mancal_la_contra_escora_2)

        # Gerador - Mancal L. A. Casquilho
        self.leitura_temperatura_mancal_la_casquilho = LeituraModbus(
            "Gerador {} - Mancal L. A. Casquilho".format(self.id),
            self.clp,
            REG_UG1_Temperatura_06,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_la_casquilho
        self.condicionador_temperatura_mancal_la_casquilho = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_mancal_la_casquilho)

        # Gerador - Mancal L.N.A. Casquilho
        self.leitura_temperatura_mancal_lna_casquilho = LeituraModbus(
            "Gerador {} - Mancal L.N.A. Casquilho".format(self.id),
            self.clp,
            REG_UG1_Temperatura_08,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_lna_casquilho
        self.condicionador_temperatura_mancal_lna_casquilho = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_mancal_lna_casquilho)
        
        # Perda na garde
        self.leitura_perda_na_grade = LeituraDelta(
            "Perda na grade ug{}".format(self.id),
            self.leituras_usina.nv_montante,
            self.leituras_usina.nv_canal_aducao,
        )
        base, limite = 10, 20
        x = self.leitura_perda_na_grade
        self.condicionador_perda_na_grade = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite, ordem=1)
        self.condicionadores.append(self.condicionador_perda_na_grade)

    def acionar_trip_logico(self) -> bool:
        """
        Envia o comando de acionamento do TRIP para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.debug(
                "[UG{}] Acionando sinal (via rede) de TRIP.".format(self.id)
            )
            response = self.clp.write_single_register(
                REG_UG1_Operacao_EmergenciaLigar, 1
            )
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    def remover_trip_logico(self) -> bool:
        """
        Envia o comando de remoção do TRIP para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.debug(
                "[UG{}] Removendo sinal (via rede) de TRIP.".format(self.id)
            )
            response = self.clp.write_single_register(
                REG_UG1_Operacao_EmergenciaLigar, 0
            )
            response = self.clp.write_single_register(
                REG_UG1_Operacao_EmergenciaDesligar, 1
            )
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    def acionar_trip_eletrico(self) -> bool:
        """
        Aciona o TRIP elétricamente via painel

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.debug(
                "[UG{}] Acionando sinal (elétrico) de TRIP.".format(self.id)
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_BLOCK_UG{}".format(self.id)],
                1,
            )
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return True

    def remover_trip_eletrico(self) -> bool:
        """
        Remove o TRIP elétricamente via painel

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.debug(
                "[UG{}] Removendo sinal (elétrico) de TRIP.".format(self.id)
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_BLOCK_UG{}".format(self.id)],
                0,
            )
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return True

    def partir(self) -> bool:
        """
        Envia o comando de parida da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.info(
                "[UG{}] Enviando comando (via rede) de partida.".format(self.id)
            )
            response = self.clp.write_single_register(REG_UG1_Operacao_US, 1)
            self.enviar_setpoint(self.setpoint)
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    def parar(self) -> bool:
        """
        Envia o comando de parada da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.info(
                "[UG{}] Enviando comando (via rede) de parada.".format(self.id)
            )
            response = self.clp.write_single_register(REG_UG1_Operacao_UP, 1)
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    def reconhece_reset_alarmes(self) -> bool:
        """
        Envia o comando de reconhece e reset dos alarmes da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.info(
                "[UG{}] Enviando comando de reconhece e reset alarmes.".format(self.id)
            )
            self.remover_trip_eletrico()
            self.remover_trip_logico()
            response = self.clp.write_single_register(
                REG_UG1_Operacao_PainelReconheceAlarmes, 1
            )
            response = response and self.clp.write_single_register(
                REG_UG1_Operacao_PainelResetAlarmes, 1
            )
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    def enviar_setpoint(self, setpoint_kw: int) -> bool:
        """
        Envia o setpoint desejado para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.setpoint = int(setpoint_kw)
            self.logger.debug(
                "[UG{}] Enviando setpoint {} kW.".format(self.id, int(self.setpoint))
            )
            response = self.clp.write_single_register(REG_UG1_Operacao_US, 1)
            response = response and self.clp.write_single_register(
                REG_UG1_RegV_ColocarCarga, 1
            )
            response = response and self.clp.write_single_register(
                REG_UG1_CtrlPotencia_ModoNivelDesligar, 1
            )
            response = response and self.clp.write_single_register(
                REG_UG1_CtrlPotencia_ModoPotenciaDesligar, 1
            )
            response = response and self.clp.write_single_register(
                REG_UG1_CtrlPotencia_Alvo, int(self.setpoint)
            )
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    @property
    def etapa_alvo(self) -> int:
        try:
            response = self.leitura_Operacao_EtapaAlvo.valor
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    @property
    def etapa_atual(self) -> int:
        try:
            response = self.leitura_Operacao_EtapaAtual.valor
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response
