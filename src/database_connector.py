import mysql.connector
from mysql.connector import pooling

class Database:

    def __init__(self):    
        self.connection_pool = pooling.MySQLConnectionPool(pool_name="my_pool",
                                                           pool_size=5,
                                                           pool_reset_session=True,
                                                           host = "localhost",
                                                           user = "moa",
                                                           password = "senhaFraca123",
                                                           database = "django_db")
                                                           
        self.conn = None
        self.cursor = None

    def commit(self):
        self.conn.commit()

    def _open(self):
        self.conn = self.connection_pool.get_connection()
        self.cursor = self.conn.cursor()

    def _close(self, commit=True):
        if commit:
            self.commit()
        self.cursor.close()
        if commit:
            self.commit()
        self.conn.close()

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
            "WHERE executado = 0;"
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
            "ug1_temp_mancal = %s, ug2_perda_grade = %s, ug2_temp_mancal = %s " \
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

    def update_agendamento(self, id_agendamento, executado):
        executado = 1 if executado else 0
        q = "UPDATE agendamentos_agendamento " \
            "SET executado = %s " \
            "WHERE id = %s;"
        self._open()
        self.execute(q, (executado, int(id_agendamento)))
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
