import json
import math
import os
from unittest.mock import MagicMock
from src.Condicionadores import *
from src.Leituras import *
from src.LeiturasUSN import *
from src.UnidadeDeGeracao import *
from pyModbusTCP.server import DataBank, ModbusServer


class UnidadeDeGeracao2(UnidadeDeGeracao):
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

        self.setpoint_minimo = self.cfg["pot_minima"]
        self.setpoint_maximo = self.cfg["pot_maxima_ug{}".format(self.id)]

        self.clp_ip = self.cfg["UG2_slave_ip"]
        self.clp_port = self.cfg["UG2_slave_porta"]
        self.clp = ModbusClient(
            host=self.clp_ip,
            port=self.clp_port,
            timeout=5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )

        self.__last_EtapaAtual = 0
        self.__last_EtapaAlvo = -1
        self.enviar_trip_eletrico = False

        
        self.uhct_filtro_de_óleo_linha_de_pressão_01_sujo = LeituraModbusBit('03.02 - UHCT - Filtro de Óleo Linha de Pressão 01 Sujo', self.clp, REG_UG2_Alarme03, 2)
        x = self.uhct_filtro_de_óleo_linha_de_pressão_01_sujo 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.uhct_filtro_de_óleo_linha_de_pressão_02_sujo = LeituraModbusBit('03.03 - UHCT - Filtro de Óleo Linha de Pressão 02 Sujo', self.clp, REG_UG2_Alarme03, 3)
        x = self.uhct_filtro_de_óleo_linha_de_pressão_02_sujo 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.uhct_nível_de_óleo_crítico = LeituraModbusBit('03.04 - UHCT - Nível de Óleo Crítico', self.clp, REG_UG2_Alarme03, 4)
        x = self.uhct_nível_de_óleo_crítico 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.dispositivo_de_sobrevelocidade_mecânico_atuado = LeituraModbusBit('04.05 - Dispositivo de SobreVelocidade Mecânico Atuado', self.clp, REG_UG2_Alarme04, 5)
        x = self.dispositivo_de_sobrevelocidade_mecânico_atuado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.turbina_falha_no_fechamento_do_distribuidor = LeituraModbusBit('04.09 - Turbina - Falha no Fechamento do Distribuidor', self.clp, REG_UG2_Alarme04, 9)
        x = self.turbina_falha_no_fechamento_do_distribuidor 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.reg_tensão_fusível_da_ponte_retificadora_queimado = LeituraModbusBit('04.13 - Reg Tensão - Fusível da Ponte Retificadora Queimado', self.clp, REG_UG2_Alarme04, 13)
        x = self.reg_tensão_fusível_da_ponte_retificadora_queimado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_bloqueio_86m_trip_atuado = LeituraModbusBit('05.06 - Relé de Bloqueio 86M Trip Atuado', self.clp, REG_UG2_Alarme05, 6)
        x = self.relé_de_bloqueio_86m_trip_atuado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_bloqueio_86m_trip_atuado_temporizado = LeituraModbusBit('05.07 - Relé de Bloqueio 86M Trip Atuado Temporizado', self.clp, REG_UG2_Alarme05, 7)
        x = self.relé_de_bloqueio_86m_trip_atuado_temporizado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_bloqueio_86m_trip_atuado_pelo_clp = LeituraModbusBit('05.08 - Relé de Bloqueio 86M Trip Atuado pelo CLP', self.clp, REG_UG2_Alarme05, 8)
        x = self.relé_de_bloqueio_86m_trip_atuado_pelo_clp 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_bloqueio_86h_trip_atuado = LeituraModbusBit('05.12 - Relé de Bloqueio 86H Trip Atuado', self.clp, REG_UG2_Alarme05, 12)
        x = self.relé_de_bloqueio_86h_trip_atuado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.relé_de_bloqueio_86h_trip_atuado_pelo_clp = LeituraModbusBit('05.13 - Relé de Bloqueio 86H Trip Atuado pelo CLP', self.clp, REG_UG2_Alarme05, 13)
        x = self.relé_de_bloqueio_86h_trip_atuado_pelo_clp 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_do_gerador_falha_no_disjuntor_50_62bf = LeituraModbusBit('06.01 - Relé de Proteção do Gerador - Falha no Disjuntor 50_62BF', self.clp, REG_UG2_Alarme06, 1)
        x = self.relé_de_proteção_do_gerador_falha_no_disjuntor_50_62bf 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_do_gerador_falha_de_hardware = LeituraModbusBit('06.02 - Relé de Proteção do Gerador - Falha de Hardware', self.clp, REG_UG2_Alarme06, 2)
        x = self.relé_de_proteção_do_gerador_falha_de_hardware 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.disjuntor_52g_atenção_disjuntor_não_inserido_ou_extraído = LeituraModbusBit('06.04 - Disjuntor 52G - ATENÇÃO! Disjuntor Não Inserido ou Extraído', self.clp, REG_UG2_Alarme06, 4)
        x = self.disjuntor_52g_atenção_disjuntor_não_inserido_ou_extraído 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.disjuntor_52g_falha_na_abertura = LeituraModbusBit('06.07 - Disjuntor 52G - Falha na Abertura', self.clp, REG_UG2_Alarme06, 7)
        x = self.disjuntor_52g_falha_na_abertura 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_enrolamento_da_fase_r_do_gerador_trip_86m_= LeituraModbusBit('08.14 - Relé de Proteção - Sobretemperatura do Enrolamento da Fase R do Gerador (Trip 86M)', self.clp, REG_UG2_Alarme08, 14)
        x = self.relé_de_proteção_sobretemperatura_do_enrolamento_da_fase_r_do_gerador_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_enrolamento_da_fase_s_do_gerador_trip_86m_= LeituraModbusBit('08.15 - Relé de Proteção - Sobretemperatura do Enrolamento da Fase S do Gerador (Trip 86M)', self.clp, REG_UG2_Alarme08, 15)
        x = self.relé_de_proteção_sobretemperatura_do_enrolamento_da_fase_s_do_gerador_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_enrolamento_da_fase_t_do_gerador_trip_86m_= LeituraModbusBit('09.00 - Relé de Proteção - Sobretemperatura do Enrolamento da Fase T do Gerador (Trip 86M)', self.clp, REG_UG2_Alarme09, 0)
        x = self.relé_de_proteção_sobretemperatura_do_enrolamento_da_fase_t_do_gerador_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_escora_1_trip_86m_= LeituraModbusBit('09.01 - Relé de Proteção - Sobretemperatura do Mancal LA do Gerador (Escora 1_(Trip 86M)', self.clp, REG_UG2_Alarme09, 1)
        x = self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_escora_1_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_escora_2_trip_86m_= LeituraModbusBit('09.02 - Relé de Proteção - Sobretemperatura do Mancal LA do Gerador (Escora 2_(Trip 86M)', self.clp, REG_UG2_Alarme09, 2)
        x = self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_escora_2_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_casquilho_trip_86m_= LeituraModbusBit('09.03 - Relé de Proteção - Sobretemperatura do Mancal LA do Gerador (Casquilho_(Trip 86M)', self.clp, REG_UG2_Alarme09, 3)
        x = self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_casquilho_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_contra_escora_1_trip_86m_= LeituraModbusBit('09.04 - Relé de Proteção - Sobretemperatura do Mancal LA do Gerador (Contra-Escora 1_(Trip 86M)', self.clp, REG_UG2_Alarme09, 4)
        x = self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_contra_escora_1_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_mancal_lna_do_gerador_casquilho_trip_86m_= LeituraModbusBit('09.05 - Relé de Proteção - Sobretemperatura do Mancal LNA do Gerador (Casquilho_(Trip 86M)', self.clp, REG_UG2_Alarme09, 5)
        x = self.relé_de_proteção_sobretemperatura_do_mancal_lna_do_gerador_casquilho_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_contra_escora_2_trip_86m_= LeituraModbusBit('09.06 - Relé de Proteção - Sobretemperatura do Mancal LA do Gerador (Contra-Escora 2_(Trip 86M)', self.clp, REG_UG2_Alarme09, 6)
        x = self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_contra_escora_2_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_óleo_do_reservatório_da_uhlm_trip_86m_= LeituraModbusBit('09.08 - Relé de Proteção - Sobretemperatura do Óleo do Reservatório da UHLM (Trip 86M)', self.clp, REG_UG2_Alarme09, 8)
        x = self.relé_de_proteção_sobretemperatura_do_óleo_do_reservatório_da_uhlm_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_óleo_na_saída_do_trocador_de_calor_da_uhlm_trip_86m_= LeituraModbusBit('09.09 - Relé de Proteção - Sobretemperatura do Óleo na Saída do Trocador de Calor da UHLM (Trip 86M)', self.clp, REG_UG2_Alarme09, 9)
        x = self.relé_de_proteção_sobretemperatura_do_óleo_na_saída_do_trocador_de_calor_da_uhlm_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.sobretemperatura_da_água_na_entrada_do_trocador_de_calor_da_uhlm_trip_86m_= LeituraModbusBit('09.10 - Sobretemperatura da Água na Entrada do Trocador de Calor da UHLM (Trip 86M)', self.clp, REG_UG2_Alarme09, 10)
        x = self.sobretemperatura_da_água_na_entrada_do_trocador_de_calor_da_uhlm_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.sobretemperatura_da_água_na_saída_do_trocador_de_calor_da_uhlm_trip_86m_= LeituraModbusBit('09.11 - Sobretemperatura da Água na Saída do Trocador de Calor da UHLM (Trip 86M)', self.clp, REG_UG2_Alarme09, 11)
        x = self.sobretemperatura_da_água_na_saída_do_trocador_de_calor_da_uhlm_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.sobretemperatura_do_óleo_do_reservatório_da_uhct_trip_86m_= LeituraModbusBit('09.12 - Sobretemperatura do Óleo do Reservatório da UHCT (Trip 86M)', self.clp, REG_UG2_Alarme09, 12)
        x = self.sobretemperatura_do_óleo_do_reservatório_da_uhct_trip_86m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_enrolamento_da_fase_r_do_gerador_trip_86e_= LeituraModbusBit('09.14 - Relé de Proteção - Sobretemperatura do Enrolamento da Fase R do Gerador (Trip 86E)', self.clp, REG_UG2_Alarme09, 14)
        x = self.relé_de_proteção_sobretemperatura_do_enrolamento_da_fase_r_do_gerador_trip_86e_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_enrolamento_da_fase_s_do_gerador_trip_86e_= LeituraModbusBit('09.15 - Relé de Proteção - Sobretemperatura do Enrolamento da Fase S do Gerador (Trip 86E)', self.clp, REG_UG2_Alarme09, 15)
        x = self.relé_de_proteção_sobretemperatura_do_enrolamento_da_fase_s_do_gerador_trip_86e_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_enrolamento_da_fase_t_do_gerador_trip_86e_= LeituraModbusBit('10.00 - Relé de Proteção - Sobretemperatura do Enrolamento da Fase T do Gerador (Trip 86E)', self.clp, REG_UG2_Alarme10, 0)
        x = self.relé_de_proteção_sobretemperatura_do_enrolamento_da_fase_t_do_gerador_trip_86e_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_escora_1_trip_86h_= LeituraModbusBit('10.01 - Relé de Proteção - Sobretemperatura do Mancal LA do Gerador (Escora 1_(Trip 86H)', self.clp, REG_UG2_Alarme10, 1)
        x = self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_escora_1_trip_86h_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_escora_2_trip_86h_= LeituraModbusBit('10.02 - Relé de Proteção - Sobretemperatura do Mancal LA do Gerador (Escora 2_(Trip 86H)', self.clp, REG_UG2_Alarme10, 2)
        x = self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_escora_2_trip_86h_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_casquilho_trip_86h_= LeituraModbusBit('10.03 - Relé de Proteção - Sobretemperatura do Mancal LA do Gerador (Casquilho_(Trip 86H)', self.clp, REG_UG2_Alarme10, 3)
        x = self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_casquilho_trip_86h_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_contra_escora_1_trip_86h_= LeituraModbusBit('10.04 - Relé de Proteção - Sobretemperatura do Mancal LA do Gerador (Contra-Escora 1_(Trip 86H)', self.clp, REG_UG2_Alarme10, 4)
        x = self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_contra_escora_1_trip_86h_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_mancal_lna_do_gerador_casquilho_trip_86h_= LeituraModbusBit('10.05 - Relé de Proteção - Sobretemperatura do Mancal LNA do Gerador (Casquilho_(Trip 86H)', self.clp, REG_UG2_Alarme10, 5)
        x = self.relé_de_proteção_sobretemperatura_do_mancal_lna_do_gerador_casquilho_trip_86h_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_contra_escora_2_trip_86h_= LeituraModbusBit('10.06 - Relé de Proteção - Sobretemperatura do Mancal LA do Gerador (Contra-Escora 2_(Trip 86H)', self.clp, REG_UG2_Alarme10, 6)
        x = self.relé_de_proteção_sobretemperatura_do_mancal_la_do_gerador_contra_escora_2_trip_86h_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_da_vedação_do_eixo_da_turbina_trip_86h_= LeituraModbusBit('10.07 - Relé de Proteção - Sobretemperatura da Vedação do Eixo da Turbina (Trip 86H)', self.clp, REG_UG2_Alarme10, 7)
        x = self.relé_de_proteção_sobretemperatura_da_vedação_do_eixo_da_turbina_trip_86h_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_óleo_do_reservatório_da_uhlm_trip_86h_= LeituraModbusBit('10.08 - Relé de Proteção - Sobretemperatura do Óleo do Reservatório da UHLM (Trip 86H)', self.clp, REG_UG2_Alarme10, 8)
        x = self.relé_de_proteção_sobretemperatura_do_óleo_do_reservatório_da_uhlm_trip_86h_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sobretemperatura_do_óleo_na_saída_do_trocador_de_calor_da_uhlm_trip_86h_= LeituraModbusBit('10.09 - Relé de Proteção - Sobretemperatura do Óleo na Saída do Trocador de Calor da UHLM (Trip 86H)', self.clp, REG_UG2_Alarme10, 9)
        x = self.relé_de_proteção_sobretemperatura_do_óleo_na_saída_do_trocador_de_calor_da_uhlm_trip_86h_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.sobretemperatura_da_água_na_entrada_do_trocador_de_calor_da_uhlm_trip_86h_= LeituraModbusBit('10.10 - Sobretemperatura da Água na Entrada do Trocador de Calor da UHLM (Trip 86H)', self.clp, REG_UG2_Alarme10, 10)
        x = self.sobretemperatura_da_água_na_entrada_do_trocador_de_calor_da_uhlm_trip_86h_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.sobretemperatura_da_água_na_saída_do_trocador_de_calor_da_uhlm_trip_86h_= LeituraModbusBit('10.11 - Sobretemperatura da Água na Saída do Trocador de Calor da UHLM (Trip 86H)', self.clp, REG_UG2_Alarme10, 11)
        x = self.sobretemperatura_da_água_na_saída_do_trocador_de_calor_da_uhlm_trip_86h_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.sobretemperatura_do_óleo_do_reservatório_da_uhct_trip_86h_= LeituraModbusBit('10.12 - Sobretemperatura do Óleo do Reservatório da UHCT (Trip 86H)', self.clp, REG_UG2_Alarme10, 12)
        x = self.sobretemperatura_do_óleo_do_reservatório_da_uhct_trip_86h_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sel700g_proteção_diferencial_do_gerador_87g_= LeituraModbusBit('10.14 - Relé de Proteção SEL700G - Proteção Diferencial do Gerador (87G)', self.clp, REG_UG2_Alarme10, 14)
        x = self.relé_de_proteção_sel700g_proteção_diferencial_do_gerador_87g_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sel700g_sobrecorrente_instantânea_de_fase_50p_= LeituraModbusBit('10.15 - Relé de Proteção SEL700G - Sobrecorrente Instantânea de Fase (50P)', self.clp, REG_UG2_Alarme10, 15)
        x = self.relé_de_proteção_sel700g_sobrecorrente_instantânea_de_fase_50p_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sel700g_sobrecorrente_com_restrição_por_tensão_51v_= LeituraModbusBit('11.00 - Relé de Proteção SEL700G - Sobrecorrente com Restrição por Tensão (51V)', self.clp, REG_UG2_Alarme11, 0)
        x = self.relé_de_proteção_sel700g_sobrecorrente_com_restrição_por_tensão_51v_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sel700g_sobre_corrente_de_sequência_negativa_instantânea_50q_= LeituraModbusBit('11.03 - Relé de Proteção SEL700G - Sobre Corrente de Sequência Negativa Instantânea (50Q)', self.clp, REG_UG2_Alarme11, 3)
        x = self.relé_de_proteção_sel700g_sobre_corrente_de_sequência_negativa_instantânea_50q_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sel700g_desequilíbrio_de_corrente_46q_= LeituraModbusBit('11.04 - Relé de Proteção SEL700G - Desequilíbrio de Corrente (46Q)', self.clp, REG_UG2_Alarme11, 4)
        x = self.relé_de_proteção_sel700g_desequilíbrio_de_corrente_46q_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sel700g_sobretensão_de_sequência_negativa_59q_= LeituraModbusBit('11.05 - Relé de Proteção SEL700G - Sobretensão de Sequência Negativa (59Q)', self.clp, REG_UG2_Alarme11, 5)
        x = self.relé_de_proteção_sel700g_sobretensão_de_sequência_negativa_59q_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sel700g_sobre_corrente_instantânea_de_neutro_50n_= LeituraModbusBit('11.06 - Relé de Proteção SEL700G - Sobre Corrente Instantânea de Neutro (50N)', self.clp, REG_UG2_Alarme11, 6)
        x = self.relé_de_proteção_sel700g_sobre_corrente_instantânea_de_neutro_50n_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sel700g_sobre_corrente_temporizada_de_neutro_51n_= LeituraModbusBit('11.07 - Relé de Proteção SEL700G - Sobre Corrente Temporizada de Neutro (51N)', self.clp, REG_UG2_Alarme11, 7)
        x = self.relé_de_proteção_sel700g_sobre_corrente_temporizada_de_neutro_51n_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sel700g_sobretensão_residual_59g_= LeituraModbusBit('11.08 - Relé de Proteção SEL700G - Sobretensão Residual (59G)', self.clp, REG_UG2_Alarme11, 8)
        x = self.relé_de_proteção_sel700g_sobretensão_residual_59g_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sel700g_potência_reversa_32p_= LeituraModbusBit('11.09 - Relé de Proteção SEL700G - Potência Reversa (32P)', self.clp, REG_UG2_Alarme11, 9)
        x = self.relé_de_proteção_sel700g_potência_reversa_32p_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sel700g_energização_indevida_50m_= LeituraModbusBit('11.12 - Relé de Proteção SEL700G - Energização Indevida (50M)', self.clp, REG_UG2_Alarme11, 12)
        x = self.relé_de_proteção_sel700g_energização_indevida_50m_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.relé_de_proteção_sel700g_falha_do_disjuntor_52g_50_62bf_= LeituraModbusBit('11.15 - Relé de Proteção SEL700G - Falha do Disjuntor 52G (50_62BF)', self.clp, REG_UG2_Alarme11, 15)
        x = self.relé_de_proteção_sel700g_falha_do_disjuntor_52g_50_62bf_
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.grtd_2000_falha_sobrecorrente_de_excitação = LeituraModbusBit('12.04 - GRTD 2000 - Falha Sobrecorrente de Excitação', self.clp, REG_UG2_Alarme12, 4)
        x = self.grtd_2000_falha_sobrecorrente_de_excitação 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.erro_de_leitura_na_entrada_analógica_de_pressão_da_caixa_espiral = LeituraModbusBit('12.11 - Erro de Leitura na Entrada Analógica de Pressão da Caixa Espiral', self.clp, REG_UG2_Alarme12, 11)
        x = self.erro_de_leitura_na_entrada_analógica_de_pressão_da_caixa_espiral 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.css_u1_alimentação_motor_carregamento_mola_disjuntor_52g_disjuntor_q220_1_desligado = LeituraModbusBit('13.07 - CSS-U1 - Alimentação Motor Carregamento Mola Disjuntor 52G - Disjuntor Q220.1 Desligado', self.clp, REG_UG2_Alarme13, 7)
        x = self.css_u1_alimentação_motor_carregamento_mola_disjuntor_52g_disjuntor_q220_1_desligado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.q49_módulo_de_temperatura_sel2600_disjuntor_q125_0_desligado = LeituraModbusBit('13.14 - Q49 - Módulo de Temperatura SEL2600 - Disjuntor Q125.0 Desligado', self.clp, REG_UG2_Alarme13, 14)
        x = self.q49_módulo_de_temperatura_sel2600_disjuntor_q125_0_desligado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.trip_vibração_excessiva_no_mancal_la_do_gerador = LeituraModbusBit('15.01 - TRIP - Vibração Excessiva no Mancal LA do Gerador', self.clp, REG_UG2_Alarme15, 1)
        x = self.trip_vibração_excessiva_no_mancal_la_do_gerador 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))
        
        self.trip_vibração_excessiva_no_mancal_loa_do_gerador = LeituraModbusBit('15.03 - TRIP - Vibração Excessiva no Mancal LOA do Gerador', self.clp, REG_UG2_Alarme15, 3)
        x = self.trip_vibração_excessiva_no_mancal_loa_do_gerador 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.reg_tensão_trip = LeituraModbusBit('04.12 - Reg Tensão - TRIP', self.clp, REG_UG2_Alarme04, 12)
        x = self.reg_tensão_trip 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.grtd_2000_falha_no_sincronismo = LeituraModbusBit('05.04 - GRTD 2000 - Falha no Sincronismo', self.clp, REG_UG2_Alarme05, 4)
        x = self.grtd_2000_falha_no_sincronismo 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.relé_de_proteção_do_gerador_trip_atuado = LeituraModbusBit('06.00 - Relé de Proteção do Gerador - Trip Atuado', self.clp, REG_UG2_Alarme06, 00)
        x = self.relé_de_proteção_do_gerador_trip_atuado 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.relé_de_proteção_sel700g_subtensão_de_fase_27p = LeituraModbusBit('11.01 - Relé de Proteção SEL700G - Subtensão de Fase (27P)', self.clp, REG_UG2_Alarme11, 1)
        x = self.relé_de_proteção_sel700g_subtensão_de_fase_27p 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.relé_de_proteção_sel700g_sobretensão_de_fase_59p = LeituraModbusBit('11.02 - Relé de Proteção SEL700G - Sobretensão de Fase (59P)', self.clp, REG_UG2_Alarme11, 2)
        x = self.relé_de_proteção_sel700g_sobretensão_de_fase_59p 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.relé_de_proteção_sel700g_perda_de_excitação_40q = LeituraModbusBit('11.10 - Relé de Proteção SEL700G - Perda de Excitação (40Q)', self.clp, REG_UG2_Alarme11, 10)
        x = self.relé_de_proteção_sel700g_perda_de_excitação_40q 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.relé_de_proteção_sel700g_volts_hertz_24 = LeituraModbusBit('11.11 - Relé de Proteção SEL700G - Volts/Hertz -24', self.clp, REG_UG2_Alarme11, 11)
        x = self.relé_de_proteção_sel700g_volts_hertz_24
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.relé_de_proteção_sel700g_subfrequência_81u = LeituraModbusBit('11.13 - Relé de Proteção SEL700G - Subfrequência (81U)', self.clp, REG_UG2_Alarme11, 13)
        x = self.relé_de_proteção_sel700g_subfrequência_81u 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.relé_de_proteção_sel700g_sobrefrequência_81o = LeituraModbusBit('11.14 - Relé de Proteção SEL700G - Sobrefrequência (81O)', self.clp, REG_UG2_Alarme11, 14)
        x = self.relé_de_proteção_sel700g_sobrefrequência_81o
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.grtd_2000_falha_na_ponte_de_excitação = LeituraModbusBit('12.00 - GRTD 2000 - Falha na Ponte de Excitação', self.clp, REG_UG2_Alarme12, 00)
        x = self.grtd_2000_falha_na_ponte_de_excitação 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.grtd_2000_falha_na_saída_analógica_do_distribuidor = LeituraModbusBit('12.01 - GRTD 2000 - Falha na Saída Analógica do Distribuidor', self.clp, REG_UG2_Alarme12, 1)
        x = self.grtd_2000_falha_na_saída_analógica_do_distribuidor 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.grtd_2000_falha_realimentação_de_tensão = LeituraModbusBit('12.02 - GRTD 2000 - Falha Realimentação de Tensão', self.clp, REG_UG2_Alarme12, 2)
        x = self.grtd_2000_falha_realimentação_de_tensão 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.grtd_2000_falha_sobretensão_de_excitação = LeituraModbusBit('12.03 - GRTD 2000 - Falha Sobretensão de Excitação', self.clp, REG_UG2_Alarme12, 3)
        x = self.grtd_2000_falha_sobretensão_de_excitação 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.grtd_2000_falha_sobrevelocidade_eletrônica = LeituraModbusBit('12.05 - GRTD 2000 - Falha Sobrevelocidade Eletrônica', self.clp, REG_UG2_Alarme12, 5)
        x = self.grtd_2000_falha_sobrevelocidade_eletrônica 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.grtd_2000_falha_na_realimentação_de_velocidade = LeituraModbusBit('12.06 - GRTD 2000 - Falha na Realimentação de velocidade', self.clp, REG_UG2_Alarme12, 6)
        x = self.grtd_2000_falha_na_realimentação_de_velocidade 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))
        
        self.grtd_2000_falha_na_realimentação_de_posição_do_distribuidor = LeituraModbusBit('12.07 - GRTD 2000 - Falha na Realimentação de posição do Distribuidor', self.clp, REG_UG2_Alarme12, 7)
        x = self.grtd_2000_falha_na_realimentação_de_posição_do_distribuidor 
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_potencia = LeituraModbus(
            "ug{}_Gerador_PotenciaAtivaMedia".format(self.id),
            self.clp,
            REG_UG2_Gerador_PotenciaAtivaMedia,
        )

        self.leitura_horimetro = LeituraModbus(
            "ug{}_HorimetroEletrico_Low".format(self.id),
            self.clp,
            REG_UG2_HorimetroEletrico_Low,
        )

        self.leitura_Operacao_EtapaAtual = LeituraModbus(
            "ug{}_Operacao_EtapaAtual".format(self.id),
            self.clp,
            REG_UG2_Operacao_EtapaAtual,
        )

        self.leitura_Operacao_EtapaAlvo = LeituraModbus(
            "ug{}_Operacao_EtapaAlvo".format(self.id),
            self.clp,
            REG_UG2_Operacao_EtapaAlvo,
        )

        # Gerador - Enrolamento fase R
        self.leitura_temperatura_enrolamento_fase_r = LeituraModbus(
            "Gerador {} - Enrolamento fase R".format(self.id),
            self.clp,
            REG_UG2_Temperatura_01,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_enrolamento_fase_r
        self.condicionador_temperatura_enrolamento_fase_r = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_enrolamento_fase_r)

        # Gerador - Enrolamento Fase S
        self.leitura_temperatura_enrolamento_fase_s = LeituraModbus(
            "Gerador {} - Enrolamento Fase S".format(self.id),
            self.clp,
            REG_UG2_Temperatura_02,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_enrolamento_fase_s
        self.condicionador_temperatura_enrolamento_fase_s = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_enrolamento_fase_s)

        # Gerador - Enrolamento fase T
        self.leitura_temperatura_enrolamento_fase_t = LeituraModbus(
            "Gerador {} - Enrolamento fase T".format(self.id),
            self.clp,
            REG_UG2_Temperatura_03,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_enrolamento_fase_t
        self.condicionador_temperatura_enrolamento_fase_t = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_enrolamento_fase_t)

        # Gerador - Mancal L.A. Escora 01
        self.leitura_temperatura_mancal_la_escora_1 = LeituraModbus(
            "Gerador {} - Mancal L.A. Escora 01".format(self.id),
            self.clp,
            REG_UG2_Temperatura_04,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_la_escora_1
        self.condicionador_temperatura_mancal_la_escora_1 = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_mancal_la_escora_1)

        # Gerador - Mancal L.A. Escora 02
        self.leitura_temperatura_mancal_la_escora_2 = LeituraModbus(
            "Gerador {} - Mancal L.A. Escora 02".format(self.id),
            self.clp,
            REG_UG2_Temperatura_05,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_la_escora_2
        self.condicionador_temperatura_mancal_la_escora_2 = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_mancal_la_escora_2)

        # Gerador - Mancal L. A. Contra Escora 01
        self.leitura_temperatura_mancal_la_contra_escora_1 = LeituraModbus(
            "Gerador {} - Mancal L. A. Contra Escora 01".format(self.id),
            self.clp,
            REG_UG2_Temperatura_07,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_la_contra_escora_1
        self.condicionador_temperatura_mancal_la_contra_escora_1 = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_mancal_la_contra_escora_1)

        # Gerador - Mancal L. A. Contra Escora 02
        self.leitura_temperatura_mancal_la_contra_escora_2 = LeituraModbus(
            "Gerador {} - Mancal L. A. Contra Escora 02".format(self.id),
            self.clp,
            REG_UG2_Temperatura_09,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_la_contra_escora_2
        self.condicionador_temperatura_mancal_la_contra_escora_2 = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_mancal_la_contra_escora_2)

        # Gerador - Mancal L. A. Casquilho
        self.leitura_temperatura_mancal_la_casquilho = LeituraModbus(
            "Gerador {} - Mancal L. A. Casquilho".format(self.id),
            self.clp,
            REG_UG2_Temperatura_06,
        )
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_la_casquilho
        self.condicionador_temperatura_mancal_la_casquilho = CondicionadorExponencial(x.descr, DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores.append(self.condicionador_temperatura_mancal_la_casquilho)

        # Gerador - Mancal L.N.A. Casquilho
        self.leitura_temperatura_mancal_lna_casquilho = LeituraModbus(
            "Gerador {} - Mancal L.N.A. Casquilho".format(self.id),
            self.clp,
            REG_UG2_Temperatura_08,
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

        

        self.condicionador_86h_e_86m_e_nao_temperaturas = CondicionadorCombinadoAND(
            "condicionador_86h_e_86m_e_nao_temperaturas",
            DEVE_SUPER_NORMALIZAR,
            [
                [True, CondicionadorBase(self.relé_de_bloqueio_86m_trip_atuado.descr, DEVE_INDISPONIBILIZAR, self.relé_de_bloqueio_86m_trip_atuado)],
                [True, CondicionadorBase(self.relé_de_bloqueio_86h_trip_atuado.descr, DEVE_NORMALIZAR, self.relé_de_bloqueio_86h_trip_atuado)],
                [False, self.condicionador_temperatura_enrolamento_fase_r],
                [False, self.condicionador_temperatura_enrolamento_fase_s],
                [False, self.condicionador_temperatura_enrolamento_fase_t],
                [False, self.condicionador_temperatura_mancal_la_escora_1],
                [False, self.condicionador_temperatura_mancal_la_escora_2],
                [False, self.condicionador_temperatura_mancal_la_contra_escora_1],
                [False, self.condicionador_temperatura_mancal_la_contra_escora_2],
                [False, self.condicionador_temperatura_mancal_la_casquilho],
                [False, self.condicionador_temperatura_mancal_lna_casquilho],
            ]        
        )

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
                REG_UG2_Operacao_EmergenciaLigar, 1
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
                REG_UG2_Operacao_EmergenciaLigar, 0
            )
            response = self.clp.write_single_register(
                REG_UG2_Operacao_EmergenciaDesligar, 1
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
            self.enviar_trip_eletrico = True
            self.logger.debug(
                "[UG{}] Acionando sinal (elétrico) de TRIP.".format(self.id)
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_BLOCK_UG{}".format(self.id)],
                [1],
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
            self.enviar_trip_eletrico = False
            self.logger.debug(
                "[UG{}] Removendo sinal (elétrico) de TRIP.".format(self.id)
            )
            DataBank.set_words(
                self.cfg["REG_MOA_OUT_BLOCK_UG{}".format(self.id)],
                [0],
            )
            DataBank.set_words(
                self.cfg['REG_PAINEL_LIDO'],
                [0],
            )
        except Exception as e:
            self.logger.warning("Exception! Traceback: {}".format(traceback.format_exc()))
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
            if not self.etapa_alvo == UNIDADE_SINCRONIZADA:
                self.logger.info(
                    "[UG{}] Enviando comando (via rede) de partida.".format(self.id)
                )
            else:
                self.logger.debug(
                    "[UG{}] Enviando comando (via rede) de partida.".format(self.id)
                ) 
            response = self.clp.write_single_register(REG_UG2_Operacao_US, 1)
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
            if not self.etapa_alvo == UNIDADE_PARADA:
                self.logger.info(
                    "[UG{}] Enviando comando (via rede) de parada.".format(self.id)
                )
            else:
                self.logger.debug(
                    "[UG{}] Enviando comando (via rede) de parada.".format(self.id)
                ) 
            response = self.clp.write_single_register(REG_UG2_Operacao_UP, 1)
            self.enviar_setpoint(0)
            response = self.clp.write_single_register(REG_UG2_Operacao_UP, 1)

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
                "[UG{}] Enviando comando de reconhece e reset alarmes. (Vai tomar aprox 10s)".format(self.id)
            )

            for _ in range(3):
                DataBank.set_words(self.cfg['REG_PAINEL_LIDO'],[0])
                self.remover_trip_eletrico()
                DataBank.set_words(self.cfg['REG_PAINEL_LIDO'],[0])
                sleep(1)
                self.remover_trip_logico()
                response = self.clp.write_single_register(
                    REG_UG2_Operacao_PCH_CovoReconheceAlarmes, 1
                )
                sleep(1)
                response = response and self.clp.write_single_register(
                    REG_UG2_Operacao_PCH_CovoResetAlarmes, 1
                )
                DataBank.set_words(self.cfg['REG_PAINEL_LIDO'],[0])
                sleep(1)

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
        
            self.setpoint_minimo = self.cfg["pot_minima"]
            self.setpoint_maximo = self.cfg["pot_maxima_ug{}".format(self.id)]

            self.setpoint = int(setpoint_kw)
            self.logger.debug(
                "[UG{}] Enviando setpoint {} kW.".format(self.id, int(self.setpoint))
            )
            if self.setpoint > 1:
                response = self.clp.write_single_register(REG_UG2_Operacao_US, 1)
            response = response and self.clp.write_single_register(
                REG_UG2_RegV_ColocarCarga, 1
            )
            response = response and self.clp.write_single_register(
                REG_UG2_CtrlPotencia_ModoNivelDesligar, 1
            )
            response = response and self.clp.write_single_register(
                REG_UG2_CtrlPotencia_ModoPotenciaDesligar, 1
            )
            response = response and self.clp.write_single_register(
                REG_UG2_CtrlPotencia_Alvo, int(self.setpoint)
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
            
            if response > 0 and response < 255:
                self.__last_EtapaAlvo = response
            else:
                self.__last_EtapaAlvo = self.etapa_atual

            return self.__last_EtapaAlvo
            
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    @property
    def etapa_atual(self) -> int:
        try:
            response = self.leitura_Operacao_EtapaAtual.valor
            if response > 0:
                self.__last_EtapaAtual = response
                return response
            else:
                return self.__last_EtapaAtual
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response

    def modbus_update_state_register(self):
        DataBank.set_words(
                    self.cfg["REG_MOA_OUT_STATE_UG{}".format(self.id)],
                    [self.etapa_atual],
                )