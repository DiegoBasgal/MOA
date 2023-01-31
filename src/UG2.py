import VAR_REG

from src.Escrita import *
from src.Leituras import *
from src.Condicionadores import *
from src.Unidade_Geracao import *
from src.Conector import Database, FieldConnector

from opcua import Client
from pyModbusTCP.server import DataBank

class UnidadeDeGeracao2(UnidadeDeGeracao):
    def __init__(self, id, cfg=None, leituras_usina=None):
        super().__init__(id)

        if not cfg or not leituras_usina:
            raise ValueError
        else:
            self.cfg = cfg
            self.leituras_usina = leituras_usina

        REG_OPC = VAR_REG.REG_OPC
        REG_MB["UG"] = VAR_REG.REG_MB["UG"]

        self.db = Database()

        self.con = FieldConnector(self.cfg)
        
        self.modo_autonomo = 1
        self.__last_EtapaAtual = 0
        self.__last_EtapaAlvo = -1

        self.QCAUGRemoto = True
        self.acionar_voip = False
        self.limpeza_grade = False
        self.TDA_FalhaComum = False
        self.FreioCmdRemoto = True
        self.avisou_emerg_voip = False
        self.enviar_trip_eletrico = False

        self.setpoint_minimo = self.cfg["pot_minima"]
        self.setpoint_maximo = self.cfg["pot_maxima_ug{}".format(self.id)]

        self.client = Client(self.cfg["client"])
        self.clp = ModbusClient(
            host=self.cfg["UG2_slave_ip"],
            port=self.cfg["UG2_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )

        self.leitura_potencia = LeituraOPC(self.client,REG_OPC["UG"]["UG2_UG_P"])

        self.leitura_horimetro_hora = LeituraOPC(self.client, REG_OPC["UG"]["UG2_UG_HORIMETRO"])

        self.leitura_Status_Comporta = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP2_COMPORTA_OPERANDO"], 0)

        self.leitura_Permissao_Abrir_Comporta = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP2_PERMISSIVOS_OK"], 31)

        self.leitura_Operacao_EtapaAtual = LeituraModbus(self.clp, REG_MB["UG"]["UG2_RV_ESTADO_OPERACAO"])
        
        self.leitura_potencia_ug1 = LeituraOPC(self.client, REG_OPC["UG"]["UG1_UG_P"])

        self.leitura_setpoint_ug1 = LeituraModbus(self.clp, REG_MB["UG"]["UG1_RV_SETPOINT_POTENCIA_ATIVA_PU"])

        # Simulador
        self.condic_ativos_sim_ug2 = LeituraOPC(self.client, REG_OPC["UG"]["REG_UG2_RetrornosAnalogicos_AUX_Condicionadores"])


        # Temperaturas
        # R
        self.leitura_temperatura_fase_R = LeituraOPC(self.client, REG_OPC["UG"]["UG2_TEMP_GERADOR_FASE_A"])
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_R
        self.condicionador_temperatura_fase_r_ug = CondicionadorExponencial("UG2_TEMP_GERADOR_FASE_A", DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_r_ug)

        # S
        self.leitura_temperatura_fase_S = LeituraOPC(self.client, REG_OPC["UG"]["UG2_TEMP_GERADOR_FASE_B"])
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_S
        self.condicionador_temperatura_fase_s_ug = CondicionadorExponencial("UG2_TEMP_GERADOR_FASE_B", DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_s_ug)
        
        # T
        self.leitura_temperatura_fase_T = LeituraOPC(self.client, REG_OPC["UG"]["UG2_TEMP_GERADOR_FASE_C"])
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_T
        self.condicionador_temperatura_fase_t_ug = CondicionadorExponencial("UG2_TEMP_GERADOR_FASE_C", DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_t_ug)
        
        # Nucleo Gerador 1
        self.leitura_temperatura_nucleo_gerador_1 = LeituraOPC(self.client, REG_OPC["UG"]["UG2_TEMP_GERADOR_NUCLEO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_nucleo_gerador_1
        self.condicionador_temperatura_nucleo_gerador_1_ug = CondicionadorExponencial("UG2_TEMP_GERADOR_NUCLEO", DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_gerador_1_ug)

        # Mancal Guia
        self.leitura_temperatura_mancal_guia = LeituraOPC(self.client, REG_OPC["UG"]["UG2_TEMP_MANCAL_GUIA_GERADOR"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_guia
        self.condicionador_temperatura_mancal_guia_ug = CondicionadorExponencial("UG2_TEMP_MANCAL_GUIA_GERADOR", DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_ug)

        # Mancal Guia Interno 1
        self.leitura_temperatura_mancal_guia_interno_1 = LeituraOPC(self.client, REG_OPC["UG"]["UG2_TEMP_1_MANCAL_GUIA_INTERNO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_guia_interno_1
        self.condicionador_temperatura_mancal_guia_interno_1_ug = CondicionadorExponencial("UG2_TEMP_1_MANCAL_GUIA_INTERNO", DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_interno_1_ug)
        
        # Mancal Guia Interno 2
        self.leitura_temperatura_mancal_guia_interno_2 = LeituraOPC(self.client, REG_OPC["UG"]["UG2_TEMP_2_MANCAL_GUIA_INTERNO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_guia_interno_2
        self.condicionador_temperatura_mancal_guia_interno_2_ug = CondicionadorExponencial("UG2_TEMP_2_MANCAL_GUIA_INTERNO", DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_interno_2_ug)
        
        # Patins Mancal Combinado 1
        self.leitura_temperatura_patins_mancal_comb_1 = LeituraOPC(self.client, REG_OPC["UG"]["UG2_TEMP_1_PATINS_MANCAL_COMBINADO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_patins_mancal_comb_1
        self.condicionador_temperatura_patins_mancal_comb_1_ug = CondicionadorExponencial("UG2_TEMP_1_PATINS_MANCAL_COMBINADO", DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_patins_mancal_comb_1_ug)
        
        # Patins Mancal Combinado 2
        self.leitura_temperatura_patins_mancal_comb_2 = LeituraOPC(self.client, REG_OPC["UG"]["UG2_TEMP_2_PATINS_MANCAL_COMBINADO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_patins_mancal_comb_2
        self.condicionador_temperatura_patins_mancal_comb_2_ug = CondicionadorExponencial("UG2_TEMP_2_PATINS_MANCAL_COMBINADO", DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_patins_mancal_comb_2_ug)
        
        # Mancal Casquilho Combinado
        self.leitura_temperatura_mancal_casq_comb = LeituraOPC(self.client, REG_OPC["UG"]["UG2_TEMP_CASQ_MANCAL_COMBINADO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_casq_comb
        self.condicionador_temperatura_mancal_casq_comb_ug = CondicionadorExponencial("UG2_TEMP_CASQ_MANCAL_COMBINADO", DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_casq_comb_ug)

        # Mancal Contra Escora Combinado
        self.leitura_temperatura_mancal_contra_esc_comb = LeituraOPC(self.client, REG_OPC["UG"]["UG2_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_contra_esc_comb
        self.condicionador_temperatura_mancal_contra_esc_comb_ug = CondicionadorExponencial("UG2_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO", DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_contra_esc_comb_ug)
        
        # Pressão Entrada Turbina
        self.leitura_pressao_turbina = LeituraOPC(self.client, REG_OPC["UG"]["UG2_PRESSAO_ENTRADA_TURBINA"], escala=0.1)
        base = 16.1
        limite = 15.5
        x = self.leitura_pressao_turbina
        self.condicionador_pressao_turbina_ug = CondicionadorExponencialReverso("UG2_PRESSAO_ENTRADA_TURBINA", DEVE_INDISPONIBILIZAR, x, base, limite)
        if self.leitura_pressao_turbina.valor != 0.0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            self.condicionadores_atenuadores.append(self.condicionador_pressao_turbina_ug)


        # Essenciais
        self.leitura_saidas_digitiais_rv_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_SAIDAS_DIGITAIS"], 0, True)
        x = self.leitura_alarme_1_rt_b0
        self.condicionadores_essenciais.append(CondicionadorBase("UG2_RV_SAIDAS_DIGITAIS - bit 00", DEVE_NORMALIZAR, x))

        self.leitura_falha_2_rv_b3 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_2"], 3)
        x = self.leitura_falha_2_rv_b3
        self.condicionadores_essenciais.append(CondicionadorBase("UG2_RV_FALHA_2 - bit 03", DEVE_NORMALIZAR, x))

        self.leitura_saidas_digitais_rt_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_SAIDAS_DIGITAIS"], 0, True)
        x = self.leitura_saidas_digitais_rt_b0
        self.condicionadores_essenciais.aapend(CondicionadorBase("UG2_RT_SAIDAS_DIGITAIS - bit 00", DEVE_NORMALIZAR, x))
    
        self.leitura_trip_rele700G_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RELE_700G_TRIP_ATUADO"], 31)
        x = self.leitura_trip_rele700G_atuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG2_RELE_700G_TRIP_ATUADO - bit 31", DEVE_NORMALIZAR, x))

        self.leitura_rele_bloq_86EH_desatuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RELE_BLOQUEIO_86EH_DESATUADO"], 28, True)
        x = self.leitura_rele_bloq_86EH_desatuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG2_RELE_BLOQUEIO_86EH_DESATUADO - bit 28", DEVE_NORMALIZAR, x))

        self.leitura_trip_rele_rv_naoatuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RV_RELE_TRIP_NAO_ATUADO"], 14, True)
        x = self.leitura_trip_rele_rv_naoatuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG2_RV_RELE_TRIP_NAO_ATUADO - bit 14", DEVE_NORMALIZAR, x))
        
        self.leitura_trip_rele_rt_naoatuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RT_RELE_TRIP_NAO_ATUADO"], 23, True)
        x = self.leitura_trip_rele_rt_naoatuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG2_RT_RELE_TRIP_NAO_ATUADO - bit 23", DEVE_NORMALIZAR, x))

        self.leitura_bt_emerg_naoatuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_BT_EMERGENCIA_NAO_ATUADO"], 11, True)
        x = self.leitura_bt_emerg_naoatuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG2_BT_EMERGENCIA_NAO_ATUADO - bit 11", DEVE_NORMALIZAR, x))

        self.leitura_clp_geral_sem_bloq_exter = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_CLP_GERAL_SEM_BLOQUEIO_EXTERNO"], 1, True)
        x = self.leitura_clp_geral_sem_bloq_exter
        self.condicionadores_essenciais.append(CondicionadorBase("UG2_CLP_GERAL_SEM_BLOQUEIO_EXTERNO - bit 1", DEVE_NORMALIZAR, x))

        self.leitura_bloq_86M_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_BLOQUEIO_86M_ATUADO"], 31)
        x = self.leitura_bloq_86M_atuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG2_BLOQUEIO_86M_ATUADO - bit 31", DEVE_NORMALIZAR, x))
        
        self.leitura_bloq_86E_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_BLOQUEIO_86E_ATUADO"], 31)
        x = self.leitura_bloq_86E_atuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG2_BLOQUEIO_86E_ATUADO - bit 31", DEVE_NORMALIZAR, x))
        
        self.leitura_bloq_86H_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_BLOQUEIO_86H_ATUADO"], 31)
        x = self.leitura_bloq_86H_atuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG2_BLOQUEIO_86H_ATUADO - bit 31", DEVE_NORMALIZAR, x))


        # Gerais
        self.leitura_falha_1_rv_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 0)
        x = self.leitura_falha_1_rv_b0
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_1 - bit 00", DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b1 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 1)
        x = self.leitura_falha_1_rv_b1
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_1 - bit 01", DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b2 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 2)
        x = self.leitura_falha_1_rv_b2
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_1 - bit 02", DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b3 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 3)
        x = self.leitura_falha_1_rv_b3
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_1 - bit 03", DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b4 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 4)
        x = self.leitura_falha_1_rv_b4
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_1 - bit 04", DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b5 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 5)
        x = self.leitura_falha_1_rv_b5
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_1 - bit 05", DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b10 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 10)
        x = self.leitura_falha_1_rv_b10
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_1 - bit 10", DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b11 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 11)
        x = self.leitura_falha_1_rv_b11
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_1 - bit 11", DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b12 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 12)
        x = self.leitura_falha_1_rv_b12
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_1 - bit 12", DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b13 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 13)
        x = self.leitura_falha_1_rv_b13
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_1 - bit 13", DEVE_NORMALIZAR, x))
        
        self.leitura_alarme_1_rt_b8 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_ALARMES_1"], 8)
        x = self.leitura_alarme_1_rt_b8
        self.condicionadores.append(CondicionadorBase("UG2_RT_ALARMES_1 - bit 08", DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rt_b1 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 1)
        x = self.leitura_falha_1_rt_b1
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 01", DEVE_NORMALIZAR, x))
        
        self.leitura_falha_1_rt_b2 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 2)
        x = self.leitura_falha_1_rt_b2
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 02", DEVE_NORMALIZAR, x))
        
        self.leitura_falha_1_rt_b3 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 3)
        x = self.leitura_falha_1_rt_b3
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 03", DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b2 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_2"], 2)
        x = self.leitura_falha_2_rt_b2
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_2 - bit 02", DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b5 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_2"], 5)
        x = self.leitura_falha_2_rt_b5
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_2 - bit 05", DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b6 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_2"], 6)
        x = self.leitura_falha_2_rt_b6
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_2 - bit 06", DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b7 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_2"], 7)
        x = self.leitura_falha_2_rt_b7
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_2 - bit 07", DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b10 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_2"], 10)
        x = self.leitura_falha_2_rt_b10
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_2 - bit 10", DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b11 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_2"], 11)
        x = self.leitura_falha_2_rt_b11
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_2 - bit 11", DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b12 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_2"], 12)
        x = self.leitura_falha_2_rt_b12
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_2 - bit 12", DEVE_NORMALIZAR, x))
        
        self.leitura_falha_bomba_1_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_UHRV_BOMBA_1_FALHA"], 0)
        x = self.leitura_falha_bomba_1_uhrv
        self.condicionadores.append(CondicionadorBase("UG2_UHRV_BOMBA_1_FALHA - bit 00", DEVE_NORMALIZAR, x))
        
        self.leitura_falha_bomba_2_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_UHRV_BOMBA_2_FALHA"], 2)
        x = self.leitura_falha_bomba_2_uhrv
        self.condicionadores.append(CondicionadorBase("UG2_UHRV_BOMBA_2_FALHA - bit 02", DEVE_NORMALIZAR, x))

        self.leitura_falha_bomba_1_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_UHLM_BOMBA_1_FALHA"], 4)
        x = self.leitura_falha_bomba_1_uhlm
        self.condicionadores.append(CondicionadorBase("UG2_UHLM_BOMBA_1_FALHA - bit 04", DEVE_NORMALIZAR, x))

        self.leitura_falha_bomba_2_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_UHLM_BOMBA_2_FALHA"], 6)
        x = self.leitura_falha_bomba_2_uhlm
        self.condicionadores.append(CondicionadorBase("UG2_UHLM_BOMBA_2_FALHA - bit 06", DEVE_NORMALIZAR, x))
       
        self.leitura_alarme_rele_rv_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RV_RELE_ALARME_ATUADO"], 15)
        x = self.leitura_alarme_rele_rv_atuado
        self.condicionadores.append(CondicionadorBase("UG2_RV_RELE_ALARME_ATUADO - bit 15", DEVE_NORMALIZAR, 15))

        self.leitura_sistema_agua_clp_geral_ok = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_CLP_GERAL_SISTEMA_AGUA_OK"], 2, True)
        x = self.leitura_sistema_agua_clp_geral_ok
        self.condicionadores.append(CondicionadorBase("UG2_CLP_GERAL_SISTEMA_AGUA_OK - bit 02", DEVE_NORMALIZAR, x))

        self.leitura_clp_geral_com_tens_barra_essenc = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_CLP_GERAL_COM_TENSAO_BARRA_ESSENCIAIS"], 3, True)
        x = self.leitura_clp_geral_com_tens_barra_essenc
        self.condicionadores.append(CondicionadorBase("UG2_CLP_GERAL_COM_TENSAO_BARRA_ESSENCIAIS - bit 03", DEVE_NORMALIZAR, x))

        self.leitura_disparo_mecanico_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_DISPARO_MECANICO_ATUADO"], 9)
        x = self.leitura_disparo_mecanico_atuado
        self.condicionadores.append(CondicionadorBase("UG2_DISPARO_MECANICO_ATUADO - bit 09", DEVE_NORMALIZAR, x))

        self.leitura_disparo_mecanico_desatuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_DISPARO_MECANICO_DESATUADO"], 8, True)
        x = self.leitura_disparo_mecanico_desatuado
        self.condicionadores.append(CondicionadorBase("UG2_DISPARO_MECANICO_DESATUADO - bit 08", DEVE_NORMALIZAR, x))

        self.leitura_falha_habilitar_sistema_agua = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_HABILITAR_SISTEMA_AGUA"], 11)
        x = self.leitura_falha_habilitar_sistema_agua
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_HABILITAR_SISTEMA_AGUA - bit 11", DEVE_NORMALIZAR, x))

        self.leitura_trip_temp_oleo_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_OLEO_UHLM"], 4)
        x = self.leitura_trip_temp_oleo_uhlm
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_OLEO_UHLM - bit 04", DEVE_NORMALIZAR, x))

        self.leitura_trip_temp_oleo_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_OLEO_UHRV"], 5)
        x = self.leitura_trip_temp_oleo_uhrv
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_OLEO_UHRV - bit 05", DEVE_NORMALIZAR, x))

        self.leitura_parada_bloq_abertura_disj = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_PARADA_BLOQUEIO_ABERTURA_DISJUNTOR"], 11)
        x = self.leitura_parada_bloq_abertura_disj
        self.condicionadores.append(CondicionadorBase("UG2_PARADA_BLOQUEIO_ABERTURA_DISJUNTOR - bit 11", DEVE_NORMALIZAR, x))

        self.leitura_parada_bloq_descarga_pot = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_PARADA_BLOQUEIO_DESCARGA_POTENCIA"], 10)
        x = self.leitura_parada_bloq_descarga_pot
        self.condicionadores.append(CondicionadorBase("UG2_PARADA_BLOQUEIO_DESCARGA_POTENCIA - bit 10", DEVE_NORMALIZAR, x))

        self.leitura_falha_pressao_linha_b1_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_UHLM_FALHA_PRESSAO_LINHA_B1"], 9)
        x = self.leitura_falha_pressao_linha_b1_uhlm
        self.condicionadores.append(CondicionadorBase("UG2_UHLM_FALHA_PRESSAO_LINHA_B1 - bit 09", DEVE_NORMALIZAR, x))

        self.leitura_falha_pressao_linha_b2_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_UHLM_FALHA_PRESSAO_LINHA_B2"], 10)
        x = self.leitura_falha_pressao_linha_b2_uhlm
        self.condicionadores.append(CondicionadorBase("UG2_UHLM_FALHA_PRESSAO_LINHA_B2 - bit 10", DEVE_NORMALIZAR, x))

        self.leitura_falha_pressostato_linha_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_UHLM_FALHA_PRESSOSTATO_LINHA"], 11)
        x = self.leitura_falha_pressostato_linha_uhlm
        self.condicionadores.append(CondicionadorBase("UG2_UHLM_FALHA_PRESSOSTATO_LINHA - bit 11", DEVE_NORMALIZAR, x))

        self.leitura_falha_habilitar_rv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RV_FALHA_HABILITAR_RV"], 0)
        x = self.leitura_falha_habilitar_rv
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_HABILITAR_RV - bit 00", DEVE_NORMALIZAR, x))

        self.leitura_falha_partir_rv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RV_FALHA_PARTIR_RV"], 1)
        x = self.leitura_falha_partir_rv
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_PARTIR_RV - bit 01", DEVE_NORMALIZAR, x))

        self.leitura_falha_desabilitar_rv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RV_FALHA_DESABILITAR_RV"], 2)
        x = self.leitura_falha_desabilitar_rv
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_DESABILITAR_RV - bit 02", DEVE_NORMALIZAR, x))

        self.leitura_falha_habilitar_rt = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RT_FALHA_HABILITAR"], 16)
        x = self.leitura_falha_habilitar_rt
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHA_HABILITAR - bit 16", DEVE_NORMALIZAR, x))

        self.leitura_falha_partir_rt = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RT_FALHA_PARTIR"], 17)
        x = self.leitura_falha_partir_rt
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHA_PARTIR - bit 17", DEVE_NORMALIZAR, x))


        self.leitura_alarme_1_rt_b0 = LeituraModbusBit(self.clp, REG_OPC["UG"]["UG2_RT_ALARMES_1"], 0)
        x = self.leitura_alarme_1_rt_b0
        self.condicionadores.append(CondicionadorBase("UG2_RT_ALARMES_1 - bit 00", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_alarme_1_rt_b4 = LeituraModbusBit(self.clp, REG_OPC["UG"]["UG2_RT_ALARMES_1"], 4)
        x = self.leitura_alarme_1_rt_b4
        self.condicionadores.append(CondicionadorBase("UG2_RT_ALARMES_1 - bit 04", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_alarme_1_rt_b5 = LeituraModbusBit(self.clp, REG_OPC["UG"]["UG2_RT_ALARMES_1"], 5)
        x = self.leitura_alarme_1_rt_b5
        self.condicionadores.append(CondicionadorBase("UG2_RT_ALARMES_1 - bit 05", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 0)
        x = self.leitura_falha_1_rt_b0
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 00", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b4 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 4)
        x = self.leitura_falha_1_rt_b4
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 04", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b5 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 5)
        x = self.leitura_falha_1_rt_b5
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 05", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b6 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 6)
        x = self.leitura_falha_1_rt_b6
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 06", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b7 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 7)
        x = self.leitura_falha_1_rt_b7
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 07", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b8 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 8)
        x = self.leitura_falha_1_rt_b8
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 08", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b9 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 9)
        x = self.leitura_falha_1_rt_b9
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 09", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b10 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 10)
        x = self.leitura_falha_1_rt_b10
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 10", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b11 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 11)
        x = self.leitura_falha_1_rt_b11
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 11", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b12 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 12)
        x = self.leitura_falha_1_rt_b12
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 12", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b13 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 13)
        x = self.leitura_falha_1_rt_b13
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 13", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b14 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 14)
        x = self.leitura_falha_1_rt_b14
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 14", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b15 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_1"], 15)
        x = self.leitura_falha_1_rt_b15
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHAS_1 - bit 15", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rt_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHAS_2"], 0)
        x = self.leitura_falha_2_rt_b0
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHAS_2 - bit 00", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rt_b1 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHAS_2"], 1)
        x = self.leitura_falha_2_rt_b1
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHAS_2 - bit 01", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rt_b3 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHAS_2"], 3)
        x = self.leitura_falha_2_rt_b3
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHAS_2 - bit 03", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rt_b4 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHAS_2"], 4)
        x = self.leitura_falha_2_rt_b4
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHAS_2 - bit 04", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rt_b8 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHAS_2"], 8)
        x = self.leitura_falha_2_rt_b8
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHAS_2 - bit 08", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rt_b9 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHAS_2"], 9)
        x = self.leitura_falha_2_rt_b9
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHAS_2 - bit 09", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rv_b1 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_2"], 1)
        x = self.leitura_falha_2_rv_b1
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_2 - bit 01", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rv_b2 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_2"], 2)
        x = self.leitura_falha_2_rv_b2
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_2 - bit 02", DEVE_INDISPONIBILIZAR, x))

        self.leitura_rele_700G_bf_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RELE_700G_BF_ATUADO"], 0)
        x = self.leitura_rele_700G_bf_atuado
        self.condicionadores.append(CondicionadorBase("UG2_RELE_700G_BF_ATUADO - bit 00", DEVE_INDISPONIBILIZAR, x))

        self.leitura_sup_tensao_125vcc = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_SUPERVISAO_TENSAO_125VCC"], 29, True)
        x = self.leitura_sup_tensao_125vcc
        self.condicionadores.append(CondicionadorBase("UG2_SUPERVISAO_TENSAO_125VCC - bit 29", DEVE_INDISPONIBILIZAR, x))

        self.leitura_sup_tensao_24vcc = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_SUPERVISAO_TENSAO_24VCC"], 30, True)
        x = self.leitura_sup_tensao_24vcc
        self.condicionadores.append(CondicionadorBase("UG2_SUPERVISAO_TENSAO_24VCC - bit 30", DEVE_INDISPONIBILIZAR, x))

        self.leitura_sup_bobina_52g = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_SUPERVISAO_BOBINA_52G"], 12, True)
        x = self.leitura_sup_bobina_52g
        self.condicionadores.append(CondicionadorBase("UG2_SUPERVISAO_BOBINA_52G - bit 12", DEVE_INDISPONIBILIZAR, x))

        self.leitura_sup_bobina_86eh = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_SUPERVISAO_BOBINA_86EH"], 13, True)
        x = self.leitura_sup_bobina_86eh
        self.condicionadores.append(CondicionadorBase("UG2_SUPERVISAO_BOBINA_86EH - bit 13", DEVE_INDISPONIBILIZAR, x))

        self.leitura_disj_125vcc_fechados = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_DISJUNTORES_125VCC_FECHADOS"], 31, True)
        x = self.leitura_disj_125vcc_fechados
        self.condicionadores.append(CondicionadorBase("UG2_DISJUNTORES_125VCC_FECHADOS - bit 31", DEVE_INDISPONIBILIZAR, x))

        self.leitura_disj_24vcc_fechados = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_DISJUNTORES_24VCC_FECHADOS"], 0, True)
        x = self.leitura_disj_24vcc_fechados
        self.condicionadores.append(CondicionadorBase("UG2_DISJUNTORES_24VCC_FECHADOS - bit 00", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_ponte_fase_a = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_PONTE_FASE_A"], 0)
        x = self.leitura_falha_temp_ponte_fase_a
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_PONTE_FASE_A - bit 00", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_ponte_fase_b = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_PONTE_FASE_B"], 1)
        x = self.leitura_falha_temp_ponte_fase_b
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_PONTE_FASE_B - bit 01", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_ponte_fase_c = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_PONTE_FASE_C"], 2)
        x = self.leitura_falha_temp_ponte_fase_c
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_PONTE_FASE_C - bit 02", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_trafo_excita = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_TRAFO_EXCITACAO"], 4)
        x = self.leitura_falha_temp_trafo_excita
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_TRAFO_EXCITACAO - bit 04", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_guia = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_MANCAL_GUIA"], 5)
        x = self.leitura_falha_temp_mancal_guia
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_MANCAL_GUIA - bit 05", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_oleo_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_OLEO_UHRV"], 6)
        x = self.leitura_falha_temp_oleo_uhrv
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_OLEO_UHRV - bit 06", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_oleo_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_OLEO_UHLM"], 7)
        x = self.leitura_falha_temp_oleo_uhlm
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_OLEO_UHLM - bit 07", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_casq_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_CASQ_MANCAL_COMBINADO"], 8)
        x = self.leitura_falha_temp_mancal_casq_comb
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_CASQ_MANCAL_COMBINADO - bit 08", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_con_esc_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO"], 9)
        x = self.leitura_falha_temp_mancal_con_esc_comb
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO - bit 09", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_pat_1_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_1_PATINS_MANCAL_COMBINADO"], 10)
        x = self.leitura_falha_temp_mancal_pat_1_comb
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_1_PATINS_MANCAL_COMBINADO - bit 10", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_pat_2_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_2_PATINS_MANCAL_COMBINADO"], 11)
        x = self.leitura_falha_temp_mancal_pat_2_comb
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_2_PATINS_MANCAL_COMBINADO - bit 11", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_guia_interno_1 = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_1_MANCAL_GUIA_INTERNO"], 12)
        x = self.leitura_falha_temp_mancal_guia_interno_1
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_1_MANCAL_GUIA_INTERNO - bit 12", DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_temp_mancal_guia_interno_2 = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_2_MANCAL_GUIA_INTERNO"], 13)
        x = self.leitura_falha_temp_mancal_guia_interno_2
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_2_MANCAL_GUIA_INTERNO - bit 13", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_gerador_nucleo_esta = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_GERADOR_NUCLEO_ESTATORICO"], 14)
        x = self.leitura_falha_temp_gerador_nucleo_esta
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_GERADOR_NUCLEO_ESTATORICO - bit 14", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_gerador_fase_a = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_GERADOR_FASE_A"], 15)
        x = self.leitura_falha_temp_gerador_fase_a
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_GERADOR_FASE_A - bit 15", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_gerador_fase_b = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_GERADOR_FASE_B"], 16)
        x = self.leitura_falha_temp_gerador_fase_b
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_GERADOR_FASE_B - bit 16", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_gerador_fase_c = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_TEMP_GERADOR_FASE_C"], 17)
        x = self.leitura_falha_temp_gerador_fase_c
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_TEMP_GERADOR_FASE_C - bit 17", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_pressao_entrada_turb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_PRESSAO_ENTRADA_TURBINA"], 20)
        x = self.leitura_falha_pressao_entrada_turb
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_PRESSAO_ENTRADA_TURBINA - bit 20", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_eixo_x_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_VIBRACAO_EIXO_X_MANCAL_COMBINADO"], 24)
        x = self.leitura_falha_vibra_eixo_x_mancal_comb
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_VIBRACAO_EIXO_X_MANCAL_COMBINADO - bit 24", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_eixo_y_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO"], 25)
        x = self.leitura_falha_vibra_eixo_y_mancal_comb
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO - bit 25", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_eixo_z_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO"], 26)
        x = self.leitura_falha_vibra_eixo_z_mancal_comb
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO - bit 26", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_detec_horizontal = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_VIBRACAO_DETECCAO_HORIZONTAL"], 28)
        x = self.leitura_falha_vibra_detec_horizontal
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_VIBRACAO_DETECCAO_HORIZONTAL - bit 28", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_detec_vertical = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_FALHA_VIBRACAO_DETECACAO_VERTICAL"], 29)
        x = self.leitura_falha_vibra_detec_vertical
        self.condicionadores.append(CondicionadorBase("UG2_FALHA_VIBRACAO_DETECACAO_VERTICAL - bit 29", DEVE_INDISPONIBILIZAR, x))

        self.leitura_bloqueio_86M_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_BLOQUEIO_86M_ATUADO"], 31)
        x = self.leitura_bloqueio_86M_atuado
        self.condicionadores.append(CondicionadorBase("UG2_BLOQUEIO_86M_ATUADO - bit 31", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_detec_horizontal = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_VIBRACAO_DETECCAO_HORIZONTAL"], 21)
        x = self.leitura_trip_vibra_detec_horizontal
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_VIBRACAO_DETECCAO_HORIZONTAL - bit 21", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_detec_vertical = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_VIBRACAO_DETECACAO_VERTICAL"], 22)
        x = self.leitura_trip_vibra_detec_vertical
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_VIBRACAO_DETECACAO_VERTICAL - bit 22", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_eixo_x_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_VIBRACAO_EIXO_X_MANCAL_COMBINADO"], 23)
        x = self.leitura_trip_vibra_eixo_x_mancal_comb
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_VIBRACAO_EIXO_X_MANCAL_COMBINADO - bit 23", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_eixo_y_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_VIBRACAO_EIXO_Y_MANCAL_COMBINADO"], 24)
        x = self.leitura_trip_vibra_eixo_y_mancal_comb
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_VIBRACAO_EIXO_Y_MANCAL_COMBINADO - bit 24", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_eixo_z_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_VIBRACAO_EIXO_Z_MANCAL_COMBINADO"], 25)
        x = self.leitura_trip_vibra_eixo_z_mancal_comb
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_VIBRACAO_EIXO_Z_MANCAL_COMBINADO - bit 25", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_ponte_fase_a = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_PONTE_FASE_A"], 16)
        x = self.leitura_trip_temp_ponte_fase_a
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_PONTE_FASE_A - bit 16", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_ponte_fase_b = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_PONTE_FASE_B"], 17)
        x = self.leitura_trip_temp_ponte_fase_b
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_PONTE_FASE_B - bit 17", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_ponte_fase_c = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_PONTE_FASE_C"], 18)
        x = self.leitura_trip_temp_ponte_fase_c
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_PONTE_FASE_C - bit 18", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_fase_a = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_GERADOR_FASE_A"], 19)
        x = self.leitura_trip_temp_gerador_fase_a
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_GERADOR_FASE_A - bit 19", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_fase_b = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_GERADOR_FASE_B"], 20)
        x = self.leitura_trip_temp_gerador_fase_b
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_GERADOR_FASE_B - bit 20", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_fase_c = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_GERADOR_FASE_C"], 21)
        x = self.leitura_trip_temp_gerador_fase_c
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_GERADOR_FASE_C - bit 21", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_nucleo_estatorico = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_GERADOR_NUCLEO_ESTATORICO"], 22)
        x = self.leitura_trip_temp_gerador_nucleo_estatorico
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_GERADOR_NUCLEO_ESTATORICO - bit 22", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_saida_ar = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_GERADOR_SAIDA_AR"], 23)
        x = self.leitura_trip_temp_gerador_saida_ar
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_GERADOR_SAIDA_AR - bit 23", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_trafo_ateramento = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_TRAFO_ATERRAMENTO"], 24)
        x = self.leitura_trip_temp_trafo_ateramento
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_TRAFO_ATERRAMENTO - bit 24", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_trafo_excitacao = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_TRAFO_EXCITACAO"], 25)
        x = self.leitura_trip_temp_trafo_excitacao
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_TRAFO_EXCITACAO - bit 25", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_pressao_acum_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_PRESSAO_ACUMULADOR_UHRV"], 5)
        x = self.leitura_trip_pressao_acum_uhrv
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_PRESSAO_ACUMULADOR_UHRV - bit 05", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_casq_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_CASQ_MANCAL_COMBINADO"], 18)
        x = self.leitura_trip_temp_mancal_casq_comb
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_CASQ_MANCAL_COMBINADO - bit 18", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_contra_esc_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO"], 19)
        x = self.leitura_trip_temp_mancal_contra_esc_comb
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO - bit 19", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_patins_1_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_1_PATINS_MANCAL_COMBINADO"], 20)
        x = self.leitura_trip_temp_mancal_patins_1_comb
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_1_PATINS_MANCAL_COMBINADO - bit 20", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_patins_2_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_2_PATINS_MANCAL_COMBINADO"], 21)
        x = self.leitura_trip_temp_mancal_patins_2_comb
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_2_PATINS_MANCAL_COMBINADO - bit 21", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_guia_interno_1 = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_1_MANCAL_GUIA_INTERNO"], 22)
        x = self.leitura_trip_temp_mancal_guia_interno_1
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_1_MANCAL_GUIA_INTERNO - bit 22", DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_guia_interno_2 = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_TRIP_TEMP_2_MANCAL_GUIA_INTERNO"], 23)
        x = self.leitura_trip_temp_mancal_guia_interno_2
        self.condicionadores.append(CondicionadorBase("UG2_TRIP_TEMP_2_MANCAL_GUIA_INTERNO - bit 23", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_fechar_distrib_rv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RV_FALHA_FECHAR_DISTRIBUIDOR"], 4)
        x = self.leitura_falha_fechar_distrib_rv
        self.condicionadores.append(CondicionadorBase("UG2_RV_FALHA_FECHAR_DISTRIBUIDOR - bit 04", DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_desbilitar_rt = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RT_FALHA_DESABILITAR"], 18)
        x = self.leitura_falha_desbilitar_rt
        self.condicionadores.append(CondicionadorBase("UG2_RT_FALHA_DESABILITAR - bit 18", DEVE_INDISPONIBILIZAR, x))


        # Inicializa as variáveis de controle PI para operação TDA Offline
        self.pt_controle_p = (self.leitura_pressao_turbina.valor - self.cfg["press_turbina_alvo"]) * self.cfg["pt_kp"]
        self.pt_ajuste_ie = (self.leitura_potencia.valor + self.leitura_potencia_ug1.valor) / self.cfg["pot_maxima_alvo"]
        self.pt_controle_i = self.pt_ajuste_ie - self.pt_controle_p

    def controle_cx_espiral(self):
        # Calcula PI
        self.erro_press_turbina = 0
        self.erro_press_turbina = self.leitura_pressao_turbina.valor - self.cfg["press_turbina_alvo"]

        self.logger.debug("[UG{}] Pressão Alvo: {:0.3f}, Recente: {:0.3f}".format(self.id, self.cfg["press_turbina_alvo"], self.leitura_pressao_turbina.valor))

        self.pt_controle_p = self.cfg["pt_kp"] * self.erro_press_turbina
        self.pt_controle_i = max(min((self.cfg["cx_ki"] * self.erro_press_turbina) + self.pt_controle_i, 1), 0)
        saida_pi = self.pt_controle_p + self.pt_controle_i
        
        self.logger.debug("[UG{}] PI: {:0.3f} <-- P:{:0.3f} + I:{:0.3f}; ERRO={}".format(self.id, saida_pi, self.pt_controle_p, self.pt_controle_i, self.erro_press_turbina))

        # Calcula o integrador de estabilidade e limita
        self.pt_controle_ie = max(min(saida_pi + self.pt_ajuste_ie * self.cfg["pt_kie"], 1), 0)

        # Arredondamento e limitação
        pot_alvo = max(min(round(self.cfg["pot_maxima_ug2"] * self.pt_controle_ie, 5), self.cfg["pot_maxima_ug2"],),self.cfg["pot_minima"],)

        self.logger.debug("[UG{}] Pot alvo: {:0.3f}".format(self.id, pot_alvo))

        ts = datetime.now(pytz.timezone("Brazil/East")).timestamp()
        try:
            self.db.insert_debug(
                ts,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
                0,
                0,
                0,
                0,
                self.leitura_setpoint_ug1.valor,
                self.leitura_potencia_ug1.valor,
                self.setpoint,
                self.leitura_potencia.valor,
                0,
                0,
                1,
                self.cfg["pt_kp"],
                self.cfg["pt_ki"],
                self.cfg["pt_kie"],
                self.pt_controle_ie,
            )
        except Exception as e:
            logger.exception(e)

        if self.leitura_pressao_turbina.valor >= 15.5:
            self.enviar_setpoint(pot_alvo)
        else:
            self.enviar_setpoint(0)
        print("")
        
    def acionar_trip_logico(self) -> bool:
        """
        Envia o comando de acionamento do TRIP para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.logger.debug("[UG{}] Acionando sinal de TRIP.".format(self.id))
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_PARADA_EMERGENCIA"], 4, 1)
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
            self.logger.debug("[UG{}] Removendo sinal de TRIP.".format(self.id))
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_RESET_FALHAS_PASSOS"], 0, 1)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86M"], 1, 1)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86E"], 2, 1)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86H"], 3, 1)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_UHRV_REARME_FALHAS"], 0, 1)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_UHLM_REARME_FALHAS"], 16, 1)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_BLOQUEIO_86H_ATUADO"], 31, 0)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_RELE_700G_TRIP_ATUADO"], 31, 0)
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
            self.logger.debug("[UG{}] Acionando sinal elétrico de TRIP.".format(self.id))
            DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG2"],[1],)
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
            self.logger.debug("[UG{}] Removendo sinal elétrico de TRIP.".format(self.id))
            DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG2"],[0],)
            DataBank.set_words(REG_MB["MOA"]["PAINEL_LIDO"],[0],)

            if not LeituraOPCBit(self.client, REG_OPC["SE"]["CMD_SE_FECHA_52L"], 4, True):
                self.logger.debug("Comando recebido da UG2 - Fechando Dj52L")
                self.con.fechaDj52L()
        except Exception as e:
            self.logger.debug("Exception! Traceback: {}".format(traceback.format_exc()))
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
            # na simulação, a condição a seguir, impede a partida das ugs. Retirar comentário quando for aplicar em campo
            """
            if not self.client.read_discrete_inputs(REG_UG2_COND_PART,1)[0]:
                self.logger.debug("[UG{}] Máquina sem condição de partida. Irá partir quando as condições forem reestabelecidas.".format(self.id))
                return True
            elif self.client_sa.read_coils(REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52A1Fechado)[0] != 0:
                self.logger.info("[UG{}] O Disjuntor 52A1 está aberto. Para partir a máquina, o mesmo deverá ser fechado.")
                return True
            """
            if not self.etapa_alvo == UNIDADE_SINCRONIZADA:
                self.logger.info("[UG{}] Enviando comando de partida.".format(self.id))
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_RESET_FALHAS_PASSOS"], 0, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86M"], 1, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86E"], 2, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86H"], 3, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_UHRV_REARME_FALHAS"], 0, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_UHLM_REARME_FALHAS"], 16, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_PARTIDA_CMD_SINCRONISMO"], 10, 1)
                self.enviar_setpoint(self.setpoint)
            else:
                self.logger.debug("[UG{}] A unidade já está sincronizada.".format(self.id))
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
                self.logger.info("[UG{}] Enviando comando de parada.".format(self.id))
                response = False
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_PARADA_CMD_DESABILITA_UHLM"], 15, 1)
                self.enviar_setpoint(0)
            else:
                self.logger.debug("[UG{}] A unidade já está parada.".format(self.id))
            
        except Exception as e:
            self.logger.exception(e)
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
            self.logger.info("[UG{}] Enviando comando de reconhece e reset alarmes. (Aproximadamente 10s)".format(self.id))

            for _ in range(3):
                DataBank.set_words(REG_MB["MOA"]["PAINEL_LIDO"], [0])
                self.remover_trip_eletrico()
                DataBank.set_words(REG_MB["MOA"]["PAINEL_LIDO"], [0])
                sleep(1)
                self.remover_trip_logico()
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_RESET_FALHAS_PASSOS"], 0, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86M"], 1, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86E"], 2, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86H"], 3, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_UHRV_REARME_FALHAS"], 0, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_UHLM_REARME_FALHAS"], 16, 1)
                DataBank.set_words(REG_MB["MOA"]["PAINEL_LIDO"], [0])
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
            self.logger.debug("[UG{}] Enviando setpoint {} kW.".format(self.id, int(self.setpoint)))
            response = False
            if self.setpoint > 1:
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_RESET_FALHAS_PASSOS"], 0, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86M"], 1, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86E"], 2, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86H"], 3, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_UHRV_REARME_FALHAS"], 0, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_UHLM_REARME_FALHAS"], 16, 1)
                response = self.clp.write_single_register(REG_MB["UG"]["UG2_RV_SETPOINT_POTENCIA_ATIVA_PU"], self.setpoint)

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

    @property
    def status_comporta(self) -> int:
        try:
            response = self.leitura_Status_Comporta.valor
        except Exception as e:
            raise(e)
        else:
            return response

    def abrir_comporta(self) -> bool:
        try:
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["CP1_CMD_ABERTURA_TOTAL"], 1, 1)
        except Exception as e:
            raise(e)
        else:
            return response
    
    def fechar_comporta(self) -> bool:
        try:
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["CP1_CMD_FECHAMENTO"], 3, 1)
        except Exception as e:
            raise(e)
        else:
            return response

    def cracking_comporta(self) -> bool:
        try:
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["CP1_CMD_ABERTURA_CRACKING"], 1, 1)
        except Exception as e:
            raise(e)
        else:
            return response

    def modbus_update_state_register(self):
        DataBank.set_words(REG_MB["MOA"]["OUT_STATE_UG2"],[self.codigo_state],)
        DataBank.set_words(REG_MB["MOA"]["OUT_ETAPA_UG2"],[self.etapa_atual],)

        
    def interstep(self) -> None:
        if (not self.avisou_emerg_voip) and (self.condicionador_pressao_turbina_ug.valor > 0.1):
            self.avisou_emerg_voip = True

        elif self.condicionador_pressao_turbina_ug.valor < 0.05:
            self.avisou_emerg_voip = False

    def controle_limites_operacao(self):

        if self.leitura_temperatura_fase_R.valor >= self.condicionador_temperatura_fase_r_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura de Fase R da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_r_ug.valor_base, self.leitura_temperatura_fase_R.valor))
        if self.leitura_temperatura_fase_R.valor >= 0.9*(self.condicionador_temperatura_fase_r_ug.valor_limite - self.condicionador_temperatura_fase_r_ug.valor_base) + self.condicionador_temperatura_fase_r_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura de Fase R da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_r_ug.valor_limite, self.leitura_temperatura_fase_R.valor))
        
        if self.leitura_temperatura_fase_S.valor >= self.condicionador_temperatura_fase_s_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura de Fase S da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_s_ug.valor_base, self.leitura_temperatura_fase_S.valor))
        if self.leitura_temperatura_fase_S.valor >= 0.9*(self.condicionador_temperatura_fase_s_ug.valor_limite - self.condicionador_temperatura_fase_s_ug.valor_base) + self.condicionador_temperatura_fase_s_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura de Fase S da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_s_ug.valor_limite, self.leitura_temperatura_fase_S.valor))

        if self.leitura_temperatura_fase_T.valor >= self.condicionador_temperatura_fase_t_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura de Fase T da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_t_ug.valor_base, self.leitura_temperatura_fase_T.valor))
        if self.leitura_temperatura_fase_T.valor >= 0.9*(self.condicionador_temperatura_fase_t_ug.valor_limite - self.condicionador_temperatura_fase_t_ug.valor_base) + self.condicionador_temperatura_fase_t_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura de Fase T da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_t_ug.valor_limite, self.leitura_temperatura_fase_T.valor))

        if self.leitura_temperatura_nucleo_gerador_1.valor >= self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Núcleo Gerador 1 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base, self.leitura_temperatura_nucleo_gerador_1.valor))
        if self.leitura_temperatura_nucleo_gerador_1.valor >= 0.9*(self.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite - self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base) + self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Núcleo Gerador 1 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite, self.leitura_temperatura_nucleo_gerador_1.valor))
        
        if self.leitura_temperatura_mancal_guia.valor >= self.condicionador_temperatura_mancal_guia_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Guia da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_ug.valor_base, self.leitura_temperatura_mancal_guia.valor))
        if self.leitura_temperatura_mancal_guia.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_ug.valor_limite - self.condicionador_temperatura_mancal_guia_ug.valor_base) + self.condicionador_temperatura_mancal_guia_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Guia da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_ug.valor_limite, self.leitura_temperatura_mancal_guia.valor))
        
        if self.leitura_temperatura_mancal_guia_interno_1.valor >= self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Guia Interno 1 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base, self.leitura_temperatura_mancal_guia_interno_1.valor))
        if self.leitura_temperatura_mancal_guia_interno_1.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_limite - self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base) + self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Guia Interno 1 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_limite, self.leitura_temperatura_mancal_guia_interno_1.valor))
        
        if self.leitura_temperatura_mancal_guia_interno_2.valor >= self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Guia Interno 2 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base, self.leitura_temperatura_mancal_guia_interno_2.valor))
        if self.leitura_temperatura_mancal_guia_interno_2.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_limite - self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base) + self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Guia Interno 2 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_limite, self.leitura_temperatura_mancal_guia_interno_2.valor))

        if self.leitura_temperatura_patins_mancal_comb_1.valor >= self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura dos Patins do Mancal Combinado 1 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base, self.leitura_temperatura_patins_mancal_comb_1.valor))
        if self.leitura_temperatura_patins_mancal_comb_1.valor >= 0.9*(self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_limite - self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base) + self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura dos Patins do Mancal Combinado 1 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_limite, self.leitura_temperatura_patins_mancal_comb_1.valor))
        
        if self.leitura_temperatura_patins_mancal_comb_2.valor >= self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura dos Patins do Mancal Combinado 2 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base, self.leitura_temperatura_patins_mancal_comb_2.valor))
        if self.leitura_temperatura_patins_mancal_comb_2.valor >= 0.9*(self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_limite - self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base) + self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura dos Patins do Mancal Combinado 2 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_limite, self.leitura_temperatura_patins_mancal_comb_2.valor))

        if self.leitura_temperatura_mancal_casq_comb.valor >= self.condicionador_temperatura_mancal_casq_comb_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Casquilho Combinado da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_casq_comb_ug.valor_base, self.leitura_temperatura_mancal_casq_comb.valor))
        if self.leitura_temperatura_mancal_casq_comb.valor >= 0.9*(self.condicionador_temperatura_mancal_casq_comb_ug.valor_limite - self.condicionador_temperatura_mancal_casq_comb_ug.valor_base) + self.condicionador_temperatura_mancal_casq_comb_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Casquilho Combinado da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_casq_comb_ug.valor_limite, self.leitura_temperatura_mancal_casq_comb.valor))

        if self.leitura_temperatura_mancal_contra_esc_comb.valor >= self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Contra Escora Combinado da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base, self.leitura_temperatura_mancal_contra_esc_comb.valor))
        if self.leitura_temperatura_mancal_contra_esc_comb.valor >= 0.9*(self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_limite - self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base) + self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Contra Escora Combinado da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_limite, self.leitura_temperatura_mancal_contra_esc_comb.valor))

        if self.leitura_pressao_turbina.valor <= self.condicionador_pressao_turbina_ug.valor_base and self.leitura_pressao_turbina.valor != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            self.logger.warning("[UG{}] A pressão na entrada da turbina da UG passou do valor base! ({:03.2f} KGf/m2) | Leitura: {:03.2f}".format(self.id, self.condicionador_pressao_turbina_ug.valor_base, self.leitura_pressao_turbina.valor))
        if self.leitura_pressao_turbina.valor <= self.condicionador_pressao_turbina_ug.valor_limite+0.9*(self.condicionador_pressao_turbina_ug.valor_base - self.condicionador_pressao_turbina_ug.valor_limite) and self.leitura_pressao_turbina.valor != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            self.logger.critical("[UG{}] A pressão na entrada da turbina da UG está muito próxima do limite! ({:03.2f} KGf/m2) | Leitura: {:03.2f} KGf/m2".format(self.id, self.condicionador_pressao_turbina_ug.valor_limite, self.leitura_pressao_turbina.valor))

    def leituras_por_hora(self):
        # Telegram

        self.leitura_saidas_digitais_rv_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_SAIDAS_DIGITAIS"], 0)
        if self.leitura_saidas_digitais_rv_b0:
            self.logger.warning("[UG{}] O alarme do Regulador de Velocidade da UG foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_saidas_digitais_rt_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_SAIDAS_DIGITAIS"], 0)
        if self.leitura_saidas_digitais_rt_b0:
            self.logger.warning("[UG{}] O alarme do Regulador de Tensão da UG foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_falha_3_rt_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_3"], 0)
        if self.leitura_falha_3_rt_b0:
            self.logger.warning("[UG{}] Houve uma falha na leitura de potência reativa pelo Regulador de Tensão da UG. Favor Verificar.". format(self.id))
        
        self.leitura_falha_3_rt_b1 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_3"], 1)
        if self.leitura_falha_3_rt_b1:
            self.logger.warning("[UG{}] Houve uma falha na leitura da tensão terminal pelo Regulador de Tensão da UG. Favor Verificar.". format(self.id))
        
        self.leitura_falha_3_rt_b2 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_3"], 2)
        if self.leitura_falha_3_rt_b2:
            self.logger.warning("[UG{}] Houve uma falha na leitura principal da corrente de excitação pelo Regulador de Tensão da UG. Favor Verificar.". format(self.id))
        
        self.leitura_falha_3_rt_b3 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_3"], 3)
        if self.leitura_falha_3_rt_b3:
            self.logger.warning("[UG{}] Houve uma falha na leitura retaguarda da corrente de excitação pelo Regulador de Tensão da UG. Favor Verificar.". format(self.id))
        
        self.leitura_falha_3_rt_b4 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_3"], 4)
        if self.leitura_falha_3_rt_b4:
            self.logger.warning("[UG{}] Foi identificado ruído na instrumentação de reativo do Regulador de Tensão da UG. Favor Verificar.". format(self.id))
        
        self.leitura_falha_3_rt_b5 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_3"], 5)
        if self.leitura_falha_3_rt_b5:
            self.logger.warning("[UG{}] Foi identificado ruído na instrumentação de tensão do Regulador de Tensão da UG. Favor Verificar.". format(self.id))
        
        self.leitura_falha_3_rt_b6 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_3"], 6)
        if self.leitura_falha_3_rt_b6:
            self.logger.warning("[UG{}] Foi identificado ruído na instrumentação de excitação principal do Regulador de Tensão da UG. Favor Verificar.". format(self.id))
        
        self.leitura_falha_3_rt_b7 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RT_FALHAS_3"], 7)
        if self.leitura_falha_3_rt_b7:
            self.logger.warning("[UG{}] Foi identificado ruído na instrumentação de excitação retaguarda do Regulador de Tensão da UG. Favor Verificar.". format(self.id))
        
        self.leitura_falha_1_rv_b4 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 4)
        if self.leitura_falha_1_rv_b4:
            self.logger.warning("[UG{}] Houve uma falha de leitura de posição do distribuidor pelo Regulador de Velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b5 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 5)
        if self.leitura_falha_1_rv_b5:
            self.logger.warning("[UG{}] Houve uma falha de leitura de posição do rotor pelo Regulador de Velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b6 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 6)
        if self.leitura_falha_1_rv_b6:
            self.logger.warning("[UG{}] Houve uma falha de leitura de potência ativa pelo Regulador de Velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b7 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 7)
        if self.leitura_falha_1_rv_b7:
            self.logger.warning("[UG{}] Houve uma falha de leitura de referência de potência pelo Regulador de Velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b8 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 8)
        if self.leitura_falha_1_rv_b8:
            self.logger.warning("[UG{}] Houve uma falha de leitura de nível montante pelo Regulador de Velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b13 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 13)
        if self.leitura_falha_1_rv_b13:
            self.logger.warning("[UG{}] Foi identificado ruído na medição principal de velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b14 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 14)
        if self.leitura_falha_1_rv_b14:
            self.logger.warning("[UG{}] Foi identificado ruído na medição retaguarda de velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b15 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 15)
        if self.leitura_falha_1_rv_b15:
            self.logger.warning("[UG{}] Foi identificada perda na medição principal de velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_2_rv_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 0)
        if self.leitura_falha_2_rv_b0:
            self.logger.warning("[UG{}] Foi identificada perda na medição retaguarda de velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_2_rv_b4 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG2_RV_FALHA_1"], 4)
        if self.leitura_falha_2_rv_b4:
            self.logger.warning("[UG{}] Foi identificada diferença entre medidor principal e retaguarda da UG. Favor verificar.".format(self.id))
        
        self.leitura_unidade_manutencao_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_UHRV_UNIDADE_EM_MANUTENCAO"], 0)
        if self.leitura_unidade_manutencao_uhrv:
            self.logger.warning("[UG{}] UHRV da UG entrou em modo de manutenção".format(self.id))
        
        self.leitura_unidade_manutencao_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_UHLM_UNIDADE_EM_MANUTENCAO"], 4)
        if self.leitura_unidade_manutencao_uhlm:
            self.logger.warning("[UG{}] UHLM da UG entrou em modo de manutenção".format(self.id))

        self.leitura_filtro_limpo_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_UHRV_FILTRO_LIMPO"], 24, True)
        if not self.leitura_filtro_limpo_uhrv:
            self.logger.warning("[UG{}] O filtro da UHRV da UG está sujo. Favor realizar limpeza/troca.".format(self.id))

        self.leitura_filtro_limpo_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_UHLM_FILTRO_LIMPO"], 21, True)
        if not self.leitura_filtro_limpo_uhrv:
            self.logger.warning("[UG{}] O filtro da UHLM da UG está sujo. Favor realizar limpeza/troca.".format(self.id))

        self.leitura_porta_interna_fechada_cpg = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_CPG_UG_PORTA_INTERNA_FECHADA"], 12, True)
        if not self.leitura_porta_interna_fechada_cpg:
            self.logger.warning("[UG{}] A porta interna do CPG da UG está aberta. Favor fechar.".format(self.id))

        self.leitura_porta_traseira_fechada_cpg = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_CPG_UG_PORTA_TRASEIRA_FECHADA"], 13, True)
        if not self.leitura_porta_traseira_fechada_cpg:
            self.logger.warning("[UG{}] A porta traseira do CPG da UG está aberta. Favor fechar.".format(self.id))

        self.leitura_resistencia_sem_falha = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_RESISTENCIA_SEM_FALHA"], 28, True)
        if not self.leitura_resistencia_sem_falha:
            self.logger.warning("[UG{}] Houve uma falha na resistência da UG. Favor verificar.".format(self.id))

        self.leitura_escovas_gastas_polo_positivo = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ESCOVAS_GASTAS_POLO_POSITIVO"], 5)
        if self.leitura_escovas_gastas_polo_positivo:
            self.logger.warning("[UG{}] Foi identificado que as escovas do polo positivo da UG estão gastas. Favor verificar.".format(self.id))
        
        self.leitura_escovas_gastas_polo_negativo = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ESCOVAS_GASTAS_POLO_NEGATIVO"], 6)
        if self.leitura_escovas_gastas_polo_negativo:
            self.logger.warning("[UG{}] Foi identificado que as escovas do polo negativo da UG estão gastas. Favor verificar.".format(self.id))

        self.leitura_alarme_temp_ponte_fase_a = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_PONTE_FASE_A"], 0)
        if self.leitura_alarme_temp_ponte_fase_a:
            self.logger.warning("[UG{}] O alarme de temperatura da pote fase A foi acionado. Favor verificar.".format(self.id))

        self.leitura_alarme_temp_ponte_fase_b = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_PONTE_FASE_B"], 1)
        if self.leitura_alarme_temp_ponte_fase_b:
            self.logger.warning("[UG{}] O alarme de temperatura da pote fase B foi acionado. Favor verificar.".format(self.id))

        self.leitura_alarme_temp_ponte_fase_c = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_PONTE_FASE_C"], 2)
        if self.leitura_alarme_temp_ponte_fase_c:
            self.logger.warning("[UG{}] O alarme de temperatura da pote fase C foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_trafo_excitacao = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_TRAFO_EXCITACAO"], 4)
        if self.leitura_alarme_temp_trafo_excitacao:
            self.logger.warning("[UG{}] O alarme de temperatura do transformador excitação foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_mancal_guia = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_MANCAL_GUIA"], 5)
        if self.leitura_alarme_temp_mancal_guia:
            self.logger.warning("[UG{}] O alarme de temperatura do mancal guia foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_oleo_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_OLEO_UHRV"], 6)
        if self.leitura_alarme_temp_oleo_uhrv:
            self.logger.warning("[UG{}] O alarme de temperatura de óleo da UHRV foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_oleo_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_OLEO_UHLM"], 7)
        if self.leitura_alarme_temp_oleo_uhlm:
            self.logger.warning("[UG{}] O alarme de temperatura de óleo da UHLM foi acionado. Favor verificar.".format(self.id))

        self.leitura_alarme_temp_mancal_casq_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_CASQ_MANCAL_COMBINADO"], 8)
        if self.leitura_alarme_temp_mancal_casq_comb:
            self.logger.warning("[UG{}] O alarme de temperatura do mancal casquilho combinado foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_mancal_con_esc_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO"], 9)
        if self.leitura_alarme_temp_mancal_con_esc_comb:
            self.logger.warning("[UG{}] O alarme de temperatura do mancal contra escora combinado foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_patins_1_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_1_PATINS_MANCAL_COMBINADO"], 10)
        if self.leitura_alarme_temp_patins_1_mancal_comb:
            self.logger.warning("[UG{}] O alarme de temperatura do patins 1 mancal combinado foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_patins_2_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_2_PATINS_MANCAL_COMBINADO"], 11)
        if self.leitura_alarme_temp_patins_2_mancal_comb:
            self.logger.warning("[UG{}] O alarme de temperatura do patins 2 mancal combinado foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_mancal_guia_interno_1 = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_1_MANCAL_GUIA_INTERNO"], 12)
        if self.leitura_alarme_temp_mancal_guia_interno_1:
            self.logger.warning("[UG{}] O alarme de temperatura do mancal guia interno 1 foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_mancal_guia_interno_2 = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_2_MANCAL_GUIA_INTERNO"], 13)
        if self.leitura_alarme_temp_mancal_guia_interno_2:
            self.logger.warning("[UG{}] O alarme de temperatura do mancal guia interno 2 foi acionado. Favor verificar.".format(self.id))

        self.leitura_alarme_temp_nucleo_estatorico_gerador = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_GERADOR_NUCLEO_ESTATORICO"], 14)
        if self.leitura_alarme_temp_nucleo_estatorico_gerador:
            self.logger.warning("[UG{}] O alarme de temperatura do núcleo estatórico do gerador foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_temp_fase_a_gerador = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_GERADOR_FASE_A"], 15)
        if self.leitura_temp_fase_a_gerador:
            self.logger.warning("[UG{}] O alarme de temperatura de fase A do gerador foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_temp_fase_b_gerador = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_GERADOR_FASE_B"], 16)
        if self.leitura_temp_fase_b_gerador:
            self.logger.warning("[UG{}] O alarme de temperatura de fase B do gerador foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_temp_fase_c_gerador = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_TEMP_GERADOR_FASE_C"], 17)
        if self.leitura_temp_fase_c_gerador:
            self.logger.warning("[UG{}] O alarme de temperatura de fase C do gerador foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_vibra_eixo_x_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_VIBRACAO_EIXO_X_MANCAL_COMBINADO"], 24)
        if self.leitura_alarme_vibra_eixo_x_mancal_comb:
            self.logger.warning("[UG{}] O alarme de vibração do eixo X do mancal combinado foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_vibra_eixo_y_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_VIBRACAO_EIXO_Y_MANCAL_COMBINADO"], 25)
        if self.leitura_alarme_vibra_eixo_y_mancal_comb:
            self.logger.warning("[UG{}] O alarme de vibração do eixo Y do mancal combinado foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_vibra_eixo_z_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_VIBRACAO_EIXO_Z_MANCAL_COMBINADO"], 26)
        if self.leitura_alarme_vibra_eixo_z_mancal_comb:
            self.logger.warning("[UG{}] O alarme de vibração do eixo Z do mancal combinado foi acionado. Favor verificar.".format(self.id))

        self.leitura_alarme_vibra_detec_horizontal = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_VIBRACAO_DETECCAO_HORIZONTAL"], 28)
        if self.leitura_alarme_vibra_detec_horizontal:
            self.logger.warning("[UG{}] O alarme de vibração detecção horizontal foi acionado. Favor verificar.".format(self.id))

        self.leitura_alarme_vibra_detec_vertical = LeituraOPCBit(self.client, REG_OPC["UG"]["UG2_ALM_VIBRACAO_DETECCAO_VERTICAL"], 29)
        if self.leitura_alarme_vibra_detec_vertical:
            self.logger.warning("[UG{}] O alarme de vibração detecção vertical foi acionado. Favor verificar.".format(self.id))