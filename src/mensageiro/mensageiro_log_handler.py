from logging import Handler
from . import telegram_bot
from . import voip


class MensageiroHandler(Handler):

    def emit(self, record):
        log_entry = self.format(record)
        telegram_bot.enviar_a_todos(log_entry)

        if record.levelno >= 50:
            voip.enviar_voz_teste()
            print("Erro CRIT: acionando VOIP")
        return True
