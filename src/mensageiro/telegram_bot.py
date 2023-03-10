import os
import pytz
import json
import logging
import telegram
import threading

from sys import stdout
from time import sleep
from telegram import Update
from datetime import datetime
from telegram.ext import Updater, CommandHandler, CallbackContext

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

fh = logging.FileHandler(os.path.join(os.path.dirname(__file__), "logs", "telegram.log"))

ch = logging.StreamHandler(stdout)

def timeConverter(*args):
    return datetime.now(tz).timetuple()

tz = pytz.timezone("Brazil/East")

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s")
logFormatter.converter =timeConverter

fh.setFormatter(logFormatter)
ch.setFormatter(logFormatter)
fh.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.addHandler(ch)


config_file = os.path.join(os.path.dirname(__file__), "telegram_config.json")
with open(config_file, "r") as file:
    config = json.load(file)
logger.debug(f"Config: {config}")


def salvar_config():
    with open(config_file, "w") as file:
        json.dump(config, file, indent=4)


def start(update: Update, _: CallbackContext) -> None:
    chat_id = update.message.chat.id
    name = f"{update.message.from_user.full_name}"
    logger.info(f"Chamada start de {name} (Chat_id: {chat_id})")
    if chat_id in config["chat_ids"]:
        update.message.reply_text("Este Chat já esta adicionado a lista de destinatários")
    else:
        config["chat_ids"].append(chat_id)
        salvar_config()
        update.message.reply_text("Chat adicionado a lista de destinatários")


def help_command(update: Update, _: CallbackContext) -> None:
    chat_id = update.message.chat.id
    name = f"{update.message.from_user.full_name}"
    logger.info(f"Chamada help_command de {name} (Chat_id: {chat_id})")
    update.message.reply_text(
        "Esse é o comando de ajuda.\n"
        "Os comandos implementados são:\n"
        "/ajuda\n"
        "/help\n"
        "/quit\n"
        "/sair\n"
        "/spam\n"
        "/start\n"
        "\n"
        f"[DEBUG] chat.id:{update.message.chat.id:d}"
    )


def spam_command(update: Update, _: CallbackContext) -> None:
    chat_id = update.message.chat.id
    name = f"{update.message.from_user.full_name}"
    logger.info(f"Chamada spam_command de {name} (Chat_id: {chat_id})")
    for i in range(5):
        update.message.reply_text(f"SPAM! {i}/5")


def quit_command(update: Update, _: CallbackContext) -> None:
    chat_id = update.message.chat.id
    name = f"{update.message.from_user.full_name}"
    logger.info(f"Chamada quit_command de {name} (Chat_id: {chat_id})")
    chat_id = update.message.chat.id
    update.message.reply_text("Chat removido da lista.")
    config["chat_ids"].remove(chat_id)
    salvar_config()


def enviar_a_todos(mensagem):
    threading.Thread(target=threaded_enviar_a_todos, args=([mensagem])).start()


def threaded_enviar_a_todos(mensagem):
    with open(config_file, "r") as file:
        config = json.load(file)

    bot = telegram.Bot(config["bot_token"])
    for chat_id in config["chat_ids"]:
        mandou = False
        while not mandou:
            try:
                bot.send_message(chat_id=chat_id, text=mensagem)
                mandou = True
            except telegram.error.Unauthorized as e:
                logger.error(f'Erro "{e}" no chat "{chat_id}"')
                config["chat_ids"].remove(chat_id)
                salvar_config()
                enviar_a_todos(f'Erro "{e}" no chat "{chat_id}"\n Chat_id {chat_id} excluido.')
                sleep(5)
                mandou = False
            except Exception as e:
                logger.error(f'Erro "{e}" no chat "{chat_id}"')
                sleep(5)
                mandou = False

def enviar_a_todos_emergencia():
    threading.Thread(target=threaded_enviar_voz_emergencia).start()

def threaded_enviar_voz_emergencia():
    with open(config_file, "r") as file:
        config = json.load(file)

    bot = telegram.Bot(config["bot_token"])
    for chat_id in config["chat_ids"]:
        mandou = False
        while not mandou:
            try:
                bot.send_message(chat_id=chat_id, text="\U000026A0 \U0000203C EMERGÊNCIA! \U0000203C \U000026A0")
                mandou = True

            except telegram.error.Unauthorized as e:
                logger.error(f'Erro "{e}" no chat "{chat_id}"')
                config["chat_ids"].remove(chat_id)
                salvar_config()
                enviar_a_todos(f'Erro "{e}" no chat "{chat_id}"\n Chat_id {chat_id} excluido.')
                sleep(5)
                mandou = False

            except Exception as e:
                logger.error(f'Erro "{e}" no chat "{chat_id}"')
                sleep(5)
                mandou = False


def main() -> None:
    logger.info("Telegram-bot está sendo iniciado")

    updater = Updater(config["bot_token"])
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


if __name__ == "__main__":
    enviar_a_todos("[DEBUG] TESTE.")
    # main()
