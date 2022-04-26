from ast import Not
import logging
import subprocess
from cmath import sqrt
from datetime import date, datetime, timedelta
from time import sleep

from pyModbusTCP.server import DataBank
from scipy.signal import butter, filtfilt
import src.mensageiro.voip as voip
from src.field_connector import FieldConnector
from src.codes import *
from src.Condicionadores import *

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
            from src.field_connector import FieldConnector
            self.con = FieldConnector(self.cfg)

        if leituras:
            self.leituras = leituras
        else:
            from src.LeiturasUSN import LeiturasUSN
            from src.Leituras import LeituraModbus
            from src.Leituras import LeituraModbusBit
            self.leituras = LeiturasUSN(self.cfg)

        self.state_moa = 1

        # Inicializa Objs da usina
        from src.UG1 import UnidadeDeGeracao1
        from src.UG2 import UnidadeDeGeracao2
        self.ug1 = UnidadeDeGeracao1(1, cfg=self.cfg, leituras_usina=self.leituras)
        self.ug2 = UnidadeDeGeracao2(2, cfg=self.cfg, leituras_usina=self.leituras)
        self.ugs = [self.ug1, self.ug2]

        self.comporta = Comporta()
        self.avisado_em_eletrica = False

        # Define as vars inciais
        self.clp_online = False
        self.timeout_padrao = self.cfg["timeout_padrao"]
        self.timeout_emergencia = self.cfg["timeout_emergencia"]
        self.nv_fundo_reservatorio = self.cfg["nv_fundo_reservatorio"]
        self.nv_minimo = self.cfg["nv_minimo"]
        self.nv_maximo = self.cfg["nv_maximo"]
        self.nv_maximorum = self.cfg["nv_maximorum"]
        self.nv_alvo = self.cfg["nv_alvo"]
        self.kp = self.cfg["kp"]
        self.ki = self.cfg["ki"]
        self.kd = self.cfg["kd"]
        self.kie = self.cfg["kie"]
        self.kimedidor = 0
        self.controle_ie = self.cfg["saida_ie_inicial"]
        self.n_movel_l = self.cfg["n_movel_L"]
        self.n_movel_r = self.cfg["n_movel_R"]

        # Outras vars
        self.ts_ultima_tesntativa_de_normalizacao = datetime.now()
        self.state_moa = 0
        self.controle_p = 0
        self.controle_i = 0
        self.controle_d = 0
        self.clp_emergencia_acionada = 0
        self.db_emergencia_acionada = 0
        self.modo_autonomo = 1
        self.modo_de_escolha_das_ugs = 0
        self.nv_montante_recente = 0
        self.nv_montante_recentes = []
        self.nv_montante_anterior = 0
        self.nv_montante_anteriores = []
        self.erro_nv = 0
        self.erro_nv_anterior = 0
        self.aguardando_reservatorio = 0
        self.pot_disp = 0
        self.agendamentos_atrasados = 0
        self.deve_tentar_normalizar = True
        self.tentativas_de_normalizar = 0
        self.ts_nv = []
        self.borda_aviso_clp_pacp = False
        self.borda_aviso_clp_tda = False
        self.borda_aviso_clp_ug1 = False
        self.borda_aviso_clp_ug2 = False

        self.condicionadores = []
        clp_ip = self.cfg["USN_slave_ip"]
        clp_port = self.cfg["USN_slave_porta"]
        clp = ModbusClient(
            host=clp_ip,
            port=clp_port,
            timeout=5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )


        self.relé_86bf_atuado_falha_disjuntores = LeituraModbusBit('01.03 - Relé 86BF Atuado (Falha Disjuntores)', clp, REG_USINA_Alarme01, 3)
        x = self.relé_86bf_atuado_falha_disjuntores 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_86te_atuado_falha_trafo_elevador = LeituraModbusBit('01.04 - Relé 86TE Atuado (falha Trafo Elevador)', clp, REG_USINA_Alarme01, 4)
        x = self.relé_86te_atuado_falha_trafo_elevador 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.servauxiliar_seccionadora_89sa_aberta = LeituraModbusBit('01.06 - ServAuxiliar - Seccionadora 89SA Aberta', clp, REG_USINA_Alarme01, 6)
        x = self.servauxiliar_seccionadora_89sa_aberta 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.qpse_relé_proteção_woodward_f67_mra4_falha_de_hardware = LeituraModbusBit('01.11 - QPSE - Relé Proteção Woodward F67 (MRA4) - Falha de Hardware', clp, REG_USINA_Alarme01, 11)
        x = self.qpse_relé_proteção_woodward_f67_mra4_falha_de_hardware 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.pacp_relé_proteção_sel787_trip_atuado = LeituraModbusBit('01.13 - PACP - Relé Proteção SEL787 - Trip Atuado', clp, REG_USINA_Alarme01, 13)
        x = self.pacp_relé_proteção_sel787_trip_atuado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.pacp_relé_proteção_sel787_falha_de_hardware = LeituraModbusBit('01.14 - PACP - Relé Proteção SEL787 - Falha de Hardware', clp, REG_USINA_Alarme01, 14)
        x = self.pacp_relé_proteção_sel787_falha_de_hardware 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.disjuntor_52l_falha_na_abertura = LeituraModbusBit('02.00 - Disjuntor 52L - Falha na Abertura', clp, REG_USINA_Alarme02, 00)
        x = self.disjuntor_52l_falha_na_abertura 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.disjuntor_52l_falha_inconsistência = LeituraModbusBit('02.02 - Disjuntor 52L - Falha Inconsistência', clp, REG_USINA_Alarme02, 2)
        x = self.disjuntor_52l_falha_inconsistência 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.seccionadora_89l_falha_abertura_indevida = LeituraModbusBit('02.04 - Seccionadora 89L - Falha Abertura indevida', clp, REG_USINA_Alarme02, 4)
        x = self.seccionadora_89l_falha_abertura_indevida 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.seccionadora_89l_falha_aberta = LeituraModbusBit('02.05 - Seccionadora 89L - Falha Aberta', clp, REG_USINA_Alarme02, 5)
        x = self.seccionadora_89l_falha_aberta 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.trafo_elevador_monitor_falha_de_hardware = LeituraModbusBit('02.07 - Trafo Elevador - Monitor Falha de Hardware', clp, REG_USINA_Alarme02, 7)
        x = self.trafo_elevador_monitor_falha_de_hardware 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.trafo_elevador_falha_relé_buchholz_alarme = LeituraModbusBit('02.10 - Trafo Elevador - Falha Relé BuchHolz Alarme', clp, REG_USINA_Alarme02, 10)
        x = self.trafo_elevador_falha_relé_buchholz_alarme 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.trafo_elevador_falha_relé_buchholz_trip = LeituraModbusBit('02.11 - Trafo Elevador - Falha Relé BuchHolz Trip', clp, REG_USINA_Alarme02, 11)
        x = self.trafo_elevador_falha_relé_buchholz_trip 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.trafo_elevador_temperatura_enrolamento_alarme = LeituraModbusBit('02.12 - Trafo Elevador - Temperatura Enrolamento Alarme', clp, REG_USINA_Alarme02, 12)
        x = self.trafo_elevador_temperatura_enrolamento_alarme 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.trafo_elevador_temperatura_enrolamento_trip = LeituraModbusBit('02.13 - Trafo Elevador - Temperatura Enrolamento Trip', clp, REG_USINA_Alarme02, 13)
        x = self.trafo_elevador_temperatura_enrolamento_trip 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.trafo_elevador_temperatura_óleo_alarme = LeituraModbusBit('02.14 - Trafo Elevador - Temperatura Óleo Alarme', clp, REG_USINA_Alarme02, 14)
        x = self.trafo_elevador_temperatura_óleo_alarme 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.trafo_elevador_temperatura_óleo_trip = LeituraModbusBit('02.15 - Trafo Elevador - Temperatura Óleo Trip', clp, REG_USINA_Alarme02, 15)
        x = self.trafo_elevador_temperatura_óleo_trip 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.trafo_elevador_válvula_alivio_alarme = LeituraModbusBit('03.00 - Trafo Elevador - Válvula Alivio Alarme', clp, REG_USINA_Alarme03, 00)
        x = self.trafo_elevador_válvula_alivio_alarme 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.trafo_elevador_válvula_alivio_trip = LeituraModbusBit('03.01 - Trafo Elevador - Válvula Alivio Trip', clp, REG_USINA_Alarme03, 1)
        x = self.trafo_elevador_válvula_alivio_trip 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.poço_de_drenagem_nível_inundação_trip_nível_bóia_02 = LeituraModbusBit('03.06 - Poço de Drenagem - Nível Inundação TRIP (Nível Bóia 02)', clp, REG_USINA_Alarme03, 6)
        x = self.poço_de_drenagem_nível_inundação_trip_nível_bóia_02 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.falha_de_comunicação_com_o_relé_de_proteção_sel_787 = LeituraModbusBit('04.10 - Falha de Comunicação com o Relé de Proteção SEL 787', clp, REG_USINA_Alarme04, 10)
        x = self.falha_de_comunicação_com_o_relé_de_proteção_sel_787 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.pacp_alimentação_circuitos_de_comando_disj_q125_0_desligado = LeituraModbusBit('05.02 - PACP - Alimentação Circuitos de Comando - Disj. Q125_0 Desligado', clp, REG_USINA_Alarme05, 2)
        x = self.pacp_alimentação_circuitos_de_comando_disj_q125_0_desligado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.pacp_alimentação_circuitos_de_comando_do_disj_52l_disj_q125_1_desligado = LeituraModbusBit('05.03 - PACP - Alimentação Circuitos de Comando do Disj 52L - Disj. Q125_1 Desligado', clp, REG_USINA_Alarme05, 3)
        x = self.pacp_alimentação_circuitos_de_comando_do_disj_52l_disj_q125_1_desligado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.pacp_alimentação_relé_de_proteção_sel787_disj_q125_2_desligado = LeituraModbusBit('05.04 - PACP - Alimentação Relé de Proteção SEL787 - Disj. Q125_2 Desligado', clp, REG_USINA_Alarme05, 4)
        x = self.pacp_alimentação_relé_de_proteção_sel787_disj_q125_2_desligado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.pcp_u1_alimentação_circuitos_de_comando_disj_q24_1_desligado = LeituraModbusBit('05.06 - PCP-U1 - Alimentação Circuitos de Comando - Disj. Q24_1 Desligado', clp, REG_USINA_Alarme05, 6)
        x = self.pcp_u1_alimentação_circuitos_de_comando_disj_q24_1_desligado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.pcp_u2_alimentação_fonte_125_24vcc_disj_q125_3_desligado = LeituraModbusBit('05.07 - PCP-U2 - Alimentação Fonte 125/24Vcc - Disj. Q125_3 Desligado', clp, REG_USINA_Alarme05, 7)
        x = self.pcp_u2_alimentação_fonte_125_24vcc_disj_q125_3_desligado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.pdsa_alimentação_pacp_disj_q220_4_desligado = LeituraModbusBit('06.05 - PDSA - Alimentação PACP - Disj. Q220_4 Desligado', clp, REG_USINA_Alarme06, 5)
        x = self.pdsa_alimentação_pacp_disj_q220_4_desligado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.pdsa_alimentação_disj_52l_carregamento_de_mola_disj_q220_8_desligado = LeituraModbusBit('06.09 - PDSA - Alimentação Disj 52L Carregamento de Mola - Disj. Q220_8 Desligado', clp, REG_USINA_Alarme06, 9)
        x = self.pdsa_alimentação_disj_52l_carregamento_de_mola_disj_q220_8_desligado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.qpse_alimentação_woodward_f67_disj_q125_0_desligado = LeituraModbusBit('08.04 - QPSE - Alimentação Woodward F67 - Disj. Q125_0 Desligado', clp, REG_USINA_Alarme08, 4)
        x = self.qpse_alimentação_woodward_f67_disj_q125_0_desligado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_sel787_diferencial_do_transformador_87t = LeituraModbusBit('08.08 - Relé de Proteção SEL787 - Diferencial do Transformador (87T)', clp, REG_USINA_Alarme08, 8)
        x = self.relé_de_proteção_sel787_diferencial_do_transformador_87t 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_sel787_sobrecorrente_instantânea_de_fase_lado_34_5kv_50pat = LeituraModbusBit('08.09 - Relé de Proteção SEL787 - Sobrecorrente Instantânea de Fase Lado 34,5kV (50PAT)', clp, REG_USINA_Alarme08, 9)
        x = self.relé_de_proteção_sel787_sobrecorrente_instantânea_de_fase_lado_34_5kv_50pat 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_sel787_sobrecorrente_temporizada_de_fase_lado_34_5kv_51pat = LeituraModbusBit('08.10 - Relé de Proteção SEL787 - Sobrecorrente Temporizada de Fase Lado 34,5kV (51PAT)', clp, REG_USINA_Alarme08, 10)
        x = self.relé_de_proteção_sel787_sobrecorrente_temporizada_de_fase_lado_34_5kv_51pat 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_sel787_sobrecorrente_temporizada_de_fase_lado_4_16kv_51pbt = LeituraModbusBit('08.11 - Relé de Proteção SEL787 - Sobrecorrente Temporizada de Fase Lado 4,16kV (51PBT)', clp, REG_USINA_Alarme08, 11)
        x = self.relé_de_proteção_sel787_sobrecorrente_temporizada_de_fase_lado_4_16kv_51pbt 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_sel787_sobrecorrente_de_neutro_temporizada_51nat = LeituraModbusBit('08.12 - Relé de Proteção SEL787 - Sobrecorrente de Neutro Temporizada (51NAT)', clp, REG_USINA_Alarme08, 12)
        x = self.relé_de_proteção_sel787_sobrecorrente_de_neutro_temporizada_51nat 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_sel787_sobrecorrente_residual_temporizada_51gat = LeituraModbusBit('08.13 - Relé de Proteção SEL787 - Sobrecorrente Residual Temporizada (51GAT)', clp, REG_USINA_Alarme08, 13)
        x = self.relé_de_proteção_sel787_sobrecorrente_residual_temporizada_51gat 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.sistema_de_incêndio_atuado = LeituraModbusBit('09.11 - Sistema de Incêndio Atuado', clp, REG_USINA_Alarme09, 11)
        x = self.sistema_de_incêndio_atuado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_da_linha_mra4_sobrecorrente_direcional_com_restrição_por_tensão_67vr = LeituraModbusBit('10.00 - Relé de Proteção da Linha (MRA4) - Sobrecorrente Direcional com Restrição por Tensão - 67VR', clp, REG_USINA_Alarme10, 00)
        x = self.relé_de_proteção_da_linha_mra4_sobrecorrente_direcional_com_restrição_por_tensão_67vr 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_da_linha_mra4_sobrecorrente_temporizada_de_fase_51p = LeituraModbusBit('10.01 - Relé de Proteção da Linha (MRA4) - Sobrecorrente Temporizada de Fase - 51P', clp, REG_USINA_Alarme10, 1)
        x = self.relé_de_proteção_da_linha_mra4_sobrecorrente_temporizada_de_fase_51p 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_da_linha_mra4_sobrecorrente_direcional_de_fase_67r = LeituraModbusBit('10.02 - Relé de Proteção da Linha (MRA4) - Sobrecorrente Direcional de Fase - 67R', clp, REG_USINA_Alarme10, 2)
        x = self.relé_de_proteção_da_linha_mra4_sobrecorrente_direcional_de_fase_67r 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_da_linha_mra4_sobrecorrente_direcional_de_fase_67f = LeituraModbusBit('10.03 - Relé de Proteção da Linha (MRA4) - Sobrecorrente Direcional de Fase - 67F', clp, REG_USINA_Alarme10, 3)
        x = self.relé_de_proteção_da_linha_mra4_sobrecorrente_direcional_de_fase_67f 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_da_linha_mra4_sobrecorrente_temporizada_de_neutro_51n = LeituraModbusBit('10.04 - Relé de Proteção da Linha (MRA4) - Sobrecorrente Temporizada de Neutro - 51N', clp, REG_USINA_Alarme10, 4)
        x = self.relé_de_proteção_da_linha_mra4_sobrecorrente_temporizada_de_neutro_51n 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_da_linha_mra4_sobrecorrente_de_sequência_negativa_temporizada_46 = LeituraModbusBit('10.05 - Relé de Proteção da Linha (MRA4) - Sobrecorrente de Sequência Negativa Temporizada - 46', clp, REG_USINA_Alarme10, 5)
        x = self.relé_de_proteção_da_linha_mra4_sobrecorrente_de_sequência_negativa_temporizada_46 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
                
        self.relé_de_proteção_da_linha_mra4_sobretensão_de_fase_59p = LeituraModbusBit('10.07 - Relé de Proteção da Linha (MRA4) - Sobretensão de Fase - 59P', clp, REG_USINA_Alarme10, 7)
        x = self.relé_de_proteção_da_linha_mra4_sobretensão_de_fase_59p 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_da_linha_mra4_sobrefrequência_nível_1_81o = LeituraModbusBit('10.10 - Relé de Proteção da Linha (MRA4) - Sobrefrequência Nível 1 - 81O', clp, REG_USINA_Alarme10, 10)
        x = self.relé_de_proteção_da_linha_mra4_sobrefrequência_nível_1_81o 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_da_linha_mra4_falha_no_disjuntor_50_62bf = LeituraModbusBit('10.14 - Relé de Proteção da Linha (MRA4) - Falha no Disjuntor - 50/62BF', clp, REG_USINA_Alarme10, 14)
        x = self.relé_de_proteção_da_linha_mra4_falha_no_disjuntor_50_62bf 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_da_linha_mra4_sobrepotência_de_exportação_32o = LeituraModbusBit('10.15 - Relé de Proteção da Linha (MRA4) - Sobrepotência de Exportação - 32O', clp, REG_USINA_Alarme10, 15)
        x = self.relé_de_proteção_da_linha_mra4_sobrepotência_de_exportação_32o 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_da_linha_mra4_potência_ativa_reversa_32r = LeituraModbusBit('11.00 - Relé de Proteção da Linha (MRA4) - Potência Ativa Reversa - 32R', clp, REG_USINA_Alarme11, 00)
        x = self.relé_de_proteção_da_linha_mra4_potência_ativa_reversa_32r 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_da_linha_mra4_sobretensão_de_sequência_negativa_59q = LeituraModbusBit('11.01 - Relé de Proteção da Linha (MRA4) - Sobretensão de Sequência Negativa - 59Q', clp, REG_USINA_Alarme11, 1)
        x = self.relé_de_proteção_da_linha_mra4_sobretensão_de_sequência_negativa_59q 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.carregador_de_baterias_cb01_defeito_geral = LeituraModbusBit('11.06 - Carregador de Baterias CB01 - Defeito Geral', clp, REG_USINA_Alarme11, 6)
        x = self.carregador_de_baterias_cb01_defeito_geral 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.carregador_de_baterias_cb01_fuga_à_terra_pelo_positivo = LeituraModbusBit('11.08 - Carregador de Baterias CB01 - Fuga à Terra Pelo Positivo', clp, REG_USINA_Alarme11, 8)
        x = self.carregador_de_baterias_cb01_fuga_à_terra_pelo_positivo 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.carregador_de_baterias_cb01_fuga_à_terra_pelo_negativo = LeituraModbusBit('11.09 - Carregador de Baterias CB01 - Fuga à Terra Pelo Negativo', clp, REG_USINA_Alarme11, 9)
        x = self.carregador_de_baterias_cb01_fuga_à_terra_pelo_negativo 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.qcta_erro_de_leitura_na_entrada_analógica_nível_barragem_montante_grade = LeituraModbusBit('13.03 - QCTA - Erro de Leitura na Entrada Analógica Nível Barragem (Montante Grade)', clp, REG_USINA_Alarme13, 3)
        x = self.qcta_erro_de_leitura_na_entrada_analógica_nível_barragem_montante_grade 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_sel700g_sobretensão_residual_59g = LeituraModbusBit('11.08 - Relé de Proteção SEL700G - Sobretensão Residual (59G)', clp, REG_USINA_Alarme11, 8)
        x = self.relé_de_proteção_sel700g_sobretensão_residual_59g 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_sel700g_potência_reversa_32p = LeituraModbusBit('11.09 - Relé de Proteção SEL700G - Potência Reversa (32P)', clp, REG_USINA_Alarme11, 9)
        x = self.relé_de_proteção_sel700g_potência_reversa_32p 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_sel700g_energização_indevida_50m = LeituraModbusBit('11.12 - Relé de Proteção SEL700G - Energização Indevida (50M)', clp, REG_USINA_Alarme11, 12)
        x = self.relé_de_proteção_sel700g_energização_indevida_50m 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_sel700g_falha_do_disjuntor_52g_50_62bf = LeituraModbusBit('11.15 - Relé de Proteção SEL700G - Falha do Disjuntor 52G (50_62BF)', clp, REG_USINA_Alarme11, 15)
        x = self.relé_de_proteção_sel700g_falha_do_disjuntor_52g_50_62bf 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.grtd_2000_falha_sobrecorrente_de_excitação = LeituraModbusBit('12.04 - GRTD 2000 - Falha Sobrecorrente de Excitação', clp, REG_USINA_Alarme12, 4)
        x = self.grtd_2000_falha_sobrecorrente_de_excitação 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.erro_de_leitura_na_entrada_analógica_de_pressão_da_caixa_espiral = LeituraModbusBit('12.11 - Erro de Leitura na Entrada Analógica de Pressão da Caixa Espiral', clp, REG_USINA_Alarme12, 11)
        x = self.erro_de_leitura_na_entrada_analógica_de_pressão_da_caixa_espiral 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.css_u1_alimentação_motor_carregamento_mola_disjuntor_52g_disjuntor_q220_1_desligado = LeituraModbusBit('13.07 - CSS-U1 - Alimentação Motor Carregamento Mola Disjuntor 52G - Disjuntor Q220_1 Desligado', clp, REG_USINA_Alarme13, 7)
        x = self.css_u1_alimentação_motor_carregamento_mola_disjuntor_52g_disjuntor_q220_1_desligado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.q49_módulo_de_temperatura_sel2600_disjuntor_q125_0_desligado = LeituraModbusBit('13.14 - Q49 - Módulo de Temperatura SEL2600 - Disjuntor Q125_0 Desligado', clp, REG_USINA_Alarme13, 14)
        x = self.q49_módulo_de_temperatura_sel2600_disjuntor_q125_0_desligado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.trip_vibração_excessiva_no_mancal_la_do_gerador = LeituraModbusBit('15.01 - TRIP - Vibração Excessiva no Mancal LA do Gerador', clp, REG_USINA_Alarme15, 1)
        x = self.trip_vibração_excessiva_no_mancal_la_do_gerador 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.trip_vibração_excessiva_no_mancal_loa_do_gerador = LeituraModbusBit('15.03 - TRIP - Vibração Excessiva no Mancal LOA do Gerador', clp, REG_USINA_Alarme15, 3)
        x = self.trip_vibração_excessiva_no_mancal_loa_do_gerador 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
                
        self.relé_de_proteção_da_linha_mra4_subtensão_de_fase_27p = LeituraModbusBit('10.06 - Relé de Proteção da Linha (MRA4) - Subtensão de Fase - 27P', clp, REG_USINA_Alarme10, 6)
        x = self.relé_de_proteção_da_linha_mra4_subtensão_de_fase_27p
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.relé_de_proteção_da_linha_mra4_subfrequência_nível_1_81u = LeituraModbusBit('10.08 - Relé de Proteção da Linha (MRA4) - Subfrequência Nível 1 - 81U', clp, REG_USINA_Alarme10, 8)
        x = self.relé_de_proteção_da_linha_mra4_subfrequência_nível_1_81u
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.relé_de_proteção_da_linha_mra4_subfrequência_nível_2_81u = LeituraModbusBit('10.09 - Relé de Proteção da Linha (MRA4) - Subfrequência Nível 2 - 81U', clp, REG_USINA_Alarme10, 9)
        x = self.relé_de_proteção_da_linha_mra4_subfrequência_nível_2_81u
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.relé_de_proteção_da_linha_mra4_sobrefrequência_nível_2_81o = LeituraModbusBit('10.11 - Relé de Proteção da Linha (MRA4) - Sobrefrequência Nível 2 - 81O', clp, REG_USINA_Alarme10, 11)
        x = self.relé_de_proteção_da_linha_mra4_sobrefrequência_nível_2_81o
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.relé_de_proteção_da_linha_mra4_taxa_de_variação_de_frequência_81_df_dt = LeituraModbusBit('10.12 - Relé de Proteção da Linha (MRA4) - Taxa de Variação de Frequência  - 81 df/dt', clp, REG_USINA_Alarme10, 12)
        x = self.relé_de_proteção_da_linha_mra4_taxa_de_variação_de_frequência_81_df_dt
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.relé_de_proteção_da_linha_mra4_perda_de_sincronismo_78 = LeituraModbusBit('10.13 - Relé de Proteção da Linha (MRA4) - Perda de Sincronismo  - 78', clp, REG_USINA_Alarme10, 13)
        x = self.relé_de_proteção_da_linha_mra4_perda_de_sincronismo_78
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
                

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
        logger.debug("self.ug1.leitura_potencia.valor -> {}".format(self.ug1.leitura_potencia.valor))
        logger.debug("self.ug2.leitura_potencia.valor -> {}".format(self.ug2.leitura_potencia.valor))
        self.ug1.setpoint = self.ug1.leitura_potencia.valor
        self.ug2.setpoint = self.ug2.leitura_potencia.valor

    @property
    def nv_montante(self):
        return self.leituras.nv_montante.valor

    def ler_valores(self):

        # CLP
        # regs = [0]*40000
        # aux = self.clp.read_sequential(40000, 101)
        # regs += aux
        # USN
        # self.clp_emergencia_acionada = regs[self.cfg['ENDERECO_CLP_USINA_FLAGS']]
        # self.nv_montante = round((regs[self.cfg['ENDERECO_CLP_NV_MONATNTE']] * 0.001) + 620, 2)
        # self.pot_medidor = round((regs[self.cfg['ENDERECO_CLP_MEDIDOR']] * 0.001), 3)
        
        # -> Verifica conexão com CLP Tomada d'água
        #   -> Se não estiver ok, acionar emergencia CLP
        if not ping(self.cfg["TDA_slave_ip"]):
            if not self.borda_aviso_clp_tda:
                logger.warning("CLP TDA não respondeu a tentativa de comunicação!")
                self.borda_aviso_clp_tda = True
        else:
            if self.borda_aviso_clp_tda:
                logger.info("CLP TDA voltou a comunicar!")
                self.borda_aviso_clp_tda = False

        # -> Verifica conexão com CLP Sub
        #   -> Se não estiver ok, avisa por logger.warning
        if not ping(self.cfg["USN_slave_ip"]):
            if not self.borda_aviso_clp_pacp:
                logger.warning("CLP PACP não respondeu a tentativa de comunicação!")
                self.borda_aviso_clp_pacp = True
        else:
            if self.borda_aviso_clp_pacp:
                logger.info("CLP PACP voltou a comunicar!")
                self.borda_aviso_clp_pacp = False

        # -> Verifica conexão com CLP UG#
        #    -> Se não estiver ok, acionar indisponibiliza UG# e avisa por logger.warning
        # UG1
        if not ping(self.cfg["UG1_slave_ip"]):
            if not self.borda_aviso_clp_ug1:
                logger.warning("CLP UG1 não respondeu a tentativa de comunicação!")
                self.borda_aviso_clp_ug1 = True
                self.ug1.forcar_estado_restrito()
        else:
            if self.borda_aviso_clp_ug1:
                logger.info("CLP UG1 voltou a comunicar!")
                self.borda_aviso_clp_ug1 = False
                self.ug1.forcar_estado_disponivel()
        # UG2
        if not ping(self.cfg["UG2_slave_ip"]):
            if not self.borda_aviso_clp_ug2:
                logger.warning("CLP UG2 não respondeu a tentativa de comunicação!")
                self.borda_aviso_clp_ug2 = True
                self.ug2.forcar_estado_restrito()
        else:
            if self.borda_aviso_clp_ug2:
                logger.info("CLP UG2 voltou a comunicar!")
                self.borda_aviso_clp_ug2 = False
                self.ug2.forcar_estado_disponivel()

        self.clp_online = True
        self.clp_emergencia_acionada = 0

        if self.nv_montante_recente < 1:
            self.nv_montante_recentes = [self.leituras.nv_montante.valor] * 120
        self.nv_montante_recentes.append(
            round((self.leituras.nv_montante.valor + self.nv_montante_recentes[-1]) / 2, 2)
        )
        self.nv_montante_recentes = self.nv_montante_recentes[1:]

        # Filtro butterworth
        b, a = butter(4, 1, fs=60)
        self.nv_montante_recente = float(
            filtfilt(b, a, filtfilt(b, a, self.nv_montante_recentes))[-1]
        )

        self.erro_nv_anterior = self.erro_nv
        self.erro_nv = self.nv_montante_recente - self.nv_alvo

        # DB
        #
        # Ler apenas os parametros que estao disponiveis no django
        #  - Botão de emergência
        #  - Limites de operação das UGS
        #  - Modo autonomo
        #  - Modo de prioridade UGS
        #  - Niveis de operação da comporta

        parametros = self.db.get_parametros_usina()

        # Botão de emergência
        self.db_emergencia_acionada = int(parametros["emergencia_acionada"])

        # Limites de operação das UGS
        for ug in self.ugs:
            ug.prioridade = int(parametros["ug{}_prioridade".format(ug.id)])  # TODO
            ug.condicionador_perda_na_grade.valor_base = float(
                parametros["ug{}_perda_grade_alerta".format(ug.id)]
            )
            ug.condicionador_perda_na_grade.valor_limite = float(
                parametros["ug{}_perda_grade_maxima".format(ug.id)]
            )
            ug.condicionador_temperatura_enrolamento_fase_r.valor_base = float(
                parametros["temperatura_alerta_enrolamento_fase_r_ug{}".format(ug.id)]
            )
            ug.condicionador_temperatura_enrolamento_fase_s.valor_base = float(
                parametros["temperatura_alerta_enrolamento_fase_s_ug{}".format(ug.id)]
            )
            ug.condicionador_temperatura_enrolamento_fase_t.valor_base = float(
                parametros["temperatura_alerta_enrolamento_fase_t_ug{}".format(ug.id)]
            )
            ug.condicionador_temperatura_mancal_la_casquilho.valor_base = float(
                parametros["temperatura_alerta_mancal_la_casquilho_ug{}".format(ug.id)]
            )
            ug.condicionador_temperatura_mancal_la_contra_escora_1.valor_base = float(
                parametros[
                    "temperatura_alerta_mancal_la_contra_escora_1_ug{}".format(ug.id)
                ]
            )
            ug.condicionador_temperatura_mancal_la_contra_escora_2.valor_base = float(
                parametros[
                    "temperatura_alerta_mancal_la_contra_escora_2_ug{}".format(ug.id)
                ]
            )
            ug.condicionador_temperatura_mancal_la_escora_1.valor_base = float(
                parametros["temperatura_alerta_mancal_la_escora_1_ug{}".format(ug.id)]
            )
            ug.condicionador_temperatura_mancal_la_escora_2.valor_base = float(
                parametros["temperatura_alerta_mancal_la_escora_2_ug{}".format(ug.id)]
            )
            ug.condicionador_temperatura_mancal_lna_casquilho.valor_base = float(
                parametros["temperatura_alerta_mancal_lna_casquilho_ug{}".format(ug.id)]
            )
            ug.condicionador_temperatura_enrolamento_fase_r.valor_limite = float(
                parametros["temperatura_limite_enrolamento_fase_r_ug{}".format(ug.id)]
            )
            ug.condicionador_temperatura_enrolamento_fase_s.valor_limite = float(
                parametros["temperatura_limite_enrolamento_fase_s_ug{}".format(ug.id)]
            )
            ug.condicionador_temperatura_enrolamento_fase_t.valor_limite = float(
                parametros["temperatura_limite_enrolamento_fase_t_ug{}".format(ug.id)]
            )
            ug.condicionador_temperatura_mancal_la_casquilho.valor_limite = float(
                parametros["temperatura_limite_mancal_la_casquilho_ug{}".format(ug.id)]
            )
            ug.condicionador_temperatura_mancal_la_contra_escora_1.valor_limite = float(
                parametros[
                    "temperatura_limite_mancal_la_contra_escora_1_ug{}".format(ug.id)
                ]
            )
            ug.condicionador_temperatura_mancal_la_contra_escora_2.valor_limite = float(
                parametros[
                    "temperatura_limite_mancal_la_contra_escora_2_ug{}".format(ug.id)
                ]
            )
            ug.condicionador_temperatura_mancal_la_escora_1.valor_limite = float(
                parametros["temperatura_limite_mancal_la_escora_1_ug{}".format(ug.id)]
            )
            ug.condicionador_temperatura_mancal_la_escora_2.valor_limite = float(
                parametros["temperatura_limite_mancal_la_escora_2_ug{}".format(ug.id)]
            )
            ug.condicionador_temperatura_mancal_lna_casquilho.valor_limite = float(
                parametros["temperatura_limite_mancal_lna_casquilho_ug{}".format(ug.id)]
            )

        # nv_minimo
        self.nv_minimo = float(parametros["nv_minimo"])

        # Modo autonomo
        logger.debug(
            "Modo autonomo que o banco respondeu: {}".format(
                int(parametros["modo_autonomo"])
            )
        )
        self.modo_autonomo = int(parametros["modo_autonomo"])
        # Modo de prioridade UGS
        if not self.modo_de_escolha_das_ugs == int(
            parametros["modo_de_escolha_das_ugs"]
        ):
            self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
            logger.info(
                "O modo de prioridade das ugs foi alterado (#{}).".format(
                    self.modo_de_escolha_das_ugs
                )
            )

        # Niveis de operação da comporta
        # self.comporta.pos_0['anterior'] = float(parametros["nv_comporta_pos_0_ant"])
        self.comporta.pos_0["proximo"] = float(parametros["nv_comporta_pos_0_prox"])
        self.comporta.pos_1["anterior"] = float(parametros["nv_comporta_pos_1_ant"])
        self.comporta.pos_1["proximo"] = float(parametros["nv_comporta_pos_1_prox"])
        self.comporta.pos_2["anterior"] = float(parametros["nv_comporta_pos_2_ant"])
        self.comporta.pos_2["proximo"] = float(parametros["nv_comporta_pos_2_prox"])
        self.comporta.pos_3["anterior"] = float(parametros["nv_comporta_pos_3_ant"])
        self.comporta.pos_3["proximo"] = float(parametros["nv_comporta_pos_3_prox"])
        self.comporta.pos_4["anterior"] = float(parametros["nv_comporta_pos_4_ant"])
        self.comporta.pos_4["proximo"] = float(parametros["nv_comporta_pos_4_prox"])
        self.comporta.pos_5["anterior"] = float(parametros["nv_comporta_pos_5_ant"])
        # self.comporta.pos_5['proximo'] = float(parametros["nv_comporta_pos_5_prox"])

        # Parametros banco
        self.nv_alvo = float(parametros["nv_alvo"])
        self.kp = float(parametros["kp"])
        self.ki = float(parametros["ki"])
        self.kd = float(parametros["kd"])
        self.kie = float(parametros["kie"])
        self.n_movel_l = float(parametros["n_movel_L"])
        self.n_movel_r = float(parametros["n_movel_R"])

        # Le o databank interno

        if DataBank.get_words(self.cfg["REG_MOA_IN_EMERG"])[0] != 0:
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

        logger.debug(
            "Ultima tentativa: {}. Tensão na linha: RS {:2.1f}kV ST{:2.1f}kV TR{:2.1f}kV.".format(
                self.ts_ultima_tesntativa_de_normalizacao,
                self.leituras.tensao_rs.valor / 1000,
                self.leituras.tensao_st.valor / 1000,
                self.leituras.tensao_tr.valor / 1000,
            )
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
            return False

    def heartbeat(self):

        ts = datetime.now().timestamp()
        try:
            logger.debug("Inserting in db")
            ma = 1 if self.modo_autonomo else 0
            self.db.insert_debug(
                ts,
                self.kp,
                self.ki,
                self.kd,
                self.kie,
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
                self.cfg["REG_MOA_OUT_TARGET_LEVEL"], [self.nv_alvo - 620] * 1000
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

        logger.debug(agendamentos)

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
                logger.warning(
                    "Agendamento #{} Atrasado! ({}).".format(
                        agendamento[0], agendamento[3]
                    )
                )
                self.agendamentos_atrasados += 1

            if segundos_passados > 300 or self.agendamentos_atrasados > 3:
                logger.info(
                    "Os agendamentos estão muito atrasados! Acionando emergência."
                )
                self.acionar_emergencia()
                return False

            if segundos_adiantados <= 60 and not bool(agendamento[4]):
                # Está na hora e ainda não foi executado. Executar!
                logger.info(
                    "Executando gendamento #{}\n" + \
                    "Comando: {}\n" + \
                    "Data agendamento: {}\n" + \
                    "Obs: {}\n" + \
                    "Valor: {}".format(
                        agendamento[0],
                        INT_TO_AGENDAMENTOS[agendamento[3]],
                        agendamento[1],
                        agendamento[2],
                        agendamento[5],
                    )
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
                        logger.info("Alterando pot maxima para: {} kW.".format(novo))
                        self.cfg["pot_maxima_alvo"] = novo
                        self.cfg["pot_maxima_usina"] = novo
                    except Exception as e:
                        obs =  "Valor inválido no comando {} ('{}'  é inválido).".format(agendamento[0], agendamento[5])
                        logger.info(
                           obs
                        )
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

                if agendamento[3] == AGENDAMENTO_ALETRAR_NV_ALVO:
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
                        obs =  "Valor inválido no comando {} ('{}'  é inválido).".format(agendamento[0], agendamento[5])
                        logger.info(
                           obs
                        )
                        self.db.update_agendamento(agendamento[0], True, obs)
                    

                if agendamento[3] == AGENDAMENTO_UG1_ALETRAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.ug1.pot_disponivel = novo
                    except Exception as e:
                        obs =  "Valor inválido no comando {} ('{}'  é inválido).".format(agendamento[0], agendamento[5])
                        logger.info(
                           obs
                        )
                        self.db.update_agendamento(agendamento[0], True, obs)

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_MANUAL:
                    self.ug1.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_DISPONIVEL:
                    self.ug1.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug1.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG1_FORCAR_ESTADO_RESTRITO:
                    self.ug1.forcar_estado_restrito()

                if agendamento[3] == AGENDAMENTO_UG2_ALETRAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.ug2.pot_disponivel = novo
                    except Exception as e:
                        obs =  "Valor inválido no comando {} ('{}'  é inválido).".format(agendamento[0], agendamento[5])
                        logger.info(
                           obs
                        )
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
                logger.debug(
                    "O comando #{} foi executado.".format(
                        agendamento[0],
                    )
                )
                self.con.somente_reconhecer_emergencia()
                self.escrever_valores()

    def distribuir_potencia(self, pot_alvo):

        if pot_alvo < 0.1:
            for ug in self.ugs:
                ug.setpoint = 0
            return 0

        self.pot_disp = 0
        if self.ug1.disponivel:
            self.pot_disp += self.cfg["pot_maxima_ug"]
        if self.ug2.disponivel:
            self.pot_disp += self.cfg["pot_maxima_ug"]

        if self.leituras.potencia_ativa_kW.valor > self.cfg["pot_maxima_alvo"] * 0.95:
            pot_alvo = pot_alvo / (self.leituras.potencia_ativa_kW.valor/self.cfg["pot_maxima_alvo"])

        ugs = self.lista_de_ugs_disponiveis()
        logger.debug("lista_de_ugs_disponiveis:")
        for ug in ugs:
            logger.debug("UG{}".format(ug.id))

        if ugs is None:
            return False
        elif len(ugs) == 0:
            return False
        elif len(ugs) == 1:
            pot_alvo = min(pot_alvo, self.cfg["pot_maxima_ug"])
            ugs[0].setpoint = pot_alvo
            return False
        else:

            if self.leituras.dj52L_aberto.valor:
                logger.info("Fechando Disjuntor 52L.")
                self.con.fechaDj52L()

            else:

                logger.debug("Distribuindo {}".format(pot_alvo))
                if 0.1 < pot_alvo < self.cfg["pot_minima"]:
                    logger.debug("0.1 < {} < self.cfg['pot_minima']".format(pot_alvo))
                    if len(ugs) > 0:
                        ugs[0].setpoint = self.cfg["pot_minima"]
                        for ug in ugs[1:]:
                            ug.setpoint = 0
                else:
                    pot_alvo = min(pot_alvo, self.pot_disp)

                    """
                    if (
                        self.ug1.etapa_atual == UNIDADE_SINCRONIZADA
                        and self.ug2.etapa_atual == UNIDADE_SINCRONIZADA
                        and pot_alvo > (2 * self.cfg["pot_minima"] - self.cfg["margem_pot_critica"])
                    ):
                        logger.debug(
                            "Dividir entre as ugs (cada = {})".format(
                                pot_alvo / len(ugs)
                            )
                        )
                        for ug in ugs:
                            ug.setpoint = int(pot_alvo / len(ugs))
                    elif (
                        (
                            pot_alvo
                            > (
                                self.cfg["pot_maxima_ug"]
                                + self.cfg["margem_pot_critica"]
                            )
                        )
                        and (abs(self.erro_nv) > 0.02)
                        and self.ug1.disponivel
                        and self.ug2.disponivel
                    ):
                        ugs[0].setpoint = self.cfg["pot_maxima_ug"]
                        for ug in ugs[1:]:
                            ug.setpoint = pot_alvo / len(ugs)

                    elif (
                        pot_alvo
                        < (self.cfg["pot_maxima_ug"] - self.cfg["margem_pot_critica"])
                    ):
                        logger.debug(
                            "{} < self.cfg['pot_maxima_ug'] ({}) - self.cfg['margem_pot_critica'] ({})".format(
                                pot_alvo, self.cfg['pot_maxima_ug'], self.cfg["margem_pot_critica"]
                            )
                        )
                        ugs[0].setpoint = pot_alvo
                        for ug in ugs[1:]:
                            ug.setpoint = 0

                    else:
                        pot_alvo = min(pot_alvo, self.cfg["pot_maxima_ug"])
                        if len(ugs) > 0:
                            ugs[0].setpoint = pot_alvo
                            for ug in ugs[1:]:
                                ug.setpoint = 0
                    """
                    if len(ugs) == 0:
                        return False

                    if (self.ug1.etapa_atual == UNIDADE_SINCRONIZADA
                        and self.ug2.etapa_atual == UNIDADE_SINCRONIZADA
                        and pot_alvo > (self.cfg["pot_maxima_ug"] - self.cfg["margem_pot_critica"])):
                        logger.debug("Dividindo igualmente entre as UGs")
                        logger.debug("self.cfg[margem_pot_critica] = {}".format( self.cfg["margem_pot_critica"]))
                        for ug in ugs:
                            ug.setpoint = max(self.cfg["pot_minima"], pot_alvo / len(ugs))

                    elif(pot_alvo > (self.cfg["pot_maxima_ug"] + self.cfg["margem_pot_critica"])):
                        logger.debug("Dividindo desigualmente entre UGs pois está partindo uma ou mais UGs")
                        ugs[0].setpoint = self.cfg["pot_maxima_ug"]
                        for ug in ugs[1:]:
                            ug.setpoint = max(self.cfg["pot_minima"], pot_alvo / len(ugs))

                    else:
                        logger.debug("Apenas uma UG deve estar sincronizada")
                        pot_alvo = min(pot_alvo, self.cfg["pot_maxima_ug"])
                        ugs[0].setpoint = max(self.cfg["pot_minima"], pot_alvo)
                        for ug in ugs[1:]:
                            ug.setpoint = 0

                for ug in self.ugs:
                    logger.debug("UG{} SP:{}".format(ug.id, ug.setpoint))
        
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
        return ls

    def controle_normal(self):
        """
        Controle PID
        https://en.wikipedia.org/wiki/PID_controller#Proportional
        """
        logger.debug("-------------------------------------------------")

        # Calcula PID
        logger.debug(
            "Alvo: {:0.3f}, Recente: {:0.3f}".format(
                self.nv_alvo, self.nv_montante_recente
            )
        )
        if abs(self.erro_nv) <= 0.01:
            self.controle_p = self.kp * 0.5 * self.erro_nv
        else:
            self.controle_p = self.kp * self.erro_nv
        self.controle_i = max(min((self.ki * self.erro_nv) + self.controle_i, 0.8), 0)
        self.controle_d = self.kd * (self.erro_nv - self.erro_nv_anterior)
        saida_pid = (
            self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3)
        )
        logger.debug(
            "PID: {:0.3f} <-- P:{:0.3f} + I:{:0.3f} + D:{:0.3f}; ERRO={}".format(
                saida_pid,
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.erro_nv,
            )
        )

        # Calcula o integrador de estabilidade e limita
        self.controle_ie = max(min(saida_pid + self.controle_ie * self.kie, 1), 0)

        if self.nv_montante_recente >= (self.nv_maximo - 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if self.nv_montante_recente <= (self.nv_minimo + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        logger.debug("IE: {:0.3f}".format(self.controle_ie))

        # Arredondamento e limitação
        pot_alvo = max(
            min(
                round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5),
                self.cfg["pot_maxima_usina"],
            ),
            self.cfg["pot_minima"],
        )

        logger.debug("Pot alvo: {:0.3f}".format(pot_alvo))
        logger.debug("Nv alvo: {:0.3f}".format(self.nv_alvo))
        ts = datetime.now().timestamp()
        try:
            logger.debug("Inserting in db")
            ma = 1 if self.modo_autonomo else 0
            self.db.insert_debug(
                ts,
                self.kp,
                self.ki,
                self.kd,
                self.kie,
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


class Comporta:
    def __init__(self):
        self.pos_comporta = 0
        self.pos_0 = {"pos": 0, "anterior": 0.0, "proximo": 0.0}
        self.pos_1 = {"pos": 1, "anterior": 0.0, "proximo": 0.0}
        self.pos_2 = {"pos": 2, "anterior": 0.0, "proximo": 0.0}
        self.pos_3 = {"pos": 3, "anterior": 0.0, "proximo": 0.0}
        self.pos_4 = {"pos": 4, "anterior": 0.0, "proximo": 0.0}
        self.pos_5 = {"pos": 5, "anterior": 0.0, "proximo": 0.0}
        self.posicoes = [
            self.pos_0,
            self.pos_1,
            self.pos_2,
            self.pos_3,
            self.pos_4,
            self.pos_5,
        ]

    def atualizar_estado(self, nv_montante):

        self.posicoes = [
            self.pos_0,
            self.pos_1,
            self.pos_2,
            self.pos_3,
            self.pos_4,
            self.pos_5,
        ]

        if not 0 <= self.pos_comporta <= 5:
            raise IndexError("Pos comporta invalida {}".format(self.pos_comporta))

        estado_atual = self.posicoes[self.pos_comporta]
        pos_alvo = self.pos_comporta
        if nv_montante < self.pos_1["anterior"]:
            pos_alvo = 0
        else:
            if nv_montante < estado_atual["anterior"]:
                pos_alvo = self.pos_comporta - 1
            elif nv_montante >= estado_atual["proximo"]:
                pos_alvo = self.pos_comporta + 1
            pos_alvo = min(max(0, pos_alvo), 5)
        if not pos_alvo == self.pos_comporta:
            logger.info(
                "Mudança de setpoint da comprota para {} (atual:{})".format(
                    pos_alvo, self.pos_comporta
                )
            )
            self.pos_comporta = pos_alvo

        return pos_alvo


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    https://stackoverflow.com/questions/2953462/pinging-servers-in-python
    """
    ping = False
    for i in range(5):
        ping = ping or (subprocess.call(["ping", "-c", "1", host], stdout=subprocess.PIPE) == 0)
        if not ping:
            sleep(1)
    return ping
