"""
    lista de contato
    [[nome, numero],[nome, numero],[nome, numero],...]
"""
import json
from datetime import datetime
from urllib.request import Request, urlopen
from MySQLdb import connect, cursors

whats_habilitado = False
voz_habilitado = False

lista_de_contatos_padrao = []
#lista_de_contatos_padrao = [["DEBUG MOA", "41988591567"], ]


# Lê do banco
mysql_config = {
        'host': "localhost",
        'user': "root",
        'passwd': "11Marco2020@",
        'db': "django_db",
        'charset': 'utf8'
    }
db = connect(**mysql_config)

cur = db.cursor(cursors.DictCursor)
cur.execute("SELECT nome, numero FROM parametros_moa_contato")
rows = cur.fetchall()
for row in rows:
    lista_de_contatos_padrao.append([row["nome"], row["numero"]])



def enviar_whatsapp(mensagem, lista_de_contatos=None):

    if whats_habilitado:
        try:
            if lista_de_contatos is None:
                lista_de_contatos = lista_de_contatos_padrao
            from wappdriver import WhatsApp
            for contato in lista_de_contatos:
                with WhatsApp() as bot:
                    bot.send(contato[0], mensagem)
        except Exception as e:
            pass


def enviar_voz_teste(lista_de_contatos=None):

    if voz_habilitado:

        if lista_de_contatos is None:
            lista_de_contatos = lista_de_contatos_padrao

        for contato in lista_de_contatos:

            data = {
                'caller': '15420001',
                'called': '{}'.format(contato[1]),
                'audio': 'https://media1.vocaroo.com/mp3/1m8VYKqEv0yf'
            }
            headers = {
                'Content-Type': 'application/json',
                'token_auth': 'a4444db1caeb4f178a1e7a46990663'
            }

            data = json.dumps(data)
            data = str(data).encode()
            request = Request('https://api.nvoip.com.br/v1/torpedovoz', data=data, headers=headers)

            response_body = urlopen(request).read()
