import voip
import logging
import telegram_bot

from logging import Handler

class MensageiroHandler(Handler):
    def emit(self, record):
        return True
        try:
            telegram_bot.enviar_a_todos(self.format(record))
        except Exception as e:
            print(f"Erro ao logar no telegram. Exception: {repr(e)}.")

        if record.levelno >= logging.CRITICAL:
            try:
                telegram_bot.enviar_a_todos(f"[Acionando VOIP: {voip.voz_habilitado}]")
                telegram_bot.enviar_a_todos_emergencia()
                voip.enviar_voz_emergencia()
            except Exception as e:
                print(f"Erro ao ligar no voip. Exception: {repr(e)}.")
        return True
