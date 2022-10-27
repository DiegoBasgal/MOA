"""
voip.py

Este módulo tem como objetivo a efetuar a comunicação por voip.
O serviço de voip é fornecido pela nvoip e é acessado via web api.

Painel Nvoip: https://painel.nvoip.com.br
Acesso feito com as credênciais do Henrique.

"""
import os
import json
import logging
import random
import datetime
from sys import stdout
from asyncore import read
from urllib.request import Request, urlopen

# Inicializando o logger principal
logger = logging.getLogger(__name__)

# Carrega as configurações e vars
config_file = os.path.join(os.path.dirname(__file__), "voip_config.json")
with open(config_file, "r") as file:
    config = json.load(file)

caller_voip = config["caller_voip"]
voz_habilitado = config["voz_habilitado"]
napikey = config["napikey"]
user_token = config["user_token"]

lista_de_contatos_padrao = [
    ["Diego", "41999111134"],
    #["Henrique", "41999610053"]
    #["Alex", "41996319885"],
    #["Escritorio", "41996570004"],
]

Disj_GDE_QLCF_Fechado = False
TDA_FalhaComum = True


def get_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic TnZvaXBBcGlWMjpUblp2YVhCQmNHbFdNakl3TWpFPQ==",
    }
    data = "username={}&password={}&grant_type=password".format(caller_voip, user_token)
    data = str(data).encode()
    request = Request("https://api.nvoip.com.br/v2/oauth/token", data=data, headers=headers)

    try:
        response_body = urlopen(request).read()
        response_body = json.loads(response_body)
        
        return "Bearer {}".format(response_body["access_token"])
    except Exception as e:
        logger.debug("Exception NVOIP: {} ".format(e.read()))

def enviar_voz_emergencia():

    access_token = get_token()

    if voz_habilitado:
        for contato in lista_de_contatos_padrao:
            data = {
                "caller": "{}".format(caller_voip),  # caller fornecido pela nvoip
                "called": "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
                "audios": [
                    {
                        "audio": "Atenção! Houve um acionamento de emergência na PCH São Sebastião, por favor verificar a situação. Atenção! Houve um acionamento de emergência na PCH São Sebastião, por favor verificar a situação.",
                        "positionAudio": 1,
                    }
                ],
                "dtmfs": [],
            }

            headers = {"Content-Type": "application/json", "Authorization": access_token}
            data = json.dumps(data)
            data = str(data).encode()
            request = Request("https://api.nvoip.com.br/v2/torpedo/voice?napikey={}".format(napikey), data=data, headers=headers)

            response_body = urlopen(request).read()

def enviar_voz_teste():

    access_token = get_token()

    for contato in lista_de_contatos_padrao:
        data = {
            "caller": "{}".format(caller_voip),  # caller fornecido pela nvoip
            "called": "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
            "audios": [
                {
                    "audio": "Esta é apenas uma mensagem de teste. Esta é apenas uma mensagem de teste.",
                    "positionAudio": 1,
                }
            ],
            "dtmfs": [],
        }

        headers = {"Content-Type": "application/json", "Authorization": access_token}
        data = json.dumps(data)
        data = str(data).encode()
        request = Request("https://api.nvoip.com.br/v2/torpedo/voice?napikey={}".format(napikey), data=data, headers=headers)

        response_body = urlopen(request).read()

def enviar_voz_auxiliar():

    access_token = get_token()

    if Disj_GDE_QLCF_Fechado:
        for contato in lista_de_contatos_padrao:
            data = {
                "caller": "{}".format(caller_voip),  # caller fornecido pela nvoip
                "called": "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
                "audios": [
                    {
                        "audio": "Atenção! Foi identificado que o disjuntor do gerador diesel de emergência QLCF em São Sebastião foi fechado, favor verificar. Atenção! Foi identificado que o disjuntor do gerador diesel de emergência QLCF em São Sebastião foi fechado, favor verificar.",
                        "positionAudio": 1,
                    }
                ],
                "dtmfs": [],
            }

            headers = {"Content-Type": "application/json", "Authorization": access_token}
            data = json.dumps(data)
            data = str(data).encode()
            request = Request("https://api.nvoip.com.br/v2/torpedo/voice?napikey={}".format(napikey), data=data, headers=headers)

            response_body = urlopen(request).read()

    elif TDA_FalhaComum:
        for contato in lista_de_contatos_padrao:
            data = {
                "caller": "{}".format(caller_voip),  # caller fornecido pela nvoip
                "called": "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
                "audios": [
                    {
                        "audio": "Atenção! Houve uma falha de comunicação com o CLP na Tomada da Água em São Sebastião, favor verificar o telegram para mais informações. Atenção! Houve uma falha de comunicação com o CLP na Tomada da Água em São Sebastião, favor verificar o telegram para mais informações.",
                        "positionAudio": 1,
                    }
                ],
                "dtmfs": [],
            }

            headers = {"Content-Type": "application/json", "Authorization": access_token}
            data = json.dumps(data)
            data = str(data).encode()
            request = Request("https://api.nvoip.com.br/v2/torpedo/voice?napikey={}".format(napikey), data=data, headers=headers)

            response_body = urlopen(request).read()

if __name__ == "__main__":
   enviar_voz_auxiliar()
