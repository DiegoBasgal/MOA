"""
voip.py

Este módulo tem como objetivo a efetuar a comunicação por voip.
O serviço de voip é fornecido pela nvoip e é acessado via web api.

Painel Nvoip: http://painel.nvoip.com.br
Acesso feito com as credênciais do Henrique.

"""
import json
import logging
import os
from sys import stdout
from urllib.request import Request, urlopen

# Inicializando o logger principal
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if not os.path.exists("logs/"):
    os.mkdir("logs/")
fh = logging.FileHandler("logs/watchdog.log")  # log para arquivo
ch = logging.StreamHandler(stdout)  # log para linha de comando
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s")
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
lista_de_contatos_padrao = [["DEBUG MOA", "41988591567"], ["TabordaCorporativo", "41999060224"],]

# Lê do banco
# ToDo Remover o acesso direto ao banco de dados e colocar junto de algum arquivo auxilixar
from MySQLdb import connect, cursors
try:
    mysql_config = {
            "host": "localhost",
            "user": "root",
            "passwd": "11Marco2020@",  #REMOVER
            "db": "django_db",
            "charset": "utf8"
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
    """
    Esta função exemplifica como o envio de um torpedo d voz deve ser feio.
    :param lista_de_contatos: lista de contatos para ligar no formato: [["DEBUG MOA", "41988591567"],]
    :return: None
    """

    # Verifica se esta funcionalidade está habilitada, evitando ligações em momentos de testes.
    if voz_habilitado:
        logger.debug("Enviando Voz Teste")

        # Se a lista de conta não for fornecida, usa-se a lista padrão.
        if lista_de_contatos is None:
            lista_de_contatos = lista_de_contatos_padrao

        # Para cada contato na lista de contatos deve-se fazer uma chamada a web api
        for contato in lista_de_contatos:

            logger.info("Disparando torpedo de voz para {} ({})".format(contato[0], contato[1]))

            # Montagem do pacote para chamar a api
            data = {
                'caller': caller_voip,  # caller fornecido pela nvoip
                'called': '{}'.format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
                'audio': audio_teste  # URL do arquivo de audio (api acessa via GET)
            }
            headers = {
                'Content-Type': 'application/json',
                'token_auth': token_auth_voip  # Token de autenticação fornecido pela nvoip
            }

            # pharse/encode para json
            data = json.dumps(data)
            data = str(data).encode()

            # Envia a request para a api e recebe a resposta
            request = Request('https://api.nvoip.com.br/v1/torpedovoz', data=data, headers=headers)
            response_body = urlopen(request).read()
            logger.debug("Response: {} ".format(response_body))
