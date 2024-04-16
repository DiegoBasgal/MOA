__version__ = "0.1"
__author__ = "Lucas Specht"
__description__ = "Este módulo corresponde a implementação da lógica de envio de mensagens através da API Chat Pro WhatsApp."

import json
import requests

from threading import Thread


class WhatsApp:

    @staticmethod
    def envio_grupo(mensagem):
        """
        Envia uma mensagem para o grupo da Operação Autônoma SEB
        """

        url = "https://v5.chatpro.com.br/chatpro-2322c67a69/api/v1/send_message"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": "e17cb339f10d3f9384027755ffa1c31e"
        }

        payload = {
            "number": "120363164390903005@g.us",
            "message": f"{mensagem}"
        }

        response = requests.post(url, json=payload, headers=headers)
        dict = json.loads(response.text)

        return dict['message']


    @classmethod
    def envio_todos(cls, mensagem) -> None:
        """
        Função de envio utilizando Threads, para não interromper a execução
        do ciclo principal do Watchdog.
        """

        Thread(target=cls.envio_grupo, args=(mensagem, )).start()

