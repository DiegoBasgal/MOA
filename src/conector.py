import pytz
import logging
import traceback

import dicionarios.dict as d

from time import sleep
from datetime import datetime
from mysql.connector import pooling

from dicionarios.reg import *
from dicionarios.const import *

from clients import ClpClients

logger = logging.getLogger("__main__")

class ConectorCampo:
    def __init__(self, clp: ClpClients=None):
        if not clp:
            logger.warning("[CON] Não foi possível carregar classe de conexão com os CLPs da usina.")
            raise ReferenceError
        else:
            self.clp_usn = clp.clp_dict[1]
            self.clp_tda = clp.clp_dict[2]
            self.clp_ug1 = clp.clp_dict[3]
            self.clp_ug2 = clp.clp_dict[4]

        self.dict: dict = d.shared_dict

    def normalizar_emergencia(self) -> None:
        logger.info("[CON] Normalizando emergência...")
        self.resetar_emergencia()
        self.reconhecer_emergencia()
        self.fechaDj52L()

    def resetar_emergencia(self) -> None:
        try:
            logger.debug("[CON] Reset geral.")
            self.clp_usn.write_single_coil(SA["SA_CD_ResetGeral"], 1)
            self.clp_ug1.write_single_coil(UG["UG1_CD_ResetGeral"], 1)
            self.clp_ug2.write_single_coil(UG["UG2_CD_ResetGeral"], 1)
            self.clp_tda.write_single_coil(TDA["TDA_CD_ResetGeral"], 1) if not self.dict["GLB"]["tda_offline"] else logger.debug("[CON] CLP TDA Offline, não há como realizar o reset geral")
        except Exception as e:
            logger.exception(f"[CON] Houve um erro ao realizar o reset geral. Exception: \"{repr(e)}\"")
            logger.exception(f"[CON] Traceback: {traceback.print_stack}")

    def reconhecer_emergencia(self) -> None:
        try:
            logger.debug("[CON] Cala sirene.")
            self.clp_usn.write_single_coil(SA["SA_CD_Cala_Sirene"], 1)
            self.clp_ug1.write_single_coil(UG["UG1_CD_Cala_Sirene"], 1)
            self.clp_ug2.write_single_coil(UG["UG2_CD_Cala_Sirene"], 1)
        except Exception as e:
            logger.exception(f"[CON] Houve um erro ao reconhecer os alarmes. Exception: \"{repr(e)}\"")
            logger.exception(f"[CON] Traceback: {traceback.print_stack}")

    def acionar_emergencia(self) -> None:
        try:
            logger.warning("[CON] Acionando emergência.")
            self.clp_ug1.write_single_coil(UG["UG1_CD_EmergenciaViaSuper"], 1)
            self.clp_ug2.write_single_coil(UG["UG2_CD_EmergenciaViaSuper"], 1)
            sleep(5)
            self.clp_ug1.write_single_coil(UG["UG1_CD_EmergenciaViaSuper"], 0)
            self.clp_ug2.write_single_coil(UG["UG2_CD_EmergenciaViaSuper"], 0)
        except Exception as e:
            logger.exception(f"[CON] Houve um erro ao acionar a emergência. Exception: \"{repr(e)}\"")
            logger.exception(f"[CON] Traceback: {traceback.print_stack}")

    def modifica_controles_locais(self) -> None:
        try:
            if not self.dict["GLB"]["tda_offline"]:
                self.clp_tda.write_single_coil(TDA["TDA_CD_ResetGeral"], 1)
                self.clp_tda.write_single_coil(TDA["TDA_CD_Hab_Nivel"], 0)
                self.clp_tda.write_single_coil(TDA["TDA_CD_Desab_Nivel"], 1)
                self.clp_tda.write_single_coil(TDA["TDA_CD_Hab_Religamento52L"], 0)
                self.clp_tda.write_single_coil(TDA["TDA_CD_Desab_Religamento52L"], 1)
            else:
                logger.debug("[CON] Não é possível modificar os controles locais pois o CLP da TDA se encontra offline")
        except Exception as e:
            logger.exception(f"[CON] Houve um erro ao modificar os controles locais. Exception: \"{repr(e)}\"")
            logger.exception(f"[CON] Traceback: {traceback.print_stack}")

    def fechaDj52L(self) -> bool:
        try:
            if self.get_falha52L():
                return False
            else:
                response = self.clp_usn.write_single_register(SA["SA_CD_Liga_DJ1"], 1)
                return response
        except Exception as e:
            logger.exception(f"[CON] Houver um erro ao fechar o Dj52L. Exception: \"{repr(e)}\"")
            logger.exception(f"[CON] Traceback: {traceback.print_stack}")
            return False

    def get_falha52L(self) -> bool:
        dict_flags: dict[str, int] = {
            SA["SA_RD_DJ1_FalhaInt"]: 1,
            SA["SA_ED_DisjDJ1_Local"]: 1,
            SA["SA_ED_DisjDJ1_AlPressBaixa"]: 1,
            SA["SA_ED_DisjDJ1_BloqPressBaixa"]: 1,
            SA["SA_ED_DisjDJ1_SuperBobAbert2"]: 0,
            SA["SA_ED_DisjDJ1_Sup125VccBoFeAb1"]: 0,
            SA["SA_ED_DisjDJ1_Super125VccCiMot"]: 0,
            SA["SA_ED_DisjDJ1_Super125VccCiCom"]: 0,
            SA["SA_ED_DisjDJ1_Sup125VccBoFeAb2"]: 0,
        }
        try:
            flags = 0
            for nome, valor in zip(dict_flags[0], dict_flags.values()):
                if self.clp_usn.read_discrete_inputs(nome)[0] == valor:
                    logger.debug(f"[CON] Flag -> {nome.keys()}")
                    flags += 1

            logger.info(f"[CON] Foram detectadas Flags de bloqueio ao abrir o Dj52L. Número de bloqueios ativos: \"{flags}\"") if flags else ...
            return True if flags >= 1 else False

        except Exception as e:
            logger.exception(f"[CON] Houve um erro ao ler as flags do Dj52L. Exception: \"{repr(e)}\"")
            logger.exception(f"[CON] Traceback: {traceback.print_stack}")
            return None

class ConectorBancoDados:
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

    def get_time(self) -> object:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

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

    def update_modo_moa(self, modo: bool) -> None:
        if modo:
            q = (
                "UPDATE parametros_moa_parametrosusina "
                "SET modo_autonomo = 1"
                "WHERE id = 1;"
            )
        else:
            q = (
                "UPDATE parametros_moa_parametrosusina "
                "SET modo_autonomo = 0"
                "WHERE id = 1;"
            )
        self._open()
        self.execute(q)
        self._close()

    def update_agendamento(self, id_agendamento, executado, obs=""):
        if len(obs) >= 1:
            obs = " - " + obs
        executado = 1 if executado else 0
        q = (
            "UPDATE agendamentos_agendamento "
            " SET "
            " observacao = if(observacao is null, %s, "
            " concat(observacao, %s)), "
            " executado = %s, "
            " modificado_por = 'MOA', "
            " ts_modificado = %s "
            " WHERE id = %s;"
        )
        self._open()
        self.execute(q, (obs, obs, executado, self.get_time()))
        self._close()

    def update_remove_emergencia(self) -> None:
        self._open()
        self.execute(
            "UPDATE parametros_moa_parametrosusina "
            "SET emergencia_acionada = 0 "
            "WHERE id = 1;"
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