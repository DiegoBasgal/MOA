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

from src.codes import *
from src.Leituras import  *
from src.mapa_modbus import *

from src.mensageiro.voip import Voip
from src.UG1 import UnidadeDeGeracao1
from src.UG2 import UnidadeDeGeracao2
from src.UG3 import UnidadeDeGeracao3
from src.database_connector import Database
from src.field_connector import FieldConnector
from src.Condicionadores import CondicionadorBase

logger = logging.getLogger("__main__")

class Usina:
    def __init__(self, cfg=None, db: Database=None):

        if not cfg or not db:
            raise ValueError
        else:
            self.cfg = cfg
            self.db: Database = db

        self.con = FieldConnector(self.cfg)

        self.clp: "dict[str, ModbusClient]" = {}

        self.clp["SA"] = ModbusClient(
            host=self.cfg["USN_slave_ip"],
            port=self.cfg["USN_slave_porta"],
            timeout=0.5,
            unit_id=1
        )
        self.clp["TDA"] = ModbusClient(
            host=self.cfg["TDA_slave_ip"],
            port=self.cfg["TDA_slave_porta"],
            timeout=0.5,
            unit_id=1
        )
        self.clp["MOA"] = ModbusClient(
            host=self.cfg["MOA_slave_ip"],
            port=self.cfg["MOA_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True
        )
        self.clp["UG1"] = ModbusClient(
            host=self.cfg["UG1_slave_ip"],
            port=self.cfg["UG1_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True
        )
        self.clp["UG2"] = ModbusClient(
            host=self.cfg["UG2_slave_ip"],
            port=self.cfg["UG2_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True
        )
        self.clp["UG3"] = ModbusClient(
            host=self.cfg["UG3_slave_ip"],
            port=self.cfg["UG3_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True
        )
        self.open_modbus()

        self.__potencia_ativa_kW = LeituraModbus(
            "REG_SA_RetornosAnalogicos_Medidor_potencia_kw_mp",
            self.clp["SA"],
            REG_SA_RA_PM_810_Potencia_Ativa,
            1,
            op=4,
        )
        self.__tensao_rs = LeituraModbus(
            "REG_SA_RA_PM_810_Tensao_AB",
            self.clp["SA"],
            REG_SA_RA_PM_810_Tensao_AB,
            100,
            op=4,
        )
        self.__tensao_st = LeituraModbus(
            "REG_SA_RA_PM_810_Tensao_BC",
            self.clp["SA"],
            REG_SA_RA_PM_810_Tensao_BC,
            100,
            op=4,
        )
        self.__tensao_tr = LeituraModbus(
            "REG_SA_RA_PM_810_Tensao_CA",
            self.clp["SA"],
            REG_SA_RA_PM_810_Tensao_CA,
            100,
            op=4,
        )
        self._nv_montante = LeituraModbus(
            "REG_TDA_EntradasAnalogicas_MRR_NivelMaisCasasAntes",
            self.clp["TDA"],
            REG_TDA_NivelMaisCasasAntes,
            1 / 10000,
            400,
            op=4,
        )

        """
        self.potencia_ativa_kW = LeituraNBRPower(
            "LeituraNBRPower potencia_ativa_kW",
            ip_1=cfg["MP_ip"],
            port_1=cfg["MP_port"],
            ip_2=cfg["MR_ip"],
            port_2=cfg["MR_port"],
            escala=cfg["MPMR_scale"],
        )
        """

        # Inicializa Objs da usina
        self.ug1 = UnidadeDeGeracao1(1, self.cfg, self.clp, self.db, self.con)
        self.ug2 = UnidadeDeGeracao2(2, self.cfg, self.clp, self.db, self.con)
        self.ug3 = UnidadeDeGeracao3(3, self.cfg, self.clp, self.db, self.con)
        self.ugs: list[UnidadeDeGeracao1 or UnidadeDeGeracao2 or UnidadeDeGeracao3] = [self.ug1, self.ug2, self.ug3]
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

        for ug in self.ugs:
            if ug.etapa_atual == UNIDADE_SINCRONIZADA:
                self.ug_operando += 1

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False
        self.__split3 = True if self.ug_operando == 3 else False

        self.controle_ie: int = sum(ug.leituras_ug[f"leitura_potencia_ug{ug.id}"].valor for ug in self.ugs) / self.cfg["pot_maxima_alvo"]

        self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG1"], 0)
        self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG2"], 0)
        self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG3"], 0)

        threading.Thread(target=lambda: self.leitura_condicionadores()).start()
        self.ler_valores()
        self.atualizar_limites_operacao(self.db.get_parametros_usina())
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

    def open_modbus(self):
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
        return self

    def close_modbus(self):
        logger.debug("Closing Modbus")
        self.clp["UG1"].close()
        self.clp["UG2"].close()
        self.clp["UG3"].close()
        self.clp["SA"].close()
        self.clp["TDA"].close()
        logger.debug("Closed Modbus")

    def ler_valores(self):
        self.ping_clps()

        self.clp_emergencia_acionada = 0

        if not self.TDA_Offline:
            if self.nv_montante_recente < 1:
                self.nv_montante_recentes = [self.nv_montante] * 240

            self.nv_montante_recentes.append(round(self.nv_montante, 2))
            self.nv_montante_recentes = self.nv_montante_recentes[1:]
            self.nv_montante_recente = self.nv_montante

            self.erro_nv_anterior = self.erro_nv
            self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

        parametros = self.db.get_parametros_usina()

        # Limites de operação das UGS
        self.atualizar_limites_operacao(parametros)

        self.cfg["nv_minimo"] = float(parametros["nv_minimo"])
        self.db_emergencia_acionada = int(parametros["emergencia_acionada"])

        if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
            self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
            logger.debug(f"O modo de prioridade das ugs foi alterado (#{self.modo_de_escolha_das_ugs}).")

        self.modo_autonomo = True if int(parametros["modo_autonomo"]) == 1 else False
        logger.debug(f"Modo autônomo: \"{'Ativado' if int(parametros['modo_autonomo']) == 1 else 'Desativado'}\"")

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

        self.heartbeat()

    def escrever_valores(self):

        if self.modo_autonomo:
            self.con.TDA_Offline = True if self.TDA_Offline else False
            self.con.modifica_controles_locais()

        try:
            valores = [
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),  # timestamp
                1 if self.aguardando_reservatorio else 0,  # aguardando_reservatorio
                self.nv_montante if not self.TDA_Offline else 0,  # nv_montante
                self.ug1.leituras_ug[f"leitura_potencia_ug1"].valor,  # ug1_pot
                self.ug1.setpoint,  # ug1_setpot
                self.ug2.leituras_ug[f"leitura_potencia_ug2"].valor,  # ug2_pot
                self.ug2.setpoint,  # ug2_setpot
                self.ug3.leituras_ug[f"leitura_potencia_ug3"].valor,  # ug3_pot
                self.ug3.setpoint,  # ug3_setpot
            ]
            self.db.update_valores_usina(valores)

        except Exception as e:
            logger.exception(f"Houve um erro ao gravar os parâmetros da Usina no Banco. Exception: \"{repr(e)}\"")
            logger.debug(f"Traceback: {traceback.print_stack}")

        try:
            self.db.insert_debug(
                time(),
                1 if self.modo_autonomo else 0,
                self.nv_montante_recente,
                self.erro_nv,
                self.ug1.setpoint,
                self.ug1.leituras_ug[f"leitura_potencia_ug1"].valor,
                self.ug2.setpoint,
                self.ug2.leituras_ug[f"leitura_potencia_ug2"].valor,
                self.ug3.setpoint,
                self.ug3.leituras_ug[f"leitura_potencia_ug3"].valor,
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
            )
        except Exception as e:
            logger.exception(f"Houve um erro ao gravar os parâmetros debug no Banco. Exception: \"{repr(e)}\"")
            logger.debug(f"Traceback: {traceback.print_stack}")

    def atualizar_limites_operacao(self, db):
        parametros = db
        for ug in self.ugs:
            ug.prioridade = int(parametros[f"ug{ug.id}_prioridade"])

            ug.condicionador_temperatura_fase_r_ug.valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{ug.id}"])
            ug.condicionador_temperatura_fase_r_ug.valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{ug.id}"])

            ug.condicionador_temperatura_fase_s_ug.valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{ug.id}"])
            ug.condicionador_temperatura_fase_s_ug.valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{ug.id}"])

            ug.condicionador_temperatura_fase_t_ug.valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{ug.id}"])
            ug.condicionador_temperatura_fase_t_ug.valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{ug.id}"])

            ug.condicionador_temperatura_nucleo_estator_ug.valor_base = float(parametros[f"alerta_temperatura_nucleo_estator_ug{ug.id}"])
            ug.condicionador_temperatura_nucleo_estator_ug.valor_limite = float(parametros[f"limite_temperatura_nucleo_estator_ug{ug.id}"])

            ug.condicionador_temperatura_mancal_rad_dia_1_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_rad_dia_1_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_rad_dia_1_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_rad_dia_1_ug{ug.id}"])

            ug.condicionador_temperatura_mancal_rad_dia_2_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_rad_dia_2_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_rad_dia_2_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_rad_dia_2_ug{ug.id}"])

            ug.condicionador_temperatura_mancal_rad_tra_1_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_rad_tra_1_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_rad_tra_1_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_rad_tra_1_ug{ug.id}"])

            ug.condicionador_temperatura_mancal_rad_tra_2_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_rad_tra_2_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_rad_tra_2_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_rad_tra_2_ug{ug.id}"])

            ug.condicionador_temperatura_saida_de_ar_ug.valor_base = float(parametros[f"alerta_temperatura_saida_de_ar_ug{ug.id}"])
            ug.condicionador_temperatura_saida_de_ar_ug.valor_limite = float(parametros[f"limite_temperatura_saida_de_ar_ug{ug.id}"])

            ug.condicionador_temperatura_mancal_guia_escora_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_escora_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_guia_escora_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_escora_ug{ug.id}"])

            ug.condicionador_temperatura_mancal_guia_radial_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_radial_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_guia_radial_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_radial_ug{ug.id}"])

            ug.condicionador_temperatura_mancal_guia_contra_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_contra_ug{ug.id}"])
            ug.condicionador_temperatura_mancal_guia_contra_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_contra_ug{ug.id}"])

            ug.condicionador_caixa_espiral_ug.valor_base = float(parametros[f"alerta_caixa_espiral_ug{ug.id}"])
            ug.condicionador_caixa_espiral_ug.valor_limite = float(parametros[f"limite_caixa_espiral_ug{ug.id}"])

    def acionar_emergencia(self):
        self.con.acionar_emergencia()
        self.clp_emergencia_acionada = 1

    def normalizar_emergencia(self):
        logger.info("Normalizando Usina...")
        logger.debug(f"Tensão na linha: \
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
            if not(self.cfg["TENSAO_LINHA_BAIXA"] < self.__tensao_rs.valor < self.cfg["TENSAO_LINHA_ALTA"] \
                and self.cfg["TENSAO_LINHA_BAIXA"] < self.__tensao_st.valor < self.cfg["TENSAO_LINHA_ALTA"] \
                and self.cfg["TENSAO_LINHA_BAIXA"] < self.__tensao_tr.valor < self.cfg["TENSAO_LINHA_ALTA"]):
                return False
            else:
                return True
        except Exception as e:
            logger.error(f"Erro ao ler valores da linha. Exception: \"{repr(e)}\".")
            return False

    def aguardar_tensao(self, delay):
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

    def heartbeat(self):

        self.clp["MOA"].write_single_coil(self.cfg["REG_PAINEL_LIDO"], [1])
        self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_MODE"], [self.modo_autonomo])
        self.clp["MOA"].write_single_register(self.cfg["REG_MOA_OUT_STATUS"], self._state_moa)

        for ug in self.ugs:
            ug.modbus_update_state_register()

        if self.modo_autonomo:
            self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_EMERG"], [1 if self.clp_emergencia_acionada else 0])
            self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_TARGET_LEVEL"], [int((self.cfg["nv_alvo"] - 400) * 1000)])
            self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_SETPOINT"], [int(sum(ug.setpoint for ug in self.ugs))])

            if self.clp["MOA"].read_coils(self.cfg["REG_MOA_IN_EMERG"]) == 1 and not self.avisado_em_eletrica:
                self.avisado_em_eletrica = True
                for ug in self.ugs: ug.deve_ler_condicionadores = True

            elif self.clp["MOA"].read_coils(self.cfg["REG_MOA_IN_EMERG"]) == 0 and self.avisado_em_eletrica:
                self.avisado_em_eletrica = False
                for ug in self.ugs: ug.deve_ler_condicionadores = False

            if self.clp["MOA"].read_coils(self.cfg["REG_MOA_IN_EMERG_UG1"]) == 1:
                self.ug1.deve_ler_condicionadores = True

            if self.clp["MOA"].read_coils(self.cfg["REG_MOA_IN_EMERG_UG2"]) == 1:
                self.ug2.deve_ler_condicionadores = True

            if self.clp["MOA"].read_coils(self.cfg["REG_MOA_IN_EMERG_UG3"]) == 1:
                self.ug3.deve_ler_condicionadores = True

            if self.clp["MOA"].read_coils(self.cfg["REG_MOA_IN_HABILITA_AUTO"]) == 1:
                self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_IN_HABILITA_AUTO"], 1)
                self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_IN_DESABILITA_AUTO"], 0)
                self.modo_autonomo = True

            if self.clp["MOA"].read_coils(self.cfg["REG_MOA_IN_DESABILITA_AUTO"]) == 1:
                self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_IN_HABILITA_AUTO"], 0)
                self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_IN_DESABILITA_AUTO"], 1)
                self.modo_autonomo = False

            if self.clp["MOA"].read_coils(self.cfg["REG_MOA_OUT_BLOCK_UG1"]) == 1:
                self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG1"], 1)

            elif self.clp["MOA"].read_coils(self.cfg["REG_MOA_OUT_BLOCK_UG1"]) == 0:
                self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG1"], 0)

            if self.clp["MOA"].read_coils(self.cfg["REG_MOA_OUT_BLOCK_UG2"]) == 1:
                self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG2"], 1)

            elif self.clp["MOA"].read_coils(self.cfg["REG_MOA_OUT_BLOCK_UG2"]) == 0:
                self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG2"], 0)

            if self.clp["MOA"].read_coils(self.cfg["REG_MOA_OUT_BLOCK_UG3"]) == 1:
                self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG3"], 1)

            elif self.clp["MOA"].read_coils(self.cfg["REG_MOA_OUT_BLOCK_UG3"]) == 0:
                self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG3"], 0)

        elif not self.modo_autonomo:
            if self.clp["MOA"].read_coils(self.cfg["REG_MOA_IN_HABILITA_AUTO"]) == 1:
                self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_IN_HABILITA_AUTO"], 1)
                self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_IN_DESABILITA_AUTO"], 0)
                self.modo_autonomo = True

            self.clp["MOA"].write_single_register(self.cfg["REG_MOA_OUT_TARGET_LEVEL"], int(0))
            self.clp["MOA"].write_single_register(self.cfg["REG_MOA_OUT_SETPOINT"], int(0))
            self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_EMERG"], 0)
            self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG1"], 0)
            self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG2"], 0)
            self.clp["MOA"].write_single_coil(self.cfg["REG_MOA_OUT_BLOCK_UG3"], 0)


    def get_agendamentos_pendentes(self):
        """
        Retorna os agendamentos pendentes para a usina.
        :return: list[] agendamentos

        agora = self.get_time()
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
        agora = self.get_time()
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


            if segundos_passados > 240:
                logger.info(f"Agendamento #{agendamento[0]} Atrasado! ({agendamento[3]}).")
                self.agendamentos_atrasados += 1

            if segundos_passados > 300 or self.agendamentos_atrasados > 3:
                logger.warning("Os agendamentos estão muito atrasados! Acionando emergência.")
                self.acionar_emergencia()
                return False

            if segundos_adiantados <= 60 and not bool(agendamento[4]):
                # Está na hora e ainda não foi executado. Executar!
                logger.info(f"Executando agendamento: {agendamento[0]}\n \
                    Comando: {AGN_STR_DICT[agendamento[3]]}\n \
                    Data: {agendamento[1]}\n \
                    Observação: {agendamento[2]}\n \
                    {f'Valor: {agendamento[5]}' if agendamento[5] is not None else ...}"
                )


                # se o MOA estiver em autonomo e o agendamento não for executavel em autonomo
                #   marca como executado e altera a descricao
                #   proximo
                if (self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_autmoatico"]):
                    obs = "Este agendamento não tem efeito com o módulo em modo autônomo. Executado sem realizar nenhuma ação"
                    logger.debug(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True

                # se o MOA estiver em manual e o agendamento não for executavel em manual
                #   marca como executado e altera a descricao
                #   proximo
                if (not self.modo_autonomo and not self.db.get_executabilidade(agendamento[3])["executavel_em_manual"]):
                    obs = "Este agendamento não tem efeito com o módulo em modo manual. Executado sem realizar nenhuma ação"
                    logger.debug(obs)
                    self.db.update_agendamento(agendamento[0], True, obs)
                    return True

                # Exemplo Case agendamento:
                """if agendamento[3] == AGENDAMENTO_DISPARAR_MENSAGEM_TESTE:
                    # Coloca em emergência
                    logger.debug("Disparando mensagem teste (comando via agendamento).")
                    self.disparar_mensagem_teste()"""

                if agendamento[3] == AGENDAMENTO_INDISPONIBILIZAR:
                    # Coloca em emergência
                    logger.info("Indisponibilizando a usina (comando via agendamento).")
                    for ug in self.ugs:
                        ug.forcar_estado_indisponivel()
                    while (not self.ugs[0].etapa_atual == UNIDADE_PARADA and not self.ugs[1].etapa_atual == UNIDADE_PARADA):
                        self.ler_valores()
                        logger.debug("Indisponibilizando Usina... \n(freezing for 10 seconds)")
                        sleep(10)
                    self.acionar_emergencia()
                    logger.debug("Emergência pressionada após indizponibilização agendada mudando para modo manual para evitar normalização automática.")
                    self.modo_autonomo = 0

                if agendamento[3] == AGENDAMENTO_ALTERAR_NV_ALVO:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido).")

                    self.cfg["nv_alvo"] = novo

                if agendamento[3] == AGENDAMENTO_BAIXAR_POT_UGS_MINIMO:
                    try:
                        for ug in self.ugs:
                            self.cfg[f"pot_maxima_ug{ug.id}"] = self.cfg["pot_limpeza_grade"]

                            if ug.etapa_atual == UNIDADE_PARADA or ug.etapa_atual == UNIDADE_PARANDO:
                                logger.debug(f"A UG{ug.id} já está no estado parada/parando.")
                            else:
                                ug.limpeza_grade = True
                                logger.debug(f"Enviando o setpoint de limpeza de grade ({self.cfg['pot_limpeza_grade']}) para a UG{ug.id}")

                    except Exception as e:
                        logger.debug(f"Traceback: {repr(e)}")

                if agendamento[3] == AGENDAMENTO_NORMALIZAR_POT_UGS_MINIMO:
                    try:
                        for ug in self.ugs:
                            self.cfg[f"pot_maxima_ug{ug.id}"] = self.cfg["pot_maxima_ug"]

                            ug.limpeza_grade = False
                            ug.enviar_setpoint(self.cfg["pot_maxima_ug"])

                    except Exception as e:
                        logger.debug(f"Traceback: {repr(e)}")

                if agendamento[3] == AGENDAMENTO_UG1_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug1"] = novo
                        self.ug1.pot_disponivel = novo
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido).")

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
                        self.cfg["pot_maxima_ug2"] = novo
                        self.ug2.pot_disponivel = novo
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido).")

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_MANUAL:
                    self.ug2.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_DISPONIVEL:
                    self.ug2.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug2.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG2_FORCAR_ESTADO_RESTRITO:
                    self.ug2.forcar_estado_restrito()

                if agendamento[3] == AGENDAMENTO_UG3_ALTERAR_POT_LIMITE:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_ug3"] = novo
                        self.ug3.pot_disponivel = novo
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido).")

                if agendamento[3] == AGENDAMENTO_UG3_FORCAR_ESTADO_MANUAL:
                    self.ug3.forcar_estado_manual()

                if agendamento[3] == AGENDAMENTO_UG3_FORCAR_ESTADO_DISPONIVEL:
                    self.ug3.forcar_estado_disponivel()

                if agendamento[3] == AGENDAMENTO_UG3_FORCAR_ESTADO_INDISPONIVEL:
                    self.ug3.forcar_estado_indisponivel()

                if agendamento[3] == AGENDAMENTO_UG3_FORCAR_ESTADO_RESTRITO:
                    self.ug3.forcar_estado_restrito()

                if agendamento[3] == AGENDAMENTO_ALTERAR_POT_LIMITE_TODAS_AS_UGS:
                    try:
                        novo = float(agendamento[5].replace(",", "."))
                        self.cfg["pot_maxima_alvo"] = novo
                        self.db._open()
                        self.db.execute(f"UPDATE parametros_moa_parametrosusina SET pot_nominal = {novo}")
                        self.db._close()
                    except Exception as e:
                        logger.info(f"Valor inválido no comando #{agendamento[0]} ({agendamento[3]} é inválido).")

                # Após executar, indicar no banco de dados
                self.db.update_agendamento(int(agendamento[0]), 1)
                logger.info(f"O comando #{agendamento[0]} - {agendamento[5]} foi executado.")
                self.con.somente_reconhecer_emergencia()
                self.escrever_valores()

    def distribuir_potencia(self, pot_alvo):

        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs:
                ug.setpoint = 0
            return 0

        pot_medidor = self.__potencia_ativa_kW.valor
        logger.debug(f"Potência no medidor: {pot_medidor:0.3f}")

        # implementação nova
        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])

        pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

        try:
            if pot_medidor > self.cfg["pot_maxima_alvo"] * 0.97 and pot_alvo >= self.cfg["pot_maxima_alvo"]:
                pot_alvo = self.pot_alvo_anterior * (1 - 0.5 * ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))

        except TypeError as e:
            logger.info("A comunicação com os MFs falhou.")

        self.pot_alvo_anterior = pot_alvo

        logger.debug(f"Potência alvo pós ajuste: {pot_alvo:0.3f}")

        ugs = self.lista_de_ugs_disponiveis()
        self.pot_disp = 0
        self.ajuste_manual = 0

        for ug in ugs:
            logger.debug(f"UG{ug.id}")
            self.pot_disp += ug.cfg[f"pot_maxima_ug{ugs[0].id}"]
            if ug.manual:
                logger.debug(f"UG{ug.id} Manual -> {ug.leituras_ug[f'leitura_potencia_ug{ug.id}'].valor}")
                self.ajuste_manual += ug.leituras_ug[f'leitura_potencia_ug{ug.id}'].valor
        if ugs is None:
            return False
        elif len(ugs) == 0:
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

    def lista_de_ugs_disponiveis(self):
        """
        Retorn uma lista de ugs disponiveis conforme a ordenação selecionada
        """
        ls = []
        for ug in self.ugs:
            if ug.disponivel and ug.etapa_atual in UNIDADE_LISTA_DE_ETAPAS:
                ls.append(ug)

        if self.modo_de_escolha_das_ugs == MODO_ESCOLHA_MANUAL:
            # escolher por maior prioridade primeiro
            #!!TODO: corrigir etapa_atual
            ls = sorted(ls, key=lambda y: (-1 * y.etapa_atual, -1 * y.leituras_ug[f'leitura_potencia_ug{y.id}'].valor, -1 * y.setpoint, y.prioridade,),)
            logger.debug("")
            logger.debug("UGs disponíveis em ordem (prioridade):")
        else:
            # escolher por menor horas_maquina primeiro
            ls = sorted(ls, key=lambda y: (-1 * y.etapa_atual, y.leituras_ug[f"leitura_horimetro_ug{y.id}"].valor, -1 * y.leituras_ug[f'leitura_potencia_ug{ug.id}'].valor, -1 * y.setpoint,),)
            # ls = sorted(ls, key=lambda y: (-1 * y.etapa_atual if y.etapa_atual == UNIDADE_SINCRONIZADA else y.leitura_horimetro.valor,
                                            #-1 * y.leitura_potencia.valor,
                                            #-1 * y.setpoint,),)
            logger.debug("")
            logger.debug("UGs disponíveis em ordem (horas-máquina):")
        return ls

    def controle_normal(self):
        """
        Controle PID
        https://en.wikipedia.org/wiki/PID_controller#Proportional
        """
        logger.debug("-------------------------------------------------")

        # Calcula PID
        logger.debug(f"NÍVEL -> Leitura: {self.nv_montante_recente:0.3f}; Alvo: {self.cfg['nv_alvo']:0.3f}")

        self.controle_p = self.cfg["kp"] * self.erro_nv

        if self.pid_inicial == -1:
            self.controle_i = max(min(self.controle_ie - self.controle_p, 0.8), 0)
            self.pid_inicial = 0
        else:
            self.controle_i = max(min((self.cfg["ki"] * self.erro_nv) + self.controle_i, 0.8), 0)
            self.controle_d = self.cfg["kd"] * (self.erro_nv - self.erro_nv_anterior)

        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))

        logger.debug(f"PID -> {saida_pid:0.3f} P:{self.controle_p:0.3f} + I:{self.controle_i:0.3f} + D:{self.controle_d:0.3f}; ERRO={self.erro_nv}")

        # Calcula o integrador de estabilidade e limita
        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)

        if self.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if self.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        logger.debug(f"IE -> {self.controle_ie:0.3f}")
        logger.debug("")

        # Arredondamento e limitação
        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"],), self.cfg["pot_minima"],)

        logger.debug(f"Potência alvo: {pot_alvo:0.3f}")

        pot_alvo = self.distribuir_potencia(pot_alvo)

    def ping_clps(self) -> None:
        # -> Verifica conexão com CLP Tomada d'água
        if not ping(self.cfg["TDA_slave_ip"]):
            self.TDA_Offline = True
            self.db.update_tda_offline(True)
            if self.TDA_Offline and self.hb_borda_emerg_ping == 0:
                self.hb_borda_emerg_ping = 1
                logger.warning("CLP TDA não respondeu a tentativa de comunicação!")

        if ping(self.cfg["TDA_slave_ip"]) and self.hb_borda_emerg_ping == 1:
            logger.info("Comunicação com o CLP TDA reestabelecida.")
            self.hb_borda_emerg_ping = 0
            self.TDA_Offline = False
            self.db.update_tda_offline(False)

        # -> Verifica conexão com CLP Sub
        if not ping(self.cfg["USN_slave_ip"]):
            logger.warning("CLP 'USN' (PACP) não respondeu a tentativa de comunicação!")

        # -> Verifica conexão com CLP UG#
        if not ping(self.cfg["UG1_slave_ip"]):
            logger.warning("CLP UG1 não respondeu a tentativa de comunicação!")
            self.ug1.forcar_estado_restrito()

        if not ping(self.cfg["UG2_slave_ip"]):
            logger.warning("CLP UG2 não respondeu a tentativa de comunicação!")
            self.ug2.forcar_estado_restrito()

        if not ping(self.cfg["UG3_slave_ip"]):
            logger.warning("CLP UG3 não respondeu a tentativa de comunicação!")
            self.ug3.forcar_estado_restrito()

    def leitura_periodica(self, delay: int) -> None:
        logger.debug("Iniciando o timer de leitura periódica.")
        try:
            proxima_leitura = time() + delay
            while True:
                self.leituras_temporizadas()
                for ug in self.ugs: ug.leituras_temporizadas()
                sleep(1)
                self.verificar_voip()
                sleep(max(0, proxima_leitura - time()))
                proxima_leitura += (time() - proxima_leitura) // delay * delay + delay

        except Exception:
            logger.error(f"Houve um problema ao executar a leitura periódica.")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def verificar_voip(self) -> None:
        try:
            for _, v in vd.voip_dict.items():
                if v[0]:
                    Voip.acionar_chamada()
                    break

        except Exception:
            logger.exception(f"Houve um problema ao ligar por Voip.")
            logger.exception(f"Traceback: {traceback.format_exc()}")

    def leitura_condicionadores(self) -> None:
        #Lista de condicionadores essenciais que devem ser lidos a todo momento
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        self.leitura_ED_SA_QCAP_TensaoPresenteTSA = LeituraModbusCoil("ED_SA_QCAP_TensaoPresenteTSA", self.clp["SA"], REG_SA_ED_SA_QCAP_TensaoPresenteTSA, )
        x = self.leitura_ED_SA_QCAP_TensaoPresenteTSA
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_NORMALIZAR, x))

        self.leitura_ED_SA_SEL787_Trip = LeituraModbusCoil("ED_SA_SEL787_Trip", self.clp["SA"], REG_SA_ED_SA_SEL787_Trip, )
        x = self.leitura_ED_SA_SEL787_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SA_SEL311_Trip = LeituraModbusCoil( "ED_SA_SEL311_Trip", self.clp["SA"], REG_SA_ED_SA_SEL311_Trip, )
        x = self.leitura_ED_SA_SEL311_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        # MRU3 é o relé de bloqueio 27/59N
        self.leitura_ED_SA_MRU3_Trip = LeituraModbusCoil("ED_SA_MRU3_Trip", self.clp["SA"], REG_SA_ED_SA_MRU3_Trip, )
        x = self.leitura_ED_SA_MRU3_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        # MRL1 é o relé de bloqueio 86T
        self.leitura_ED_SA_MRL1_Trip = LeituraModbusCoil("ED_SA_MRL1_Trip", self.clp["SA"], REG_SA_ED_SA_MRL1_Trip, )
        x = self.leitura_ED_SA_MRL1_Trip
        self.condicionadores_essenciais.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SA_QCADE_Disj52E1Trip = LeituraModbusCoil( "ED_SA_QCADE_Disj52E1Trip", self.clp["SA"], REG_SA_ED_SA_QCADE_Disj52E1Trip, )
        x = self.leitura_ED_SA_QCADE_Disj52E1Trip
        self.condicionadores_essenciais.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        #Lista de condiconadores que deverão ser lidos apenas quando houver uma chamada de leitura
        #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        if not self.TDA_Offline:
            self.leitura_ED_TDA_QcataDisj52ETrip = LeituraModbusCoil("ED_TDA_QcataDisj52ETrip", self.clp["SA"], REG_TDA_ED_QcataDisj52ETrip, )
            x = self.leitura_ED_TDA_QcataDisj52ETrip
            self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

            self.leitura_ED_TDA_QcataDisj52ETripDisjSai = LeituraModbusCoil("ED_TDA_QcataDisj52ETripDisjSai", self.clp["SA"], REG_TDA_ED_QcataDisj52ETripDisjSai, )
            x = self.leitura_ED_TDA_QcataDisj52ETripDisjSai
            self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

            self.leitura_ED_TDA_QcataDisj52EFalha380VCA = LeituraModbusCoil("ED_TDA_QcataDisj52EFalha380VCA", self.clp["SA"], REG_TDA_ED_QcataDisj52EFalha380VCA, )
            x = self.leitura_ED_TDA_QcataDisj52EFalha380VCA
            self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        # MRU3 é o relé de bloqueio 27/59N
        self.leitura_ED_SA_MRU3_Falha = LeituraModbusCoil("ED_SA_MRU3_Falha", self.clp["SA"], REG_SA_ED_SA_MRU3_Falha, )
        x = self.leitura_ED_SA_MRU3_Falha
        self.condicionadores.append(CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x))

        self.leitura_ED_SA_SEL787_FalhaInterna = LeituraModbusCoil( "ED_SA_SEL787_FalhaInterna", self.clp["SA"], REG_SA_ED_SA_SEL787_FalhaInterna, )
        x = self.leitura_ED_SA_SEL787_FalhaInterna
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_SEL311_Falha = LeituraModbusCoil( "ED_SA_SEL311_Falha", self.clp["SA"], REG_SA_ED_SA_SEL311_Falha, )
        x = self.leitura_ED_SA_SEL311_Falha
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_CTE_Falta125Vcc = LeituraModbusCoil( "ED_SA_CTE_Falta125Vcc", self.clp["SA"], REG_SA_ED_SA_CTE_Falta125Vcc, )
        x = self.leitura_ED_SA_CTE_Falta125Vcc
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_CTE_Secc89TE_Aberta = LeituraModbusCoil( "ED_SA_CTE_Secc89TE_Aberta", self.clp["SA"], REG_SA_ED_SA_CTE_Secc89TE_Aberta, )
        x = self.leitura_ED_SA_CTE_Secc89TE_Aberta
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_TE_AlarmeDetectorGas = LeituraModbusCoil( "ED_SA_TE_AlarmeDetectorGas", self.clp["SA"], REG_SA_ED_SA_TE_AlarmeDetectorGas, )
        x = self.leitura_ED_SA_TE_AlarmeDetectorGas
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_TE_AlarmeNivelMaxOleo = LeituraModbusCoil( "ED_SA_TE_AlarmeNivelMaxOleo", self.clp["SA"], REG_SA_ED_SA_TE_AlarmeNivelMaxOleo, )
        x = self.leitura_ED_SA_TE_AlarmeNivelMaxOleo
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_TE_AlarmeAlivioPressao = LeituraModbusCoil( "ED_SA_TE_AlarmeAlivioPressao", self.clp["SA"], REG_SA_ED_SA_TE_AlarmeAlivioPressao, )
        x = self.leitura_ED_SA_TE_AlarmeAlivioPressao
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_TE_AlarmeTempOleo = LeituraModbusCoil( "ED_SA_TE_AlarmeTempOleo", self.clp["SA"], REG_SA_ED_SA_TE_AlarmeTempOleo, )
        x = self.leitura_ED_SA_TE_AlarmeTempOleo
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_TE_AlarmeTempEnrolamento = ( LeituraModbusCoil( "ED_SA_TE_AlarmeTempEnrolamento", self.clp["SA"], REG_SA_ED_SA_TE_AlarmeTempEnrolamento, ) )
        x = self.leitura_ED_SA_TE_AlarmeTempEnrolamento
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_TE_AlarmeDesligamento = LeituraModbusCoil( "ED_SA_TE_AlarmeDesligamento", self.clp["SA"], REG_SA_ED_SA_TE_AlarmeDesligamento, )
        x = self.leitura_ED_SA_TE_AlarmeDesligamento
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_TE_Falha = LeituraModbusCoil( "ED_SA_TE_Falha", self.clp["SA"], REG_SA_ED_SA_TE_Falha, )
        x = self.leitura_ED_SA_TE_Falha
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_FalhaDisjTPsProt = LeituraModbusCoil( "ED_SA_FalhaDisjTPsProt", self.clp["SA"], REG_SA_ED_SA_FalhaDisjTPsProt, )
        x = self.leitura_ED_SA_FalhaDisjTPsProt
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_FalhaDisjTPsSincr = LeituraModbusCoil( "ED_SA_FalhaDisjTPsSincr", self.clp["SA"], REG_SA_ED_SA_FalhaDisjTPsSincr, )
        x = self.leitura_ED_SA_FalhaDisjTPsSincr
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_CSA1_Secc_Aberta = LeituraModbusCoil( "ED_SA_CSA1_Secc_Aberta", self.clp["SA"], REG_SA_ED_SA_CSA1_Secc_Aberta, )
        x = self.leitura_ED_SA_CSA1_Secc_Aberta
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_CSA1_FusivelQueimado = LeituraModbusCoil( "ED_SA_CSA1_FusivelQueimado", self.clp["SA"], REG_SA_ED_SA_CSA1_FusivelQueimado, )
        x = self.leitura_ED_SA_CSA1_FusivelQueimado
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_CSA1_FaltaTensao125Vcc = LeituraModbusCoil( "ED_SA_CSA1_FaltaTensao125Vcc", self.clp["SA"], REG_SA_ED_SA_CSA1_FaltaTensao125Vcc, )
        x = self.leitura_ED_SA_CSA1_FaltaTensao125Vcc
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_QCADE_Nivel4 = LeituraModbusCoil( "ED_SA_QCADE_Nivel4", self.clp["SA"], REG_SA_ED_SA_QCADE_Nivel4, )
        x = self.leitura_ED_SA_QCADE_Nivel4
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_QCADE_NivelMuitoAlto = LeituraModbusCoil( "ED_SA_QCADE_NivelMuitoAlto", self.clp["SA"], REG_SA_ED_SA_QCADE_NivelMuitoAlto, )
        x = self.leitura_ED_SA_QCADE_NivelMuitoAlto
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_QCADE_Falha220VCA = LeituraModbusCoil( "ED_SA_QCADE_Falha220VCA", self.clp["SA"], REG_SA_ED_SA_QCADE_Falha220VCA, )
        x = self.leitura_ED_SA_QCADE_Falha220VCA
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        # Verificar
        self.leitura_ED_SA_QCCP_Disj72ETrip = LeituraModbusCoil( "ED_SA_QCCP_Disj72ETrip", self.clp["SA"], REG_SA_ED_SA_QCCP_Disj72ETrip, )
        x = self.leitura_ED_SA_QCCP_Disj72ETrip
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_QCCP_Falta125Vcc = LeituraModbusCoil( "ED_SA_QCCP_Falta125Vcc", self.clp["SA"], REG_SA_ED_SA_QCCP_Falta125Vcc, )
        x = self.leitura_ED_SA_QCCP_Falta125Vcc
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_QCCP_TripDisjAgrup = LeituraModbusCoil( "ED_SA_QCCP_TripDisjAgrup", self.clp["SA"], REG_SA_ED_SA_QCCP_TripDisjAgrup, )
        x = self.leitura_ED_SA_QCCP_TripDisjAgrup
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_QCAP_Falta125Vcc = LeituraModbusCoil( "ED_SA_QCAP_Falta125Vcc", self.clp["SA"], REG_SA_ED_SA_QCAP_Falta125Vcc, )
        x = self.leitura_ED_SA_QCAP_Falta125Vcc
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_QCAP_TripDisjAgrup = LeituraModbusCoil( "ED_SA_QCAP_TripDisjAgrup", self.clp["SA"], REG_SA_ED_SA_QCAP_TripDisjAgrup, )
        x = self.leitura_ED_SA_QCAP_TripDisjAgrup
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_QCAP_Disj52A1Falha = LeituraModbusCoil( "ED_SA_QCAP_Disj52A1Falha", self.clp["SA"], REG_SA_ED_SA_QCAP_Disj52A1Falha, )
        x = self.leitura_ED_SA_QCAP_Disj52A1Falha
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_QCAP_Disj52EFalha = LeituraModbusCoil( "ED_SA_QCAP_Disj52EFalha", self.clp["SA"], REG_SA_ED_SA_QCAP_Disj52EFalha, )
        x = self.leitura_ED_SA_QCAP_Disj52EFalha
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_GMG_DisjFechado = LeituraModbusCoil( "ED_SA_GMG_DisjFechado", self.clp["SA"], REG_SA_ED_SA_GMG_DisjFechado, )
        x = self.leitura_ED_SA_GMG_DisjFechado
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RA_SEL787_Targets = LeituraModbusCoil( "RA_SEL787_Targets", self.clp["SA"], REG_SA_RA_SEL787_Targets, )
        x = self.leitura_RA_SEL787_Targets
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RA_SEL787_Targets_Links_Bit00 = ( LeituraModbusCoil( "RA_SEL787_Targets_Links_Bit00", self.clp["SA"], REG_SA_RA_SEL787_Targets_Links_Bit00, ) )
        x = self.leitura_RA_SEL787_Targets_Links_Bit00
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RA_SEL787_Targets_Links_Bit01 = ( LeituraModbusCoil( "RA_SEL787_Targets_Links_Bit01", self.clp["SA"], REG_SA_RA_SEL787_Targets_Links_Bit01, ) )
        x = self.leitura_RA_SEL787_Targets_Links_Bit01
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RA_SEL787_Targets_Links_Bit02 = ( LeituraModbusCoil( "RA_SEL787_Targets_Links_Bit02", self.clp["SA"], REG_SA_RA_SEL787_Targets_Links_Bit02, ) )
        x = self.leitura_RA_SEL787_Targets_Links_Bit02
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RA_SEL787_Targets_Links_Bit03 = ( LeituraModbusCoil( "RA_SEL787_Targets_Links_Bit03", self.clp["SA"], REG_SA_RA_SEL787_Targets_Links_Bit03, ) )
        x = self.leitura_RA_SEL787_Targets_Links_Bit03
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RA_SEL787_Targets_Links_Bit04 = ( LeituraModbusCoil( "RA_SEL787_Targets_Links_Bit04", self.clp["SA"], REG_SA_RA_SEL787_Targets_Links_Bit04, ) )
        x = self.leitura_RA_SEL787_Targets_Links_Bit04
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RA_SEL787_Targets_Links_Bit05 = ( LeituraModbusCoil( "RA_SEL787_Targets_Links_Bit05", self.clp["SA"], REG_SA_RA_SEL787_Targets_Links_Bit05, ) )
        x = self.leitura_RA_SEL787_Targets_Links_Bit05
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RA_SEL787_Targets_Links_Bit06 = ( LeituraModbusCoil( "RA_SEL787_Targets_Links_Bit06", self.clp["SA"], REG_SA_RA_SEL787_Targets_Links_Bit06, ) )
        x = self.leitura_RA_SEL787_Targets_Links_Bit06
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RA_SEL787_Targets_Links_Bit07 = ( LeituraModbusCoil( "RA_SEL787_Targets_Links_Bit07", self.clp["SA"], REG_SA_RA_SEL787_Targets_Links_Bit07, ) )
        x = self.leitura_RA_SEL787_Targets_Links_Bit07
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_DJ1_FalhaInt = LeituraModbusCoil( "RD_DJ1_FalhaInt", self.clp["SA"], REG_SA_RD_DJ1_FalhaInt, )
        x = self.leitura_RD_DJ1_FalhaInt
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_RD_CLP_Falha = LeituraModbusCoil( "RD_CLP_Falha", self.clp["SA"], REG_SA_RD_CLP_Falha, )
        x = self.leitura_RD_CLP_Falha
        self.condicionadores.append( CondicionadorBase(x.descr, DEVE_INDISPONIBILIZAR, x) )

        self.leitura_ED_SA_QLCF_Disj52ETrip = LeituraModbusCoil( "ED_SA_QLCF_Disj52ETrip", self.clp["SA"], REG_SA_ED_SA_QLCF_Disj52ETrip)
        self.leitura_ED_SA_QLCF_TripDisjAgrup = LeituraModbusCoil( "ED_SA_QLCF_TripDisjAgrup", self.clp["SA"], REG_SA_ED_SA_QLCF_TripDisjAgrup)
        self.leitura_ED_SA_QCAP_SubtensaoBarraGeral = LeituraModbusCoil( "ED_SA_QCAP_SubtensaoBarraGeral", self.clp["SA"], REG_SA_ED_SA_QCAP_SubtensaoBarraGeral)
        self.leitura_ED_SA_GMG_Alarme = LeituraModbusCoil( "ED_SA_GMG_Alarme", self.clp["SA"], REG_SA_ED_SA_GMG_Alarme)
        self.leitura_ED_SA_GMG_Trip = LeituraModbusCoil( "ED_SA_GMG_Trip", self.clp["SA"], REG_SA_ED_SA_GMG_Trip)
        self.leitura_ED_SA_GMG_Operacao = LeituraModbusCoil( "ED_SA_GMG_Operacao", self.clp["SA"], REG_SA_ED_SA_GMG_Operacao)
        self.leitura_ED_SA_GMG_BaixoComb = LeituraModbusCoil( "ED_SA_GMG_BaixoComb", self.clp["SA"], REG_SA_ED_SA_GMG_BaixoComb)
        self.leitura_RD_BbaDren1_FalhaAcion = LeituraModbusCoil( "RD_BbaDren1_FalhaAcion", self.clp["SA"], REG_SA_RD_BbaDren1_FalhaAcion)
        self.leitura_RD_BbaDren2_FalhaAcion = LeituraModbusCoil( "RD_BbaDren2_FalhaAcion", self.clp["SA"], REG_SA_RD_BbaDren2_FalhaAcion)
        self.leitura_RD_BbaDren3_FalhaAcion = LeituraModbusCoil( "RD_BbaDren3_FalhaAcion", self.clp["SA"], REG_SA_RD_BbaDren3_FalhaAcion)
        self.leitura_RD_SA_GMG_FalhaAcion = LeituraModbusCoil( "RD_SA_GMG_FalhaAcion", self.clp["SA"], REG_SA_RD_SA_GMG_FalhaAcion)
        self.leitura_RD_FalhaComunSETDA = LeituraModbusCoil( "RD_FalhaComunSETDA", self.clp["SA"], REG_SA_RD_FalhaComunSETDA)
        self.leitura_ED_SA_QCAP_Disj52EFechado = LeituraModbusCoil( "ED_SA_QCAP_Disj52EFechado", self.clp["SA"], REG_SA_ED_SA_QCAP_Disj52EFechado)
        self.leitura_ED_SA_QCADE_BombasDng_Auto = LeituraModbusCoil( "ED_SA_QCADE_BombasDng_Auto", self.clp["SA"], REG_SA_ED_SA_QCADE_BombasDng_Auto)

    def leituras_temporizadas(self) -> None:
        if self.leitura_ED_SA_QLCF_Disj52ETrip.valor != 0 and not vd.voip_dict["SA_QLCF_DISJ_52E_TRIP"]:
            logger.warning("O Disjuntor do Gerador Diesel de Emergência QLCF identificou um sinal de TRIP, favor verificar.")
            vd.voip_dict["SA_QLCF_DISJ_52E_TRIP"] = True
        elif self.leitura_ED_SA_QLCF_Disj52ETrip.valor == 0 and vd.voip_dict["SA_QLCF_DISJ_52E_TRIP"]:
            vd.voip_dict["SA_QLCF_DISJ_52E_TRIP"] = False

        if self.leitura_ED_SA_QLCF_TripDisjAgrup.valor != 0 and not vd.voip_dict["SA_QLCF_TRIP_DISJ_AGRUP"]:
            logger.warning("O sensor do Disjuntor de Agrupamento QLCF identificou um sinal de trip, favor verificar.")
            vd.voip_dict["SA_QLCF_TRIP_DISJ_AGRUP"] = True
        elif self.leitura_ED_SA_QLCF_TripDisjAgrup.valor == 0 and vd.voip_dict["SA_QLCF_TRIP_DISJ_AGRUP"]:
            vd.voip_dict["SA_QLCF_TRIP_DISJ_AGRUP"] = False

        if self.leitura_ED_SA_QCAP_SubtensaoBarraGeral.valor != 0 and not vd.voip_dict["SA_QCAP_SUBTENSAO_BARRA_GERAL"]:
            logger.warning("O sensor de Subtensão do Barramento Geral QCAP foi acionado, favor verificar.")
            vd.voip_dict["SA_QCAP_SUBTENSAO_BARRA_GERAL"] = True
        elif self.leitura_ED_SA_QCAP_SubtensaoBarraGeral.valor == 0 and vd.voip_dict["SA_QCAP_SUBTENSAO_BARRA_GERAL"]:
            vd.voip_dict["SA_QCAP_SUBTENSAO_BARRA_GERAL"] = False

        if self.leitura_ED_SA_GMG_Alarme.valor != 0 and not vd.voip_dict["SA_GMG_ALARME"]:
            logger.warning("O alarme do Grupo Motor Gerador foi acionado, favor verificar.")
            vd.voip_dict["SA_GMG_ALARME"] = True
        elif self.leitura_ED_SA_GMG_Alarme.valor == 0 and vd.voip_dict["SA_GMG_ALARME"]:
            vd.voip_dict["SA_GMG_ALARME"] = False

        if self.leitura_ED_SA_GMG_Trip.valor != 0 and not vd.voip_dict["SA_GMG_TRIP"]:
            logger.warning("O sensor de TRIP do Grupo Motor Gerador foi acionado, favor verificar.")
            vd.voip_dict["SA_GMG_TRIP"] = True
        elif self.leitura_ED_SA_GMG_Trip.valor == 0 and vd.voip_dict["SA_GMG_TRIP"]:
            vd.voip_dict["SA_GMG_TRIP"] = False

        if self.leitura_ED_SA_GMG_Operacao.valor != 0 and not vd.voip_dict["SA_GMG_OPERACAO"]:
            logger.warning("O sensor de operação do Grupo Motor Gerador foi acionado, favor verificar.")
            vd.voip_dict["SA_GMG_OPERACAO"] = True
        elif self.leitura_ED_SA_GMG_Operacao.valor == 0 and vd.voip_dict["SA_GMG_OPERACAO"]:
            vd.voip_dict["SA_GMG_OPERACAO"] = False

        if self.leitura_ED_SA_GMG_BaixoComb.valor != 0 and not vd.voip_dict["SA_GMG_BAIXO_COMB"]:
            logger.warning("O sensor de de combustível do Grupo Motor Gerador retornou que o nível está baixo, favor reabastercer o gerador.")
            vd.voip_dict["SA_GMG_BAIXO_COMB"] = True
        elif self.leitura_ED_SA_GMG_BaixoComb.valor == 0 and vd.voip_dict["SA_GMG_BAIXO_COMB"]:
            vd.voip_dict["SA_GMG_BAIXO_COMB"] = False

        if self.leitura_RD_BbaDren1_FalhaAcion.valor != 0 and not vd.voip_dict["BBA_DREN_1_FALHA_ACION"]:
            logger.warning("O sensor da Bomba de Drenagem 1 identificou uma falha no acionamento, favor verificar.")
            vd.voip_dict["BBA_DREN_1_FALHA_ACION"] = True
        elif self.leitura_RD_BbaDren1_FalhaAcion.valor == 0 and vd.voip_dict["BBA_DREN_1_FALHA_ACION"]:
            vd.voip_dict["BBA_DREN_1_FALHA_ACION"] = False

        if self.leitura_RD_BbaDren2_FalhaAcion.valor != 0 and not vd.voip_dict["BBA_DREN_2_FALHA_ACION"]:
            logger.warning("O sensor da Bomba de Drenagem 2 identificou uma falha no acionamento, favor verificar.")
            vd.voip_dict["BBA_DREN_2_FALHA_ACION"] = True
        elif self.leitura_RD_BbaDren2_FalhaAcion.valor == 0 and vd.voip_dict["BBA_DREN_2_FALHA_ACION"]:
            vd.voip_dict["BBA_DREN_2_FALHA_ACION"] = False

        if self.leitura_RD_BbaDren3_FalhaAcion.valor != 0 and not vd.voip_dict["BBA_DREN_3_FALHA_ACION"]:
            logger.warning("O sensor da Bomba de Drenagem 3 identificou uma falha no acionamento, favor verificar.")
            vd.voip_dict["BBA_DREN_3_FALHA_ACION"] = True
        elif self.leitura_RD_BbaDren3_FalhaAcion.valor == 0 and vd.voip_dict["BBA_DREN_3_FALHA_ACION"]:
            vd.voip_dict["BBA_DREN_3_FALHA_ACION"] = False

        if self.leitura_RD_SA_GMG_FalhaAcion.valor != 0 and not vd.voip_dict["SA_GMG_FALHA_ACION"]:
            logger.warning("O sensor do Grupo Motor Gerador identificou uma falha no acionamento, favor verificar.")
            vd.voip_dict["SA_GMG_FALHA_ACION"] = True
        elif self.leitura_RD_SA_GMG_FalhaAcion.valor == 0 and vd.voip_dict["SA_GMG_FALHA_ACION"]:
            vd.voip_dict["SA_GMG_FALHA_ACION"] = False

        if self.leitura_RD_FalhaComunSETDA.valor == 1 and not vd.voip_dict["FALHA_COMUM_SETDA"]:
            logger.warning("Houve uma falha de comunicação com o CLP da Subestação e o CLP da Tomada da Água, favor verificar")
            vd.voip_dict["FALHA_COMUM_SETDA"] = True
        elif self.leitura_RD_FalhaComunSETDA.valor == 0 and vd.voip_dict["FALHA_COMUM_SETDA"]:
            vd.voip_dict["FALHA_COMUM_SETDA"] = False

        if self.leitura_ED_SA_QCAP_Disj52EFechado.valor == 1 and not vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"]:
            logger.warning("O Disjuntor do Gerador Diesel de Emergência QLCF foi fechado.")
            vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"] = True
        elif self.leitura_ED_SA_QCAP_Disj52EFechado.valor == 0 and vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"]:
            vd.voip_dict["SA_QCAP_DISJ_52E_FECHADO"] = False

        if self.leitura_ED_SA_QCADE_BombasDng_Auto.valor == 0 and not vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"]:
            logger.warning("O poço de drenagem da Usina entrou em modo remoto, favor verificar.")
            vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"] = True
        elif self.leitura_ED_SA_QCADE_BombasDng_Auto.valor == 1 and vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"]:
            vd.voip_dict["SA_QCADE_BOMBAS_DNG_AUTO"] = False

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
