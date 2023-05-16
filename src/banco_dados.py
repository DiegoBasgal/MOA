import pytz
import mariadb.connections

from datetime import datetime

class Database:
    def __init__(self, pool_name: str):
        self.cnx = mariadb.ConnectionPool(
            host="localhost",
            user="moa",
            password="&264H3$M@&z$",
            database="django_db",
            pool_name=pool_name,
            pool_size=10,
            pool_validation_interval=250,
        )

        self.conn = self.cnx.get_connection()
        self.cursor = self.conn.cursor()


    def get_ultimo_estado_ug(self, ug_id) -> int:
        self.cursor.execute(
            f"SELECT ug{ug_id}_ultimo_estado "
            "FROM `debug`.`moa_debug` "
            "ORDER BY ts DESC"
            "LIMIT 1;"
        )
        estado = self.cursor.fetchone()
        return estado

    def get_parametros_usina(self) -> list:
        self.cursor.execute("SHOW COLUMNS FROM parametros_parametrosusina")
        cols = self.cursor.fetchall()

        self.cursor.execute("SELECT * FROM parametros_parametrosusina WHERE id = 1")
        parametros_raw = self.cursor.fetchone()
        parametros = {}

        for i in range(len(cols)):
            parametros[cols[i][0]] = parametros_raw[i]

        self.conn.commit()
        return parametros

    def get_agendamentos_pendentes(self) -> list:
        self.cursor.execute(
            "SELECT * "
            "FROM agendamentos_agendamento "
            "WHERE executado = 0 AND data <= ((NOW() + INTERVAL 3 HOUR) + INTERVAL 55 SECOND);"
        )
        result = self.cursor.fetchall()

        self.conn.commit()
        return result

    def get_contato_emergencia(self) -> list:
        self.cursor.execute("SELECT * FROM parametros_contato")
        rows = self.cursor.fetchall()
        parametros = {}

        for _ in range(len(rows)):
            parametros = rows

        self.conn.commit()
        return parametros

    def get_executabilidade(self, id_comando) -> dict:
        self.cursor.execute(
            "SELECT executavel_em_autmoatico, executavel_em_manual "
            "FROM parametros_comando "
            "WHERE id = %s", tuple([id_comando])
        )
        parametros_raw = self.cursor.fetchone()

        self.conn.commit()
        return {
            "executavel_em_autmoatico": parametros_raw[0],
            "executavel_em_manual": parametros_raw[1],
            }

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

    def update_remove_emergencia(self) -> None:
        self.cursor.execute(
            "UPDATE parametros_parametrosusina "
            "SET emergencia_acionada = 0 "
            "WHERE id = 1;",
        )
        self.conn.commit()

    def update_tda_offline(self, status=False) -> None:
        if status:
            self.cursor.execute(
                "UPDATE parametros_parametrosusina "
                "SET tda_offline = 1"
                "WHERE id = 1"
            )
        else:
            self.cursor.execute(
                "UPDATE parametros_parametrosusina "
                "SET tda_offline = 0"
                "WHERE id = 1"
            )
        self.conn.commit()

    def update_valores_usina(self, values) -> None:
        self.cursor.execute(
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
            "WHERE id = 1;",
            tuple(values)
        )
        self.conn.commit()

    def update_debug(self, valores) -> None:
        self.cursor.execute(
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
                    "%s,%s, "
                    "%s);",
                    tuple(valores)
        )
        self.conn.commit()

    def update_agendamento(self, id_agendamento, executado, obs="") -> None:
        if len(obs) >= 1:
            obs = " - " + obs

        self.cursor.execute(
            "UPDATE agendamentos_agendamento "
            "SET "
            "observacao = if(observacao is null,%s, "
            "oncat(observacao, %s)), "
            "executado = %s, "
            "modificado_por = 'MOA', "
            "ts_modificado = %s "
            "WHERE id = %s;",
            (obs, obs, 1 if executado else 0, datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), int(id_agendamento))
        )
        self.conn.commit()