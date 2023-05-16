import sys
import pytz
import logging
import threading
import traceback
import subprocess

import src.mensageiro.dict as vd

from time import sleep, time
from datetime import  datetime, timedelta
from pyModbusTCP.client import ModbusClient

from src.Leituras import  *
from src.dicionarios.regs import *
from src.dicionarios.const import *

from src.banco_dados import Database
from src.mensageiro.voip import Voip
from src.conector import ConectorCampo
from src.agendamentos import Agendamentos
from src.unidade_geracao import UnidadeGeracao
from src.Condicionadores import CondicionadorBase

logger = logging.getLogger("__main__")

class Usina:
    def __init__(self, cfg=None, db: Database=None):

        if not cfg or not db:
            raise ValueError
        else:
            self.cfg = cfg
            self.db: Database = db

        self.clp: "dict[str, ModbusClient]" = {}

        self.clp["SA"] = ModbusClient(
            host=self.cfg["USN_slave_ip"],
            port=self.cfg["USN_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True
        )
        self.clp["TDA"] = ModbusClient(
            host=self.cfg["TDA_slave_ip"],
            port=self.cfg["TDA_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True
        )
        self.clp["MOA"] = ModbusClient(
            host=self.cfg["MOA_slave_ip"],
            port=self.cfg["MOA_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
        )
        self.clp["UG1"] = ModbusClient(
            host=self.cfg["UG1_slave_ip"],
            port=self.cfg["UG1_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
        )
        self.clp["UG2"] = ModbusClient(
            host=self.cfg["UG2_slave_ip"],
            port=self.cfg["UG2_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
        )
        self.clp["UG3"] = ModbusClient(
            host=self.cfg["UG3_slave_ip"],
            port=self.cfg["UG3_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
        )
        self.open_modbus()

        self.agn = Agendamentos(self.cfg, self.db)
        self.con = ConectorCampo(self.cfg, self.clp)

        self.ug1 = UnidadeGeracao(1, self.cfg, self.clp, self.db, self.con)
        self.ug2 = UnidadeGeracao(2, self.cfg, self.clp, self.db, self.con)
        self.ug3 = UnidadeGeracao(3, self.cfg, self.clp, self.db, self.con)
        self.ugs: "list[UnidadeGeracao]" = [self.ug1, self.ug2, self.ug3]
        for ug in self.ugs: ug.lista_ugs = self.ugs

        CondicionadorBase.ugs = self.ugs

        self._state_moa = 1

        self._modo_autonomo = False

        self.agendamentos_atrasados = 0
        self.modo_de_escolha_das_ugs = 0
        self.aguardando_reservatorio = 0
        self.tentativas_de_normalizar = 0

        self.hb_borda_emerg_ping = 0

        self.erro_nv = 0
        self.erro_nv_anterior = 0
        self.nv_montante_recente = 0
        self.nv_montante_anterior = 0

        self.controle_p = 0
        self.controle_i = 0
        self.controle_d = 0
        self.pid_inicial = -1

        self.pot_disp = 0
        self.ug_operando = 0
        self.pot_alvo_anterior = -1

        self.db_emergencia_acionada = 0
        self.clp_emergencia_acionada = 0

        self.tensao_ok = True
        self.timer_tensao = None
        self.TDA_Offline = False
        self.hb_borda_emerg = False
        self.acionar_voip_usn = False
        self.avisado_em_eletrica = False
        self.deve_tentar_normalizar = True
        self.deve_normalizar_forcado = False
        self.deve_ler_condicionadores = False

        self.ts_nv = []
        self.nv_montante_recentes = []
        self.nv_montante_anteriores = []

        self.condicionadores: "list[CondicionadorBase]" = []
        self.condicionadores_essenciais: "list[CondicionadorBase]" = []

        self.ts_last_ping_tda = self.get_time()
        self.ts_ultima_tentativa_normalizacao = self.get_time()

        self.ajustar_inicializacao()
        self.leituras_iniciais()
        self.ler_valores()
        self.escrever_valores()

    @property
    def nv_montante(self):
        return self._nv_montante.valor

    @property
    def modo_autonomo(self) -> bool:
        return self._modo_autonomo

    @modo_autonomo.setter
    def modo_autonomo(self, modo: bool) -> None:
        self._modo_autonomo = modo
        self.db.update_modo_moa(modo)

    @staticmethod
    def get_time() -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def ajustar_inicializacao(self) -> None:
        for ug in self.ugs:
            if ug.etapa_atual == UNIDADE_SINCRONIZADA:
                self.ug_operando += 1

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False
        self.__split3 = True if self.ug_operando == 3 else False

        self.controle_ie: int = sum(ug.leitura_potencia.valor for ug in self.ugs) / self.cfg["pot_maxima_alvo"]

        self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG1"], 0)
        self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG2"], 0)
        self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG3"], 0)

    def normalizar_emergencia(self) -> bool:
        logger.info("Normalizando Usina...")
        logger.debug(
            f"Tensão na linha: \
            RS {self.__tensao_rs.valor / 1000:2.1f}kV \
            ST {self.__tensao_st.valor / 1000:2.1f}kV \
            TR {self.__tensao_tr.valor / 1000:2.1f}kV."
        )

        if not self.verificar_tensao():
            self.tensao_ok = False
            return False

        elif self.deve_normalizar_forcado or (self.deve_tentar_normalizar and (self.get_time() - self.ts_ultima_tentativa_normalizacao).seconds >= 60 * self.tentativas_de_normalizar):
            self.tentativas_de_normalizar += 1
            self.ts_ultima_tentativa_normalizacao = self.get_time()
            self.con.TDA_Offline = True if self.TDA_Offline else False
            self.con.normalizar_emergencia()
            self.clp_emergencia_acionada = 0
            self.db.update_remove_emergencia()
            self.db_emergencia_acionada = 0
            return True

        else:
            logger.debug("A normalização foi executada menos de 1 minuto atrás.")
            self.tensao_ok = True
            return False

    def verificar_tensao(self) -> bool:
        try:
            if not(TENSAO_LINHA_BAIXA < self.__tensao_rs.valor < TENSAO_LINHA_ALTA \
                and TENSAO_LINHA_BAIXA < self.__tensao_st.valor < TENSAO_LINHA_ALTA \
                and TENSAO_LINHA_BAIXA < self.__tensao_tr.valor < TENSAO_LINHA_ALTA):
                return False
            else:
                return True

        except Exception:
            logger.error(f"Erro ao verificar tensão na linha.")
            return False

    def aguardar_tensao(self, delay) -> bool:
        temporizador = time() + delay
        logger.warning("Iniciando o timer para a normalização da tensão na linha")

        while time() <= temporizador:
            sleep(time() - (time() - 15))
            if self.verificar_tensao():
                self.timer_tensao = True
                return True

        logger.warning("Não foi possível reestabelecer a tensão na linha")
        self.timer_tensao = False
        return False

    def ler_valores(self) -> None:
        self.verificar_clps()

        if not self.TDA_Offline:
            if self.nv_montante_recente < 1:
                self.nv_montante_recentes = [self.nv_montante] * 240

            self.nv_montante_recentes.append(round(self.nv_montante, 2))
            self.nv_montante_recentes = self.nv_montante_recentes[1:]
            self.nv_montante_recente = self.nv_montante

            self.erro_nv_anterior = self.erro_nv
            self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

        if self.modo_autonomo:
            self.con.modifica_controles_locais()

        self.atualizar_parametros_operacao()
        self.heartbeat()

    def escrever_valores(self) -> None:
        try:
            v_params = [
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                1 if self.aguardando_reservatorio else 0,
                self.nv_montante if not self.TDA_Offline else 0,
                self.ug1.leitura_potencia.valor,
                self.ug1.setpoint,
                self.ug2.leitura_potencia.valor,
                self.ug2.setpoint,
                self.ug3.leitura_potencia.valor,
                self.ug3.setpoint,
            ]
            self.db.update_valores_usina(v_params)

        except Exception:
            logger.error(f"Houve um erro ao gravar os parâmetros da Usina no Banco.")
            logger.debug(f"Traceback: {traceback.format_exc()}")

        try:
            v_debug = [
                time(),
                1 if self.modo_autonomo else 0,
                self.nv_montante_recente,
                self.erro_nv,
                self.ug1.setpoint,
                self.ug1.leitura_potencia.valor,
                self.ug1.codigo_state,
                self.ug2.setpoint,
                self.ug2.leitura_potencia.valor,
                self.ug2.codigo_state,
                self.ug3.setpoint,
                self.ug3.leitura_potencia.valor,
                self.ug3.codigo_state,
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"]
            ]
            self.db.update_debug(v_debug)

        except Exception:
            logger.error(f"Houve um erro ao gravar os parâmetros debug no Banco.")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def heartbeat(self) -> None:
        self.clp["MOA"].write_single_coil(REG["PAINEL_LIDO"], [1])
        self.clp["MOA"].write_single_coil(REG["MOA_OUT_MODE"], [1 if self.modo_autonomo else 0])
        self.clp["MOA"].write_single_register(REG["MOA_OUT_STATUS"], self._state_moa)

        for ug in self.ugs: ug.modbus_update_state_register()

        if self.modo_autonomo:
            self.clp["MOA"].write_single_coil(REG["MOA_OUT_EMERG"], [1 if self.clp_emergencia_acionada else 0])
            self.clp["MOA"].write_single_coil(REG["MOA_OUT_TARGET_LEVEL"], [int((self.cfg["nv_alvo"] - 400) * 1000)])
            self.clp["MOA"].write_single_coil(REG["MOA_OUT_SETPOINT"], [int(sum(ug.setpoint for ug in self.ugs))])

            if self.clp["MOA"].read_coils(REG["MOA_IN_EMERG"]) == 1 and not self.avisado_em_eletrica:
                self.avisado_em_eletrica = True
                for ug in self.ugs: ug.deve_ler_condicionadores = True

            elif self.clp["MOA"].read_coils(REG["MOA_IN_EMERG"]) == 0 and self.avisado_em_eletrica:
                self.avisado_em_eletrica = False
                for ug in self.ugs: ug.deve_ler_condicionadores = False

            if self.clp["MOA"].read_coils(REG["MOA_IN_EMERG_UG1"]) == 1:
                self.ug1.deve_ler_condicionadores = True

            if self.clp["MOA"].read_coils(REG["MOA_IN_EMERG_UG2"]) == 1:
                self.ug2.deve_ler_condicionadores = True

            if self.clp["MOA"].read_coils(REG["MOA_IN_EMERG_UG3"]) == 1:
                self.ug3.deve_ler_condicionadores = True

            if self.clp["MOA"].read_coils(REG["MOA_IN_HABILITA_AUTO"]) == 1:
                self.clp["MOA"].write_single_coil(REG["MOA_IN_HABILITA_AUTO"], 1)
                self.clp["MOA"].write_single_coil(REG["MOA_IN_DESABILITA_AUTO"], 0)
                self.modo_autonomo = True

            if self.clp["MOA"].read_coils(REG["MOA_IN_DESABILITA_AUTO"]) == 1:
                self.clp["MOA"].write_single_coil(REG["MOA_IN_HABILITA_AUTO"], 0)
                self.clp["MOA"].write_single_coil(REG["MOA_IN_DESABILITA_AUTO"], 1)
                self.modo_autonomo = False

            if self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG1"]) == 1:
                self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG1"], 1)

            elif self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG1"]) == 0:
                self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG1"], 0)

            if self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG2"]) == 1:
                self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG2"], 1)

            elif self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG2"]) == 0:
                self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG2"], 0)

            if self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG3"]) == 1:
                self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG3"], 1)

            elif self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG3"]) == 0:
                self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG3"], 0)

        elif not self.modo_autonomo:
            if self.clp["MOA"].read_coils(REG["MOA_IN_HABILITA_AUTO"]) == 1:
                self.clp["MOA"].write_single_coil(REG["MOA_IN_HABILITA_AUTO"], 1)
                self.clp["MOA"].write_single_coil(REG["MOA_IN_DESABILITA_AUTO"], 0)
                self.modo_autonomo = True

            self.clp["MOA"].write_single_register(REG["MOA_OUT_TARGET_LEVEL"], int(0))
            self.clp["MOA"].write_single_register(REG["MOA_OUT_SETPOINT"], int(0))
            self.clp["MOA"].write_single_coil(REG["MOA_OUT_EMERG"], 0)
            self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG1"], 0)
            self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG2"], 0)
            self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG3"], 0)

    def atualizar_parametros_operacao(self) -> None:
        parametros = self.db.get_parametros_usina()

        self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
        self.cfg["kp"] = float(parametros["kp"])
        self.cfg["ki"] = float(parametros["ki"])
        self.cfg["kd"] = float(parametros["kd"])
        self.cfg["kie"] = float(parametros["kie"])
        self.cfg["pot_maxima_usina"] = float(parametros["pot_nominal_ug"]) * 3
        self.cfg["pot_maxima_alvo"] = float(parametros["pot_nominal"])
        self.cfg["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])
        self.cfg["margem_pot_critica"] = float(parametros["margem_pot_critica"])
        self.cfg["cx_kp"] = float(parametros["cx_kp"])
        self.cfg["cx_ki"] = float(parametros["cx_ki"])
        self.cfg["cx_kie"] = float(parametros["cx_kie"])
        self.cfg["press_cx_alvo"] = float(parametros["press_cx_alvo"])
        self.cfg["nv_minimo"] = float(parametros["nv_minimo"])

        self.db_emergencia_acionada = int(parametros["emergencia_acionada"])

        if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
            self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
            logger.debug(f"O modo de prioridade das ugs foi alterado (#{self.modo_de_escolha_das_ugs}).")

        if int(parametros["modo_autonomo"]) == 1 and not self.modo_autonomo:
            self.modo_autonomo = True
            logger.debug(f"Modo autônomo: \"{'Ativado'}\"")

        elif int(parametros["modo_autonomo"]) == 0 and self.modo_autonomo:
            self.modo_autonomo = False
            logger.debug(f"Modo autônomo: \"{'Desativado'}\"")

        for ug in self.ugs:
            ug.atualizar_limites_operacao(parametros)

    def lista_de_ugs_disponiveis(self) -> "list[UnidadeGeracao]":
        ls = []
        for ug in self.ugs:
            if ug.disponivel and ug.etapa_atual in UNIDADE_LISTA_DE_ETAPAS:
                ls.append(ug)

        if self.modo_de_escolha_das_ugs == MODO_ESCOLHA_MANUAL:
            #!!TODO: corrigir etapa_atual
            ls = sorted(ls, key=lambda y: (-1 * y.etapa_atual, -1 * y.leitura_potencia.valor, -1 * y.setpoint, y.prioridade))
            logger.debug("")
            logger.debug("UGs disponíveis em ordem (prioridade):")
        else:
            ls = sorted(ls, key=lambda y: (-1 * y.etapa_atual, y.leitura_horimetro.valor, -1 * y.leitura_potencia.valor, -1 * y.setpoint))
            # ls = sorted(ls, key=lambda y: (-1 * y.etapa_atual if y.etapa_atual == UNIDADE_SINCRONIZADA else y.leitura_horimetro.valor,
                                            #-1 * y.leitura_potencia.valor,
                                            #-1 * y.setpoint,),)
            logger.debug("")
            logger.debug("UGs disponíveis em ordem (horas-máquina):")

        return ls

    def calcular_pid_potencia(self) -> None:
        logger.debug("-------------------------------------------------")
        logger.debug(f"NÍVEL -> Leitura: {self.nv_montante_recente:0.3f}; Alvo: {self.cfg['nv_alvo']:0.3f}")

        self.controle_p = self.cfg["kp"] * self.erro_nv

        if self.pid_inicial == -1:
            self.controle_i = max(min(self.controle_ie - self.controle_p, 0.8), 0)
            self.pid_inicial = 0
        else:
            self.controle_i = max(min((self.cfg["ki"] * self.erro_nv) + self.controle_i, 0.8), 0)
            self.controle_d = self.cfg["kd"] * (self.erro_nv - self.erro_nv_anterior)

        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))
        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)

        logger.debug(f"PID -> {saida_pid:0.3f} P:{self.controle_p:0.3f} + I:{self.controle_i:0.3f} + D:{self.controle_d:0.3f}; ERRO={self.erro_nv}")

        if self.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if self.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"],), self.cfg["pot_minima"],)

        logger.debug(f"IE -> {self.controle_ie:0.3f}")
        logger.debug("")
        logger.debug(f"Potência alvo: {pot_alvo:0.3f}")

        pot_alvo = self.ajustar_potencia(pot_alvo)

    def ajustar_potencia(self, pot_alvo) -> None:
        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs:
                ug.setpoint = 0
            return 0

        pot_medidor = self.__potencia_ativa_kW.valor
        logger.debug(f"Potência no medidor: {pot_medidor:0.3f}")

        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])

        pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

        if pot_medidor > self.cfg["pot_maxima_alvo"] * 0.97 and pot_alvo >= self.cfg["pot_maxima_alvo"]:
            pot_alvo = self.pot_alvo_anterior * (1 - 0.5 * ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))

        self.pot_alvo_anterior = pot_alvo

        logger.debug(f"Potência alvo pós ajuste: {pot_alvo:0.3f}")

        self.distribuir_potencia(pot_alvo)

    def distribuir_potencia(self, pot_alvo) -> None:
        ugs = self.lista_de_ugs_disponiveis()
        self.pot_disp = 0
        self.ajuste_manual = 0

        for ug in ugs:
            logger.debug(f"UG{ug.id}")
            self.pot_disp += ug.cfg[f"pot_maxima_ug{ugs[0].id}"]

            if ug.manual:
                logger.debug(f"UG{ug.id} Manual -> {ug.leitura_potencia.valor}")
                self.ajuste_manual += ug.leitura_potencia.valor

        if ugs is None or len(ugs) == 0:
            return False

        logger.debug("")
        logger.debug(f"Distribuindo: {pot_alvo:0.3f}")

        sp = (pot_alvo - self.ajuste_manual) / self.cfg["pot_maxima_usina"]

        self.__split1 = True if sp > (0) else self.__split1
        self.__split2 = (True if sp > ((self.cfg["pot_maxima_ug"] / self.cfg["pot_maxima_usina"]) + self.cfg["margem_pot_critica"]) else self.__split2)
        self.__split3 = (True if sp > (2 * (self.cfg["pot_maxima_ug"] / self.cfg["pot_maxima_usina"]) + self.cfg["margem_pot_critica"]) else self.__split3)

        self.__split3 = False if sp < (2 * (self.cfg["pot_maxima_ug"] / self.cfg["pot_maxima_usina"]) - self.cfg["margem_pot_critica"]) else self.__split3
        self.__split2 = False if sp < ((self.cfg["pot_maxima_ug"] / self.cfg["pot_maxima_usina"]) - self.cfg["margem_pot_critica"]) else self.__split2
        self.__split1 = False if sp < (self.cfg["pot_minima"] / self.cfg["pot_maxima_usina"]) else self.__split1

        logger.debug(f"SP<-{sp}")
        if len(ugs) == 3:

            if self.__split3:
                logger.debug("Split 3")
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = sp * ugs[1].setpoint_maximo
                ugs[2].setpoint = sp * ugs[2].setpoint_maximo

            elif self.__split2:
                logger.debug("Split 2")
                sp = sp * 3 / 2
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = sp * ugs[1].setpoint_maximo
                ugs[2].setpoint = 0

            elif self.__split1:
                logger.debug("Split 1")
                sp = sp * 3 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = 0
                ugs[2].setpoint = 0

            else:
                for ug in ugs:
                    ug.setpoint = 0

        elif len(ugs) == 2:
            if self.__split2 or self.__split3:
                logger.debug("Split 2B")
                sp = sp * 3 / 2
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = sp * ugs[1].setpoint_maximo

            elif self.__split1:
                logger.debug("Split 1")
                sp = sp * 3 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = 0

            else:
                ugs[0].setpoint = 0
                ugs[1].setpoint = 0

        elif len(ugs) == 1:
            logger.debug("Split 3B")
            ugs[0].setpoint = 3 * sp * ugs[0].setpoint_maximo

        return pot_alvo

    def open_modbus(self) -> None:
        logger.debug("Opening Modbus")
        if not self.clp["UG1"].open():
            raise ConnectionError(f"Modbus client ({self.cfg['UG1_slave_ip']}:{self.cfg['UG1_slave_porta']}) failed to open.")

        if not self.clp["UG2"].open():
            raise ConnectionError(f"Modbus client ({self.cfg['UG2_slave_ip']}:{self.cfg['UG2_slave_porta']}) failed to open.")

        if not self.clp["UG3"].open():
            raise ConnectionError(f"Modbus client ({self.cfg['UG3_slave_ip']}:{self.cfg['UG3_slave_porta']}) failed to open.")

        if not self.clp["SA"].open():
            raise ConnectionError(f"Modbus client ({self.cfg['USN_slave_ip']}:{self.cfg['USN_slave_porta']}) failed to open.")

        if not self.clp["TDA"].open():
            raise ConnectionError(f"Modbus client ({self.cfg['TDA_slave_ip']}:{self.cfg['TDA_slave_porta']}) failed to open.")

        if not self.clp["MOA"].open():
            raise ConnectionError(f"Modbus client ({self.cfg['MOA_slave_ip']}:{self.cfg['MOA_slave_porta']}) failed to open.")

        logger.debug("Openned Modbus")

    def close_modbus(self) -> None:
        logger.debug("Closing Modbus")
        self.clp["UG1"].close()
        self.clp["UG2"].close()
        self.clp["UG3"].close()
        self.clp["SA"].close()
        self.clp["TDA"].close()
        logger.debug("Closed Modbus")

    def verificar_clps(self) -> None:
        if not ping(self.cfg["TDA_slave_ip"]):
            self.TDA_Offline = True
            self.db.update_tda_offline(True)
            if self.TDA_Offline and self.hb_borda_emerg_ping == 0:
                self.hb_borda_emerg_ping = 1
                logger.critical("CLP TDA não respondeu a tentativa de comunicação!")

        elif ping(self.cfg["TDA_slave_ip"]) and self.hb_borda_emerg_ping == 1:
            logger.info("Comunicação com o CLP TDA reestabelecida.")
            self.hb_borda_emerg_ping = 0
            self.TDA_Offline = False
            self.db.update_tda_offline(False)

        if not ping(self.cfg["USN_slave_ip"]):
            logger.critical("CLP SA não respondeu a tentativa de ping!")
        if self.clp["SA"].open():
            self.clp["SA"].close()
        else:
            logger.critical("CLP SA não respondeu a tentativa de conexão ModBus!")
            self.clp["SA"].close()

        if not ping(self.cfg["MOA_slave_ip"]):
            logger.warning("CLP MOA não respondeu a tentativa de ping!")
        if self.clp["MOA"].open():
            self.clp["MOA"].close()
        else:
            logger.warning("CLP MOA não respondeu a tentativa de conexão ModBus!")

        for ug in self.ugs:
            if not ping(self.cfg[f"UG{ug.id}_slave_ip"]):
                logger.critical(f"CLP UG{ug.id} não respondeu a tentativa de ping!")
                self.ug1.forcar_estado_manual()
            if self.clp[f"UG{ug.id}"].open():
                self.clp[f"UG{ug.id}"].close()
            else:
                self.ug1.forcar_estado_manual()
                logger.critical(f"CLP UG{ug.id} não respondeu a tentativa de conexão ModBus!")

    def leitura_periodica(self, delay: int) -> None:
        try:
            proxima_leitura = time() + delay
            while True:
                self.leituras_temporizadas()
                for ug in self.ugs: ug.leituras_temporizadas()

                if True in (vd.voip_dict[r][0] for r in vd.voip_dict):
                    Voip.acionar_chamada()
                    pass

                sleep(max(0, proxima_leitura - time()))

        except Exception:
            logger.error(f"Houve um problema ao executar a leitura periódica.")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def leituras_temporizadas(self) -> None:
        if self.leitura_ED_SA_QLCF_Disj52ETrip.valor != 0 and not vd.voip_dict["SA_QLCF_DISJ_52E_TRIP"][0]:
            logger.warning("O Disjuntor do Gerador Diesel de Emergência QLCF identificou um sinal de TRIP, favor verificar.")
            vd.voip_dict["SA_QLCF_DISJ_52E_TRIP"][0] = True
        elif self.leitura_ED_SA_QLCF_Disj52ETrip.valor == 0 and vd.voip_dict["SA_QLCF_DISJ_52E_TRIP"][0]:
            vd.voip_dict["SA_QLCF_DISJ_52E_TRIP"][0] = False

        if self.leitura_ED_SA_QLCF_TripDisjAgrup.valor != 0 and not vd.voip_dict["SA_QLCF_TRIP_DISJ_AGRUP"][0]:
            logger.warning("O sensor do Disjuntor de Agrupamento QLCF identificou um sinal de trip, favor verificar.")
            vd.voip_dict["SA_QLCF_TRIP_DISJ_AGRUP"][0] = True
        elif self.leitura_ED_SA_QLCF_TripDisjAgrup.valor == 0 and vd.voip_dict["SA_QLCF_TRIP_DISJ_AGRUP"][0]:
            vd.voip_dict["SA_QLCF_TRIP_DISJ_AGRUP"][0] = False

        if self.leitura_ED_SA_QCAP_SubtensaoBarraGeral.valor != 0 and not vd.voip_dict["SA_QCAP_SUBTENSAO_BARRA_GERAL"][0]:
            logger.warning("O sensor de Subtensão do Barramento Geral QCAP foi acionado, favor verificar.")
            vd.voip_dict["SA_QCAP_SUBTENSAO_BARRA_GERAL"][0] = True
        elif self.leitura_ED_SA_QCAP_SubtensaoBarraGeral.valor == 0 and vd.voip_dict["SA_QCAP_SUBTENSAO_BARRA_GERAL"][0]:
            vd.voip_dict["SA_QCAP_SUBTENSAO_BARRA_GERAL"][0] = False

        if self.leitura_ED_SA_GMG_Alarme.valor != 0 and not vd.voip_dict["SA_GMG_ALARME"][0]:
            logger.warning("O alarme do Grupo Motor Gerador foi acionado, favor verificar.")
            vd.voip_dict["SA_GMG_ALARME"][0] = True
        elif self.leitura_ED_SA_GMG_Alarme.valor == 0 and vd.voip_dict["SA_GMG_ALARME"][0]:
            vd.voip_dict["SA_GMG_ALARME"][0] = False

        if self.leitura_ED_SA_GMG_Trip.valor != 0 and not vd.voip_dict["SA_GMG_TRIP"][0]:
            logger.warning("O sensor de TRIP do Grupo Motor Gerador foi acionado, favor verificar.")
            vd.voip_dict["SA_GMG_TRIP"][0] = True
        elif self.leitura_ED_SA_GMG_Trip.valor == 0 and vd.voip_dict["SA_GMG_TRIP"][0]:
            vd.voip_dict["SA_GMG_TRIP"][0] = False

        if self.leitura_ED_SA_GMG_Operacao.valor != 0 and not vd.voip_dict["SA_GMG_OPERACAO"][0]:
            logger.warning("O sensor de operação do Grupo Motor Gerador foi acionado, favor verificar.")
            vd.voip_dict["SA_GMG_OPERACAO"][0] = True
        elif self.leitura_ED_SA_GMG_Operacao.valor == 0 and vd.voip_dict["SA_GMG_OPERACAO"][0]:
            vd.voip_dict["SA_GMG_OPERACAO"][0] = False

        if self.leitura_ED_SA_GMG_BaixoComb.valor != 0 and not vd.voip_dict["SA_GMG_BAIXO_COMB"][0]:
            logger.warning("O sensor de de combustível do Grupo Motor Gerador retornou que o nível está baixo, favor reabastercer o gerador.")
            vd.voip_dict["SA_GMG_BAIXO_COMB"][0] = True
        elif self.leitura_ED_SA_GMG_BaixoComb.valor == 0 and vd.voip_dict["SA_GMG_BAIXO_COMB"][0]:
            vd.voip_dict["SA_GMG_BAIXO_COMB"][0] = False

        if self.leitura_RD_BbaDren1_FalhaAcion.valor != 0 and not vd.voip_dict["BBA_DREN_1_FALHA_ACION"][0]:
            logger.warning("O sensor da Bomba de Drenagem 1 identificou uma falha no acionamento, favor verificar.")
            vd.voip_dict["BBA_DREN_1_FALHA_ACION"][0] = True
        elif self.leitura_RD_BbaDren1_FalhaAcion.valor == 0 and vd.voip_dict["BBA_DREN_1_FALHA_ACION"][0]:
            vd.voip_dict["BBA_DREN_1_FALHA_ACION"][0] = False

        if self.leitura_RD_BbaDren2_FalhaAcion.valor != 0 and not vd.voip_dict["BBA_DREN_2_FALHA_ACION"][0]:
            logger.warning("O sensor da Bomba de Drenagem 2 identificou uma falha no acionamento, favor verificar.")
            vd.voip_dict["BBA_DREN_2_FALHA_ACION"][0] = True
        elif self.leitura_RD_BbaDren2_FalhaAcion.valor == 0 and vd.voip_dict["BBA_DREN_2_FALHA_ACION"][0]:
            vd.voip_dict["BBA_DREN_2_FALHA_ACION"][0] = False

        if self.leitura_RD_BbaDren3_FalhaAcion.valor != 0 and not vd.voip_dict["BBA_DREN_3_FALHA_ACION"][0]:
            logger.warning("O sensor da Bomba de Drenagem 3 identificou uma falha no acionamento, favor verificar.")
            vd.voip_dict["BBA_DREN_3_FALHA_ACION"][0] = True
        elif self.leitura_RD_BbaDren3_FalhaAcion.valor == 0 and vd.voip_dict["BBA_DREN_3_FALHA_ACION"][0]:
            vd.voip_dict["BBA_DREN_3_FALHA_ACION"][0] = False

        if self.leitura_RD_SA_GMG_FalhaAcion.valor != 0 and not vd.voip_dict["SA_GMG_FALHA_ACION"][0]:
            logger.warning("O sensor do Grupo Motor Gerador identificou uma falha no acionamento, favor verificar.")
            vd.voip_dict["SA_GMG_FALHA_ACION"][0] = True
        elif self.leitura_RD_SA_GMG_FalhaAcion.valor == 0 and vd.voip_dict["SA_GMG_FALHA_ACION"][0]:
            vd.voip_dict["SA_GMG_FALHA_ACION"][0] = False

        if self.leitura_RD_FalhaComunSETDA.valor == 1 and not vd.voip_dict["FALHA_COMUM_SETDA"][0]:
            logger.warning("Houve uma falha de comunicação com o CLP da Subestação e o CLP da Tomada da Água, favor verificar")
            vd.voip_dict["FALHA_COMUM_SETDA"][0] = True
        elif self.leitura_RD_FalhaComunSETDA.valor == 0 and vd.voip_dict["FALHA_COMUM_SETDA"][0]:
            vd.voip_dict["FALHA_COMUM_SETDA"][0] = False

        if self.leitura_ED_SA_QCAP_Disj52EFechado.valor == 1 and not vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0]:
            logger.warning("O Disjuntor do Gerador Diesel de Emergência QLCF foi fechado.")
            vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0] = True
        elif self.leitura_ED_SA_QCAP_Disj52EFechado.valor == 0 and vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0]:
            vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"][0] = False

        if self.leitura_ED_SA_QCADE_BombasDng_Auto.valor == 0 and not vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0]:
            logger.warning("O poço de drenagem da Usina entrou em modo remoto, favor verificar.")
            vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0] = True
        elif self.leitura_ED_SA_QCADE_BombasDng_Auto.valor == 1 and vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0]:
            vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"][0] = False

    def leituras_iniciais(self) -> None:
        # leituras de sistemas essenciais para a operação
        self.__potencia_ativa_kW = LeituraModbus(
            "SA_EA_Medidor_potencia_kw_mp",
            self.clp["SA"],
            REG["SA_EA_PM_810_Potencia_Ativa"],
            1,
            op=4,
        )
        self.__tensao_rs = LeituraModbus(
            "SA_EA_PM_810_Tensao_AB",
            self.clp["SA"],
            REG["SA_EA_PM_810_Tensao_ab"],
            100,
            op=4,
        )
        self.__tensao_st = LeituraModbus(
            "SA_EA_PM_810_Tensao_BC",
            self.clp["SA"],
            REG["SA_EA_PM_810_Tensao_bc"],
            100,
            op=4,
        )
        self.__tensao_tr = LeituraModbus(
            "SA_EA_PM_810_Tensao_CA",
            self.clp["SA"],
            REG["SA_EA_PM_810_Tensao_ca"],
            100,
            op=4,
        )
        self._nv_montante = LeituraModbus(
            "TDA_EntradasAnalogicas_MRR_NivelMaisCasasAntes",
            self.clp["TDA"],
            REG["TDA_EA_NivelAntesGrade"],
            1 / 10000,
            400,
            op=4,
        )

        # Leituras para acionamento periódico
        self.leitura_ED_SA_GMG_Trip = LeituraModbusCoil("ED_SA_GMG_Trip", self.clp["SA"], REG["SA_ED_GMG_Trip"])
        self.leitura_ED_SA_GMG_Alarme = LeituraModbusCoil("ED_SA_GMG_Alarme", self.clp["SA"], REG["SA_ED_GMG_Alarme"])
        self.leitura_ED_SA_GMG_Operacao = LeituraModbusCoil("ED_SA_GMG_Operacao", self.clp["SA"], REG["SA_ED_GMG_Operacao"])
        self.leitura_RD_FalhaComunSETDA = LeituraModbusCoil("RD_FalhaComunSETDA", self.clp["SA"], REG["SA_RD_FalhaComunSETDA"])
        self.leitura_ED_SA_GMG_BaixoComb = LeituraModbusCoil("ED_SA_GMG_BaixoComb", self.clp["SA"], REG["SA_ED_GMG_BaixoComb"])
        self.leitura_RD_SA_GMG_FalhaAcion = LeituraModbusCoil("RD_SA_GMG_FalhaAcion", self.clp["SA"], REG["SA_RD_GMG_FalhaAcion"])
        self.leitura_ED_SA_QLCF_Disj52ETrip = LeituraModbusCoil("ED_SA_QLCF_Disj52ETrip", self.clp["SA"], REG["SA_ED_QLCF_Disj52ETrip"])
        self.leitura_RD_BbaDren1_FalhaAcion = LeituraModbusCoil("RD_BbaDren1_FalhaAcion", self.clp["SA"], REG["SA_RD_BbaDren1_FalhaAcion"])
        self.leitura_RD_BbaDren2_FalhaAcion = LeituraModbusCoil("RD_BbaDren2_FalhaAcion", self.clp["SA"], REG["SA_RD_BbaDren2_FalhaAcion"])
        self.leitura_RD_BbaDren3_FalhaAcion = LeituraModbusCoil("RD_BbaDren3_FalhaAcion", self.clp["SA"], REG["SA_RD_BbaDren3_FalhaAcion"])
        self.leitura_ED_SA_QLCF_TripDisjAgrup = LeituraModbusCoil("ED_SA_QLCF_TripDisjAgrup", self.clp["SA"], REG["SA_ED_QLCF_TripDisjAgrup"])
        self.leitura_ED_SA_QCAP_Disj52EFechado = LeituraModbusCoil("ED_SA_QCAP_Disj52EFechado", self.clp["SA"], REG["SA_ED_QCAP_Disj52EFechado"])
        self.leitura_ED_SA_QCADE_BombasDng_Auto = LeituraModbusCoil("ED_SA_QCADE_BombasDng_Auto", self.clp["SA"], REG["SA_ED_QCADE_BombasDng_Auto"])
        self.leitura_ED_SA_QCAP_SubtensaoBarraGeral = LeituraModbusCoil("ED_SA_QCAP_SubtensaoBarraGeral", self.clp["SA"], REG["SA_ED_QCAP_SubtensaoBarraGeral"])

        ### CONDICIONADORES ESSENCIAIS
        self.leitura_ED_SA_QCAP_TensaoPresenteTSA = LeituraModbusCoil("ED_SA_QCAP_TensaoPresenteTSA", self.clp["SA"], REG["SA_ED_QCAP_TensaoPresenteTSA"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_QCAP_TensaoPresenteTSA.descr, DEVE_NORMALIZAR, self.leitura_ED_SA_QCAP_TensaoPresenteTSA))

        self.leitura_ED_SA_SEL787_Trip = LeituraModbusCoil("ED_SA_SEL787_Trip", self.clp["SA"], REG["SA_ED_SEL787_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_SEL787_Trip.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_SEL787_Trip))

        self.leitura_ED_SA_SEL311_Trip = LeituraModbusCoil("ED_SA_SEL311_Trip", self.clp["SA"], REG["SA_ED_SEL311_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_SEL311_Trip.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_SEL311_Trip))

        self.leitura_ED_SA_MRU3_Trip = LeituraModbusCoil("ED_SA_MRU3_Trip", self.clp["SA"], REG["SA_ED_MRU3_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_MRU3_Trip.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_MRU3_Trip))

        self.leitura_ED_SA_MRL1_Trip = LeituraModbusCoil("ED_SA_MRL1_Trip", self.clp["SA"], REG["SA_ED_MRL1_Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_MRL1_Trip.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_MRL1_Trip))

        self.leitura_ED_SA_QCADE_Disj52E1Trip = LeituraModbusCoil("ED_SA_QCADE_Disj52E1Trip", self.clp["SA"], REG["SA_ED_QCADE_Disj52E1Trip"])
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Disj52E1Trip.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_QCADE_Disj52E1Trip))

        ### CONDICIONADORES NORMAIS
        if not self.TDA_Offline:
            self.leitura_ED_TDA_QcataDisj52ETrip = LeituraModbusCoil("ED_TDA_QcataDisj52ETrip", self.clp["TDA"], REG["TDA_ED_QcataDisj52ETrip"])
            self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52ETrip.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_TDA_QcataDisj52ETrip))

            self.leitura_ED_TDA_QcataDisj52ETripDisjSai = LeituraModbusCoil("ED_TDA_QcataDisj52ETripDisjSai", self.clp["TDA"], REG["TDA_ED_QcataDisj52ETripDisjSai"])
            self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52ETripDisjSai.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_TDA_QcataDisj52ETripDisjSai))

            self.leitura_ED_TDA_QcataDisj52EFalha380VCA = LeituraModbusCoil("ED_TDA_QcataDisj52EFalha380VCA", self.clp["TDA"], REG["TDA_ED_QcataDisj52EFalha380VCA"])
            self.condicionadores.append(CondicionadorBase(self.leitura_ED_TDA_QcataDisj52EFalha380VCA.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_TDA_QcataDisj52EFalha380VCA))

        self.leitura_ED_SA_MRU3_Falha = LeituraModbusCoil("ED_SA_MRU3_Falha", self.clp["SA"], REG["SA_ED_MRU3_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_MRU3_Falha.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_MRU3_Falha))

        self.leitura_ED_SA_SEL787_FalhaInterna = LeituraModbusCoil("ED_SA_SEL787_FalhaInterna", self.clp["SA"], REG["SA_ED_SEL787_FalhaInterna"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_SEL787_FalhaInterna.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_SEL787_FalhaInterna))

        self.leitura_ED_SA_SEL311_Falha = LeituraModbusCoil("ED_SA_SEL311_Falha", self.clp["SA"], REG["SA_ED_SEL311_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_SEL311_Falha.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_SEL311_Falha))

        self.leitura_ED_SA_CTE_Falta125Vcc = LeituraModbusCoil("ED_SA_CTE_Falta125Vcc", self.clp["SA"], REG["SA_ED_CTE_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CTE_Falta125Vcc.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_CTE_Falta125Vcc))

        self.leitura_ED_SA_CTE_Secc89TE_Aberta = LeituraModbusCoil("ED_SA_CTE_Secc89TE_Aberta", self.clp["SA"], REG["SA_ED_CTE_Secc89TE_Aberta"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CTE_Secc89TE_Aberta.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_CTE_Secc89TE_Aberta))

        self.leitura_ED_SA_TE_AlarmeDetectorGas = LeituraModbusCoil("ED_SA_TE_AlarmeDetectorGas", self.clp["SA"], REG["SA_ED_TE_AlarmeDetectorGas"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeDetectorGas.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeDetectorGas))

        self.leitura_ED_SA_TE_AlarmeNivelMaxOleo = LeituraModbusCoil("ED_SA_TE_AlarmeNivelMaxOleo", self.clp["SA"], REG["SA_ED_TE_AlarmeNivelMaxOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeNivelMaxOleo.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeNivelMaxOleo))

        self.leitura_ED_SA_TE_AlarmeAlivioPressao = LeituraModbusCoil("ED_SA_TE_AlarmeAlivioPressao", self.clp["SA"], REG["SA_ED_TE_AlarmeAlivioPressao"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeAlivioPressao.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeAlivioPressao))

        self.leitura_ED_SA_TE_AlarmeTempOleo = LeituraModbusCoil("ED_SA_TE_AlarmeTempOleo", self.clp["SA"], REG["SA_ED_TE_AlarmeTempOleo"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeTempOleo.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeTempOleo))

        self.leitura_ED_SA_TE_AlarmeTempEnrolamento = LeituraModbusCoil("ED_SA_TE_AlarmeTempEnrolamento", self.clp["SA"], REG["SA_ED_TE_AlarmeTempEnrolamento"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeTempEnrolamento.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeTempEnrolamento))

        self.leitura_ED_SA_TE_AlarmeDesligamento = LeituraModbusCoil("ED_SA_TE_AlarmeDesligamento", self.clp["SA"], REG["SA_ED_TE_AlarmeDesligamento"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_AlarmeDesligamento.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_TE_AlarmeDesligamento))

        self.leitura_ED_SA_TE_Falha = LeituraModbusCoil("ED_SA_TE_Falha", self.clp["SA"], REG["SA_ED_TE_Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_TE_Falha.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_TE_Falha))

        self.leitura_ED_SA_FalhaDisjTPsProt = LeituraModbusCoil("ED_SA_FalhaDisjTPsProt", self.clp["SA"], REG["SA_ED_FalhaDisjTPsProt"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsProt.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_FalhaDisjTPsProt))

        self.leitura_ED_SA_FalhaDisjTPsSincr = LeituraModbusCoil("ED_SA_FalhaDisjTPsSincr", self.clp["SA"], REG["SA_ED_FalhaDisjTPsSincr"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_FalhaDisjTPsSincr.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_FalhaDisjTPsSincr))

        self.leitura_ED_SA_CSA1_Secc_Aberta = LeituraModbusCoil("ED_SA_CSA1_Secc_Aberta", self.clp["SA"], REG["SA_ED_CSA1_Secc_Aberta"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_Secc_Aberta.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_CSA1_Secc_Aberta))

        self.leitura_ED_SA_CSA1_FusivelQueimado = LeituraModbusCoil("ED_SA_CSA1_FusivelQueimado", self.clp["SA"], REG["SA_ED_CSA1_FusivelQueimado"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_FusivelQueimado.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_CSA1_FusivelQueimado))

        self.leitura_ED_SA_CSA1_FaltaTensao125Vcc = LeituraModbusCoil("ED_SA_CSA1_FaltaTensao125Vcc", self.clp["SA"], REG["SA_ED_CSA1_FaltaTensao125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_CSA1_FaltaTensao125Vcc.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_CSA1_FaltaTensao125Vcc))

        self.leitura_ED_SA_QCADE_Nivel4 = LeituraModbusCoil("ED_SA_QCADE_Nivel4", self.clp["SA"], REG["SA_ED_QCADE_Nivel4"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Nivel4.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_QCADE_Nivel4))

        self.leitura_ED_SA_QCADE_NivelMuitoAlto = LeituraModbusCoil("ED_SA_QCADE_NivelMuitoAlto", self.clp["SA"], REG["SA_ED_QCADE_NivelMuitoAlto"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_NivelMuitoAlto.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_QCADE_NivelMuitoAlto))

        self.leitura_ED_SA_QCADE_Falha220VCA = LeituraModbusCoil("ED_SA_QCADE_Falha220VCA", self.clp["SA"], REG["SA_ED_QCADE_Falha220VCA"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCADE_Falha220VCA.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_QCADE_Falha220VCA))

        # Verificar
        self.leitura_ED_SA_QCCP_Disj72ETrip = LeituraModbusCoil("ED_SA_QCCP_Disj72ETrip", self.clp["SA"], REG["SA_ED_QCCP_Disj72ETrip"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_Disj72ETrip.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_QCCP_Disj72ETrip))

        self.leitura_ED_SA_QCCP_Falta125Vcc = LeituraModbusCoil("ED_SA_QCCP_Falta125Vcc", self.clp["SA"], REG["SA_ED_QCCP_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_Falta125Vcc.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_QCCP_Falta125Vcc))

        self.leitura_ED_SA_QCCP_TripDisjAgrup = LeituraModbusCoil("ED_SA_QCCP_TripDisjAgrup", self.clp["SA"], REG["SA_ED_QCCP_TripDisjAgrup"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCCP_TripDisjAgrup.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_QCCP_TripDisjAgrup))

        self.leitura_ED_SA_QCAP_Falta125Vcc = LeituraModbusCoil("ED_SA_QCAP_Falta125Vcc", self.clp["SA"], REG["SA_ED_QCAP_Falta125Vcc"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Falta125Vcc.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_QCAP_Falta125Vcc))

        self.leitura_ED_SA_QCAP_TripDisjAgrup = LeituraModbusCoil("ED_SA_QCAP_TripDisjAgrup", self.clp["SA"], REG["SA_ED_QCAP_TripDisjAgrup"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_TripDisjAgrup.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_QCAP_TripDisjAgrup))

        self.leitura_ED_SA_QCAP_Disj52A1Falha = LeituraModbusCoil("ED_SA_QCAP_Disj52A1Falha", self.clp["SA"], REG["SA_ED_QCAP_Disj52A1Falha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Disj52A1Falha.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_QCAP_Disj52A1Falha))

        self.leitura_ED_SA_QCAP_Disj52EFalha = LeituraModbusCoil("ED_SA_QCAP_Disj52EFalha", self.clp["SA"], REG["SA_ED_QCAP_Disj52EFalha"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_QCAP_Disj52EFalha.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_QCAP_Disj52EFalha))

        self.leitura_ED_SA_GMG_DisjFechado = LeituraModbusCoil("ED_SA_GMG_DisjFechado", self.clp["SA"], REG["SA_ED_GMG_DisjFechado"])
        self.condicionadores.append(CondicionadorBase(self.leitura_ED_SA_GMG_DisjFechado.descr, DEVE_INDISPONIBILIZAR, self.leitura_ED_SA_GMG_DisjFechado))

        self.leitura_RD_DJ1_FalhaInt = LeituraModbusCoil("RD_DJ1_FalhaInt", self.clp["SA"], REG["SA_RD_DJ1_FalhaInt"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_DJ1_FalhaInt.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_DJ1_FalhaInt))

        self.leitura_RD_CLP_Falha = LeituraModbusCoil("RD_CLP_Falha", self.clp["SA"], REG["SA_RD_FalhaComuCLP"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RD_CLP_Falha.descr, DEVE_INDISPONIBILIZAR, self.leitura_RD_CLP_Falha))

        self.leitura_RA_SEL787_Targets = LeituraModbusCoil("RA_SEL787_Targets", self.clp["SA"], REG["SA_RA_SEL787_Targets"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets.descr, DEVE_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets))

        self.leitura_RA_SEL787_Targets_Links_Bit00 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit00", self.clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit00"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit00.descr, DEVE_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit00))

        self.leitura_RA_SEL787_Targets_Links_Bit01 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit01", self.clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit01"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit01.descr, DEVE_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit01))

        self.leitura_RA_SEL787_Targets_Links_Bit02 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit02", self.clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit02"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit02.descr, DEVE_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit02))

        self.leitura_RA_SEL787_Targets_Links_Bit03 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit03", self.clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit03"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit03.descr, DEVE_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit03))

        self.leitura_RA_SEL787_Targets_Links_Bit04 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit04", self.clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit04"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit04.descr, DEVE_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit04))

        self.leitura_RA_SEL787_Targets_Links_Bit05 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit05", self.clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit05"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit05.descr, DEVE_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit05))

        self.leitura_RA_SEL787_Targets_Links_Bit06 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit06", self.clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit06"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit06.descr, DEVE_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit06))

        self.leitura_RA_SEL787_Targets_Links_Bit07 = LeituraModbusCoil("RA_SEL787_Targets_Links_Bit07", self.clp["SA"], REG["SA_RA_SEL787_Targets_Links_Bit07"])
        self.condicionadores.append(CondicionadorBase(self.leitura_RA_SEL787_Targets_Links_Bit07.descr, DEVE_INDISPONIBILIZAR, self.leitura_RA_SEL787_Targets_Links_Bit07))


def ping(host):
    ping = False
    for i in range(2):
        ping = ping or (subprocess.call(["ping", "-c", "1", "-w", "1", host], stdout=subprocess.PIPE) == 0)
        if not ping:
            pass
    return ping
