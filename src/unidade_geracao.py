import pytz
import logging
import traceback

import os
import json

from time import sleep
from datetime import datetime

from src.conector import *
from src.leituras import *
from src.reg import *
from src.condicionadores import *
from src.unidade_geracao_sm import *

logger = logging.getLogger("__main__")

# Class Stub
class UnidadeDeGeracao:
    ...

class UnidadeDeGeracao:
    def __init__(self, id: int, cfg=None):

        if not cfg:
            raise ValueError
        else:
            config_file = os.path.join(os.path.dirname(__file__), "cfg.json")
            with open(config_file, "r") as file:
                self.cfg = json.load(file)

        # Variáveis privadas
        self.__id = id
        self.__etapa_alvo = 0
        self.__etapa_atual = 0
        self.__last_EtapaAtual = 0
        self.__last_EtapaAlvo = -1
        self.__tempo_entre_tentativas = 0
        self.__limite_tentativas_de_normalizacao = 3

        self.__next_state = StateDisponivel(self)

        # Variáveis protegidas
        self._setpoint = 0
        self._prioridade = 0
        self._setpoint_minimo = 0
        self._setpoint_maximo = 0
        self._temperatura_base = 100
        self._temperatura_limite = 200
        self._pressao_caixa_base = 16.50
        self._pressao_caixa_limite = 15.50
        self._tentativas_de_normalizacao = 0

        self._condicionadores = []
        self._condicionadores_essenciais = []
        self._condicionadores_atenuadores = []

        self._cx_kp = self.cfg["cx_kp"]
        self._cx_ki = self.cfg["cx_ki"]
        self._cx_kie = self.cfg["cx_kie"]
        
        # Variáveis públicas
        self.modo_autonomo = 1
        self.cx_ajuste_ie = 0.1
        self.tempo_normalizar = 0

        self.acionar_voip = False
        self.limpeza_grade = False
        self.release_timer = False
        self.norma_agendada = False
        self.avisou_emerg_voip = False
        self.ler_condicionadores = False
        self.enviar_trip_eletrico = False
        self.aux_tempo_sincronizada = None

        self.pressao_alvo = self.cfg["press_cx_alvo"]
        self.setpoint_minimo = self.cfg["pot_minima"]
        self.setpoint_maximo = self.cfg[f"pot_maxima_ug{self.id}"]

        # Classes públicas
        self.con = FieldConnector()
        self.db = DatabaseConnector()
        self.ts_auxiliar = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

        # Clients modbus
        self.clp_ug = ModbusClient(
            host=CFG[f"UG{self.id}_slave_ip"],
            port=CFG[f"UG{self.id}_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )
        self.clp_sa = ModbusClient(
            host=CFG["USN_slave_ip"],
            port=CFG["USN_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )
        self.clp_moa = ModbusClient(
            host=CFG["MOA_slave_ip"],
            port=CFG["MOA_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )

        # Simulador -> remover em produção
        self.leitura_Operacao_EtapaAtual = LeituraModbus(
            f"[UG{self.id}] Etapa Aux SIM",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosDigitais_EtapaAux_Sim"],
            1,
            op=4
        )
        self.condic_ativos_sim = LeituraModbus(
            f"[UG{self.id}] Condicionadores Aux SIM",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetrornosAnalogicos_AUX_Condicionadores"],
        )

        # Leituras
        self.leitura_potencia = LeituraModbus(
            f"[UG{self.id}] Potência",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosAnalogicos_MWR_PM_710_Potencia_Ativa"],
            op=4,
        )
        self.leitura_potencia_outra_ug = LeituraModbus(
            f"[UG{2 if self.id == 1 else 1}] Potência",
            self.clp_ug,
            UG[f"REG_UG{2 if self.id == 1 else 1}_RetornosAnalogicos_MWR_PM_710_Potencia_Ativa"],
            op=4,
        )
        self.leitura_setpoint_outra_ug = LeituraModbus(
            f"[UG{2 if self.id == 1 else 1}]",
            self.clp_ug,
            UG[f"REG_UG{2 if self.id == 1 else 1}_SaidasAnalogicas_MWW_SPPotAtiva"],
            op=4
        )
        self.leitura_horimetro_hora = LeituraModbus(
            f"[UG{self.id}] Horímetro horas",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosAnalogicos_MWR_Horimetro_Gerador"],
            op=4,
        )
        self.leitura_horimetro_min = LeituraModbus(
            f"[UG{self.id}] Horímetro minutos",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosAnalogicos_MWR_Horimetro_Gerador_min"],
            op=4,
            escala=1/60
        )
        self.leitura_horimetro = LeituraSoma(
            f"[UG{self.id}] Horímetro",
            self.leitura_horimetro_hora,
            self.leitura_horimetro_min
        )
        self.leitura_Operacao_EtapaAlvo = LeituraModbus(
            f"[UG{self.id}] Etapa Alvo",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosDigitais_EtapaAlvo_Sim"],
            1,
            op=4
        )

        # Leituras -> Condicionadores
        # Fase R
        self.leitura_temperatura_fase_R = LeituraModbus(
            f"[UG{self.id}] Temperatura Fase R",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosAnalogicos_MWR_Temperatura_01"],
            op=4
        )
        self.condicionador_temperatura_fase_r_ug = CondicionadorExponencial(
            self.leitura_temperatura_fase_R.descr, 
            DEVE_INDISPONIBILIZAR, 
            self.leitura_temperatura_fase_R, 
            self._temperatura_base, 
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_r_ug)

        # Fase S
        self.leitura_temperatura_fase_S = LeituraModbus(
            f"[UG{self.id}] Temperatura Fase S",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosAnalogicos_MWR_Temperatura_02"],
            op=4
        )
        self.condicionador_temperatura_fase_s_ug = CondicionadorExponencial(
            self.leitura_temperatura_fase_S.descr,
            DEVE_INDISPONIBILIZAR,
            self.leitura_temperatura_fase_S,
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_s_ug)

        # Fase T
        self.leitura_temperatura_fase_T = LeituraModbus(
            f"[UG{self.id}] Temperatura Fase T",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosAnalogicos_MWR_Temperatura_03"],
            op=4
        )
        self.condicionador_temperatura_fase_t_ug = CondicionadorExponencial(
            self.leitura_temperatura_fase_T.descr,
            DEVE_INDISPONIBILIZAR,
            self.leitura_temperatura_fase_T,
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_t_ug)

        # Nucleo Gerador 1
        self.leitura_temperatura_nucleo_gerador_1 = LeituraModbus(
            f"[UG{self.id}] Temperatura Núcleo Gerador 1",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosAnalogicos_MWR_Temperatura_04"],
            op=4
        )
        self.condicionador_temperatura_nucleo_gerador_1_ug = CondicionadorExponencial(
            self.leitura_temperatura_nucleo_gerador_1.descr,
            DEVE_INDISPONIBILIZAR,
            self.leitura_temperatura_nucleo_gerador_1,
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_gerador_1_ug)

        # Nucleo Gerador 2
        self.leitura_temperatura_nucleo_gerador_2 = LeituraModbus(
            f"[UG{self.id}] Temperatura Núcleo Gerador 2",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosAnalogicos_MWR_Temperatura_04"],
            op=4
        )
        self.condicionador_temperatura_nucleo_gerador_2_ug = CondicionadorExponencial(
            self.leitura_temperatura_nucleo_gerador_2.descr,
            DEVE_INDISPONIBILIZAR,
            self.leitura_temperatura_nucleo_gerador_2,
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_gerador_2_ug)

        # Nucleo Gerador 3
        self.leitura_temperatura_nucleo_gerador_3 = LeituraModbus(
            f"[UG{self.id}] Temperatura Núcleo Gerador 3",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosAnalogicos_MWR_Temperatura_04"],
            op=4
        )
        self.condicionador_temperatura_nucleo_gerador_3_ug = CondicionadorExponencial(
            self.leitura_temperatura_nucleo_gerador_3.descr,
            DEVE_INDISPONIBILIZAR,
            self.leitura_temperatura_nucleo_gerador_3,
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_gerador_3_ug)

        # Mancal Casquilho Radial
        self.leitura_temperatura_mancal_casq_rad = LeituraModbus(
            f"[UG{self.id}] Temperatura Mancal Casquilho Radial",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosAnalogicos_MWR_Temperatura_08"],
            op=4
        )
        self.condicionador_temperatura_mancal_casq_rad_ug = CondicionadorExponencial(
            self.leitura_temperatura_mancal_casq_rad.descr,
            DEVE_INDISPONIBILIZAR,
            self.leitura_temperatura_mancal_casq_rad,
            self._temperatura_base,
            self._temperatura_limite,
        )
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_casq_rad_ug)

        # Mancal Casquilho Combinado
        self.leitura_temperatura_mancal_casq_comb = LeituraModbus(
            f"[UG{self.id}] Temperatura Mancal Casquilho Combinado",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosAnalogicos_MWR_Temperatura_10"],
            op=4
        )
        self.condicionador_temperatura_mancal_casq_comb_ug = CondicionadorExponencial(
            self.leitura_temperatura_mancal_casq_comb.descr,
            DEVE_INDISPONIBILIZAR,
            self.leitura_temperatura_mancal_casq_comb,
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_casq_comb_ug)

        # Mancal Escora Combinado
        self.leitura_temperatura_mancal_escora_comb = LeituraModbus(
            f"[UG{self.id}] Temperatura Mancal Escora Combinado",
            self.clp_ug,
            UG[f"REG_UG{self.id}_RetornosAnalogicos_MWR_Temperatura_07"],
            op=4
        )
        self.condicionador_temperatura_mancal_escora_comb_ug = CondicionadorExponencial(
            self.leitura_temperatura_mancal_escora_comb.descr,
            DEVE_INDISPONIBILIZAR,
            self.leitura_temperatura_mancal_escora_comb,
            self._temperatura_base,
            self._temperatura_limite
        )
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_escora_comb_ug)

        # CX Espiral
        self.leitura_caixa_espiral = LeituraModbus(
            f"[UG{self.id}] Pressão Caixa espiral",
            self.clp_ug,
            UG[f"REG_UG{self.id}_EntradasAnalogicas_MRR_PressK1CaixaExpiral_MaisCasas"],
            escala=0.1,
            op=4
        )
        self.condicionador_caixa_espiral_ug = CondicionadorExponencialReverso(
            self.leitura_caixa_espiral.descr,
            DEVE_INDISPONIBILIZAR,
            self.leitura_caixa_espiral,
            self._pressao_caixa_base,
            self._pressao_caixa_limite
        )
        self.condicionadores_atenuadores.append(self.condicionador_caixa_espiral_ug)

    # Property Privadas
    @property
    def id(self) -> int:
        return self.__id

    @property
    def manual(self) -> bool:
        return isinstance(self.__next_state, StateManual)

    @property
    def restrito(self) -> bool:
        return isinstance(self.__next_state, StateRestrito)

    @property
    def disponivel(self) -> bool:
        return isinstance(self.__next_state, StateDisponivel)

    @property
    def indisponivel(self) -> bool:
        return isinstance(self.__next_state, StateIndisponivel)

    @property
    def etapa_atual(self) -> int:
        try:
            leitura = self.leitura_Operacao_EtapaAtual.valor
            if 0 < leitura < 255:
                self.__last_EtapaAtual = leitura
                self.__etapa_atual = leitura
                return self.__etapa_atual
            else:
                return self.__last_EtapaAtual
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar a leitura da etapa atual.\nException: \"{traceback.format_exc()}\"")
            return False

    @property
    def etapa_alvo(self) -> int:
        try:
            leitura = self.leitura_Operacao_EtapaAlvo.valor
            if 0 < leitura < 255:
                self.__last_EtapaAlvo = leitura
                self.__etapa_alvo = leitura
                return self.__etapa_alvo
            else:
                self.__last_EtapaAlvo = self.etapa_atual
                return self.__last_EtapaAlvo
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar a leitura da etapa alvo.\nException: \"{traceback.format_exc()}\"")
            return False

    @property
    def tempo_entre_tentativas(self) -> int:
        return self.__tempo_entre_tentativas

    @property
    def limite_tentativas_de_normalizacao(self) -> int:
        return self.__limite_tentativas_de_normalizacao


    # Property/Setter Protegidas
    @property
    def cx_kp(self) -> float:
        return self._cx_kp

    @cx_kp.setter
    def cx_kp(self, var) -> float:
        self._cx_kp = var

    @property
    def cx_ki(self) -> float:
        return self._cx_ki

    @cx_ki.setter
    def cx_ki(self, var) -> float:
        self._cx_ki = var

    @property
    def cx_kie(self) -> float:
        return self._cx_kie

    @cx_kie.setter
    def cx_kie(self, var) -> float:
        self._cx_kie = var

    @property
    def codigo_state(self) -> int:
        return self._codigo_state

    @codigo_state.setter
    def codigo_state(self, var) -> int:
        self._codigo_state = var

    @property
    def prioridade(self) -> int:
        return self._prioridade

    @prioridade.setter
    def prioridade(self, var) -> None:
        self._prioridade = var

    @property
    def setpoint(self) -> int:
        return self._setpoint

    @setpoint.setter
    def setpoint(self, var: int):
        if var < self.setpoint_minimo:
            self._setpoint = 0
        elif var > self.setpoint_maximo:
            self._setpoint = self.setpoint_maximo
        else:
            self._setpoint = int(var)
        logger.debug(f"[UG{self.id}] SP<-{var}")

    @property
    def setpoint_minimo(self) -> int:
        return self._setpoint_minimo

    @setpoint_minimo.setter
    def setpoint_minimo(self, var: int):
        self._setpoint_minimo = var

    @property
    def setpoint_maximo(self) -> int:
        return self._setpoint_maximo

    @setpoint_maximo.setter
    def setpoint_maximo(self, var: int):
        self._setpoint_maximo = var

    @property
    def temperaturas_base(self) -> int:
        return self._temperatura_base

    @temperaturas_base.setter
    def temperatura_base(self, var: int):
        self._temperatura_base = var

    @property
    def temperaturas_limite(self) -> int:
        return self._temperatura_limite

    @temperaturas_base.setter
    def temperatura_limite(self, var: int):
        self._temperatura_limite = var

    @property
    def pressao_caixa_base(self) -> float:
        return self._pressao_caixa_base

    @pressao_caixa_base.setter
    def temperatura_base(self, var: float):
        self._pressao_caixa_base = var
    
    @property
    def pressao_caixa_limite(self) -> float:
        return self._pressao_caixa_limite

    @temperaturas_base.setter
    def pressao_caixa_limite(self, var: float):
        self._pressao_caixa_limite = var

    @property
    def tentativas_de_normalizacao(self) -> int:
        return self._tentativas_de_normalizacao

    @tentativas_de_normalizacao.setter
    def tentativas_de_normalizacao(self, var: int):
        if 0 <= var and var == int(var):
            self._tentativas_de_normalizacao = int(var)
        else:
            raise ValueError(f"[UG{self.id}] Valor deve se um inteiro positivo")

    @property
    def condicionadores(self) -> list([CondicionadorBase]):
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: list([CondicionadorBase])):
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> list([CondicionadorBase]):
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: list([CondicionadorBase])):
        self._condicionadores_essenciais = var

    @property
    def condicionadores_atenuadores(self) -> list([CondicionadorBase]):
        return self._condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: list([CondicionadorBase])):
        self._condicionadores_atenuadores = var


    # Funções
    def step(self) -> None:
        try:
            logger.debug(f"[UG{self.id}] Step -> (Tentativas de normalização: {self.tentativas_de_normalizacao}/{self.limite_tentativas_de_normalizacao}).")
            self.interstep()
            self.__next_state = self.__next_state.step()
            self.modbus_update_state_register()
        except Exception as e:
            logger.error(f"[UG{self.id}] Erro na execução da máquina de estados -> step.\nException: {traceback.format_exc()}")
            raise e

    def interstep(self) -> None:
        try:
            if not self.avisou_emerg_voip and self.condicionador_caixa_espiral_ug.valor > 0.1:
                self.avisou_emerg_voip = True
            elif self.condicionador_caixa_espiral_ug.valor < 0.05:
                self.avisou_emerg_voip = False
        except Exception as e:
            logger.error(f"[UG{self.id}] Erro na execução da máquina de estados -> interstep.\nException: {traceback.format_exc()}")
            raise e

    def modbus_update_state_register(self) -> None:
        try:
            self.clp_moa.write_single_coil(self.cfg[f"REG_MOA_OUT_STATE_UG{self.id}"], [self.codigo_state])
            self.clp_moa.write_single_coil(self.cfg[f"REG_MOA_OUT_ETAPA_UG{self.id}"], [self.etapa_atual])
        except Exception as e:
            logger.error(f"[UG{self.id}] Não foi possível escrever os valores no CLP MOA.\nException: {traceback.format_exc()}")
            raise e

    def carregar_parametros(self, parametros: dict) -> None:
        try:
            for key, val in parametros.items():
                while not key[0:1] == "__":
                    key = "_" + key[:]
                setattr(self, key, val)
                logger.debug(f"[UG{self.id}] Variavél carregada: {key} = {val}.")
        except Exception as e:
            logger.error(f"[UG{self.id}] Não foi possível carregar os parâmetros.\nException: {traceback.format_exc()}")
            raise e

    def partir(self) -> bool:
        try:
            if self.clp_sa.read_coils(SA[f"REG_SA_EntradasDigitais_MXI_SA_QCAP_Disj52A{self.id}Fechado"])[0] != 0:
                logger.info(f"[UG{self.id}] O Disjuntor 52A{self.id} está aberto. Favor fechá-lo para partir a UG.")
                return True

            if not self.etapa_atual == UNIDADE_SINCRONIZADA:
                logger.info(f"[UG{self.id}] Enviando comando de partida.")
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_ResetGeral"], 1)
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_ResetRele700G"], 1)
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_ResetReleBloq86H"], 1)
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_ResetReleBloq86M"], 1)
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_ResetReleRT"], 1)
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_ResetRV"], 1)
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_Cala_Sirene"], 1)
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_IniciaPartida"], 1)
                self.enviar_setpoint(self.setpoint)
            else:
                logger.debug(f"[UG{self.id}] A UG já está sincronizada.")
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_Cala_Sirene"], 1)
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível partir a UG.\nException: \"{traceback.format_exc()}\"")
            return False
        else:
            return response

    def parar(self) -> bool:
        try:
            if not self.etapa_atual == UNIDADE_PARADA:
                logger.info(f"[UG{self.id}] Enviando comando de parada.")
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_AbortaPartida"], 1)
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_AbortaSincronismo"], 1)
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_Cala_Sirene"], 1)
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_IniciaParada"], 1)
                self.enviar_setpoint(0)
            else:
                logger.debug(f"[UG{self.id}] A unidade já está parada.")
                response = self.clp_ug.write_single_coil(UG["REG_UG1_ComandosDigitais_MXW_Cala_Sirene"], 1)
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível partir a UG.\nException: \"{traceback.format_exc()}\"")
            return False
        else:
            return response

    def enviar_setpoint(self, setpoint_kw: int) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Enviando setpoint {int(setpoint_kw)}kW.")
            self.setpoint = int(setpoint_kw)
            response = False
            if self.setpoint > 1:
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_ResetGeral"], 1)
                response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_RV_RefRemHabilita"], 1)
                response = self.clp_ug.write_single_register(UG[f"REG_UG{self.id}_SaidasAnalogicas_MWW_SPPotAtiva"], self.setpoint)
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o setpoint.\nException: {traceback.format_exc()}")
            return False
        else:
            return response

    def acionar_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Acionando TRIP -> Lógico.")
            response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_EmergenciaViaSuper"], 1)
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel acionar o TRIP lógico.\nException: {traceback.format_exc()}")
            return False
        else:
            return response

    def remover_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Removendo TRIP -> Lógico.")
            response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_ResetGeral"], 1)
            response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_EntradasDigitais_MXI_ReleBloqA86HAtuado"], 0)
            response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_RetornosDigitais_MXR_700G_Trip"], 0)
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível remover o TRIP lógico.\nException: \"{traceback.format_exc()}\"")
            return False
        else:
            return response

    def acionar_trip_eletrico(self) -> bool:
        try:
            self.enviar_trip_eletrico = True
            logger.debug(f"[UG{self.id}] Acionando TRIP -> Elétrico.")
            self.clp_moa.write_single_coil(self.cfg[f"REG_MOA_OUT_BLOCK_UG{self.id}"], [1])
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível acionar o TRIP elétrico.\nException: \"{traceback.format_exc()}\"")
            return False
        else:
            return True

    def remover_trip_eletrico(self) -> bool:
        try:
            if self.clp_sa.read_coils(SA["REG_SA_ComandosDigitais_MXW_Liga_DJ1"])[0] == 0:
                logger.debug(f"[UG{self.id}] Comando recebido -> Fechando DJ52L.")
                self.con.fechaDj52L()
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível fechar o DJ52L.\nException: \"{traceback.format_exc()}\"")

        try:
            self.enviar_trip_eletrico = False
            logger.debug(f"[UG{self.id}] Removendo TRIP -> Elétrico.")
            self.clp_moa.write_single_coil(self.cfg[f"REG_MOA_OUT_BLOCK_UG{self.id}"], [0])
            self.clp_moa.write_single_coil(self.cfg["REG_PAINEL_LIDO"], [0])
            response = self.clp_ug.write_single_coil(UG[f"REG_UG{self.id}_ComandosDigitais_MXW_Cala_Sirene"], 1)
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível remover o TRIP elétrico.\nException: \"{traceback.format_exc()}\"")
            return False
        else:
            return response

    def reconhece_reset_alarmes(self) -> bool:
        try:
            logger.info(f"[UG{self.id}] Enviando comando de reconhecer e resetar alarmes.")
            for x in range(3):
                logger.debug(f"[UG{self.id}] Tentativa: {x}/3")
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
                sleep(1)
                self.clp_moa.write_single_coil(self.cfg["REG_PAINEL_LIDO"], [0])
                sleep(1)
        except:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o comando de reconhecer e resetar alarmes.\nException: {traceback.format_exc()}")
            return False
        else:
            return True

    def forcar_estado_manual(self) -> bool:
        try:
            self.__next_state = StateManual(self)
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel forçar o estado manual.\nException: {traceback.format_exc()}")
            return False
        else:
            return True

    def forcar_estado_restrito(self) -> bool:
        try:
            self.__next_state = StateRestrito(self)
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel forçar o estado restrito.\nException: {traceback.format_exc()}")
            return False
        else:
            return True

    def forcar_estado_indisponivel(self) -> bool:
        try:
            self.__next_state = StateIndisponivel(self)
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel forçar o estado indisponível.\nException: {traceback.format_exc()}")
            return False
        else:
            return True

    def forcar_estado_disponivel(self) -> bool:
        try:
            self.reconhece_reset_alarmes()
            sleep(1)
            self.__next_state = StateDisponivel(self)
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel forçar o estado disponível.\nException: {traceback.format_exc()}")
            return False
        else:
            return True

    def controle_cx_espiral(self) -> None:
        self.cx_kp = (self.leitura_caixa_espiral.valor - self.cfg["press_cx_alvo"]) * self.cfg["cx_kp"]
        self.cx_ajuste_ie = (self.leitura_potencia.valor + self.leitura_potencia_outra_ug.valor) / self.cfg["pot_maxima_alvo"]
        self.cx_ki = self.cx_ajuste_ie - self.cx_kp

        erro_press_cx = 0
        erro_press_cx = self.leitura_caixa_espiral.valor - self.cfg["press_cx_alvo"]

        logger.debug(f"[UG{self.id}] Pressão Alvo: {self.pressao_alvo:0.3f}, Recente: {self.leitura_caixa_espiral.valor:0.3f}")

        self.cx_controle_p = self.cfg["cx_kp"] * erro_press_cx
        self.cx_controle_i = max(min((self.cfg["cx_ki"] * erro_press_cx) + self.cx_controle_i, 1), 0)
        saida_pi = self.cx_controle_p + self.cx_controle_i
        
        logger.debug(f"[UG{self.id}] PI: {saida_pi:0.3f} <-- P: {self.cx_controle_p:0.3f} + I: {self.cx_controle_i:0.3f}; ERRO={erro_press_cx}")

        self.cx_controle_ie = max(min(saida_pi + self.cx_ajuste_ie * self.cfg["cx_kie"], 1), 0)

        pot_alvo = max(min(round(self.cfg[f"pot_maxima_ug{self.id}"] * self.cx_controle_ie, 5), self.cfg[f"pot_maxima_ug{self.id}"],),self.cfg["pot_minima"],)

        logger.debug(f"[UG{self.id}] Pot alvo: {pot_alvo:0.3f}")

        self.enviar_setpoint(pot_alvo) if self.leitura_caixa_espiral.valor >= 15.5 else self.enviar_setpoint(0)

        try:
            self.db.insert_debug(
                datetime.now(pytz.timezone("Brazil/East")).timestamp(),
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
                0, # cp
                0, # ci
                0, # cd
                0, # cie
                self.setpoint,
                self.leitura_potencia.valor,
                self.leitura_setpoint_outra_ug.valor,
                self.leitura_setpoint_outra_ug.valor,
                0, # nivel
                erro_press_cx,
                1, # modo autonomo
                self.cfg["cx_kp"],
                self.cfg["cx_ki"],
                self.cfg["cx_kie"],
                self.cx_controle_ie,
            )
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel inserir dados no Banco.\nException: {traceback.format_exc()}")

    def controle_limites_operacao(self) -> None:
        fase_r = [self.leitura_temperatura_fase_R.valor, self.condicionador_temperatura_fase_r_ug.valor_base, self.condicionador_temperatura_fase_r_ug.valor_limite]
        fase_s = [self.leitura_temperatura_fase_S.valor, self.condicionador_temperatura_fase_s_ug.valor_base, self.condicionador_temperatura_fase_s_ug.valor_limite]
        fase_t = [self.leitura_temperatura_fase_T.valor, self.condicionador_temperatura_fase_t_ug.valor_base, self.condicionador_temperatura_fase_t_ug.valor_limite]
        nucleo_1 = [self.leitura_temperatura_nucleo_gerador_1.valor, self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base, self.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite]
        nucleo_2 = [self.leitura_temperatura_nucleo_gerador_2.valor, self.condicionador_temperatura_nucleo_gerador_2_ug.valor_base, self.condicionador_temperatura_nucleo_gerador_2_ug.valor_limite]
        nucleo_3 = [self.leitura_temperatura_nucleo_gerador_3.valor, self.condicionador_temperatura_nucleo_gerador_3_ug.valor_base, self.condicionador_temperatura_nucleo_gerador_3_ug.valor_limite]
        mancal_CR = [self.leitura_temperatura_mancal_casq_rad.valor, self.condicionador_temperatura_mancal_casq_rad_ug.valor_base, self.condicionador_temperatura_mancal_casq_rad_ug.valor_limite]
        mancal_CC = [self.leitura_temperatura_mancal_casq_comb.valor, self.condicionador_temperatura_mancal_casq_comb_ug.valor_base, self.condicionador_temperatura_mancal_casq_comb_ug.valor_limite]
        mancal_EC = [self.leitura_temperatura_mancal_escora_comb.valor, self.condicionador_temperatura_mancal_escora_comb_ug.valor_base, self.condicionador_temperatura_mancal_escora_comb_ug.valor_limite]
        caixa_espiral = [self.leitura_caixa_espiral.valor, self.condicionador_caixa_espiral_ug.valor_base, self.condicionador_caixa_espiral_ug.valor_limite]

        if fase_r[0] >= fase_r[1]:
            logger.warning(f"[UG{self.id}] A temperatura de Fase R da UG passou do valor base! ({fase_r[1]}C) | Leitura: {fase_r[0]}C")
        if fase_r[0] >= 0.9*(fase_r[2] - fase_r[1]) + fase_r[1]:
            logger.critical(f"[UG{self.id}] A temperatura de Fase R da UG está muito próxima do limite! ({fase_r[2]}C) | Leitura: {fase_r[0]}C")

        if fase_s[0] >= fase_s[1]:
            logger.warning(f"[UG{self.id}] A temperatura de Fase S da UG passou do valor base! ({fase_s[1]}C) | Leitura: {fase_s[0]}C")
        if fase_s[0] >= 0.9*(fase_s[2] - fase_s[1]) + fase_s[1]:
            logger.critical(f"[UG{self.id}] A temperatura de Fase S da UG está muito próxima do limite! ({fase_s[2]}C) | Leitura: {fase_s[0]}C")

        if fase_t[0] >= fase_t[1]:
            logger.warning(f"[UG{self.id}] A temperatura de Fase T da UG passou do valor base! ({fase_t[1]}C) | Leitura: {fase_t[0]}C")
        if fase_t[0] >= 0.9*(fase_t[2] - fase_t[1]) + fase_t[1]:
            logger.critical(f"[UG{self.id}] A temperatura de Fase T da UG está muito próxima do limite! ({fase_t[2]}C) | Leitura: {fase_t[0]}C")

        if nucleo_1[0] >= nucleo_1[1]:
            logger.warning(f"[UG{self.id}] A temperatura do Núcleo Gerador 1 da UG passou do valor base! ({nucleo_1[1]}C) | Leitura: {nucleo_1[0]}C")
        if nucleo_1[0] >= 0.9*(nucleo_1[2] - nucleo_1[1]) + nucleo_1[1]:
            logger.critical(f"[UG{self.id}] A temperatura do Núcleo Gerador 1 da UG está muito próxima do limite! ({nucleo_1[2]}C) | Leitura: {nucleo_1[0]}C")

        if nucleo_2[0] >= nucleo_2[1]:
            logger.warning(f"[UG{self.id}] A temperatura do Núcleo Gerador 2 da UG passou do valor base! ({nucleo_2[1]}C) | Leitura: {nucleo_2[0]}C")
        if nucleo_2[0] >= 0.9*(nucleo_2[2] - nucleo_2[1]) + nucleo_2[1]:
            logger.critical(f"[UG{self.id}] A temperatura do Núcleo Gerador 2 da UG está muito próxima do limite! ({nucleo_2[2]}C) | Leitura: {nucleo_2[0]}C")

        if nucleo_3[0] >= nucleo_3[1]:
            logger.warning(f"[UG{self.id}] A temperatura do Núcleo Gerador 3 da UG passou do valor base! ({nucleo_3[1]}C) | Leitura: {nucleo_3[0]}C")
        if nucleo_3[0] >= 0.9*(nucleo_3[2] - nucleo_3[1]) + nucleo_3[1]:
            logger.critical(f"[UG{self.id}] A temperatura do Núcleo Gerador 3 da UG está muito próxima do limite! ({nucleo_3[2]}C) | Leitura: {nucleo_3[0]}C")

        if mancal_CR[0] >= mancal_CR[1]:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Casquilho Radial da UG passou do valor base! ({mancal_CR[1]}C) | Leitura: {mancal_CR[0]}C")
        if mancal_CR[0] >= 0.9*(mancal_CR[2] - mancal_CR[1]) + mancal_CR[1]:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Casquilho Radial da UG está muito próxima do limite! ({mancal_CR[2]}C) | Leitura: {mancal_CR[0]}C")

        if mancal_CC[0] >= mancal_CC[1]:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Casquilho Combinado da UG passou do valor base! ({mancal_CC[1]}C) | Leitura: {mancal_CC[0]}C")
        if mancal_CC[0] >= 0.9*(mancal_CC[2] - mancal_CC[1]) + mancal_CC[1]:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Casquilho Combinado da UG está muito próxima do limite! ({mancal_CC[2]}C) | Leitura: {mancal_CC[0]}C")

        if mancal_EC[0] >= mancal_EC[1]:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Escora Combinado da UG passou do valor base! ({mancal_EC[1]}C) | Leitura: {mancal_EC[0]}C")
        if mancal_EC[0] >= 0.9*(mancal_EC[2] - mancal_EC[1]) + mancal_EC[1]:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Escora Combinado da UG está muito próxima do limite! ({mancal_EC[2]}C) | Leitura: {mancal_EC[0]}C")

        if caixa_espiral[0] <= caixa_espiral[1] and caixa_espiral[0] != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            logger.warning(f"[UG{self.id}] A pressão Caixa Espiral da UG passou do valor base! ({caixa_espiral[1]:03.2f} KGf/m2) | Leitura: {caixa_espiral[0]:03.2f}")
        if caixa_espiral[0] <= caixa_espiral[2]+0.9*(caixa_espiral[1] - caixa_espiral[2]) and caixa_espiral[0] != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            logger.critical(f"[UG{self.id}] A pressão Caixa Espiral da UG está muito próxima do limite! ({caixa_espiral[2]:03.2f} KGf/m2) | Leitura: {caixa_espiral[0]:03.2f} KGf/m2")

    def leituras_por_hora(self) -> None:
        raise NotImplementedError
