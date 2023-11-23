__version__ = "0.2"
__author__ = "Lucas Lavratti", "Henrique Pfeifer", "Diego Basgal"
__description__ = "Este módulo corresponde a implementação da conexão e interação com o Banco de Dados MariaDB."

import pytz
import mariadb.connections

from datetime import datetime


class BancoDados:
    def __init__(self, pool_name: "str"):

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

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


    def get_ultimo_estado_ug(self, ug_id: "int") -> "int":
        """
        Função para extrair o último estado da Unidade de Geração do Banco.
        """

        self.cursor.execute(
            f"SELECT ug{ug_id}_ultimo_estado "
            "FROM parametros_parametrosusina "
            "WHERE id = 1;"
        )
        estado = self.cursor.fetchone()
        return estado

    def get_parametros_usina(self) -> "list":
        """
        Função para extrair os parâmetros alterados na Interface WEB.
        """

        self.cursor.execute("SHOW COLUMNS FROM parametros_parametrosusina")
        cols = self.cursor.fetchall()

        self.cursor.execute("SELECT * FROM parametros_parametrosusina WHERE id = 1")
        parametros_raw = self.cursor.fetchone()
        parametros = {}

        for i in range(len(cols)):
            parametros[cols[i][0]] = parametros_raw[i]

        self.conn.commit()
        return parametros

    def get_agendamentos_pendentes(self) -> "list":
        """
        Função para extrair a lista de agendamentos pendentes criados na Interface WEB.
        """

        self.cursor.execute(
            "SELECT * "
            "FROM agendamentos_agendamento "
            "WHERE executado = 0 AND data <= (NOW() + INTERVAL 30 SECOND);"
        )
        result = self.cursor.fetchall()

        self.conn.commit()
        return result

    def get_contato_emergencia(self) -> "list":
        """
        Função para extrair lista de contatos de sobreaviso adicionados na Interface
        WEB, para chamada por Voip.
        """

        self.cursor.execute("SELECT * FROM contatos_contato")
        rows = self.cursor.fetchall()
        parametros = {}

        for _ in range(len(rows)):
            parametros = rows

        self.conn.commit()
        return parametros

    def get_executabilidade(self, id_comando: "int") -> "dict":
        """
        Função para extrair a variável de verificação do modo de execução de
        agendamentos.
        """

        self.cursor.execute(
            "SELECT executavel_em_automatico, executavel_em_manual "
            "FROM parametros_comando "
            "WHERE id = %s", tuple([id_comando])
        )
        parametros_raw = self.cursor.fetchone()

        self.conn.commit()
        return {
            "executavel_em_automatico": parametros_raw[0],
            "executavel_em_manual": parametros_raw[1],
            }

    def update_modo_moa(self, modo: "bool") -> "None":
        """
        Função para atualizar o modo do MOA no Banco.
        """

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

    def update_remove_emergencia(self) -> "None":
        """
        Função para atualizar o valor de emergência (desativada) do Banco.
        """

        self.cursor.execute(
            "UPDATE parametros_parametrosusina "
            "SET emergencia_acionada = 0 "
            "WHERE id = 1;",
        )
        self.conn.commit()

    def update_valores_usina(self, valores: "list") -> "None":
        """
        Função para atualizar os valores de operação do MOA no Banco.
        """

        self.cursor.execute(
            "UPDATE parametros_parametrosusina "
            "SET timestamp = %s, "
            "aguardando_reservatorio = %s, "
            "nv_montante = %s, "
            "ug1_pot = %s, "
            "ug1_setpot = %s, "
            "ug1_ultimo_estado = %s, "
            "ug2_pot = %s, "
            "ug2_setpot = %s, "
            "ug2_ultimo_estado = %s, "
            "ug3_pot = %s, "
            "ug3_setpot = %s, "
            "ug3_ultimo_estado = %s, "
            "ug4_pot = %s, "
            "ug4_setpot = %s, "
            "ug4_ultimo_estado = %s "
            "WHERE id = 1;",
            tuple(valores)
        )
        self.conn.commit()

    def update_debug(self, valores: "list") -> "None":
        """
        Função para atualizar os valores de operação DEBUG do MOA no Banco.
        """

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
                    "%s,%s, "
                    "%s,%s,);",
                    tuple(valores)
        )
        self.conn.commit()

    def update_controle_estados(self, valores: "int") -> "None":
        """
        Função para atualizar o último estado das Unidades de Geração no Banco.
        """

        self.cursor.execute(
            "INSERT INTO parametros_controleestados "
            "VALUES (%s,%s, "
                    "%s,%s, "
                    "%s);",
                    tuple(valores)
        )
        self.conn.commit()

    def update_alarmes(self, valores: "list") -> "None":
        """
        Função para atualizar a lista de acionamentos/alarmes para visualização
        na interface WEB.
        """

        self.cursor.execute(
            "INSERT INTO alarmes_alarmes "
            "VALUES (%s, %s, %s);",
            tuple(valores)
        )
        self.conn.commit()

    def update_agendamento(self, id_agendamento: "int", executado: "int", obs: "str"="") -> "None":
        """
        Função para atualizar se o agendamento foi executado no Banco para a interface
        WEB.
        """

        if len(obs) >= 1:
            obs = " - " + obs

        self.cursor.execute(
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
        self.conn.commit()