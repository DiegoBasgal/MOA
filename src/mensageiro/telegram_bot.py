"""
telegram_bot.py

Este módulo implementa um bot para a integração com o telegram.
Existem duas maneiras de utilizar esta integração:

"Server": Uma thread deve ficar ativada para que o bot possa interagir
com mensagens enviadas a ele. Para utilizar este modo basta usar o main().

"Server-less": A implementação permite que o bot envie mensagens aos
destinatários mesmo que não esteja trodando continuamente, porém isto
significa que o bot não atenderá a comandois recebidos no chat.
A principal maneira de se utilizar o modo server-less é através da
função enviar_a_todos().

"""
import json
import logging
import os
from sys import stdout
import telegram


# Inicializando o logger principal
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if not os.path.exists(os.path.join(os.path.dirname(__file__),"logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__),"logs"))
fh = logging.FileHandler(os.path.join(os.path.dirname(__file__),"logs", "telegram.log"))  # log para arquivo
ch = logging.StreamHandler(stdout)  # log para linha de comando

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s")
fh.setFormatter(logFormatter)
ch.setFormatter(logFormatter)
fh.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.addHandler(ch)

# Carrega as configurações e vars
config_file = os.path.join(os.path.dirname(__file__), 'telegram_config.json')
with open(config_file, 'r') as file:
    config = json.load(file)
logger.debug("Config: {}".format(config))


def salvar_config():
    """
    Esta função possibilita salvar as configurações carregadas em memória no
    arquivo json relevante.
    :return: None
    """
    with open(config_file, "w") as file:
        json.dump(config, file, indent=4)

def enviar_a_todos(mensagem):
    """
    Esta função é referente a operação do bot em modo "server-less".
    Esta função envia a mensagem para todos os destinatários cadastrados na lista.
    A lista de destinatários é carregada novamente no início da função.
    Isso pode acarretar em inconsistências caso o modo "server" esteja
    ativo no mesmo momento e altere o arquivo.

    :param mensagem: A menmsagem a ser enviada, já como String formatada.
    :return: None
    """

    # Carrega as configurações e vars
    with open(config_file, 'r') as file:
        config = json.load(file)

    bot = telegram.Bot(config['bot_token'])
    for chat_id in config['chat_ids']:
        try:
            bot.send_message(chat_id=chat_id, text=mensagem)
        except telegram.error.Unauthorized as e:
            logger.error("Erro \"{}\" no chat \"{}\"".format(e, chat_id))
            config['chat_ids'].remove(chat_id)
            salvar_config()
            enviar_a_todos("Erro \"{}\" no chat \"{}\"\n Chat_id {} excluido.".format(e, chat_id, chat_id))
            continue
        except Exception as e:
            logger.error("Erro \"{}\" no chat \"{}\"".format(e, chat_id))
            continue