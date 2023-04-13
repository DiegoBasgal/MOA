import pytz
import mariadb.connections

from datetime import datetime


class Database:
    def __init__(self):
        self.cnx = mariadb.ConnectionPool(
            pool_name="my_pool",
            pool_size=10,
            pool_validation_interval=250,
            host="localhost",
            user="moa",
            password="&264H3$M@&z$",
            database="django_db",
        )

        self.conn = self.cnx.get_connection()
        self.cursor = self.conn.cursor()

    def get_parametros_usina(self):
        self.cursor.execute("SHOW COLUMNS FROM parametros_parametrosusina")
        cols = self.cursor.fetchall()

        self.cursor.execute("SELECT * FROM parametros_parametrosusina WHERE id = 1")
        parametros_raw = self.cursor.fetchone()
        parametros = {}
        for i in range(len(cols)):
            parametros[cols[i][0]] = parametros_raw[i]
        self.conn.commit()

        return parametros

    def get_agendamentos_pendentes(self):
        q = (
            "SELECT *"
            "FROM agendamentos_agendamento "
            "WHERE executado = 0 AND data <= ((NOW() + INTERVAL 3 HOUR) + INTERVAL 55 SECOND);"
        )
        self.cursor.execute(q)
        result = self.cursor.fetchall()
        self.conn.commit()
        return result

    def update_parametros_usina(self, values):
        q = (
            "UPDATE parametros_parametrosusina "
            "SET timestamp = %s, "
            "kp = %s, "
            "ki = %s, "
            "kd = %s, "
            "kie = %s, "
            "nv_alvo = %s "
            "WHERE id = 1"
        )
        self.cursor.execute(q, tuple(values))
        self.conn.commit()
        return True

    def update_valores_usina(self, values):
        q = (
            "UPDATE parametros_parametrosusina "
            "SET timestamp = %s, "
            "aguardando_reservatorio = %s, "
            "nv_montante = %s, "
            "ug1_pot = %s, "
            "ug1_setpot = %s, "
            "ug2_pot = %s, "
            "ug2_setpot = %s, "
            "ug3_pot = %s, "
            "ug3_setpot = %s "
            "WHERE id = 1"
        )
        self.cursor.execute(q, tuple(values))
        self.conn.commit()
        return True

    def update_modo_moa(self, modo: bool) -> None:
        if modo:
            self.cursor.execute(
                "UPDATE parametros_parametrosusina " \
                "SET modo_autonomo = 1 " \
                "WHERE id = 1"
            )
        else:
            self.cursor.execute(
                "UPDATE parametros_parametrosusina " \
                "SET modo_autonomo = 0 " \
                "WHERE id = 1"
            )
        self.conn.commit()

    def update_tda_offline(self, status=False):
        q = ("UPDATE parametros_parametrosusina "
            "SET tda_offline = 1"
            "WHERE id = 1") if status else \
            ("UPDATE parametros_parametrosusina "
            "SET tda_offline = 0"
            "WHERE id = 1")
        self.cursor.execute(q)
        self.conn.commit()
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
        self.cursor.execute(q, (obs, obs, executado, datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), int(id_agendamento)))
        self.conn.commit()

    def update_habilitar_autonomo(self):
        q = (
            "UPDATE parametros_parametrosusina "
            "SET modo_autonomo = 1 "
            "WHERE id = 1;"
        )
        self.cursor.execute(
            q,
        )
        self.conn.commit()

    def update_desabilitar_autonomo(self):
        q = (
            "UPDATE parametros_parametrosusina "
            "SET modo_autonomo = 0 "
            "WHERE id = 1;"
        )
        self.cursor.execute(
            q,
        )
        self.conn.commit()

    def update_remove_emergencia(self):
        q = (
            "UPDATE parametros_parametrosusina "
            "SET emergencia_acionada = 0 "
            "WHERE id = 1;"
        )
        self.cursor.execute(
            q,
        )
        self.conn.commit()

    def insert_debug(self,
        ts, ma,
        erro, nv,
        sp1, p1,
        sp2, p2,
        sp3, p3,
        cp, ci,
        cd, cie,
        kp, ki,
        kd, kie
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
            "%s,%s);"
        )
        self.cursor.execute(
            q,
            tuple([
                ts,
                ma,
                erro,
                nv,
                sp1,
                p1,
                sp2,
                p2,
                sp3,
                p3,
                cp,
                ci,
                cd,
                cie,
                kp,
                ki,
                kd,
                kie,
            ]),
        )
        self.conn.commit()

    def get_executabilidade(self, id_comando):
        q = "SELECT executavel_em_autmoatico, executavel_em_manual FROM parametros_comando WHERE id = %s"
        self.cursor.execute(q, tuple([id_comando]))
        parametros_raw = self.cursor.fetchone()
        self.conn.commit()
        return {
            "executavel_em_autmoatico": parametros_raw[0],
            "executavel_em_manual": parametros_raw[1],
        }

    def get_contato_emergencia(self):
        self.cursor.execute("SELECT * FROM parametros_contato")
        rows = self.cursor.fetchall()
        parametros = {}
        for row in range(len(rows)):
            parametros = rows
        self.conn.commit()
        return parametros