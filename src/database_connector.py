"""
databse_connector.py

Implementado segundo sugestão de carusot42
https://stackoverflow.com/questions/38076220/python-mysqldb-connection-in-a-class/38078544

Here's some sample code where we create a table, add some data, and then read it back out:
with Database('my_db.sqlite') as db:
    db.execute('CREATE TABLE comments(pkey INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR, comment_body VARCHAR, date_posted TIMESTAMP)')
    db.execute('INSERT INTO comments (username, comment_body, date_posted) VALUES (?, ?, current_date)', ('tom', 'this is a comment'))
    comments = db.query('SELECT * FROM comments')
    print(comments)
"""
from datetime import datetime

import mysql.connector


class Database:

    def __init__(self):
        self.config = {
            'host': "localhost",
            'user': "root",
            'passwd': "11Marco2020@",
            'db': "django_db",
            'charset': 'utf8',
        }

        # Paulo: criar pool com 5 conexões
        self._conn = mysql.connector.connect(**self.config)
        self._cursor = self._conn.cursor()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

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
        cols = self.query("SHOW COLUMNS FROM parametros_moa_parametrosusina")
        self.execute("SELECT * FROM parametros_moa_parametrosusina WHERE id = 1")
        parametros_raw = self.fetchone()
        parametros = {}
        for i in range(len(cols)):
            parametros[cols[i][0]] = parametros_raw[i]
        return parametros

    def get_agendamentos_pendentes(self):
        q = """SELECT id, DATE_SUB(data, INTERVAL 3 HOUR), comando_id, executado
                         FROM agendamentos_agendamento
                         WHERE executado = 0"""
        return self.query(q)

    def update_parametrosusina(self, values):
        q = """ UPDATE parametros_moa_parametrosusina
                             SET
                             timestamp = '{}',
                             aguardando_reservatorio = {},
                             clp_online = {},
                             nv_montante = {},
                             pot_disp = {},
                             ug1_disp = {},
                             ug1_pot = {},
                             ug1_setpot = {},
                             ug1_sinc = {},
                             ug1_tempo = {},
                             ug2_disp = {},
                             ug2_pot = {},
                             ug2_setpot = {},
                             ug2_sinc = {},
                             ug2_tempo = {},
                             pos_comporta = {},
                             ug1_perda_grade = {},
                             ug1_temp_mancal = {},
                             ug2_perda_grade = {},
                             ug2_temp_mancal = {}        
                             WHERE id = 1; 
                             """.format(*values)
        self.execute(q)
        return True

    def update_agendamento(self, id_agendamento, executado):
        if executado:
            executado = 1
        else:
            executado = 0
        q = "UPDATE agendamentos_agendamento " \
            "SET executado = {} " \
            "WHERE id = {}".format(executado, int(id_agendamento))
        self.execute(q)

    def update_emergencia(self, estado):
        if estado:
            estado = 1
        else:
            estado = 0
        q = """UPDATE parametros_moa_parametrosusina
                   SET emergencia_acionada = '{}'
                   WHERE id = 1; """.format(estado)
        self.execute(q)
