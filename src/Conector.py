import pytz
import logging

from time import sleep
from opcua import Client, ua
from datetime import datetime
from mysql.connector import pooling

from src.VAR_REG import *
from src.Escrita import *
from src.Leituras import *

logger = logging.getLogger("__main__")

class Database:
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
        pt_kp,
        pt_ki,
        pt_kie,
        pt_c_ie,
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
                    pt_kp,
                    pt_ki,
                    pt_kie,
                    pt_c_ie,
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

class FieldConnector:
    def __init__(self, cfg=None):

        if cfg is None:
            raise Exception("A cfg dict is required")
        else:
            self.client = Client(cfg["client"])

        self.warned_ug1 = False
        self.warned_ug2 = False
        self.TDA_Offline = False

    def modifica_controles_locais(self):
        if not self.TDA_Offline:
            EscritaOPCBit(self.client, REG_OPC["TDA"]["CP1_CMD_REARME_FALHAS"], 0, 1)
            EscritaOPCBit(self.client, REG_OPC["TDA"]["CP1_CMD_REARME_FALHAS"], 0, 1)
        else:
            logger.debug("Não é possível modificar os controles locais pois o CLP da TDA se encontra offline")

    def open(self):
        logger.debug("Conectando ao servidor OPC")
        if not self.client.connect():
            raise ua.UaError("OPC Client ({}) failed to open.".format(self.client))

        logger.debug("Conectado!")
        return self

    def close(self):
        logger.debug("Encerrando conexão OPC")
        self.client.disconnect()
        logger.debug("Conexão encerrada!")

    def fechaDj52L(self):
        if not self.get_flag_falha52L():
            return False
        else:
            # utilizar o write_value_bool para o ambiente em produção e write_single_register para a simulação
            response = EscritaOPCBit(self.client, REG_OPC["SE"]["CMD_SE_FECHA_52L"], 4, 1)
            return response

    def normalizar_emergencia(self):
        logger.info("Reconhecendo alarmes, resetando usina e fechando Dj52L")
        logger.debug("Reconhece/Reset alarmes")
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG1_CMD_RESET_FALHAS_PASSOS"], 0, 1)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG1_CMD_REARME_BLOQUEIO_86M"], 1, 1)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG1_CMD_REARME_BLOQUEIO_86E"], 2, 1)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG1_CMD_REARME_BLOQUEIO_86H"], 3, 1)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG1_CMD_UHRV_REARME_FALHAS"], 0, 1)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG1_CMD_UHLM_REARME_FALHAS"], 16, 1)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_RESET_FALHAS_PASSOS"], 0, 1)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86M"], 1, 1)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86E"], 2, 1)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_REARME_BLOQUEIO_86H"], 3, 1)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_UHRV_REARME_FALHAS"], 0, 1)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_UHLM_REARME_FALHAS"], 16, 1)
        EscritaOPCBit(self.client, REG_OPC["SA"]["RESET_FALHAS_BARRA_CA"], 0, 1)
        EscritaOPCBit(self.client, REG_OPC["SA"]["RESET_FALHAS_SISTEMA_AGUA"], 1, 1)
        EscritaOPCBit(self.client, REG_OPC["SA"]["REARME_BLOQUEIO_GERAL_E_FALHAS_SA"], 23, 1)
        EscritaOPCBit(self.client, REG_OPC["SE"]["CMD_SE_REARME_BLOQUEIO_GERAL"], 0, 1)
        EscritaOPCBit(self.client, REG_OPC["SE"]["CMD_SE_REARME_86T"], 1, 1)
        EscritaOPCBit(self.client, REG_OPC["SE"]["CMD_SE_REARME_86BF"], 2, 1)
        EscritaOPCBit(self.client, REG_OPC["SE"]["REARME_86BF_86T"], 22, 1)
        EscritaOPCBit(self.client, REG_OPC["SE"]["CMD_SE_RESET_REGISTROS"], 5, 1)
        EscritaOPCBit(self.client, REG_OPC["TDA"]["CP1_CMD_REARME_FALHAS"], 0, 1) if not self.TDA_Offline else logger.debug("CLP TDA Offline, não há como realizar o reset geral")
        EscritaOPCBit(self.client, REG_OPC["TDA"]["CP1_CMD_REARME_FALHAS"], 0, 1) if not self.TDA_Offline else logger.debug("CLP TDA Offline, não há como realizar o reset geral")
        logger.debug("Fecha Dj52L")
        self.fechaDj52L()

    def somente_reconhecer_emergencia(self):
        logger.debug("XAV possui apenas reconhecimento interno de alarmes")

    def acionar_emergencia(self):
        logger.warning("FC: Acionando emergencia")
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG1_CMD_PARADA_EMERGENCIA"], 4, 1)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_PARADA_EMERGENCIA"], 4, 1)
        sleep(5)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG1_CMD_PARADA_EMERGENCIA"], 4, 0)
        EscritaOPCBit(self.client, REG_OPC["UG"]["UG2_CMD_PARADA_EMERGENCIA"], 4, 0)

    def get_flag_falha52L(self):
        # adicionar estado do disjuntor
        if LeituraOPC(self.client, REG_OPC["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert1"]) == 0:
            logger.info("DisjDJ1_SuperBobAbert1")
            return True

        if LeituraOPC(self.client, REG_OPC["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert2"]) == 0:
            logger.info("DisjDJ1_SuperBobAbert2")
            return True

        if LeituraOPC(self.client, REG_OPC["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiMot"]) == 0:
            logger.info("DisjDJ1_Super125VccCiMot")
            return True

        if LeituraOPC(self.client, REG_OPC["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiCom"]) == 0:
            logger.info("DisjDJ1_Super125VccCiCom")
            return True

        if LeituraOPC(self.client, REG_OPC["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa"]) == 1:
            logger.info("DisjDJ1_AlPressBaixa")
            return True

        if LeituraOPC(self.client, REG_OPC["REG_SA_RetornosDigitais_MXR_DJ1_FalhaInt"]) == 1:
            logger.info("MXR_DJ1_FalhaInt")
            return True

        if LeituraOPC(self.client, REG_OPC["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa"]) == 1:
            logger.info("DisjDJ1_BloqPressBaixa")
            return True

        if LeituraOPC(self.client, REG_OPC["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb1"]) == 0:
            logger.info("DisjDJ1_Sup125VccBoFeAb1")
            return True

        if LeituraOPC(self.client, REG_OPC["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb2"]) == 0:
            logger.info("DisjDJ1_Sup125VccBoFeAb2")
            return True

        if LeituraOPC(self.client, REG_OPC["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Local"])[0] == 1:
            logger.info("DisjDJ1_Local")
            return True

        if LeituraOPC(self.client, REG_OPC["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_MolaDescarregada"])[0] == 1:
            logger.info("DisjDJ1_MolaDescarregada")
            return True

        return False