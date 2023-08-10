__version__ = "0.2"
__author__ = "Lucas Lavratti"
__credits__ = ["Diego Basgal", ...]
__description__ = "Este módulo corresponde a implementação da tratativa de loggers para uso nos módulos de Mensageiro."

import logging

import src.dicionarios.dict as dct

from logging import Handler

from src.mensageiro.voip import Voip
from src.mensageiro.whatsapp import WhatsApp

class MensageiroHandler(Handler):

    def emit(self, record) -> "bool":
        """
        Função para captar mensagens de logger e tratamento para disparo via
        WhatsApp ou acionamento NVoip.
        """
        return False

        log_entry = self.format(record)

        WhatsApp.envio_todos(log_entry)

        if record.levelno >= logging.CRITICAL:
            WhatsApp.envio_todos(f"[MSG] Foi identificado um acionamento Crítico. Acionando VOIP...")
            dct.voip["EMERGENCIA"][0] = True
            Voip.acionar_chamada()

        return True
