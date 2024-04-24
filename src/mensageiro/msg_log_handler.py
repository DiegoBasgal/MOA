import logging

import src.dicionarios.dict as vd

from logging import Handler

from .voip import Voip
from .whatsapp import WhatsApp

class MensageiroHandler(Handler):

    def emit(self, record):
        return
        log_entry = self.format(record)

        try:
            WhatsApp.envio_todos(f"{log_entry}")

        except Exception:
            print(f"Erro ao logar WhatsApp.")

        if record.levelno >= logging.CRITICAL:
            try:
                WhatsApp.envio_todos(f"Foi identificada um acionamento Crítico. Acionando VOIP...")
                vd.voip["EMERGENCIA"][0] = True
                Voip.acionar_chamada()

            except Exception:
                print(f"Erro ao ligar por Voip.")

        return True
