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
fh = logging.FileHandler("telegram_bot.log")
ch = logging.StreamHandler(stdout)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
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

def salvar_config(config):
    with open(config_file, "w") as file:
        json.dump(config, file, indent=4)


def start(update: Update, _: CallbackContext) -> None:
    chat_id = update.message.chat.id
    name = "{}".format(update.message.from_user.full_name)
    logger.info("Chamada start de {} (Chat_id: {})".format(name, chat_id))
    if chat_id in config['chat_ids']:
        update.message.reply_text('Este Chat já esta adicionado a lista de destinatários')
    else:
        config['chat_ids'].append(chat_id)
        salvar_config(config)
        update.message.reply_text('Chat adicionado a lista de destinatários')


def help_command(update: Update, _: CallbackContext) -> None:
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
    chat_id = update.message.chat.id
    name = "{}".format(update.message.from_user.full_name)
    logger.info("Chamada spam_command de {} (Chat_id: {})".format(name, chat_id))
    for i in range(5):
        update.message.reply_text("SPAM! {}/5".format(i))


def quit_command(update: Update, _: CallbackContext) -> None:
    chat_id = update.message.chat.id
    name = "{}".format(update.message.from_user.full_name)
    logger.info("Chamada quit_command de {} (Chat_id: {})".format(name, chat_id))
    chat_id = update.message.chat.id
    update.message.reply_text("Chat removido da lista.")
    config['chat_ids'].remove(chat_id)
    salvar_config(config)


def enviar_a_todos(mensagem):

    bot = telegram.Bot(config['bot_token'])
    for chat_id in config['chat_ids']:
        try:
            bot.send_message(chat_id=chat_id, text=mensagem)
        except telegram.error.Unauthorized as e:
            logger.error("Erro \"{}\" no chat \"{}\"".format(e, chat_id))
            config['chat_ids'].remove(chat_id)
            salvar_config(config)
            enviar_a_todos("Erro \"{}\" no chat \"{}\"\n Chat_id {} excluido.".format(e, chat_id, chat_id))
            continue
        except Exception as e:
            logger.error("Erro \"{}\" no chat \"{}\"".format(e, chat_id))
            continue

def main() -> None:

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
