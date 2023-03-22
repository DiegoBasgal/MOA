__author__ = "Lucas Lavratti", "Diego Basgal"
__credits__ = "Lucas Lavratti" , "Diego Basgal"

__version__ = "0.2"
__status__ = "Development"
__maintainer__ = "Diego Basgal"
__email__ = "diego.garcia@ritmoenergia.com.br"
__description__ = "Este módulo corresponde a implementação de conexão com setores de campo (TDA, BAY, SE...)."


import pytz
import logging

from time import sleep
from datetime import datetime
from mysql.connector import pooling

from escrita import *

from dicionarios.reg import *
from conversor_protocolo.conversor import *

from clients import ClientsUsn

logger = logging.getLogger("__main__")

class ConectorCampo:
    def __init__(
            self,
            sd: dict | None = ...,
            cln: ClientsUsn | None = ...,
            escritas: list[EscritaBase] = ...
        ) -> ...:

        if not cln:
            raise ValueError("[CON] Não foi possível carregar o dicionário compartilhado.")
        else:
            self.dict = sd

        if not cln:
            raise ConnectionError("[CON] Não foi possível carregar classe de conexão com os clientes da usina.")
        else:
            self.opc = cln.opc_client
            self.clp_ug1 = cln.clp_dict[1]
            self.clp_ug2 = cln.clp_dict[2]

        if not escritas:
            raise ValueError("[CON] Não foi possível carregar lista com classes de Escrita")
        else:
            self.esc_opc: EscritaOpc = escritas[0]
            self.esc_opc_bit: EscritaOpcBit = escritas[1]


    def modifica_controles_locais(self):
        if not self.dict["GLB"]["tda_offline"]:
            self.esc_opc_bit.escrever(OPC_UA["TDA"]["CP1_CMD_REARME_FALHAS"], valor=1, bit=0)
            self.esc_opc_bit.escrever(OPC_UA["TDA"]["CP2_CMD_REARME_FALHAS"], valor=1, bit=0)
        else:
            logger.debug("Não é possível modificar os controles locais pois o CLP da TDA se encontra offline")

    def fechaDj52L(self):
        """if not self.get_flag_falha52L():
            return False
        else:"""
        # utilizar o write_value_bool para o ambiente em produção e write_single_register para a simulação
        res = self.esc_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_FECHA_52L"], valor=1, bit=4)
        return res

    def normalizar_emergencia(self):
        logger.info("[CON] Normalizando emergência")
        self.fechaDj52L()

    def resetar_emergencia(self) -> bool:
        try:
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_RESET_FALHAS_PASSOS"], valor=1, bit=0)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_REARME_BLOQUEIO_86M"], valor=1, bit=1)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_REARME_BLOQUEIO_86E"], valor=1, bit=2)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_REARME_BLOQUEIO_86H"], valor=1, bit=3)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_UHRV_REARME_FALHAS"], valor=1, bit=0)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_UHLM_REARME_FALHAS"], valor=1, bit=16)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_RESET_FALHAS_PASSOS"], valor=1, bit=0)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_REARME_BLOQUEIO_86M"], valor=1, bit=1)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_REARME_BLOQUEIO_86E"], valor=1, bit=2)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_REARME_BLOQUEIO_86H"], valor=1, bit=3)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_UHRV_REARME_FALHAS"], valor=1, bit=0)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_UHLM_REARME_FALHAS"], valor=1, bit=16)
            res = self.esc_opc_bit.escrever(OPC_UA["SA"]["RESET_FALHAS_BARRA_CA"], valor=1, bit=0)
            res = self.esc_opc_bit.escrever(OPC_UA["SA"]["RESET_FALHAS_SISTEMA_AGUA"], valor=1, bit=1)
            res = self.esc_opc_bit.escrever(OPC_UA["SA"]["REARME_BLOQUEIO_GERAL_E_FALHAS_SA"], valor=1, bit=23)
            res = self.esc_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_REARME_BLOQUEIO_GERAL"], valor=1, bit=0)
            res = self.esc_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_REARME_86T"], valor=1, bit=1)
            res = self.esc_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_REARME_86BF"], valor=1, bit=2)
            res = self.esc_opc_bit.escrever(OPC_UA["SE"]["REARME_86BF_86T"], valor=1, bit=22)
            res = self.esc_opc_bit.escrever(OPC_UA["SE"]["CMD_SE_RESET_REGISTROS"], valor=1, bit=5)
            if not self.dict["GLB"]["tda_offline"]:
                self.esc_opc_bit.escrever(OPC_UA["TDA"]["CP1_CMD_REARME_FALHAS"], valor=1, bit=0)
                self.esc_opc_bit.escrever(OPC_UA["TDA"]["CP2_CMD_REARME_FALHAS"], valor=1, bit=0) 
            else: 
                logger.debug("CLP TDA Offline, não há como realizar o reset geral")
            return res

        except Exception as e:
            logger.exception(f"[CON] Houve um erro ao realizar o reset geral. Exception: \"{repr(e)}\"")
            logger.exception(f"[CON] Traceback: {traceback.print_stack}")
            return False

    def reconhecer_emergencia(self):
        logger.debug("XAV possui apenas reconhecimento interno de alarmes")

    def acionar_emergencia(self) -> bool:
        logger.warning("FC: Acionando emergencia")
        try:
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_PARADA_EMERGENCIA"], valor=1, bit=4)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_PARADA_EMERGENCIA"], valor=1, bit=4)
            sleep(5)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG1_CMD_PARADA_EMERGENCIA"], valor=0, bit=4)
            res = self.esc_opc_bit.escrever(OPC_UA["UG"]["UG2_CMD_PARADA_EMERGENCIA"], valor=0, bit=4)
            return res

        except Exception as e:
            logger.exception(f"[CON] Houve um erro ao realizar acionar a emergência. Exception: \"{repr(e)}\"")
            logger.exception(f"[CON] Traceback: {traceback.print_stack}")
            return False

    # TODO verificar flags de falha dj XAV
    """def get_flag_falha52L(self):
        # adicionar estado do disjuntor
        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert1"]) == 0:
            logger.info("DisjDJ1_SuperBobAbert1")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_SuperBobAbert2"]) == 0:
            logger.info("DisjDJ1_SuperBobAbert2")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiMot"]) == 0:
            logger.info("DisjDJ1_Super125VccCiMot")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Super125VccCiCom"]) == 0:
            logger.info("DisjDJ1_Super125VccCiCom")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_AlPressBaixa"]) == 1:
            logger.info("DisjDJ1_AlPressBaixa")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_RetornosDigitais_MXR_DJ1_FalhaInt"]) == 1:
            logger.info("MXR_DJ1_FalhaInt")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_BloqPressBaixa"]) == 1:
            logger.info("DisjDJ1_BloqPressBaixa")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb1"]) == 0:
            logger.info("DisjDJ1_Sup125VccBoFeAb1")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Sup125VccBoFeAb2"]) == 0:
            logger.info("DisjDJ1_Sup125VccBoFeAb2")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_Local"])[0] == 1:
            logger.info("DisjDJ1_Local")
            return True

        if LeituraOPC(self.opc, OPC_UA["REG_SA_EntradasDigitais_MXI_SA_DisjDJ1_MolaDescarregada"])[0] == 1:
            logger.info("DisjDJ1_MolaDescarregada")
            return True

        return False"""


class ConectorBay:
    def __init__(self, conversor: NativoParaExterno=None, dados: dict[str, bool]=None) -> None:
        if None in (conversor, dados):
            logger.warning("Erro ao carregar argumentos da classe \"ConectorBay\".")
            raise ImportError
        else:
            self.dados = dados
            self.conv = conversor

        

    def verificar_status_DJs(self) -> bool:
        return




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