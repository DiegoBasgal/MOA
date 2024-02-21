__version__ = "0.2"
__author__ = "Lucas Lavratti"
__credits__ = ["Diego Basgal", ...]
__description__ = "Este módulo corresponde a implementação da tratativa de loggers para uso nos módulos de Mensageiro."

from logging import Handler

from mensageiro.whatsapp import WhatsApp

class MensageiroHandler(Handler):

    def emit(self, record) -> "bool":
        """
        Função para captar mensagens de logger e tratamento para disparo via
        WhatsApp ou acionamento NVoip.
        """

        log_entry = self.format(record)

        WhatsApp.envio_todos(log_entry)

        return True
