import logging
import subprocess

import src.mensageiro.voip as voip

from time import sleep, time
from datetime import datetime, timedelta
from pyModbusTCP.server import DataBank

from src.codes import *
from src.Leituras import *
from src.Condicionadores import *

from src.UG1 import UnidadeDeGeracao1
from src.UG2 import UnidadeDeGeracao2
from src.LeiturasUSN import LeiturasUSN
from src.field_connector import FieldConnector


logger = logging.getLogger("__main__")


class Usina:
    def __init__(self, cfg=None, db=None, con=None, leituras=None):

        if not cfg or not db:
            raise ValueError
        else:
            self.cfg = cfg
            self.db = db

        if con:
            self.con = con
        else:

            self.con = FieldConnector(self.cfg)

        if leituras:
            self.leituras = leituras
        else:

            self.leituras = LeiturasUSN(self.cfg)

        self.state_moa = 1

        # Inicializa Objs da usina

        self.ug1 = UnidadeDeGeracao1(1, cfg=self.cfg, leituras_usina=self.leituras)
        self.ug2 = UnidadeDeGeracao2(2, cfg=self.cfg, leituras_usina=self.leituras)
        self.ugs = [self.ug1, self.ug2]

        self.avisado_em_eletrica = False

        # Define as vars inciais
        self.ts_ultima_tesntativa_de_normalizacao = datetime.now()

        self.erro_nv = 0
        self.pot_disp = 0
        self.state_moa = 0
        self.controle_p = 0
        self.controle_i = 0
        self.controle_d = 0
        self.modo_autonomo = 1
        self.erro_nv_anterior = 0
        self.nv_montante_recente = 0
        self.nv_montante_anterior = 0
        self.agendamentos_atrasados = 0
        self.db_emergencia_acionada = 0
        self.modo_de_escolha_das_ugs = 0
        self.clp_emergencia_acionada = 0
        self.aguardando_reservatorio = 0
        self.tentativas_de_normalizar = 0

        self.tensao_ok = False
        self.timer_tensao = None
        self.acionar_voip = False
        self.falha_abertura_comp = False
        self.avisado_em_eletrica = False
        self.borda_aviso_clp_tda = False
        self.borda_aviso_clp_ug1 = False
        self.borda_aviso_clp_ug2 = False
        self.borda_aviso_clp_pacp = False
        self.falha_fechamento_comp = False
        self.deve_tentar_normalizar = True
        self.falha_fechamento_DJ52L = False
        self.alarme_temp_oleo_trafo = False
        self.alarme_temp_enrol_trafo = False
        self.falha_part_grupo_diesel = False

        self.ts_nv = []
        self.condicionadores = []
        self.nv_montante_recentes = []
        self.nv_montante_anteriores = []

        self.clp = ModbusClient(
            host=self.cfg["USN_slave_ip"],
            port=self.cfg["USN_slave_porta"],
            timeout=5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )

        self.relé_86bf_atuado_falha_disjuntores = LeituraModbusBit('01.03 - Relé 86BF Atuado (Falha Disjuntores)', self.clp, REG_USINA_Alarme01, 3)
        x = self.relé_86bf_atuado_falha_disjuntores
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_86te_atuado_falha_trafo_elevador = LeituraModbusBit('01.04 - Relé 86TE Atuado (falha Trafo Elevador)', self.clp, REG_USINA_Alarme01, 4)
        x = self.relé_86te_atuado_falha_trafo_elevador
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.servauxiliar_seccionadora_89sa_aberta = LeituraModbusBit('01.06 - ServAuxiliar - Seccionadora 89SA Aberta', self.clp, REG_USINA_Alarme01, 6)
        x = self.servauxiliar_seccionadora_89sa_aberta
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.qpse_relé_proteção_woodward_f67_mra4_trip_atuado = LeituraModbusBit('01.10 - QPSE - Relé Proteção Woodward F67 (MRA4) - Trip Atuado', self.clp, REG_USINA_Alarme01, 10)
        x = self.qpse_relé_proteção_woodward_f67_mra4_trip_atuado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.qpse_relé_proteção_woodward_f67_mra4_falha_de_hardware = LeituraModbusBit('01.11 - QPSE - Relé Proteção Woodward F67 (MRA4) - Falha de Hardware', self.clp, REG_USINA_Alarme01, 11)
        x = self.qpse_relé_proteção_woodward_f67_mra4_falha_de_hardware
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.pacp_relé_proteção_sel787_trip_atuado = LeituraModbusBit('01.13 - PACP - Relé Proteção SEL787 - Trip Atuado', self.clp, REG_USINA_Alarme01, 13)
        x = self.pacp_relé_proteção_sel787_trip_atuado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.pacp_relé_proteção_sel787_falha_de_hardware = LeituraModbusBit('01.14 - PACP - Relé Proteção SEL787 - Falha de Hardware', self.clp, REG_USINA_Alarme01, 14)
        x = self.pacp_relé_proteção_sel787_falha_de_hardware
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.disjuntor_52l_falha_na_abertura = LeituraModbusBit('02.00 - Disjuntor 52L - Falha na Abertura', self.clp, REG_USINA_Alarme02, 00)
        x = self.disjuntor_52l_falha_na_abertura
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.disjuntor_52l_falha_inconsistência = LeituraModbusBit('02.02 - Disjuntor 52L - Falha Inconsistência', self.clp, REG_USINA_Alarme02, 2)
        x = self.disjuntor_52l_falha_inconsistência
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.seccionadora_89l_falha_abertura_indevida = LeituraModbusBit('02.04 - Seccionadora 89L - Falha Abertura indevida', self.clp, REG_USINA_Alarme02, 4)
        x = self.seccionadora_89l_falha_abertura_indevida
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.seccionadora_89l_falha_aberta = LeituraModbusBit('02.05 - Seccionadora 89L - Falha Aberta', self.clp, REG_USINA_Alarme02, 5)
        x = self.seccionadora_89l_falha_aberta
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.trafo_elevador_monitor_falha_de_hardware = LeituraModbusBit('02.07 - Trafo Elevador - Monitor Falha de Hardware', self.clp, REG_USINA_Alarme02, 7)
        x = self.trafo_elevador_monitor_falha_de_hardware
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.trafo_elevador_falha_relé_buchholz_alarme = LeituraModbusBit('02.10 - Trafo Elevador - Falha Relé BuchHolz Alarme', self.clp, REG_USINA_Alarme02, 10)
        x = self.trafo_elevador_falha_relé_buchholz_alarme
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.trafo_elevador_falha_relé_buchholz_trip = LeituraModbusBit('02.11 - Trafo Elevador - Falha Relé BuchHolz Trip', self.clp, REG_USINA_Alarme02, 11)
        x = self.trafo_elevador_falha_relé_buchholz_trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.trafo_elevador_temperatura_enrolamento_alarme = LeituraModbusBit('02.12 - Trafo Elevador - Temperatura Enrolamento Alarme', self.clp, REG_USINA_Alarme02, 12)
        x = self.trafo_elevador_temperatura_enrolamento_alarme
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.trafo_elevador_temperatura_enrolamento_trip = LeituraModbusBit('02.13 - Trafo Elevador - Temperatura Enrolamento Trip', self.clp, REG_USINA_Alarme02, 13)
        x = self.trafo_elevador_temperatura_enrolamento_trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.trafo_elevador_temperatura_óleo_alarme = LeituraModbusBit('02.14 - Trafo Elevador - Temperatura Óleo Alarme', self.clp, REG_USINA_Alarme02, 14)
        x = self.trafo_elevador_temperatura_óleo_alarme
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.trafo_elevador_temperatura_óleo_trip = LeituraModbusBit('02.15 - Trafo Elevador - Temperatura Óleo Trip', self.clp, REG_USINA_Alarme02, 15)
        x = self.trafo_elevador_temperatura_óleo_trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.trafo_elevador_válvula_alivio_alarme = LeituraModbusBit('03.00 - Trafo Elevador - Válvula Alivio Alarme', self.clp, REG_USINA_Alarme03, 00)
        x = self.trafo_elevador_válvula_alivio_alarme
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.trafo_elevador_válvula_alivio_trip = LeituraModbusBit('03.01 - Trafo Elevador - Válvula Alivio Trip', self.clp, REG_USINA_Alarme03, 1)
        x = self.trafo_elevador_válvula_alivio_trip
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.poço_de_drenagem_nível_inundação_trip_nível_bóia_02 = LeituraModbusBit('03.06 - Poço de Drenagem - Nível Inundação TRIP (Nível Bóia 02)', self.clp, REG_USINA_Alarme03, 6)
        x = self.poço_de_drenagem_nível_inundação_trip_nível_bóia_02
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.falha_de_comunicação_com_o_relé_de_proteção_sel_787 = LeituraModbusBit('04.10 - Falha de Comunicação com o Relé de Proteção SEL 787', self.clp, REG_USINA_Alarme04, 10)
        x = self.falha_de_comunicação_com_o_relé_de_proteção_sel_787
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.pacp_alimentação_circuitos_de_comando_disj_q125_0_desligado = LeituraModbusBit('05.02 - PACP - Alimentação Circuitos de Comando - Disj. Q125_0 Desligado', self.clp, REG_USINA_Alarme05, 2)
        x = self.pacp_alimentação_circuitos_de_comando_disj_q125_0_desligado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.pacp_alimentação_circuitos_de_comando_do_disj_52l_disj_q125_1_desligado = LeituraModbusBit('05.03 - PACP - Alimentação Circuitos de Comando do Disj 52L - Disj. Q125_1 Desligado', self.clp, REG_USINA_Alarme05, 3)
        x = self.pacp_alimentação_circuitos_de_comando_do_disj_52l_disj_q125_1_desligado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.pacp_alimentação_relé_de_proteção_sel787_disj_q125_2_desligado = LeituraModbusBit('05.04 - PACP - Alimentação Relé de Proteção SEL787 - Disj. Q125_2 Desligado', self.clp, REG_USINA_Alarme05, 4)
        x = self.pacp_alimentação_relé_de_proteção_sel787_disj_q125_2_desligado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.pcp_u1_alimentação_circuitos_de_comando_disj_q24_1_desligado = LeituraModbusBit('05.06 - PCP-U1 - Alimentação Circuitos de Comando - Disj. Q24_1 Desligado', self.clp, REG_USINA_Alarme05, 6)
        x = self.pcp_u1_alimentação_circuitos_de_comando_disj_q24_1_desligado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.pcp_u2_alimentação_fonte_125_24vcc_disj_q125_3_desligado = LeituraModbusBit('05.07 - PCP-U2 - Alimentação Fonte 125/24Vcc - Disj. Q125_3 Desligado', self.clp, REG_USINA_Alarme05, 7)
        x = self.pcp_u2_alimentação_fonte_125_24vcc_disj_q125_3_desligado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.pdsa_alimentação_pacp_disj_q220_4_desligado = LeituraModbusBit('06.05 - PDSA - Alimentação PACP - Disj. Q220_4 Desligado', self.clp, REG_USINA_Alarme06, 5)
        x = self.pdsa_alimentação_pacp_disj_q220_4_desligado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.pdsa_alimentação_disj_52l_carregamento_de_mola_disj_q220_8_desligado = LeituraModbusBit('06.09 - PDSA - Alimentação Disj 52L Carregamento de Mola - Disj. Q220_8 Desligado', self.clp, REG_USINA_Alarme06, 9)
        x = self.pdsa_alimentação_disj_52l_carregamento_de_mola_disj_q220_8_desligado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.qpse_alimentação_woodward_f67_disj_q125_0_desligado = LeituraModbusBit('08.04 - QPSE - Alimentação Woodward F67 - Disj. Q125_0 Desligado', self.clp, REG_USINA_Alarme08, 4)
        x = self.qpse_alimentação_woodward_f67_disj_q125_0_desligado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_sel787_diferencial_do_transformador_87t = LeituraModbusBit('08.08 - Relé de Proteção SEL787 - Diferencial do Transformador (87T)', self.clp, REG_USINA_Alarme08, 8)
        x = self.relé_de_proteção_sel787_diferencial_do_transformador_87t
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_sel787_sobrecorrente_instantânea_de_fase_lado_34_5kv_50pat = LeituraModbusBit('08.09 - Relé de Proteção SEL787 - Sobrecorrente Instantânea de Fase Lado 34,5kV (50PAT)', self.clp, REG_USINA_Alarme08, 9)
        x = self.relé_de_proteção_sel787_sobrecorrente_instantânea_de_fase_lado_34_5kv_50pat
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_sel787_sobrecorrente_temporizada_de_fase_lado_34_5kv_51pat = LeituraModbusBit('08.10 - Relé de Proteção SEL787 - Sobrecorrente Temporizada de Fase Lado 34,5kV (51PAT)', self.clp, REG_USINA_Alarme08, 10)
        x = self.relé_de_proteção_sel787_sobrecorrente_temporizada_de_fase_lado_34_5kv_51pat
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_sel787_sobrecorrente_temporizada_de_fase_lado_4_16kv_51pbt = LeituraModbusBit('08.11 - Relé de Proteção SEL787 - Sobrecorrente Temporizada de Fase Lado 4,16kV (51PBT)', self.clp, REG_USINA_Alarme08, 11)
        x = self.relé_de_proteção_sel787_sobrecorrente_temporizada_de_fase_lado_4_16kv_51pbt
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_sel787_sobrecorrente_de_neutro_temporizada_51nat = LeituraModbusBit('08.12 - Relé de Proteção SEL787 - Sobrecorrente de Neutro Temporizada (51NAT)', self.clp, REG_USINA_Alarme08, 12)
        x = self.relé_de_proteção_sel787_sobrecorrente_de_neutro_temporizada_51nat
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_sel787_sobrecorrente_residual_temporizada_51gat = LeituraModbusBit('08.13 - Relé de Proteção SEL787 - Sobrecorrente Residual Temporizada (51GAT)', self.clp, REG_USINA_Alarme08, 13)
        x = self.relé_de_proteção_sel787_sobrecorrente_residual_temporizada_51gat
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.sistema_de_incêndio_atuado = LeituraModbusBit('09.11 - Sistema de Incêndio Atuado', self.clp, REG_USINA_Alarme09, 11)
        x = self.sistema_de_incêndio_atuado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_da_linha_mra4_sobrecorrente_direcional_com_restrição_por_tensão_67vr = LeituraModbusBit('10.00 - Relé de Proteção da Linha (MRA4) - Sobrecorrente Direcional com Restrição por Tensão - 67VR', self.clp, REG_USINA_Alarme10, 00)
        x = self.relé_de_proteção_da_linha_mra4_sobrecorrente_direcional_com_restrição_por_tensão_67vr
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_da_linha_mra4_sobrecorrente_temporizada_de_fase_51p = LeituraModbusBit('10.01 - Relé de Proteção da Linha (MRA4) - Sobrecorrente Temporizada de Fase - 51P', self.clp, REG_USINA_Alarme10, 1)
        x = self.relé_de_proteção_da_linha_mra4_sobrecorrente_temporizada_de_fase_51p
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_da_linha_mra4_sobrecorrente_direcional_de_fase_67r = LeituraModbusBit('10.02 - Relé de Proteção da Linha (MRA4) - Sobrecorrente Direcional de Fase - 67R', self.clp, REG_USINA_Alarme10, 2)
        x = self.relé_de_proteção_da_linha_mra4_sobrecorrente_direcional_de_fase_67r
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_da_linha_mra4_sobrecorrente_direcional_de_fase_67f = LeituraModbusBit('10.03 - Relé de Proteção da Linha (MRA4) - Sobrecorrente Direcional de Fase - 67F', self.clp, REG_USINA_Alarme10, 3)
        x = self.relé_de_proteção_da_linha_mra4_sobrecorrente_direcional_de_fase_67f
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_da_linha_mra4_sobrecorrente_temporizada_de_neutro_51n = LeituraModbusBit('10.04 - Relé de Proteção da Linha (MRA4) - Sobrecorrente Temporizada de Neutro - 51N', self.clp, REG_USINA_Alarme10, 4)
        x = self.relé_de_proteção_da_linha_mra4_sobrecorrente_temporizada_de_neutro_51n
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_da_linha_mra4_sobrecorrente_de_sequência_negativa_temporizada_46 = LeituraModbusBit('10.05 - Relé de Proteção da Linha (MRA4) - Sobrecorrente de Sequência Negativa Temporizada - 46', self.clp, REG_USINA_Alarme10, 5)
        x = self.relé_de_proteção_da_linha_mra4_sobrecorrente_de_sequência_negativa_temporizada_46
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.relé_de_proteção_da_linha_mra4_sobretensão_de_fase_59p = LeituraModbusBit('10.07 - Relé de Proteção da Linha (MRA4) - Sobretensão de Fase - 59P', self.clp, REG_USINA_Alarme10, 7)
        x = self.relé_de_proteção_da_linha_mra4_sobretensão_de_fase_59p
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_da_linha_mra4_sobrefrequência_nível_1_81o = LeituraModbusBit('10.10 - Relé de Proteção da Linha (MRA4) - Sobrefrequência Nível 1 - 81O', self.clp, REG_USINA_Alarme10, 10)
        x = self.relé_de_proteção_da_linha_mra4_sobrefrequência_nível_1_81o
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_da_linha_mra4_falha_no_disjuntor_50_62bf = LeituraModbusBit('10.14 - Relé de Proteção da Linha (MRA4) - Falha no Disjuntor - 50/62BF', self.clp, REG_USINA_Alarme10, 14)
        x = self.relé_de_proteção_da_linha_mra4_falha_no_disjuntor_50_62bf
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_da_linha_mra4_sobrepotência_de_exportação_32o = LeituraModbusBit('10.15 - Relé de Proteção da Linha (MRA4) - Sobrepotência de Exportação - 32O', self.clp, REG_USINA_Alarme10, 15)
        x = self.relé_de_proteção_da_linha_mra4_sobrepotência_de_exportação_32o
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_da_linha_mra4_potência_ativa_reversa_32r = LeituraModbusBit('11.00 - Relé de Proteção da Linha (MRA4) - Potência Ativa Reversa - 32R', self.clp, REG_USINA_Alarme11, 00)
        x = self.relé_de_proteção_da_linha_mra4_potência_ativa_reversa_32r
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_da_linha_mra4_sobretensão_de_sequência_negativa_59q = LeituraModbusBit('11.01 - Relé de Proteção da Linha (MRA4) - Sobretensão de Sequência Negativa - 59Q', self.clp, REG_USINA_Alarme11, 1)
        x = self.relé_de_proteção_da_linha_mra4_sobretensão_de_sequência_negativa_59q
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.carregador_de_baterias_cb01_defeito_geral = LeituraModbusBit('11.06 - Carregador de Baterias CB01 - Defeito Geral', self.clp, REG_USINA_Alarme11, 6)
        x = self.carregador_de_baterias_cb01_defeito_geral
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.carregador_de_baterias_cb01_fuga_à_terra_pelo_positivo = LeituraModbusBit('11.08 - Carregador de Baterias CB01 - Fuga à Terra Pelo Positivo', self.clp, REG_USINA_Alarme11, 8)
        x = self.carregador_de_baterias_cb01_fuga_à_terra_pelo_positivo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.carregador_de_baterias_cb01_fuga_à_terra_pelo_negativo = LeituraModbusBit('11.09 - Carregador de Baterias CB01 - Fuga à Terra Pelo Negativo', self.clp, REG_USINA_Alarme11, 9)
        x = self.carregador_de_baterias_cb01_fuga_à_terra_pelo_negativo
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.qcta_erro_de_leitura_na_entrada_analógica_nível_barragem_montante_grade = LeituraModbusBit('13.03 - QCTA - Erro de Leitura na Entrada Analógica Nível Barragem (Montante Grade)', self.clp, REG_USINA_Alarme13, 3)
        x = self.qcta_erro_de_leitura_na_entrada_analógica_nível_barragem_montante_grade
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_sel700g_sobretensão_residual_59g = LeituraModbusBit('11.08 - Relé de Proteção SEL700G - Sobretensão Residual (59G)', self.clp, REG_USINA_Alarme11, 8)
        x = self.relé_de_proteção_sel700g_sobretensão_residual_59g
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_sel700g_potência_reversa_32p = LeituraModbusBit('11.09 - Relé de Proteção SEL700G - Potência Reversa (32P)', self.clp, REG_USINA_Alarme11, 9)
        x = self.relé_de_proteção_sel700g_potência_reversa_32p
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_sel700g_energização_indevida_50m = LeituraModbusBit('11.12 - Relé de Proteção SEL700G - Energização Indevida (50M)', self.clp, REG_USINA_Alarme11, 12)
        x = self.relé_de_proteção_sel700g_energização_indevida_50m
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_sel700g_falha_do_disjuntor_52g_50_62bf = LeituraModbusBit('11.15 - Relé de Proteção SEL700G - Falha do Disjuntor 52G (50_62BF)', self.clp, REG_USINA_Alarme11, 15)
        x = self.relé_de_proteção_sel700g_falha_do_disjuntor_52g_50_62bf
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.grtd_2000_falha_sobrecorrente_de_excitação = LeituraModbusBit('12.04 - GRTD 2000 - Falha Sobrecorrente de Excitação', self.clp, REG_USINA_Alarme12, 4)
        x = self.grtd_2000_falha_sobrecorrente_de_excitação
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.erro_de_leitura_na_entrada_analógica_de_pressão_da_caixa_espiral = LeituraModbusBit('12.11 - Erro de Leitura na Entrada Analógica de Pressão da Caixa Espiral', self.clp, REG_USINA_Alarme12, 11)
        x = self.erro_de_leitura_na_entrada_analógica_de_pressão_da_caixa_espiral
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.css_u1_alimentação_motor_carregamento_mola_disjuntor_52g_disjuntor_q220_1_desligado = LeituraModbusBit('13.07 - CSS-U1 - Alimentação Motor Carregamento Mola Disjuntor 52G - Disjuntor Q220_1 Desligado', self.clp, REG_USINA_Alarme13, 7)
        x = self.css_u1_alimentação_motor_carregamento_mola_disjuntor_52g_disjuntor_q220_1_desligado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.q49_módulo_de_temperatura_sel2600_disjuntor_q125_0_desligado = LeituraModbusBit('13.14 - Q49 - Módulo de Temperatura SEL2600 - Disjuntor Q125_0 Desligado', self.clp, REG_USINA_Alarme13, 14)
        x = self.q49_módulo_de_temperatura_sel2600_disjuntor_q125_0_desligado
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.trip_vibração_excessiva_no_mancal_la_do_gerador = LeituraModbusBit('15.01 - TRIP - Vibração Excessiva no Mancal LA do Gerador', self.clp, REG_USINA_Alarme15, 1)
        x = self.trip_vibração_excessiva_no_mancal_la_do_gerador
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.trip_vibração_excessiva_no_mancal_loa_do_gerador = LeituraModbusBit('15.03 - TRIP - Vibração Excessiva no Mancal LOA do Gerador', self.clp, REG_USINA_Alarme15, 3)
        x = self.trip_vibração_excessiva_no_mancal_loa_do_gerador
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.relé_de_proteção_da_linha_mra4_subtensão_de_fase_27p = LeituraModbusBit('10.06 - Relé de Proteção da Linha (MRA4) - Subtensão de Fase - 27P', self.clp, REG_USINA_Alarme10, 6)
        x = self.relé_de_proteção_da_linha_mra4_subtensão_de_fase_27p
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.relé_de_proteção_da_linha_mra4_subfrequência_nível_1_81u = LeituraModbusBit('10.08 - Relé de Proteção da Linha (MRA4) - Subfrequência Nível 1 - 81U', self.clp, REG_USINA_Alarme10, 8)
        x = self.relé_de_proteção_da_linha_mra4_subfrequência_nível_1_81u
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.relé_de_proteção_da_linha_mra4_subfrequência_nível_2_81u = LeituraModbusBit('10.09 - Relé de Proteção da Linha (MRA4) - Subfrequência Nível 2 - 81U', self.clp, REG_USINA_Alarme10, 9)
        x = self.relé_de_proteção_da_linha_mra4_subfrequência_nível_2_81u
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.relé_de_proteção_da_linha_mra4_sobrefrequência_nível_2_81o = LeituraModbusBit('10.11 - Relé de Proteção da Linha (MRA4) - Sobrefrequência Nível 2 - 81O', self.clp, REG_USINA_Alarme10, 11)
        x = self.relé_de_proteção_da_linha_mra4_sobrefrequência_nível_2_81o
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.relé_de_proteção_da_linha_mra4_taxa_de_variação_de_frequência_81_df_dt = LeituraModbusBit('10.12 - Relé de Proteção da Linha (MRA4) - Taxa de Variação de Frequência  - 81 df/dt', self.clp, REG_USINA_Alarme10, 12)
        x = self.relé_de_proteção_da_linha_mra4_taxa_de_variação_de_frequência_81_df_dt
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.relé_de_proteção_da_linha_mra4_perda_de_sincronismo_78 = LeituraModbusBit('10.13 - Relé de Proteção da Linha (MRA4) - Perda de Sincronismo  - 78', self.clp, REG_USINA_Alarme10, 13)
        x = self.relé_de_proteção_da_linha_mra4_perda_de_sincronismo_78
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_poco_nivel_1 = LeituraModbus('Poço Nível 1', self.clp, REG_USINA_Poco_Nivel, 0)
        self.leitura_poco_nivel_2 = LeituraModbus('Poço Nível 2', self.clp, REG_USINA_Poco_Nivel, 1)
        self.leitura_poco_nivel_3 = LeituraModbus('Poço Nível 3', self.clp, REG_USINA_Poco_Nivel, 2)
        self.leitura_poco_nivel_4 = LeituraModbus('Poço Nível 4', self.clp, REG_USINA_Poco_Nivel, 3)
        self.leitura_poco_nivel_5 = LeituraModbus('Poço Nível 5', self.clp, REG_USINA_Poco_Nivel, 4)
        self.leitura_poco_nivel_6 = LeituraModbus('Poço Nível 6', self.clp, REG_USINA_Poco_Nivel, 5)

        self.condicionadores.append(
            CondicionadorCombinadoAND(
                "MRA4 & Poço NV6 Inundação & não Poço NV5",
                DEVE_SUPER_NORMALIZAR,
                [
                    [True, CondicionadorBase(self.qpse_relé_proteção_woodward_f67_mra4_trip_atuado.descr, DEVE_NORMALIZAR, self.qpse_relé_proteção_woodward_f67_mra4_trip_atuado)],
                    [True, CondicionadorBase(self.leitura_poco_nivel_6.descr, DEVE_INDISPONIBILIZAR, self.leitura_poco_nivel_6)],
                    [False, CondicionadorBase(self.leitura_poco_nivel_5.descr, DEVE_NORMALIZAR, self.leitura_poco_nivel_5)],
                ]
            )
        )

        self.falta_fase_trafo_auxiliar = LeituraModbusBit("01.07 - Serviço Auxiliar - Falta de Fase Fonte 01 (Trafo Auxiliar)", self.clp, REG_USINA_Alarme01, 7)
        self.falta_fase_grupo_diesel = LeituraModbusBit("01.08 - Serviço Auxiliar - Falta de Fase Fonte 02 (Frupo Diesel)", self.clp, REG_USINA_Alarme01, 8)
        self.alarme_nivel_oleo_alto_trafo_elevador = LeituraModbusBit("02.08 - Trafo Elevador - Nível Óleo Alto Alarme", self.clp, REG_USINA_Alarme02, 8)
        self.alarme_nivel_muito_alto_poco_drenagem = LeituraModbusBit("03.05 - Poço de Drenagem - Nível Muito Alto Alarme", self.clp, REG_USINA_Alarme03, 5)
        self.falha_acionamento_bomba_drenagem_1 = LeituraModbusBit("03.07 - Bomba de Drenagem 01 - Falha no Acionamento", self.clp, REG_USINA_Alarme03, 7)
        self.falha_acionamento_bomba_drenagem_2 = LeituraModbusBit("03.09 - Bomba de Drenagem 02 - Falha no Acionamento", self.clp, REG_USINA_Alarme03, 9)
        self.falha_sistema_filtro = LeituraModbusBit("03.13 - Filtro Água Primário - Falha no Sistema de Filtro", self.clp, REG_USINA_Alarme03, 13)
        self.alarme_nivel_minimo_barragem = LeituraModbusBit("04.05 - Nível Barragem - Nível Minimo Alarme", self.clp, REG_USINA_Alarme04, 5)
        self.falha_com_clp_pacp_qcta = LeituraModbusBit("04.09 - Falha de Comunicação entre o self.clp do PACP com o self.clp do QCTA", self.clp, REG_USINA_Alarme04, 9)
        self.disj_q3804_desligado = LeituraModbusBit("06.01 - PDSA - Alimentação Carregador Baterias - Disj. Q380.4 Desligado", self.clp, REG_UG1_Alarme06, 1)
        self.disj_1q3800_desligado = LeituraModbusBit("06.11 - PDSA - Alimentação Cargas Essenciais UG01 - Disj. 1Q380.0 Desligado", self.clp, REG_UG1_Alarme06, 11)
        self.falha_analog_ar_comprimido = LeituraModbusBit("09.02 - Falha Entrada Analógica Pressão Sistema Ar Comprimido", self.clp, REG_USINA_Alarme09, 2)
        self.diferencial_grade_suja = LeituraModbusBit("09.09 - Diferencial Grade Suja", self.clp, REG_USINA_Alarme09, 9)
        self.difenrecial_grade_muito_suja = LeituraModbusBit("09.10 - Diferencial Grade Muito Suja", self.clp, REG_USINA_Alarme09, 10)
        self.tensao_anormal_ret_cons = LeituraModbusBit("11.07 - Carregador de Baterias CB01 - Tensão Anormal no Retificador ou Consumidor", self.clp, REG_USINA_Alarme11, 7)
        self.anormalidade_baterias = LeituraModbusBit("11.10 - Carregador de Baterias CB01 - Anormalidade nas Baterias", self.clp, REG_USINA_Alarme11, 10)
        self.flutuacao_anormal = LeituraModbusBit("11.11 - Carregador de Baterias CB01 - Flutuação Anormal", self.clp, REG_USINA_Alarme11, 11)
        self.falta_fase = LeituraModbusBit("12.02 - QCTA - UHTA - Falta Fase", self.clp, REG_USINA_Alarme12, 2)
        self.filtro_sujo = LeituraModbusBit("12.03 - QCTA - UHTA - Filtro Sujo", self.clp, REG_USINA_Alarme12, 3)
        self.falha_acionamento_bomba_1 = LeituraModbusBit("12.10 - QCTA - UHTA - Falha Acionamento da Bomba 01", self.clp, REG_USINA_Alarme12, 10)
        self.falha_acionamento_bomba_2 = LeituraModbusBit("12.12 - QCTA - UHTA - Falha Acionamento da Bomba 02", self.clp, REG_USINA_Alarme12, 12)
        self.trafo_elevador_temperatura_enrolamento_alarme = LeituraModbusBit('02.12 - Trafo Elevador - Temperatura Enrolamento Alarme', self.clp, REG_USINA_Alarme02, 12)
        self.trafo_elevador_temperatura_oleo_alarme = LeituraModbusBit('02.14 - Trafo Elevador - Temperatura Óleo Alarme', self.clp, REG_USINA_Alarme02, 14)
        self.falha_partida_grupo_diesel = LeituraModbusBit('01.09 - Serviço Auxiliar - Falha na Partida do Grupo Diesel', self.clp, REG_USINA_Alarme01, 9)
        self.disjuntor_52l_falha_no_fechamento = LeituraModbusBit('02.01 - Disjuntor 52L - Falha no Fechamento', self.clp, REG_USINA_Alarme02, 1)
        self.falha_abertura_comporta = LeituraModbusBit("12.05 - QCTA - Comporta Falha na Abertura", self.clp, REG_USINA_Alarme12, 15)
        self.falha_fechamento_comporta = LeituraModbusBit("13.00 - QCTA - Comporta Falha no Fechamento", self.clp, REG_USINA_Alarme13, 00)

        pars = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            self.cfg["kp"],
            self.cfg["ki"],
            self.cfg["kd"],
            self.cfg["kie"],
            0, #self.n_movel_l,
            0, #self.n_movel_r,
            self.cfg["nv_alvo"],
        ]
        self.con.open()
        self.db.update_parametros_usina(pars)

        # ajuste inicial ie
        if self.cfg["saida_ie_inicial"] == "auto":
            self.controle_ie = (
                self.ug1.leitura_potencia.valor + self.ug2.leitura_potencia.valor
            ) / self.cfg["pot_maxima_alvo"]
        else:
            self.controle_ie = self.cfg["saida_ie_inicial"]

        self.controle_i = self.controle_ie

        # ajuste inicial SP
        logger.debug(f"[UG1] Leitura de potência -> {self.ug1.leitura_potencia.valor}")
        logger.debug(f"[UG2] Leitura de potência -> {self.ug2.leitura_potencia.valor}")
        self.ug1.setpoint = self.ug1.leitura_potencia.valor
        self.ug2.setpoint = self.ug2.leitura_potencia.valor

    @property
    def nv_montante(self):
        return self.leituras.nv_montante.valor

    def ler_valores(self):

        # self.clp
        # regs = [0]*40000
        # aux = self.self.clp.read_sequential(40000, 101)
        # regs += aux
        # USN
        # self.clp_emergencia_acionada = regs[self.cfg['ENDERECO_CLP_USINA_FLAGS']]
        # self.nv_montante = round((regs[self.cfg['ENDERECO_CLP_NV_MONATNTE']] * 0.001) + 620, 2)
        # self.pot_medidor = round((regs[self.cfg['ENDERECO_CLP_MEDIDOR']] * 0.001), 3)

        # -> Verifica conexão com self.clp Tomada d'água
        #   -> Se não estiver ok, acionar emergencia self.clp
        if not ping(self.cfg["TDA_slave_ip"]):
            if not self.borda_aviso_clp_tda:
                logger.warning("self.clp TDA não respondeu a tentativa de comunicação!")
                self.borda_aviso_clp_tda = True
        else:
            if self.borda_aviso_clp_tda:
                logger.info("self.clp TDA voltou a comunicar!")
                self.borda_aviso_clp_tda = False

        # -> Verifica conexão com self.clp Sub
        #   -> Se não estiver ok, avisa por logger.warning
        if not ping(self.cfg["USN_slave_ip"]):
            if not self.borda_aviso_clp_pacp:
                logger.warning("self.clp PACP não respondeu a tentativa de comunicação!")
                self.borda_aviso_clp_pacp = True
        else:
            if self.borda_aviso_clp_pacp:
                logger.info("self.clp PACP voltou a comunicar!")
                self.borda_aviso_clp_pacp = False

        # -> Verifica conexão com self.clp UG#
        #    -> Se não estiver ok, acionar indisponibiliza UG# e avisa por logger.warning
        # UG1
        if not ping(self.cfg["UG1_slave_ip"]):
            if not self.borda_aviso_clp_ug1:
                self.ug1.salvar_estado_anterior()
                logger.warning("self.clp UG1 não respondeu a tentativa de comunicação!")
                self.borda_aviso_clp_ug1 = True
                self.ug1.forcar_estado_restrito()
        else:
            if self.borda_aviso_clp_ug1:
                logger.info("self.clp UG1 voltou a comunicar!")
                self.borda_aviso_clp_ug1 = False
                if self.ug1.estado_anterior == MOA_UNIDADE_MANUAL:
                    self.ug1.forcar_estado_manual()
                elif self.ug1.estado_anterior == MOA_UNIDADE_DISPONIVEL:
                    self.ug1.forcar_estado_disponivel()
                elif self.ug1.estado_anterior == MOA_UNIDADE_RESTRITA:
                    self.ug1.forcar_estado_restrito()
                else:
                    self.ug1.forcar_estado_indisponivel()
        # UG2
        if not ping(self.cfg["UG2_slave_ip"]):
            if not self.borda_aviso_clp_ug2:
                self.ug2.salvar_estado_anterior()
                logger.warning("self.clp UG2 não respondeu a tentativa de comunicação!")
                self.borda_aviso_clp_ug2 = True
                self.ug2.forcar_estado_restrito()
        else:
            if self.borda_aviso_clp_ug2:
                logger.info("self.clp UG2 voltou a comunicar!")
                self.borda_aviso_clp_ug2 = False
                if self.ug2.estado_anterior == MOA_UNIDADE_MANUAL:
                    self.ug2.forcar_estado_manual()
                elif self.ug2.estado_anterior == MOA_UNIDADE_DISPONIVEL:
                    self.ug2.forcar_estado_disponivel()
                elif self.ug2.estado_anterior == MOA_UNIDADE_RESTRITA:
                    self.ug2.forcar_estado_restrito()
                else:
                    self.ug2.forcar_estado_indisponivel()

        self.clp_online = True
        self.clp_emergencia_acionada = 0

        if self.nv_montante_recente < 1:
            self.nv_montante_recentes = [self.leituras.nv_montante.valor] * 240
        self.nv_montante_recentes.append(
            round(self.leituras.nv_montante.valor, 2)
        )
        self.nv_montante_recentes = self.nv_montante_recentes[1:]

        """
        # Filtro butterworth
        b, a = butter(8, 4, fs=120)
        self.nv_montante_recente = float(
            filtfilt(b, a, self.nv_montante_recentes)[-1]
        )
        """

        smoothing = 5
        ema = [sum(self.nv_montante_recentes) / len(self.nv_montante_recentes)]
        for nv in self.nv_montante_recentes:
            ema.append((nv * (smoothing / (1 + len(self.nv_montante_recentes)))) + ema[-1] * (1 - (smoothing / (1 + len(self.nv_montante_recentes)))))
        self.nv_montante_recente = ema[-1]

        self.erro_nv_anterior = self.erro_nv
        self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

        # DB
        #
        # Ler apenas os parametros que estao disponiveis no django
        #  - Botão de emergência
        #  - Limites de operação das UGS
        #  - Modo autonomo
        #  - Modo de prioridade UGS

        parametros = self.db.get_parametros_usina()

        # Botão de emergência
        self.db_emergencia_acionada = int(parametros["emergencia_acionada"])

        # Limites de operação das UGS
        for ug in self.ugs:
            ug.prioridade = int(parametros[f"ug{ug.id}_prioridade"])
            ug.condicionador_perda_na_grade.valor_base = float(parametros[f"ug{ug.id}_perda_grade_alerta"])
            ug.condicionador_perda_na_grade.valor_limite = float(parametros[f"ug{ug.id}_perda_grade_maxima"])
            ug.condicionador_temperatura_enrolamento_fase_r.valor_base = float(parametros[f"temperatura_alerta_enrolamento_fase_r_ug{ug.id}"])
            ug.condicionador_temperatura_enrolamento_fase_s.valor_base = float(parametros[f"temperatura_alerta_enrolamento_fase_s_ug{ug.id}"])
            ug.condicionador_temperatura_enrolamento_fase_t.valor_base = float(parametros[f"temperatura_alerta_enrolamento_fase_t_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_la_casquilho.valor_base = float(parametros[f"temperatura_alerta_mancal_la_casquilho_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_la_contra_escora_1.valor_base = float(parametros[f"temperatura_alerta_mancal_la_contra_escora_1_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_la_contra_escora_2.valor_base = float(parametros[f"temperatura_alerta_mancal_la_contra_escora_2_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_la_escora_1.valor_base = float(parametros[f"temperatura_alerta_mancal_la_escora_1_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_la_escora_2.valor_base = float(parametros[f"temperatura_alerta_mancal_la_escora_2_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_lna_casquilho.valor_base = float(parametros[f"temperatura_alerta_mancal_lna_casquilho_ug{ug.id}"])
            ug.condicionador_temperatura_enrolamento_fase_r.valor_limite = float(parametros[f"temperatura_limite_enrolamento_fase_r_ug{ug.id}"])
            ug.condicionador_temperatura_enrolamento_fase_s.valor_limite = float(parametros[f"temperatura_limite_enrolamento_fase_s_ug{ug.id}"])
            ug.condicionador_temperatura_enrolamento_fase_t.valor_limite = float(parametros[f"temperatura_limite_enrolamento_fase_t_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_la_casquilho.valor_limite = float(parametros[f"temperatura_limite_mancal_la_casquilho_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_la_contra_escora_1.valor_limite = float(parametros[f"temperatura_limite_mancal_la_contra_escora_1_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_la_contra_escora_2.valor_limite = float(parametros[f"temperatura_limite_mancal_la_contra_escora_2_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_la_escora_1.valor_limite = float(parametros[f"temperatura_limite_mancal_la_escora_1_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_la_escora_2.valor_limite = float(parametros[f"temperatura_limite_mancal_la_escora_2_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_lna_casquilho.valor_limite = float(parametros[f"temperatura_limite_mancal_lna_casquilho_ug{ug.id}"])

        # nv_minimo
        self.cfg["nv_minimo"] = float(parametros["nv_minimo"])

        # Modo autonomo
        logger.debug(f"Modo autonomo que o banco respondeu: {int(parametros['modo_autonomo'])}")
        self.modo_autonomo = int(parametros["modo_autonomo"])
        # Modo de prioridade UGS
        if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
            self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
            logger.info(f"O modo de prioridade das ugs foi alterado (#{self.modo_de_escolha_das_ugs}).")


        # Parametros banco
        self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
        self.cfg["kp"] = float(parametros["kp"])
        self.cfg["ki"] = float(parametros["ki"])
        self.cfg["kd"] = float(parametros["kd"])
        self.cfg["kie"] = float(parametros["kie"])

        # Le o databank interno

        if DataBank.get_words(self.cfg["REG_MOA_IN_EMERG"])[0] == 1:
            logger.debug(f"Comando recebido via painel: \"Emergência\"")
            logger.debug("Lendo Condicionadores...")
            self.avisado_em_eletrica = True
        else:
            self.avisado_em_eletrica = False

        if DataBank.get_words(self.cfg["REG_MOA_IN_HABILITA_AUTO"])[0] == 1:
            DataBank.set_words(self.cfg["REG_MOA_IN_HABILITA_AUTO"], [0])
            DataBank.set_words(self.cfg["REG_MOA_IN_DESABILITA_AUTO"], [0])
            self.modo_autonomo = 1

        if (
            DataBank.get_words(self.cfg["REG_MOA_IN_DESABILITA_AUTO"])[0] == 1
            or self.modo_autonomo == 0
        ):
            DataBank.set_words(self.cfg["REG_MOA_IN_HABILITA_AUTO"], [0])
            DataBank.set_words(self.cfg["REG_MOA_IN_DESABILITA_AUTO"], [0])
            self.modo_autonomo = 0
            self.entrar_em_modo_manual()

        self.heartbeat()

    def escrever_valores(self):

        if self.modo_autonomo:
            self.con.desliga_controles_locais()

        # DB
        # Escreve no banco
        # Paulo: mover lógica de escrever no banco para um método em DBService
        valores = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            1 if self.aguardando_reservatorio else 0,
            1 if self.clp_online else 0,
            self.nv_montante,
            self.pot_disp,
            1 if self.ug1.disponivel else 0,
            self.ug1.leitura_potencia.valor,
            self.ug1.setpoint,
            self.ug1.etapa_atual,
            self.ug1.leitura_horimetro.valor,
            1 if self.ug2.disponivel else 0,
            self.ug2.leitura_potencia.valor,
            self.ug2.setpoint,
            self.ug2.etapa_atual,
            self.ug2.leitura_horimetro.valor,
            0,
            self.ug1.leitura_perda_na_grade.valor,
            self.ug2.leitura_perda_na_grade.valor
        ]

        self.db.update_valores_usina(valores)

    def acionar_emergencia(self):
        self.con.acionar_emergencia()
        self.clp_emergencia_acionada = 1

    def normalizar_emergencia(self):

        logger.info("Normalizando (e verificaçẽos)")

        logger.debug(f"Ultima tentativa: {self.ts_ultima_tesntativa_de_normalizacao}. Tensão na linha: \
            RS {self.leituras.tensao_rs.valor / 1000:2.1f}kV \
            ST{self.leituras.tensao_st.valor / 1000:2.1f}kV \
            TR{self.leituras.tensao_tr.valor / 1000:2.1f}kV."
        )

        if not (
            self.cfg["TENSAO_LINHA_BAIXA"]
            < self.leituras.tensao_rs.valor
            < self.cfg["TENSAO_LINHA_ALTA"]
            and self.cfg["TENSAO_LINHA_BAIXA"]
            < self.leituras.tensao_st.valor
            < self.cfg["TENSAO_LINHA_ALTA"]
            and self.cfg["TENSAO_LINHA_BAIXA"]
            < self.leituras.tensao_tr.valor
            < self.cfg["TENSAO_LINHA_ALTA"]
        ):
            logger.warn("Tensão na linha fora do limite.")
            self.tensao_ok = False
            return False
        elif (
            self.deve_tentar_normalizar
            and (datetime.now() - self.ts_ultima_tesntativa_de_normalizacao).seconds
            >= 60 * self.tentativas_de_normalizar
        ):
            self.tentativas_de_normalizar += 1
            self.ts_ultima_tesntativa_de_normalizacao = datetime.now()
            logger.info("Normalizando a Usina")
            self.con.normalizar_emergencia()
            self.clp_emergencia_acionada = 0
            logger.info("Normalizando no banco")
            self.db.update_remove_emergencia()
            self.db_emergencia_acionada = 0
            return True
        else:
            self.tensao_ok = True
            return False

    def aguardar_tensao(self, delay):
        temporizador = time() + delay
        logger.warning("Iniciando o timer para a normalização da tensão na linha")

        while time() <= temporizador:
            sleep(time() - (time() - 15))
            if (self.cfg["TENSAO_LINHA_BAIXA"] < self.leituras.tensao_rs.valor < self.cfg["TENSAO_LINHA_ALTA"] \
                and self.cfg["TENSAO_LINHA_BAIXA"] < self.leituras.tensao_st.valor < self.cfg["TENSAO_LINHA_ALTA"] \
                and self.cfg["TENSAO_LINHA_BAIXA"] < self.leituras.tensao_tr.valor < self.cfg["TENSAO_LINHA_ALTA"]):
                logger.info("Tensão na linha reestabelecida.")
                self.timer_tensao = True
                return True

        logger.warning("Não foi possível reestabelecer a tensão na linha")
        self.timer_tensao = False
        return False

    def heartbeat(self):

        ts = datetime.now().timestamp()
        try:
            logger.debug("Inserting in db")
            ma = 1 if self.modo_autonomo else 0
            self.db.insert_debug(
                ts,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.ug1.setpoint,
                self.ug1.leitura_potencia.valor,
                self.ug2.setpoint,
                self.ug2.leitura_potencia.valor,
                self.nv_montante_recente,
                self.erro_nv,
                ma,
            )
        except Exception as e:
            pass

        agora = datetime.now()
        ano = int(agora.year)
        mes = int(agora.month)
        dia = int(agora.day)
        hor = int(agora.hour)
        mnt = int(agora.minute)
        seg = int(agora.second)
        mil = int(agora.microsecond / 1000)
        DataBank.set_words(0, [ano, mes, dia, hor, mnt, seg, mil])
        DataBank.set_words(self.cfg["REG_MOA_OUT_STATUS"], [self.state_moa])
        DataBank.set_words(self.cfg["REG_MOA_OUT_MODE"], [self.modo_autonomo])
        if self.modo_autonomo:
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_EMERG"],
                [1 if self.clp_emergencia_acionada else 0],
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_TARGET_LEVEL"], [self.cfg["nv_alvo"] - 620] * 1000
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_SETPOINT"],
                [self.ug1.setpoint + self.ug2.setpoint],
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_BLOCK_UG1"],
                [1 if self.ug1.enviar_trip_eletrico else 0]
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_BLOCK_UG2"],
                [1 if self.ug2.enviar_trip_eletrico else 0]
            )

        else:
            DataBank.set_words(self.cfg["REG_MOA_OUT_EMERG"], [0])
            DataBank.set_words(self.cfg["REG_MOA_OUT_TARGET_LEVEL"], [0])
            DataBank.set_words(self.cfg["REG_MOA_OUT_SETPOINT"], [0])
            DataBank.set_words(self.cfg["REG_MOA_OUT_BLOCK_UG1"], [0])
            DataBank.set_words(self.cfg["REG_MOA_OUT_BLOCK_UG2"], [0])

    def get_agendamentos_pendentes(self):
        """
        Retorna os agendamentos pendentes para a usina.
        :return: list[] agendamentos

        agora = datetime.now()
        agora = agora - timedelta(seconds=agora.second, microseconds=agora.microsecond)
        """
        agendamentos_pendentes = []
        agendamentos = self.db.get_agendamentos_pendentes()
        for agendamento in agendamentos:
            ag = list(agendamento)
            # ag -> [id, data, observacao, comando_id, executado, campo_auxiliar, criado_por, modificado_por, ts_criado, ts_modificado]
            ag[1] = ag[1] - timedelta(0, 60 * 60 * 3)
            agendamentos_pendentes.append(ag)
        return agendamentos_pendentes

    def verificar_agendamentos(self):
        """
        Verifica os agendamentos feitos pelo django no banco de dados e lida com eles, executando, etc...
        """
        agora = datetime.now()
        agendamentos = self.get_agendamentos_pendentes()

        # resolve os agendamentos muito juntos
        limite_entre_agendamentos_iguais = 300 # segundos
        agendamentos = sorted(agendamentos, key=lambda x:(x[3], x[1]))
        i = 0
        j = len(agendamentos)
        while i < j - 1:

            if agendamentos[i][3] == agendamentos[i+1][3] and (agendamentos[i+1][1] - agendamentos[i][1]).seconds < limite_entre_agendamentos_iguais:
                ag_concatenado = agendamentos.pop(i)
                obs = "Este agendamento foi concatenado ao seguinte por motivos de temporização."
                logger.warning(obs)
                self.db.update_agendamento(ag_concatenado[0], True, obs)
                i -= 1

            i += 1
            j = len(agendamentos)

        if len(agendamentos) == 0:
            return True

        self.agendamentos_atrasados = 0
        for agendamento in agendamentos:
            # ag -> [id, data, observacao, comando_id, executado, campo_auxiliar, criado_por, modificado_por, ts_criado, ts_modificado]
            if agora > agendamento[1]:
                segundos_adiantados = 0
                segundos_passados = (agora - agendamento[1]).seconds
                logger.debug(segundos_passados)
            else:
                segundos_adiantados = (agendamento[1] - agora).seconds
                segundos_passados = 0

            if segundos_passados > 60:
                logger.warning(f"Agendamento: {agendamento[0]} Atrasado! ({agendamento[3]}).")
                self.agendamentos_atrasados += 1

            if segundos_passados > 300 or self.agendamentos_atrasados > 3:
                logger.info("Os agendamentos estão muito atrasados! Acionando emergência.")
                self.acionar_emergencia()
                return False

            if segundos_adiantados <= 60 and not bool(agendamento[4]):
                # Está na hora e ainda não foi executado. Executar!
                logger.info(f"Executando agendamento: {agendamento[0]}\n \
                    Comando: {INT_TO_AGENDAMENTOS[agendamento[3]]}\ \
                    Data: {agendamento[1]}\n \
                    Observação: {agendamento[2]}\n \
                    {f'Valor: {agendamento[5]}' if agendamento[5] is not None else ...}"
                )

                # se o MOA estiver em autonomo e o agendamento não for executavel em autonomo
                #   marca como executado e altera a descricao
                #   proximo
                if self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_autmoatico"]:
                    obs = "Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação"
                    logger.warning(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True

                # se o MOA estiver em manual e o agendamento não for executavel em manual
                #   marca como executado e altera a descricao
                #   proximo
                if not self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_manual"]:
                    obs = "Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação"
                    logger.warning(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True


                # Exemplo Case agendamento:
                if agendamento[3] == AGENDAMENTO_DISPARAR_MENSAGEM_TESTE:
                    # Coloca em emergência
                    logger.info("Disparando mensagem teste.")
                    self.disparar_mensagem_teste()

                #Pot Maxima UG
                if agendamento[3] == AGENDAMENTO_ALETRAR_POT_MAX:
                    # Coloca em emergência
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        logger.info(f"Alterando pot maxima para: {novo} kW.")
                        self.cfg["pot_maxima_alvo"] = novo
                        self.cfg["pot_maxima_usina"] = novo
                    except Exception as e:
                        obs =  f"Valor inválido no comando {agendamento[0]} ('{agendamento[5]}', inválido)."
                        logger.info(obs)
                        self.db.update_agendamento(agendamento[0], True, obs)


                if agendamento[3] == AGENDAMENTO_INDISPONIBILIZAR:
                    # Coloca em emergência
                    logger.info("Indisponibilizando a usina.")
                    for ug in self.ugs:
                        ug.forcar_estado_indisponivel()
                    while (
                        not self.ugs[0].etapa_atual == UNIDADE_PARADA
                        and not self.ugs[1].etapa_atual == UNIDADE_PARADA
                    ):
                        self.ler_valores()
                        logger.debug(
                            "Indisponibilizando Usina... \n(freezing for 10 seconds)"
                        )
                        sleep(10)
                    self.acionar_emergencia()
                    logger.info(
                        "Emergência pressionada após indizponibilização agendada mudando para modo manual para evitar normalização automática."
                    )
                    self.entrar_em_modo_manual()

                if agendamento[3] == AGENDAMENTO_ALTERAR_NV_ALVO:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.nv_alvo = novo
                        pars = [
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            self.kp,
                            self.ki,
                            self.kd,
                            self.kie,
                            self.n_movel_l,
                            self.n_movel_r,
                            self.nv_alvo,
                        ]
                        self.db.update_parametros_usina(pars)
                        self.escrever_valores()
                    except Exception as e:
                        obs =  f"Valor inválido no comando {agendamento[0]} ('{agendamento[5]}', inválido)."
                        logger.info(obs)
                        self.db.update_agendamento(agendamento[0], True, obs)

                    self.cfg["nv_alvo"] = novo
                    pars = [
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        self.cfg["kp"],
                        self.cfg["ki"],
                        self.cfg["kd"],
                        self.cfg["kie"],
                        0, #self.n_movel_l,
                        0, #self.n_movel_r,
                        self.cfg["nv_alvo"],
                    ]
                    self.db.update_parametros_usina(pars)
                    self.escrever_valores()

                if agendamento[3] == AGENDAMENTO_UG1_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg['pot_maxima_ug1'] = novo
                        self.ug1.pot_disponivel = novo
                    except Exception as e:
                        obs =  f"Valor inválido no comando {agendamento[0]} ('{agendamento[5]}', inválido)."
                        logger.info(obs)
                        self.db.update_agendamento(agendamento[0], True, obs)

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_MANUAL:
                    self.ug1.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_DISPONIVEL:
                    self.ug1.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug1.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_RESTRITO:
                    self.ug1.forcar_estado_restrito()

                if agendamento[3] == AGENDAMENTO_UG2_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg['pot_maxima_ug2'] = novo
                        self.ug2.pot_disponivel = novo
                    except Exception as e:
                        obs =  f"Valor inválido no comando {agendamento[0]} ('{agendamento[5]}', inválido)."
                        logger.info(obs)
                        self.db.update_agendamento(agendamento[0], True, obs)

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_MANUAL:
                    self.ug2.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_DISPONIVEL:
                    self.ug2.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug2.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_RESTRITO:
                    self.ug2.forcar_estado_restrito()

                # Após executar, indicar no banco de dados
                self.db.update_agendamento(int(agendamento[0]), 1)
                logger.debug(f"O comando: {agendamento[0]} foi executado.")
                self.con.somente_reconhecer_emergencia()
                self.escrever_valores()

    def distribuir_potencia(self, pot_alvo):

        if pot_alvo < 0.1:
            for ug in self.ugs:
                ug.setpoint = 0
            return 0

        if self.leituras.potencia_ativa_kW.valor > self.cfg["pot_maxima_alvo"] * 0.95:
            pot_alvo = pot_alvo / (self.leituras.potencia_ativa_kW.valor/self.cfg["pot_maxima_alvo"])

        ugs = self.lista_de_ugs_disponiveis()
        self.pot_disp = 0
        logger.debug("lista_de_ugs_disponiveis:")
        for ug in ugs:
            logger.debug(f"UG{ug.id}")
            self.pot_disp += ug.cfg[f'pot_maxima_ug{ugs[0].id}']

        if ugs is None:
            return False
        elif len(ugs) == 0:
            return False
        elif len(ugs) == 1:
            pot_alvo = min(pot_alvo, self.cfg[f'pot_maxima_ug{ugs[0].id}'])
            ugs[0].setpoint = pot_alvo
            return False
        else:

            logger.debug(f"Distribuindo {pot_alvo}")
            if 0.1 < pot_alvo < self.cfg["pot_minima"]:
                logger.debug(f"0.1 < {pot_alvo} < Potência Mínima ({self.cfg['pot_minima']})")
                if len(ugs) > 0:
                    ugs[0].setpoint = self.cfg["pot_minima"]
                    for ug in ugs[1:]:
                        ug.setpoint = 0
            else:
                pot_alvo = min(pot_alvo, self.pot_disp)

                if len(ugs) == 0:
                    return False

                if (self.ug1.etapa_atual == UNIDADE_SINCRONIZADA
                    and self.ug2.etapa_atual == UNIDADE_SINCRONIZADA
                    and pot_alvo > (self.cfg["pot_maxima_ug"] - self.cfg["margem_pot_critica"])):
                    logger.debug("Dividindo igualmente entre as UGs")
                    logger.debug(f"Margem de potência crítica = {self.cfg['margem_pot_critica']}")
                    for ug in ugs:
                        ug.setpoint = max(self.cfg["pot_minima"], pot_alvo / len(ugs))

                elif(pot_alvo > (self.cfg["pot_maxima_ug"] + self.cfg["margem_pot_critica"])):
                    #logger.debug("Dividindo desigualmente entre UGs pois está partindo uma ou mais UGs")
                    #ugs[0].setpoint = self.cfg["pot_maxima_ug"]
                    logger.debug("Dividindo igualmente entre UGs pois está partindo uma ou mais UGs")
                    for ug in ugs[0:]:
                        ug.setpoint = max(self.cfg["pot_minima"], pot_alvo / len(ugs))

                else:
                    logger.debug("Apenas uma UG deve estar sincronizada")
                    pot_alvo = min(pot_alvo, self.cfg["pot_maxima_ug"])
                    ugs[0].setpoint = max(self.cfg["pot_minima"], pot_alvo)
                    for ug in ugs[1:]:
                        ug.setpoint = 0

            for ug in self.ugs:
                logger.debug(f"UG{ug.id} SP:{ug.setpoint}")

        return pot_alvo

    def lista_de_ugs_disponiveis(self):
        """
        Retorn uma lista de ugs disponiveis conforme a ordenação selecionada
        """
        ls = []
        for ug in self.ugs:
            if ug.disponivel:
                ls.append(ug)

        if self.modo_de_escolha_das_ugs == MODO_ESCOLHA_MANUAL:
            # escolher por maior prioridade primeiro
            ls = sorted(
                ls,
                key=lambda y: (
                    -1 * y.etapa_atual,
                    -1 * y.etapa_alvo,
                    -1 * y.leitura_potencia.valor,
                    y.prioridade,
                ),
            )
        else:
            # escolher por menor horas_maquina primeiro
            ls = sorted(
                ls,
                key=lambda y: (
                    -1 * y.etapa_atual,
                    -1 * y.etapa_alvo,
                    -1 * y.leitura_potencia.valor,
                    y.leitura_horimetro.valor,
                ),
            )
            logger.debug(ls)
        return ls

    def controle_normal(self):
        """
        Controle PID
        https://en.wikipedia.org/wiki/PID_controller#Proportional
        """
        logger.debug("-------------------------------------------------")

        # Calcula PID
        logger.debug(f"Alvo: {self.cfg['nv_alvo']:0.3f}, Recente: {self.nv_montante_recente:0.3f}")

        self.controle_p = self.cfg["kp"] * self.erro_nv
        self.controle_i = max(min((self.cfg["ki"] * self.erro_nv) + self.controle_i, 0.8), 0)
        self.controle_d = self.cfg["kd"] * (self.erro_nv - self.erro_nv_anterior)
        saida_pid = (
            self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3)
        )
        logger.debug(f"PID: {saida_pid:0.3f} <-- P:{self.controle_p:0.3f} + I:{self.controle_i:0.3f} + D:{self.controle_d:0.3f}; ERRO={self.erro_nv}")

        # Calcula o integrador de estabilidade e limita
        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)

        if self.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if self.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        logger.debug(f"IE: {self.controle_ie:0.3f}")

        # Arredondamento e limitação
        pot_alvo = max(
            min(
                round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5),
                self.cfg["pot_maxima_usina"],
            ),
            self.cfg["pot_minima"],
        )

        logger.debug(f"Pot alvo: {pot_alvo:0.3f}")
        logger.debug(f"Nv alvo: {self.cfg['nv_alvo']:0.3f}")
        ts = datetime.now().timestamp()
        try:
            logger.debug("Inserting in db")
            ma = 1 if self.modo_autonomo else 0
            self.db.insert_debug(
                ts,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.ug1.setpoint,
                self.ug1.leitura_potencia.valor,
                self.ug2.setpoint,
                self.ug2.leitura_potencia.valor,
                self.nv_montante_recente,
                self.erro_nv,
                ma,
            )
        except Exception as e:
            logger.debug(
                "Exception Banco-------------------------------------------------"
            )

        pot_alvo = self.distribuir_potencia(pot_alvo)

    def disparar_mensagem_teste(self):
        logger.debug("Este e um teste!")
        logger.info("Este e um teste!")
        logger.warning("Este e um teste!")
        voip.enviar_voz_teste()

    def entrar_em_modo_manual(self):
        self.modo_autonomo = 0
        self.db.update_modo_manual()

    def leituras_por_hora(self):
        # Disparo de mensagens por Telegram
        if self.falta_fase_trafo_auxiliar.valor != 0:
            logger.warning("O Serviço Auxiliar apontou uma falta de fase no Transformador Auxiliar! Favor verificar.")

        if self.falta_fase_grupo_diesel.valor != 0:
            logger.warning("O serviço Auxiliar apontou uma falta de fase no Grupo Diesel! Favor verificar.")

        if self.alarme_nivel_oleo_alto_trafo_elevador.valor != 0:
            logger.warning("Alarme de nível de óleo alto do Tranformador Elevador ativado! Favor verificar.")

        if self.alarme_nivel_muito_alto_poco_drenagem.valor != 0:
            logger.warning("Alarme de nível muito alto do poço de drenagem ativado! Favor verificar.")

        if self.falha_acionamento_bomba_drenagem_1.valor != 0:
            logger.warning("Houve uma falha no acionamento da bomba de drenagem 1! Favor verificar.")

        if self.falha_acionamento_bomba_drenagem_2.valor != 0:
            logger.warning("Houve uma falha no acionamento da bomba de drenagem 2! Favor verificar.")

        if self.falha_sistema_filtro.valor != 0:
            logger.warning("Houve uma falha no sistema de filtro de água primário! Favor verificar.")

        if self.alarme_nivel_minimo_barragem.valor != 0:
            logger.warning("Alarme de nível mínimo da barragem ativado! Favor verificar.")

        if self.falha_com_clp_pacp_qcta.valor != 0:
            logger.warning("Houve uma falha de comunicação entre o self.clp PACP com o self.clp QCTA! Favor verificar.")

        if self.disj_q3804_desligado.valor != 0:
            logger.warning("O disjuntor Q380.4 (alimentação de baterias) foi desligado! Favor verificar.")

        if self.disj_1q3800_desligado.valor != 0:
            logger.warning("O disjuntor 1Q308.0 (alimentação de cargas essenciais UG1) foi desligado! FAvor verificar.")

        if self.falha_analog_ar_comprimido.valor != 0:
            logger.warning("Houve uma falha na entrada analógica de pressão do sismtema de ar comprimido! Favor verificar.")

        if self.diferencial_grade_suja.valor != 0:
            logger.warning("Alarme de difenrecial de grade suja ativado! Favor verificar.")

        if self.difenrecial_grade_muito_suja.valor != 0:
            logger.warning("Alarme de diferencial de grade muito suja ativado! Favor verificar.")

        if self.tensao_anormal_ret_cons.valor != 0:
            logger.warning("Houve um registro de tensão anromal no retificar ou consumidor do carregador de baterias CB01")

        if self.anormalidade_baterias.valor != 0:
            logger.warning("Houve um registro de anormalidade nas baterias, apontado pelo carregador de baterias CB01")

        if self.flutuacao_anormal.valor != 0:
            logger.warning("Houve um  registro de flutação anromal, apontado pelo carregador de baterias CB01! Favor verificar.")

        if self.falta_fase.valor != 0:
            logger.warning("Houve um registro de falta de fase na QCTA UHTA! Favor verificar.")

        if self.filtro_sujo.valor != 0:
            logger.warning("Houve um registro de filtro sujo na QCTA UHTA! Favor verificar.")

        if self.falha_acionamento_bomba_1.valor != 0:
            logger.warning("Houve uma falha no acionamento da bomba 1 da QCTA UHTA! Favor verificar.")

        if self.falha_acionamento_bomba_2.valor != 0:
            logger.warning("Houve uma falha no acionamento da bomba 2 da QCTA UHTA! Favor verificar.")

        # Disparo de mensagens Telegram + Ligação por voip

        if self.trafo_elevador_temperatura_enrolamento_alarme.valor == 1 and self.alarme_temp_enrol_trafo == False:
            logger.warning("Alarme de temperatura do enrolamento do transformador elevdor ativado! Favor verificar.")
            self.alarme_temp_enrol_trafo = True
            self.acionar_voip = True
        elif self.trafo_elevador_temperatura_enrolamento_alarme.valor == 0 and self.alarme_temp_enrol_trafo == True:
            self.alarme_temp_enrol_trafo = False

        if self.trafo_elevador_temperatura_oleo_alarme.valor == 1 and self.alarme_temp_oleo_trafo == False:
            logger.warning("Alarme de temperatura do óleo do transformador elevador ativado! Favor verificar.")
            self.alarme_temp_oleo_trafo = True
            self.acionar_voip = True
        elif self.trafo_elevador_temperatura_oleo_alarme.valor == 0 and self.alarme_temp_oleo_trafo == True:
            self.alarme_temp_oleo_trafo = False

        if self.falha_partida_grupo_diesel.valor == 1 and self.falha_part_grupo_diesel == False:
            logger.warning("Houve uma falha na partida do grupo diesel! Favor verificar")
            self.falha_part_grupo_diesel = True
            self.acionar_voip = True
        elif self.falha_partida_grupo_diesel.valor == 0 and self.falha_part_grupo_diesel == True:
            self.falha_part_grupo_diesel = False

        if self.disjuntor_52l_falha_no_fechamento.valor == 1 and self.falha_fechamento_DJ52L == False:
            logger.warning("Houve uma falha no fechamento do Disjuntor 52L! Favor verificar.")
            self.falha_fechamento_DJ52L = True
            self.acionar_voip = True
        elif self.disjuntor_52l_falha_no_fechamento.valor == 0 and self.falha_fechamento_DJ52L == True:
            self.falha_fechamento_DJ52L = False

        if self.falha_abertura_comporta.valor == 1 and self.falha_abertura_comp == False:
            logger.warning("Houve uma falha na abertura da comportas! Favor verificar.")
            self.falha_abertura_comp = True
            self.acionar_voip = True
        elif self.falha_abertura_comporta.valor == 0 and self.falha_abertura_comp == True:
            self.falha_abertura_comp = False

        if self.falha_fechamento_comporta.valor == 1 and self.falha_fechamento_comp == False:
            logger.warning("Houve uma falha no fechamento das comportas! Favor verificar.")
            self.falha_fechamento_comp = True
            self.acionar_voip = True
        elif self.falha_fechamento_comporta.valor == 0 and self.falha_fechamento_comp == True:
            self.falha_fechamento_comp = False

        return True

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    https://stackoverflow.com/questions/2953462/pinging-servers-in-python
    """
    ping = False
    for i in range(2):
        ping = ping or (subprocess.call(["ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE) == 0)
        if not ping:
            pass
    return ping