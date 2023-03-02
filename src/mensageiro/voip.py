"""
voip.py

Este módulo tem como objetivo a efetuar a comunicação por voip.
O serviço de voip é fornecido pela nvoip e é acessado via web api.

Painel Nvoip: https://painel.nvoip.com.br
Acesso feito com as credênciais do Henrique.

"""
import os
import sys
import json
import logging
import pytz
from sys import stdout
from time import sleep
from datetime import datetime
from urllib.request import Request, urlopen
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import src.conector as conector

logger = logging.getLogger(__name__)

config_file = os.path.join(os.path.dirname(__file__), "voip_config.json")
with open(config_file, "r") as file:
    config = json.load(file)

VARS = {
    "TDA_FalhaComum": [False, "Atenção! Houve uma falha de comunicação com o CLP na Tomada da Água em Pampeana, favor verificar o telegram para mais informações. Atenção! Houve uma falha de comunicação com o CLP na Tomada da Água em Pampeana, favor verificar o telegram para mais informações."],
    "Disj_GDE_QCAP_Fechado": [False, "Atenção! Foi identificado que o disjuntor do gerador diesel de emergência QLCF em Pampeana foi fechado, favor verificar. Atenção! Foi identificado que o disjuntor do gerador diesel de emergência QLCF em Pampeana foi fechado, favor verificar."],
    "BombasDngRemoto": [False, "Atenção! Foi identificado que o painel do poço de drenagem em Pampeana saiu do modo remoto, favor verificar. Atenção! Foi identificado que o painel do poço de drenagem em Pampeana saiu do modo remoto, favor verificar."],
}

napikey = config["napikey"]
user_token = config["user_token"]
caller_voip = config["caller_voip"]
voz_habilitado = config["voz_habilitado"]

lista_de_contatos_padrao = [
    ["Diego", "41999111134"],
    #["Henrique", "41999610053"]
]

def carrega_contatos():
    phonebook = []
    db = conector.Database()
    parametros = db.get_contato_emergencia()

    for i in range(len(parametros)):
        try:
            name = str(parametros[i][1])
            phone = str(parametros[i][2])
            t_start = str(parametros[i][3]) + " " + str(parametros[i][4])
            t_end = str(parametros[i][5]) + " " + str(parametros[i][6])

            phonebook.append({"name": name, "phone": phone, "t_start": t_start, "t_end": t_end})

        except ValueError as e:
            print(f"Exception {e}. Skipped entry.")
            continue
        except AttributeError as e:
            print(f"Exception {e}. Skipped entry.")
            continue
        
    res = []
    now = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
    for addres in phonebook:
        if str(now) < addres["t_start"]:
            print(f"Not yet: {str(now)} < {addres['t_start']}")
            continue
        elif str(now) > addres["t_end"]:
            print(f"Too late: {str(now)} > {addres['t_end']}")
            continue
        else:
            res.append([addres["name"], addres["phone"]])

    return res

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

def enviar_voz_emergencia(lista_de_contatos=None):
    access_token = get_token()
    if voz_habilitado:
        logger.debug("Enviando Voz Emergencia")
        if lista_de_contatos is None:
            try:
                lista_de_contatos = carrega_contatos()
                if len(lista_de_contatos) < 1:
                    raise ValueError("Lista de contatos com problema")
            except Exception as e:
                logger.exception(e)
                lista_de_contatos = lista_de_contatos_padrao

        for contato in lista_de_contatos:
            logger.info("Disparando torpedo de voz para {} ({})".format(contato[0], contato[1]))

            data = {
                "caller": "{}".format(caller_voip),
                "called": "{}".format(contato[1]),
                "audios": [
                    {
                        "audio": "Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor verificar a situação. Atenção! Houve um acionamento de emergência na PCH Pampeana, por favor verificar a situação.",
                        "positionAudio": 1,
                    }
                ],
                "dtmfs": [],
            }

            headers = {"Content-Type": "application/json", "Authorization": access_token,}

            data = json.dumps(data)
            data = str(data).encode()

            request = Request("https://api.nvoip.com.br/v2/torpedo/voice?napikey={}".format(napikey), data=data, headers=headers,)
            try:
                response_body = urlopen(request).read()
            except Exception as e:
                logger.debug("Exception NVOIP: {} ".format(e.read()))
            else:
                logger.debug("response_body: {} ".format(response_body))

def enviar_voz_teste():
    access_token = get_token()

    if voz_habilitado:
        for contato in lista_de_contatos_padrao:
            data = {
                "caller": "{}".format(caller_voip),
                "called": "{}".format(contato[1]),
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
            try:
                response_body = urlopen(request).read()
            except Exception as e:
                logger.debug("Exception NVOIP: {} ".format(e.read()))
            else:
                logger.debug("response_body: {} ".format(response_body))

def enviar_voz_auxiliar(lista_de_contatos=None):
    access_token = get_token()

    if voz_habilitado:
        logger.debug("Enviando Voz Emergencia")

        if lista_de_contatos is None:
            try:
                lista_de_contatos = carrega_contatos()
                if len(lista_de_contatos) < 1:
                    raise ValueError("Lista de contatos com problema")
            except Exception as e:
                logger.exception(e)
                lista_de_contatos = lista_de_contatos_padrao

        for contato in lista_de_contatos:
            logger.info("Disparando torpedo de voz para {} ({})".format(contato[0], contato[1]))

            for i in VARS:
                if VARS[i][0]:
                    data = {
                        "caller": "{}".format(caller_voip),
                        "called": "{}".format(contato[1]),
                        "audios": [
                            {
                                "audio": VARS[i][1],
                                "positionAudio": 1,
                            }
                        ],
                        "dtmfs": [],
                    }
                    headers = {"Content-Type": "application/json", "Authorization": access_token,}
                    data = json.dumps(data)
                    data = str(data).encode()
                    request = Request("https://api.nvoip.com.br/v2/torpedo/voice?napikey={}".format(napikey), data=data, headers=headers,)
                    try:
                        response_body = urlopen(request).read()
                    except Exception as e:
                        logger.debug("Exception NVOIP: {} ".format(e.read()))
                    else:
                        logger.debug("response_body: {} ".format(response_body))
                    VARS[i][0] = False

if __name__ == "__main__":
   enviar_voz_auxiliar()
