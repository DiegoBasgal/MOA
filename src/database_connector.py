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

    """
    __enter__ e __exit__: exemplo de uso:
    with Database('db_file.sqlite') as db:
        # do stuff
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

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
