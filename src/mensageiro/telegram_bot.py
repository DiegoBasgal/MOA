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
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


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


def start(update: Update, _: CallbackContext) -> None:
    """
    Esta função é referente a operação do bot em modo "server".
    Esta função insere o usuário na lista de destinatários do bot.
    """
    chat_id = update.message.chat.id
    name = "{}".format(update.message.from_user.full_name)
    logger.info("Chamada start de {} (Chat_id: {})".format(name, chat_id))
    if chat_id in config['chat_ids']:
        update.message.reply_text('Este Chat já esta adicionado a lista de destinatários')
    else:
        config['chat_ids'].append(chat_id)
        salvar_config()
        update.message.reply_text('Chat adicionado a lista de destinatários')


def help_command(update: Update, _: CallbackContext) -> None:
    """
    Esta função é referente a operação do bot em modo "server".
    Esta função envia uma mensagem com informações de ajuda ao usuário.
    """
    chat_id = update.message.chat.id
    name = "{}".format(update.message.from_user.full_name)
    logger.info("Chamada help_command de {} (Chat_id: {})".format(name, chat_id))
    update.message.reply_text('Esse é o comando de ajuda.\n'
                              'Os comandos implementados são:\n'
                              '/ajuda\n'
                              '/help\n'
                              '/quit\n'
                              '/sair\n'
                              '/spam\n'
                              '/start\n'
                              '\n'
                              '[DEBUG] chat.id:{:d}'.format(update.message.chat.id))


def spam_command(update: Update, _: CallbackContext) -> None:
    """
    Esta função é referente a operação do bot em modo "server".
    Esta função envia várias (5) mensagens repetidas ao usuário.
    Utilizada em debug.
    """
    chat_id = update.message.chat.id
    name = "{}".format(update.message.from_user.full_name)
    logger.info("Chamada spam_command de {} (Chat_id: {})".format(name, chat_id))
    for i in range(5):
        update.message.reply_text("SPAM! {}/5".format(i))


def quit_command(update: Update, _: CallbackContext) -> None:
    """
    Esta função é referente a operação do bot em modo "server".
    Esta função remove um usuário ou grupo da lista de destinatários do bot.
    """
    chat_id = update.message.chat.id
    name = "{}".format(update.message.from_user.full_name)
    logger.info("Chamada quit_command de {} (Chat_id: {})".format(name, chat_id))
    chat_id = update.message.chat.id
    update.message.reply_text("Chat removido da lista.")
    config['chat_ids'].remove(chat_id)
    salvar_config()


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


def main() -> None:
    """
    Esta é a função principal do modo "server" e lida com o pooling das mensagens
    recebidas pelo telegram, efetuando assim o tratamento dos comandos relevantes.

    :return: None
    """

    logger.info("Telegram-bot está sendo iniciado")

    """ Interatividade """
    updater = Updater(config['bot_token'])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("ajuda", help_command))
    dispatcher.add_handler(CommandHandler("spam", spam_command))
    dispatcher.add_handler(CommandHandler("sair", quit_command))
    dispatcher.add_handler(CommandHandler("quit", quit_command))
    updater.start_polling()

    logger.info("Telegram-bot Iniciado")
    enviar_a_todos("[DEBUG] O Bot está ativo.")


if __name__ == '__main__':
    main()
