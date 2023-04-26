from logging import Handler

from . import telegram_bot

class MensageiroHandler(Handler):
    def emit(self, record):
        log_entry = self.format(record)
        try:
            telegram_bot.enviar_a_todos(log_entry)
        except Exception as e:
            print(f"Erro ao logar no telegram. Exception: {repr(e)}.")

        return True
