"""
mensageiro_log_handler.py

Este módulo integra o loggin com o voip e com o telegram.
A princípio pode-se substituir essa implementação por dois handlers
saparados, um para voip e um para o telegram, mas por motivos de
praticidade, foi feito em apenas um handler.
"""
import logging
from logging import Handler
from . import telegram_bot
from . import voip


class MensageiroHandler(Handler):
    """
    Esta classe é o handler que é passado para o loggin e tem
    apenas a função emit(), reposavel por emitir o log.
    """

    def emit(self, record):
        """
        Esta função recebe o texto a ser logado, já formatado, e envia para
        os dstinatários utilizando os módulos de voip e telegram.
        :param record:
        :return: True
        """
        
        log_entry = self.format(record)
        try:
            telegram_bot.enviar_a_todos(log_entry)
        except Exception as e:
            print("Erro ao logar no telegram. Exception: {}.".format(repr(e)))

        # Só dispara torpedos de voz em caso CRITICO (levelno >= 50)
        if record.levelno >= logging.CRITICAL:
            try:
                telegram_bot.enviar_a_todos("[Acionando VOIP: {}]".format(voip.voz_habilitado))
                voip.enviar_voz_emergencia()
            except Exception as e:
                print("Erro ao ligar no voip. Exception: {}.".format(repr(e)))
        return True
