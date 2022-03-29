"""
voip.py

Este módulo tem como objetivo a efetuar a comunicação por voip.
O serviço de voip é fornecido pela nvoip e é acessado via web api.

Painel Nvoip: http://painel.nvoip.com.br
Acesso feito com as credênciais do Henrique.

"""
import json
import logging
import os
from sys import stdout
from urllib.request import Request, urlopen
import random

# Inicializando o logger principal
logger = logging.getLogger(__name__)

# Carrega as configurações e vars
config_file = os.path.join(os.path.dirname(__file__), 'voip_config.json')
with open(config_file, 'r') as file:
    config = json.load(file)

audios_emerg = ['http://ritmoenergia.com.br/wp-content/uploads/2021/12/Emergencia-Alex.mp3',
                'http://ritmoenergia.com.br/wp-content/uploads/2021/12/Emergencia-Amanda.mp3',
                'http://ritmoenergia.com.br/wp-content/uploads/2021/12/Emergencia-Camila1.mp3',
                'http://ritmoenergia.com.br/wp-content/uploads/2021/12/Emergencia-Camila2.mp3',
                'http://ritmoenergia.com.br/wp-content/uploads/2021/12/Emergencia-Flavio.mp3',
                'http://ritmoenergia.com.br/wp-content/uploads/2021/12/Emergencia-Lucas.mp3',
                'http://ritmoenergia.com.br/wp-content/uploads/2021/12/Emergencia-Natali.mp3'
                ]

audios_teste = ['http://ritmoenergia.com.br/wp-content/uploads/2021/12/Teste-Alex.mp3',
                'http://ritmoenergia.com.br/wp-content/uploads/2021/12/Teste-Amanda.mp3',
                'http://ritmoenergia.com.br/wp-content/uploads/2021/12/Teste-Camila1.mp3',
                'http://ritmoenergia.com.br/wp-content/uploads/2021/12/Teste-Camila2.mp3',
                'http://ritmoenergia.com.br/wp-content/uploads/2021/12/Teste-Flavio.mp3',
                'http://ritmoenergia.com.br/wp-content/uploads/2021/12/Teste-Lucas.mp3',
                'http://ritmoenergia.com.br/wp-content/uploads/2021/12/Teste-Natali.mp3'
                ]

caller_voip = config['caller_voip']
voz_habilitado = config['voz_habilitado']
napikey = config['napikey']
user_token = config['user_token']

lista_de_contatos_padrao = [
                            #["Alex", "41996319885"], 
                            ["Escritorio", "41996570004"],
                            ["Lucas Lavratti", "41988591567"],
                            ["Luis", "48991058729"], 
                            ["Henrique P5", "41999610053"],
                        ]


lista_de_contatos_teste = [
                            #["Alex", "41996319885"], 
                            ["Lucas Lavratti", "41988591567"],
                            #["Luis", "48991058729"], 
                            ["Henrique P5", "41999610053"],
                        ]


def enviar_voz_emergencia(lista_de_contatos=None):

    access_token = get_token()
    """
    Esta função exemplifica como o envio de um torpedo d voz deve ser feio.
    :param lista_de_contatos: lista de contatos para ligar no formato: [["DEBUG MOA", "41988591567"],]
    :return: None
    """

    audio_url = random.choice(audios_emerg)

    # Verifica se esta funcionalidade está habilitada, evitando ligações em momentos de testes.
    if voz_habilitado:
        logger.debug("Enviando Voz Emergencia: {}".format(audio_url))

        # Se a lista de conta não for fornecida, usa-se a lista padrão.
        if lista_de_contatos is None:
            lista_de_contatos = lista_de_contatos_padrao

        # Para cada contato na lista de contatos deve-se fazer uma chamada a web api
        for contato in lista_de_contatos:

            logger.info("Disparando torpedo de voz para {} ({})".format(contato[0], contato[1]))

            # Montagem do pacote para chamar a api
            data = {
                'caller': "{}".format(caller_voip),  # caller fornecido pela nvoip
                'called': "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
                'audios': [{
                    'audio': audio_url,  # URL do arquivo de audio (api acessa via GET)
                    'positionAudio':1}],
                'dtmfs':[]
            }
            headers = {
                'Content-Type': 'application/json',
                'Authorization': access_token
            }

            # pharse/encode para json
            data = json.dumps(data)
            data = str(data).encode()

            # Envia a request para a api e recebe a resposta
            request = Request('https://api.nvoip.com.br/v2/torpedo/voice?napikey={}'.format(napikey), data=data, headers=headers)
            try:
                response_body = urlopen(request).read()
            except Exception as e:
                logger.debug("Exception NVOIP: {} ".format(e.read()))
            else:
                logger.debug("response_body: {} ".format(response_body))

def enviar_voz_teste():

    access_token = get_token()

    audio_url = random.choice(audios_teste)
    logger.debug("Enviando Voz Teste: {}".format(audio_url))
    for contato in lista_de_contatos_teste:
        logger.info("Disparando torpedo de voz teste para {} ({})".format(contato[0], contato[1]))
        data = {
            'caller': "{}".format(caller_voip),  # caller fornecido pela nvoip
            'called': "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
            'audios': [{
                'audio': audio_url,  # URL do arquivo de audio (api acessa via GET)
                'positionAudio':1}],
            'dtmfs':[]
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        data = json.dumps(data)
        data = str(data).encode()
        request = Request('https://api.nvoip.com.br/v2/torpedo/voice?napikey={}'.format(napikey), data=data, headers=headers)
        try:
            response_body = urlopen(request).read()
        except Exception as e:
            logger.debug("Exception NVOIP: {} ".format(e.read()))

def get_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic TnZvaXBBcGlWMjpUblp2YVhCQmNHbFdNakl3TWpFPQ=='
    }
    data = "username={}&password={}&grant_type=password".format(caller_voip, user_token)
    data = str(data).encode()
    request = Request('https://api.nvoip.com.br/v2/oauth/token', data=data, headers=headers)
    try:
        response_body = urlopen(request).read()
        response_body = json.loads(response_body)
        return 'Bearer {}'.format(response_body['access_token'])
    except Exception as e:
        logger.debug("Exception NVOIP: {} ".format(e.read()))
    

if __name__ == "__main__":
    enviar_voz_teste()