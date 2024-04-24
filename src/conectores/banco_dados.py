import pytz
import mariadb.connections

from datetime import datetime


class BancoDados:
    cnx = mariadb.ConnectionPool(
        host="localhost",
        user="moa",
        password="&264H3$M@&z$",
        database="django_db",
        pool_name='MOA',
        pool_size=10,
        pool_validation_interval=250,
    )

    conn = cnx.get_connection()
    cursor = conn.cursor()


    @classmethod
    def get_ultimo_estado_ug(cls, ug_id: "int") -> "int":
        """
        Função para extrair o último estado da Unidade de Geração do Banco.
        """

        cls.cursor.execute(
            f"SELECT ug{ug_id}_ultimo_estado "
            "FROM parametros_parametrosusina "
            "WHERE id = 1;"
        )
        estado = cls.cursor.fetchone()
        return estado


    @classmethod
    def get_parametros_usina(cls) -> "list":
        """
        Função para extrair os parâmetros alterados na Interface WEB.
        """

        cls.cursor.execute(
            "SHOW COLUMNS "
            "FROM parametros_parametrosusina"
        )
        cols = cls.cursor.fetchall()

        cls.cursor.execute(
            "SELECT * "
            "FROM parametros_parametrosusina "
            "WHERE id = 1;"
        )
        parametros_raw = cls.cursor.fetchone()
        parametros = {}

        for i in range(len(cols)):
            parametros[cols[i][0]] = parametros_raw[i]

        cls.conn.commit()
        return parametros


    @classmethod
    def get_agendamentos_pendentes(cls) -> "list":
        """
        Função para extrair a lista de agendamentos pendentes criados na Interface WEB.
        """

        cls.cursor.execute(
            "SELECT * "
            "FROM agendamentos_agendamento "
            "WHERE executado = 0 "
            "AND data <= (NOW() + INTERVAL 30 SECOND);" # - INTERVAL 3 HOUR -> Timezone
        )
        result = cls.cursor.fetchall()

        cls.conn.commit()
        return result


    @classmethod
    def get_contato_emergencia(cls) -> "list":
        """
        Função para extrair lista de contatos de sobreaviso adicionados na Interface
        WEB, para chamada por Voip.
        """

        cls.cursor.execute(
            "SELECT * "
            "FROM contatos_contato"
        )
        rows = cls.cursor.fetchall()
        parametros = {}

        for _ in range(len(rows)):
            parametros = rows

        cls.conn.commit()
        return parametros


    @classmethod
    def get_executabilidade(cls, id_comando: "int") -> "dict":
        """
        Função para extrair a variável de verificação do modo de execução de
        agendamentos.
        """

        cls.cursor.execute(
            "SELECT executavel_em_automatico, executavel_em_manual "
            "FROM parametros_comando "
            "WHERE id = %s",
            tuple([id_comando])
        )
        parametros_raw = cls.cursor.fetchone()

        cls.conn.commit()
        return {
            "executavel_em_automatico": parametros_raw[0],
            "executavel_em_manual": parametros_raw[1],
            }


    @classmethod
    def get_timestamp_moa(cls) -> "datetime":
        cls.cursor.execute(
            "SELECT ts "
            "FROM parametros_parametrosusina "
            "WHERE id = 1"
        )

        ts = cls.cursor.fetchone()
        cls.conn.commit()
        return ts


    @classmethod
    def update_modo_moa(cls, modo: "bool") -> "None":
        """
        Função para atualizar o modo do MOA no Banco.
        """

        if modo:
            cls.cursor.execute(
                "UPDATE parametros_parametrosusina "
                "SET modo_autonomo = 1 "
                "WHERE id = 1"
            )
        else:
            cls.cursor.execute(
                "UPDATE parametros_parametrosusina "
                "SET modo_autonomo = 0 "
                "WHERE id = 1"
            )
        cls.conn.commit()


    @classmethod
    def update_nv_alvo(self, valores: "list") -> "None":
        self.cursor.execute(
            "UPDATE parametros_parametrosusina "
            "SET nv_alvo = %s "
            "WHERE id = 1;",
            tuple(valores)
        )
        self.conn.commit()


    @classmethod
    def update_remove_emergencia(cls) -> "None":
        """
        Função para atualizar o valor de emergência (desativada) do Banco.
        """

        cls.cursor.execute(
            "UPDATE parametros_parametrosusina "
            "SET emergencia_acionada = 0 "
            "WHERE id = 1;",
        )
        cls.conn.commit()


    @classmethod
    def update_valores_usina(cls, valores: "list") -> "None":
        """
        Função para atualizar os valores de operação do MOA no Banco.
        """

        cls.cursor.execute(
            "UPDATE parametros_parametrosusina "
            "SET timestamp = %s, "
            "aguardando_reservatorio = %s, "
            "nv_montante = %s, "
            "ug1_pot = %s, "
            "ug1_setpot = %s, "
            "ug1_ultimo_estado = %s, "
            "ug2_pot = %s, "
            "ug2_setpot = %s, "
            "ug2_ultimo_estado = %s "
            "WHERE id = 1;",
            tuple(valores)
        )
        cls.conn.commit()


    @classmethod
    def update_debug(cls, valores: "list") -> "None":
        """
        Função para atualizar os valores de operação DEBUG do MOA no Banco.
        """

        cls.cursor.execute(
            "INSERT INTO `debug`.`moa_debug` "
            "VALUES (%s,%s, "
                    "%s,%s, "
                    "%s,%s, "
                    "%s,%s, "
                    "%s,%s, "
                    "%s,%s, "
                    "%s,%s, "
                    "%s,%s, "
                    "%s,%s);",
                    tuple(valores)
        )
        cls.conn.commit()


    @classmethod
    def update_controle_estados(cls, valores: "list") -> "None":
        """
        Função para atualizar o último estado das Unidades de Geração no Banco.
        """

        cls.cursor.execute(
            "INSERT INTO parametros_controleestados "
            "VALUES (%s,%s,%s);",
            tuple(valores)
        )
        cls.conn.commit()


    @classmethod
    def update_alarmes(cls, valores: "list") -> "None":
        """
        Função para atualizar a lista de acionamentos/alarmes para visualização
        na interface WEB.
        """

        cls.cursor.execute(
            "INSERT INTO alarmes_alarmes "
            "VALUES (%s, %s, %s, %s);",
            tuple(valores)
        )
        cls.conn.commit()


    @classmethod
    def update_agendamento(cls, id_agendamento: "int", executado: "int", obs="") -> "None":
        """
        Função para atualizar se o agendamento foi executado no Banco para a interface
        WEB.
        """

        if len(obs) >= 1:
            obs = " - " + obs

        cls.cursor.execute(
            "UPDATE agendamentos_agendamento "
            "SET "
            "observacao = if(observacao is null,%s, "
            "concat(observacao, %s)), "
            "executado = %s, "
            "modificado_por = 'MOA', "
            "ts_modificado = %s "
            "WHERE id = %s;",
            (obs, obs, 1 if executado else 0, datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), int(id_agendamento))
        )
        cls.conn.commit()