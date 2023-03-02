import pytz
import logging

from time import sleep
from datetime import datetime
from mysql.connector import pooling
from pyModbusTCP.client import ModbusClient

from VAR_REG import *

logger = logging.getLogger("__main__")

class ModbusClientFailedToOpen(Exception):
    pass

class ModbusFailedToFetch(Exception):
    pass

class FieldConnector:
    def __init__(self, cfg=None):

        if cfg is None:
            raise Exception("A CFG dict is required")
        else:
            self.ug1_ip = CFG["UG1_slave_ip"]
            self.ug1_port = CFG["UG1_slave_porta"]
            self.ug2_ip = CFG["UG2_slave_ip"]
            self.ug2_port = CFG["UG2_slave_porta"]
            self.sa_ip = CFG["USN_slave_ip"]
            self.sa_port = CFG["USN_slave_ip"]
            self.tda_ip = CFG["TDA_slave_ip"]
            self.tda_port =  CFG["TDA_slave_ip"]

        self.ug1_clp = ModbusClient(
            host=CFG["UG1_slave_ip"],
            port=CFG["UG1_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )
        self.ug2_clp = ModbusClient(
            host=CFG["UG2_slave_ip"],
            port=CFG["UG2_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )
        self.usn_clp = ModbusClient(
            host=CFG["USN_slave_ip"],
            port=CFG["USN_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )
        self.tda_clp = ModbusClient(
            host=CFG["TDA_slave_ip"],
            port=CFG["TDA_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
            auto_close=True,
        )

        self.warned_ug1 = False
        self.warned_ug2 = False
        self.TDA_Offline = False

    def modifica_controles_locais(self):
        if not self.TDA_Offline:
            self.tda_clp.write_single_coil(TDA["REG_TDA_ComandosDigitais_MXW_ResetGeral"], 1)
            self.tda_clp.write_single_coil(TDA["REG_TDA_ComandosDigitais_MXW_Hab_Nivel"], 0)
            self.tda_clp.write_single_coil(TDA["REG_TDA_ComandosDigitais_MXW_Desab_Nivel"], 1)
            self.tda_clp.write_single_coil(TDA["REG_TDA_ComandosDigitais_MXW_Hab_Religamento52L"], 0)
            self.tda_clp.write_single_coil(TDA["REG_TDA_ComandosDigitais_MXW_Desab_Religamento52L"], 1)
        else:
            logger.debug("Não é possível modificar os controles locais pois o CLP da TDA se encontra offline")

    def open(self):
        logger.debug("Opening Modbus")
        if not self.ug1_clp.open():
            raise ModbusClientFailedToOpen(f"Modbus client ({self.ug1_ip}:{self.ug1_port}) failed to open.")

        if not self.ug2_clp.open():
            raise ModbusClientFailedToOpen(f"Modbus client ({self.ug2_ip}:{self.ug2_port}) failed to open.")

        if not self.usn_clp.open():
            raise ModbusClientFailedToOpen(f"Modbus client ({self.sa_ip}:{self.sa_port}) failed to open.")

        if not self.tda_clp.open():
            raise ModbusClientFailedToOpen(f"Modbus client ({self.tda_ip}:{self.tda_port}) failed to open.")

        logger.debug("Openned Modbus")
        return self

    def close(self):
        logger.debug("Closing Modbus")
        self.ug1_clp.close()
        self.ug2_clp.close()
        self.usn_clp.close()
        self.tda_clp.close()
        logger.debug("Closed Modbus")

    def fechaDj52L(self):
        if not self.get_flag_falha52L():
            return False
        else:
            response = self.usn_clp.write_single_register(SA["REG_SA_ComandosDigitais_MXW_Liga_DJ1"], 1)
            return response

    def normalizar_emergencia(self):
        logger.info("Reconhecendo alarmes, resetando usina e fechando Dj52L")
        logger.debug("Reconhece/Reset alarmes")
        self.ug1_clp.write_single_coil(UG["REG_UG1_ComandosDigitais_MXW_ResetGeral"], 1)
        self.ug2_clp.write_single_coil(UG["REG_UG2_ComandosDigitais_MXW_ResetGeral"], 1)
        self.usn_clp.write_single_coil(SA["REG_SA_ComandosDigitais_MXW_ResetGeral"], 1)
        self.tda_clp.write_single_coil(TDA["REG_TDA_ComandosDigitais_MXW_ResetGeral"], 1) if not self.TDA_Offline else logger.debug("CLP TDA Offline, não há como realizar o reset geral")
        self.ug1_clp.write_single_coil(UG["REG_UG1_ComandosDigitais_MXW_Cala_Sirene"], 1)
        self.ug2_clp.write_single_coil(UG["REG_UG2_ComandosDigitais_MXW_Cala_Sirene"], 1)
        self.usn_clp.write_single_coil(SA["REG_SA_ComandosDigitais_MXW_Cala_Sirene"], 1)
        logger.debug("Fecha Dj52L")
        self.fechaDj52L()

    def somente_reconhecer_emergencia(self):
        logger.debug("Somente reconhece alarmes não implementado em SEB")
        self.ug1_clp.write_single_coil(UG["REG_UG1_ComandosDigitais_MXW_Cala_Sirene"], 1)
        self.ug2_clp.write_single_coil(UG["REG_UG2_ComandosDigitais_MXW_Cala_Sirene"], 1)
        self.usn_clp.write_single_coil(SA["REG_SA_ComandosDigitais_MXW_Cala_Sirene"], 1)

    def acionar_emergencia(self):
        logger.warning("FC: Acionando emergencia")
        self.ug1_clp.write_single_coil(UG["REG_UG1_ComandosDigitais_MXW_EmergenciaViaSuper"], 1)
        self.ug2_clp.write_single_coil(UG["REG_UG2_ComandosDigitais_MXW_EmergenciaViaSuper"], 1)
        sleep(5)
        self.ug1_clp.write_single_coil(UG["REG_UG1_ComandosDigitais_MXW_EmergenciaViaSuper"], 0)
        self.ug2_clp.write_single_coil(UG["REG_UG2_ComandosDigitais_MXW_EmergenciaViaSuper"], 0)

    def get_flag_falha52L(self):
        if self.usn_clp.read_discrete_inputs(SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert1"])[0] == 0:
            logger.info("DisjDJ1_SuperBobAbert1")
            return True

        if self.usn_clp.read_discrete_inputs(SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert2"])[0] == 0:
            logger.info("DisjDJ1_SuperBobAbert2")
            return True

        if self.usn_clp.read_discrete_inputs(SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiMot"])[0] == 0:
            logger.info("DisjDJ1_Super125VccCiMot")
            return True

        if self.usn_clp.read_discrete_inputs(SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiCom"])[0] == 0:
            logger.info("DisjDJ1_Super125VccCiCom")
            return True

        if self.usn_clp.read_discrete_inputs(SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa"])[0] == 1:
            logger.info("DisjDJ1_AlPressBaixa")
            return True

        if self.usn_clp.read_discrete_inputs(SA["REG_SA_RetornosDigitais_MXR_DJ1_FalhaInt"])[0] == 1:
            logger.info("MXR_DJ1_FalhaInt")
            return True

        if self.usn_clp.read_discrete_inputs(SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa"])[0] == 1:
            logger.info("DisjDJ1_BloqPressBaixa")
            return True

        if self.usn_clp.read_discrete_inputs(SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb1"])[0] == 0:
            logger.info("DisjDJ1_Sup125VccBoFeAb1")
            return True

        if self.usn_clp.read_discrete_inputs(SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb2"])[0] == 0:
            logger.info("DisjDJ1_Sup125VccBoFeAb2")
            return True

        if self.usn_clp.read_discrete_inputs(SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Local"])[0] == 1:
            logger.info("DisjDJ1_Local")
            return True

        if self.usn_clp.read_discrete_inputs(SA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_MolaDescarregada"])[0] == 1:
            logger.info("DisjDJ1_MolaDescarregada")
            return True

        return False

class DatabaseConnector:
    def __init__(self):
        self.connection_pool = pooling.MySQLConnectionPool(
            pool_name="my_pool",
            pool_size=10,
            pool_reset_session=True,
            host="localhost",
            user="moa",
            password="&264H3$M@&z$",
            database="django_db",
        )
        
        self.conn = None
        self.cursor = None
        self.conn = self.connection_pool.get_connection()
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def _open(self):
        # self.conn = self.connection_pool.get_connection()
        # self.cursor = self.conn.cursor()
        pass

    def _close(self, commit=True):
        if commit:
            self.commit()
        # self.cursor.close()
        if commit:
            self.commit()
        # self.conn.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def get_parametros_usina(self):
        self._open()
        cols = self.query("SHOW COLUMNS FROM parametros_moa_parametrosusina")
        self.execute("SELECT * FROM parametros_moa_parametrosusina WHERE id = 1")
        parametros_raw = self.fetchone()
        parametros = {}
        for i in range(len(cols)):
            parametros[cols[i][0]] = parametros_raw[i]
        self._close()
        return parametros

    def get_agendamentos_pendentes(self):
        q = (
            "SELECT *"
            "FROM agendamentos_agendamento "
            "WHERE executado = 0 AND data <= ((NOW() + INTERVAL 3 HOUR) + INTERVAL 55 SECOND);"
        )
        self._open()
        result = self.query(q)
        self._close()
        return result

    def update_parametros_usina(self, values):
        q = (
            "UPDATE parametros_moa_parametrosusina "
            "SET timestamp = %s, "
            "kp = %s, "
            "ki = %s, "
            "kd = %s, "
            "kie = %s, "
            "nv_alvo = %s "
            "WHERE id = 1"
        )
        self._open()
        self.execute(q, tuple(values))
        self._close()
        return True

    def update_valores_usina(self, values):
        q = (
            "UPDATE parametros_moa_parametrosusina "
            "SET timestamp = %s, "
            "aguardando_reservatorio = %s, "
            "clp_online = %s, "
            "nv_montante = %s, "
            "ug1_disp = %s, "
            "ug1_pot = %s, "
            "ug1_setpot = %s, "
            "ug1_sinc = %s, "
            "ug1_tempo = %s, "
            "ug2_disp = %s, "
            "ug2_pot = %s, "
            "ug2_setpot = %s, "
            "ug2_sinc = %s, "
            "ug2_tempo = %s "
            "WHERE id = 1"
        )
        self._open()
        self.execute(q, tuple(values))
        self._close()
        return True

    def update_modo_manual(self):
        q = (
            "UPDATE parametros_moa_parametrosusina "
            "SET modo_autonomo = 0 "
            "WHERE id = 1"
        )
        self._open()
        self.execute(
            q,
        )
        self._close()
        return True

    def update_agendamento(self, id_agendamento, executado, obs=""):
        if len(obs) >= 1:
            obs = " - " + obs
        executado = 1 if executado else 0
        q = (
            "UPDATE agendamentos_agendamento "
            " SET "
            " observacao = if(observacao is null,%s, "
            "concat(observacao, %s)), "
            " executado = %s, "
            " modificado_por = 'MOA', "
            " ts_modificado = %s "
            " WHERE id = %s;"
        )
        self._open()
        self.execute(q, (obs, obs, executado, datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), int(id_agendamento)))
        self._close()

    def update_habilitar_autonomo(self):
        q = (
            "UPDATE parametros_moa_parametrosusina "
            "SET modo_autonomo = 1 "
            "WHERE id = 1;"
        )
        self._open()
        self.execute(
            q,
        )
        self._close()

    def update_desabilitar_autonomo(self):
        q = (
            "UPDATE parametros_moa_parametrosusina "
            "SET modo_autonomo = 0 "
            "WHERE id = 1;"
        )
        self._open()
        self.execute(
            q,
        )
        self._close()

    def update_remove_emergencia(self):
        q = (
            "UPDATE parametros_moa_parametrosusina "
            "SET emergencia_acionada = 0 "
            "WHERE id = 1;"
        )
        self._open()
        self.execute(
            q,
        )
        self._close()

    def insert_debug(
        self,
        ts,
        kp,
        ki,
        kd,
        kie,
        cp,
        ci,
        cd,
        cie,
        sp1,
        p1,
        sp2,
        p2,
        nv,
        erro,
        ma,
        cx_kp,
        cx_ki,
        cx_kie,
        cx_c_ie,
    ):
        q = (
            "INSERT INTO `debug`.`moa_debug` "
            "VALUES (%s,%s, "
            "%s,%s, "
            "%s,%s, "
            "%s,%s, "
            "%s,%s, "
            "%s,%s, "
            "%s,%s, "
            "%s,%s, "
            "%s,%s, "
            "%s,%s);"
        )
        self._open()
        self.execute(
            q,
            tuple(
                [
                    ts,
                    kp,
                    ki,
                    kd,
                    kie,
                    cp,
                    ci,
                    cd,
                    cie,
                    sp1,
                    p1,
                    sp2,
                    p2,
                    nv,
                    erro,
                    ma,
                    cx_kp,
                    cx_ki,
                    cx_kie,
                    cx_c_ie,
                ]
            ),
        )
        self._close()

    def get_executabilidade(self, id_comando):
        q = "SELECT executavel_em_autmoatico, executavel_em_manual FROM parametros_moa_comando WHERE id = %s"
        self._open()
        self.execute(q, tuple([id_comando]))
        parametros_raw = self.fetchone()
        self._close()
        return {
            "executavel_em_autmoatico": parametros_raw[0],
            "executavel_em_manual": parametros_raw[1],
        }

    def get_contato_emergencia(self):
        self._open()
        self.execute("SELECT * FROM parametros_moa_contato")
        rows = self.fetchall()
        parametros = {}
        for row in range(len(rows)):
            parametros = rows
        self._close()
        return parametros

class ClpConnector:
    def __init__(self, ip, port):
        self.modbus_clp = ModbusClient(host=ip, port=port, timeout=0.1, unit_id=1)

    def is_online(self):
        if self.modbus_clp.read_holding_registers(0):
            return True
        else:
            return False

    def write_to_single(self, register, value):
        if self.modbus_clp.open():
            self.modbus_clp.write_single_register(register, int(value))
            self.modbus_clp.close()
            return True
        else:
            raise ConnectionError

    def read_sequential(self, fisrt, quantity):
        self.modbus_clp.open()
        result = self.modbus_clp.read_holding_registers(fisrt, quantity)
        self.modbus_clp.close()
        if result:
            return result
        else:
            raise ConnectionError