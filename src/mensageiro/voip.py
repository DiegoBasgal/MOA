import json
import logging
import os
from sys import stdout
from urllib.request import Request, urlopen
# from MySQLdb import connect, cursors

# Inicializando o logger principal
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# LOG to file
fh = logging.FileHandler("voip.log")
ch = logging.StreamHandler(stdout)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fh.setFormatter(logFormatter)
ch.setFormatter(logFormatter)
fh.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.addHandler(ch)

# Carrega as configurações e vars
config_file = os.path.join(os.path.dirname(__file__), 'voip_config.json')
with open(config_file, 'r') as file:
    config = json.load(file)

audio_teste = config['audio_teste']
caller_voip = config['caller_voip']
token_auth_voip = config['token_auth_voip']
voz_habilitado = config['voz_habilitado']


lista_de_contatos_padrao = [["DEBUG MOA", "41988591567"],]

# TODO: Separar acessos ao banco de dados
# Lê do banco
try:
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
except Exception as e:
    logger.error("Exception ao ler os contatos do banco de dados. {}".format(e))


def enviar_voz_teste(lista_de_contatos=None):

    if voz_habilitado:
        logger.debug("Enviando Voz Teste")
        if lista_de_contatos is None:
            lista_de_contatos = lista_de_contatos_padrao

        for contato in lista_de_contatos:
            logger.info("Disparando torpedo de voz para {} ({})".format(contato[0], contato[1]))

            data = {
                'caller': caller_voip,
                'called': '{}'.format(contato[1]),
                'audio': audio_teste
            }
            headers = {
                'Content-Type': 'application/json',
                'token_auth': token_auth_voip
            }

            data = json.dumps(data)
            data = str(data).encode()
            request = Request('https://api.nvoip.com.br/v1/torpedovoz', data=data, headers=headers)
            response_body = urlopen(request).read()
            logger.debug("Response: {} ".format(response_body))

