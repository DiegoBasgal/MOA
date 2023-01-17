from datetime import datetime
import mysql.connector
from mysql.connector import pooling

class Database:

    def __init__(self):    
        self.connection_pool = pooling.MySQLConnectionPool(pool_name="my_pool",
                                                           pool_size=10,
                                                           pool_reset_session=True,
                                                           host = "localhost",
                                                           user = "moa",
                                                           password = "senhaFraca123",
                                                           database = "django_db")
                                                           
        self.conn = None
        self.cursor = None
        self.conn = self.connection_pool.get_connection()
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def _open(self):
        #self.conn = self.connection_pool.get_connection()
        #self.cursor = self.conn.cursor()
        pass

    def _close(self, commit=True):
        if commit:
            self.commit()
        #self.cursor.close()
        if commit:
            self.commit()
        #self.conn.close()

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
        q = "SELECT *" \
            "FROM agendamentos_agendamento " \
            "WHERE executado = 0 AND data <= ((NOW() + INTERVAL 3 HOUR) + INTERVAL 55 SECOND);"
        self._open()
        result =  self.query(q)
        self._close()
        return result

    def update_parametros_usina(self, values):
        q = "UPDATE parametros_moa_parametrosusina " \
            "SET timestamp = %s, " \
            "kp = %s, ki = %s, kd = %s,  kie = %s, n_movel_L = %s, n_movel_R = %s, nv_alvo = %s " \
            "WHERE id = 1"
        self._open()
        self.execute(q, tuple(values))
        self._close()
        return True

    
    def update_valores_usina(self, values):
        q = "UPDATE parametros_moa_parametrosusina " \
            "SET timestamp = %s, aguardando_reservatorio = %s, clp_online = %s, nv_montante = %s, pot_disp = %s, " \
            "ug1_disp = %s, ug1_pot = %s, ug1_setpot = %s, ug1_sinc = %s, ug1_tempo = %s, ug2_disp = %s, ug2_pot = %s, " \
            "ug2_setpot = %s, ug2_sinc = %s, ug2_tempo = %s, pos_comporta = %s, ug1_perda_grade = %s, " \
            "ug2_perda_grade = %s " \
            "WHERE id = 1"
        self._open()
        self.execute(q, tuple(values))
        self._close()
        return True

    def update_modo_manual(self):
        q = "UPDATE parametros_moa_parametrosusina " \
            "SET modo_autonomo = 0 " \
            "WHERE id = 1"
        self._open()
        self.execute(q,)
        self._close()
        return True

    def update_agendamento(self, id_agendamento, executado, obs=''):
        if len(obs) >= 1:
            obs = " - " + obs
        executado = 1 if executado else 0
        q  = "UPDATE agendamentos_agendamento " \
            " SET " \
            " observacao = if(observacao is null, %s, concat(observacao, %s)), " \
            " executado = %s, " \
            " modificado_por = 'MOA', " \
            " ts_modificado = %s " \
            " WHERE id = %s;"
        self._open()
        self.execute(q, (obs, obs, executado, datetime.now(), int(id_agendamento)))
        self._close()

    def update_habilitar_autonomo(self):
        q = "UPDATE parametros_moa_parametrosusina " \
            "SET modo_autonomo = 1 " \
            "WHERE id = 1;"
        self._open()
        self.execute(q,)
        self._close()

    def update_desabilitar_autonomo(self):
        q = "UPDATE parametros_moa_parametrosusina " \
            "SET modo_autonomo = 0 " \
            "WHERE id = 1;"
        self._open()
        self.execute(q,)
        self._close()

    def update_remove_emergencia(self):
        q = "UPDATE parametros_moa_parametrosusina " \
            "SET emergencia_acionada = 0 " \
            "WHERE id = 1;"
        self._open()
        self.execute(q,)
        self._close()

    def insert_debug(self, ts, kp, ki, kd, kie, cp, ci, cd, cie, sp1, p1, sp2, p2, nv, erro, ma):
        q = "INSERT INTO `debug`.`moa_debug` " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ); "
        self._open()
        self.execute(q,tuple([ts, kp, ki, kd, kie, cp, ci, cd, cie, sp1, p1, sp2, p2, nv, erro, ma]))
        self._close()

    def get_executabilidade(self, id_comando):
        q = "SELECT executavel_em_autmoatico, executavel_em_manual FROM parametros_moa_comando WHERE id = %s"
        self._open()
        self.execute(q,tuple([id_comando]))
        parametros_raw = self.fetchone()
        self._close()
        return {'executavel_em_autmoatico':parametros_raw[0], 'executavel_em_manual':parametros_raw[1]}
    
    def get_contato_emergencia(self):
        self._open()
        self.execute("SELECT * FROM parametros_moa_contato")
        rows = self.fetchall()
        parametros = {}
        for row in range(len(rows)):
            parametros = rows
        self._close()
        return parametros

