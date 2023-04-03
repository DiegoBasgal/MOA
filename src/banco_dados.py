__version__ = "0.2"
__author__ = "Lucas Lavratti"
__credits__ = ["Diego Basgal" , ...]
__description__ = "Este módulo corresponde a implementação da conexão com banco de dados."

import pytz

from datetime import datetime
from mysql.connector import pooling, MySQLConnection

# TODO refatorar banco de dados tanto no moa, quanto no banco mesmo e interface web

class BancoDados:
    connection_pool: pooling.MySQLConnectionPool = pooling.MySQLConnectionPool(
        pool_name="my_pool",
        pool_size=10,
        pool_reset_session=True,
        host="localhost",
        user="moa",
        password="&264H3$M@&z$",
        database="django_db",
    )

    cursor = None
    connect: pooling.MySQLConnectionPool = None

    @classmethod
    def _open(cls) -> None:
        cls.connect = cls.connection_pool.get_connection()
        cls.cursor = cls.connect.cursor()

    @classmethod
    def _close(cls, commit=True) -> None:
        if commit:
            cls.commit()
        # cls.connect.close()

    @classmethod
    def query(cls, sql, params=None):
        cls.cursor.execute(sql, params or ())
        return cls.cursor.fetchall()

    @classmethod
    def get_agendamentos_pendentes(cls) -> dict:
        cls._open()
        result = cls.query(
            "SELECT *"
            "FROM agendamentos_agendamento "
            "WHERE executado = 0 AND data <= ((NOW() + INTERVAL 3 HOUR) + INTERVAL 55 SECOND);"
        )
        cls._close()
        return result

    @classmethod
    def get_executabilidade(cls, id_comando: int) -> dict:
        cls._open()
        cls.execute(
            "SELECT executavel_em_autmoatico, executavel_em_manual FROM parametros_moa_comando WHERE id = %s", 
            tuple([id_comando])
        )
        parametros_raw = cls.fetchone()
        cls._close()
        return {
            "executavel_em_autmoatico": parametros_raw[0],
            "executavel_em_manual": parametros_raw[1],
        }

    @classmethod
    def get_parametros_usina(cls) -> dict:
        cls._open()
        cols = cls.query("SHOW COLUMNS FROM parametros_moa_parametrosusina")
        cls.cursor.execute("SELECT * FROM parametros_moa_parametrosusina WHERE id = 1")
        parametros_raw = cls.cursor.fetchall()
        parametros = {}
        for i in range(len(parametros_raw)):
            parametros[cols[i][0]] = parametros_raw[i]
        cls._close()
        return parametros


    @classmethod
    def get_contato_emergencia(cls) -> dict:
        cls._open()
        cls.execute("SELECT * FROM parametros_moa_contato")
        rows = cls.fetchall()
        parametros = {}
        for row in range(len(rows)):
            parametros = rows
        cls._close()
        return parametros

    @classmethod
    def update_valores_usina(cls, values) -> None:
        cls._open()
        cls.execute(
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
            "WHERE id = 1",
            tuple(values)
        )
        cls._close()

    @classmethod
    def update_modo_moa(cls, modo: bool) -> None:
        cls._open()
        if modo:
            cls.execute(
                "UPDATE parametros_moa_parametrosusina "
                "SET modo_autonomo = 1"
                "WHERE id = 1;"
            )
        else:
            cls.execute(
                "UPDATE parametros_moa_parametrosusina "
                "SET modo_autonomo = 0"
                "WHERE id = 1;"
            )
        cls._close()

    @classmethod
    def update_remove_emergencia(cls) -> None:
        cls._open()
        cls.execute(
            "UPDATE parametros_moa_parametrosusina "
            "SET emergencia_acionada = 0 "
            "WHERE id = 1;"
        )
        cls._close()

    @classmethod
    def update_agendamento(cls, id_agendamento: int, executado: int=0, obs="") -> None:
        if len(obs) >= 1:
            obs = " - " + obs
        cls._open()
        cls.execute(
            "UPDATE agendamentos_agendamento "
            " SET "
            " observacao = if(observacao is null, %s, "
            " concat(observacao, %s)), "
            " executado = %s, "
            " modificado_por = 'MOA', "
            " ts_modificado = %s "
            " WHERE id = %s;",
            (obs, obs, executado, cls.get_time())
        )
        cls._close()

    @classmethod
    def insert_debug(
        cls, ts,
        kp, ki,
        kd, kie,
        cp, ci,
        cd, cie,
        sp1, p1,
        sp2, p2,
        nv, erro,
        ma
    ) -> None:
        cls._open()
        cls.execute(
            "INSERT INTO `debug`.`moa_debug` "
            "VALUES (%s,%s, "
                    "%s,%s, "
                    "%s,%s, "
                    "%s,%s, "
                    "%s,%s, "
                    "%s,%s, "
                    "%s,%s, "
                    "%s,%s);",
            tuple([
                ts, kp,
                ki, kd,
                kie, cp,
                ci, cd,
                cie, sp1,
                p1, sp2,
                p2, nv,
                erro,ma
                ]),
        )
        cls._close()