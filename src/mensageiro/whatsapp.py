import json
import requests

from threading import Thread

class WhatsApp:

    @staticmethod
    def enviar_mensagem(num_destino, mensagem):
        #--> Envia uma mensagem para um numero especifico, ou ID do grupo destino

        url = "https://v5.chatpro.com.br/chatpro-ace98c12f9/api/v1/send_message"
        headers = {"accept": "application/json",
             "content-type": "application/json",
            "Authorization": "52c5e8171974cd0d780db547d59a3f17"}

        payload = {"number": f"{num_destino}",
                  "message": f"{mensagem}"}

        response = requests.post(url, json=payload, headers=headers)
        dict = json.loads(response.text)

        return dict['message']

    @staticmethod
    def chats_ativos():
        #--> Retorna uma lista com todos os chats ativos no whatsapp da Instancia

        url = "https://v5.chatpro.com.br/chatpro-ace98c12f9/api/v1/chats"
        headers = {"accept": "application/json",
            "Authorization": "52c5e8171974cd0d780db547d59a3f17"}

        response = requests.get(url, headers=headers)
        return response.text

    @staticmethod
    def saldo_atual():
        #--> Retorna a quantidade de créditos disponiveis para utilização

        url = "https://api.chatpro.com.br/painel/ws/endpoint.php?action=saldo"
        headers = {"accept": "application/json",
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfdWlkIjoiMTJlYmEzOTA5ZjRmMDQ4OWI2ODc0NGMxMjFkNDAwNGYiLCJpZCI6IjI1MzM3IiwiZW1haWwiOiJsdWNhcy5zcGVjaHRAcml0bW9lbmVyZ2lhLmNvbS5iciJ9.Tc-XjWDicVHCHZ_ZQuHMtZBb1nNKt0Nh9KfehuN2BM4"}

        response = requests.get(url, headers=headers)
        dict = json.loads(response.text)

        return dict['user']['saldo']

    @classmethod
    def verificar_saldo(cls):
        #--> Caso restem apenas 100 mensagens, um aviso será disparado
        # para avisar a necessidade de uma recarga

        saldo = int(cls.saldo_atual())

        if saldo <= 100:
            WhatsApp.enviar_mensagem('120363164390903005@g.us', f'Atenção o saldo de mensagens está a baixo de 100! Saldo atual: {saldo}')

    @staticmethod
    def envio_grupo(mensagem):
        #--> Envia uma mensagem para o grupo de LOGS

        url = "https://v5.chatpro.com.br/chatpro-ace98c12f9/api/v1/send_message"
        headers = {"accept": "application/json",
             "content-type": "application/json",
            "Authorization": "52c5e8171974cd0d780db547d59a3f17"}

        payload = {"number": "120363164390903005@g.us",
                  "message": f"{mensagem}"}

        response = requests.post(url, json=payload, headers=headers)
        dict = json.loads(response.text)

        return dict['message']

    @classmethod
    def envio_todos(cls, mensagem) -> None:
        Thread(target=cls.envio_grupo, args=(mensagem, )).start()