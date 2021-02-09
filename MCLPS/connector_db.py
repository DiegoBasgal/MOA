import pyodbc

def __conectardb():
    """
    Uso interno apenas, retorna um cursor no banco
    Dados para a conexão com o banco de dados
    """

    DB_SERVER = "DEV-SUPER-1\MSSQL_DEV"
    DB_SERVER = "localhost\MSSQL_DEV"
    DB_DATABASE = 'CLP'

    #  Melhorar a segurança na conexao com o banco de dados.
    #  Usar o 'sa' não é adequado. Oferece riscos desnecessários ao sistema.
    DB_USERNAME = 'sa'
    DB_PASSWORD = 'sa123'

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + DB_SERVER +
                          ';DATABASE=' + DB_DATABASE + ';UID=' + DB_USERNAME + ';PWD=' + DB_PASSWORD, autocommit=True)
    cursor = cnxn.cursor()
    return cursor


def get_amostras():

    cursor = __conectardb()
    cursor.execute("""
    -- Sleciona os dados necessários para reproduzir o comportamento da usina no MCLPS
    SELECT [E3TimeStamp]
          ,[nivel_montante]
          ,[potencia_ug1]
          ,[energia_ug1]
          ,[potencia_ug2]
          ,[energia_ug2]
          ,[comporta_value]
          ,[comporta_fechada]
          ,[comporta_pos_1]
          ,[comporta_pos_2]
          ,[comporta_pos_3]
          ,[comporta_pos_4]
          ,[comporta_aberta]
    FROM [CLP].[dbo].[amostragem_usina]
    ORDER BY E3TimeStamp ASC
    """)

    lista = []
    for row in cursor:
        lista.append([elem for elem in row])

    return lista


def get_amostras_afluente():

    try:
        cursor = __conectardb()
        cursor.execute("""
        -- Sleciona os dados necessários para reproduzir o comportamento da usina no MCLPS
        SELECT TOP(100000000) horario, vazao
        FROM [CLP].[dbo].[amostragem_afluente]
        ORDER BY horario ASC
        """)

        lista = []
        for row in cursor:
            lista.append([elem for elem in row])

        return lista

    except Exception as e:
        raise e


def executar_q(q):
    cursor = __conectardb()
    cursor.execute(q)
    return cursor


