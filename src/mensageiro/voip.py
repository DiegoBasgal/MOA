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
from sys import stdout
from datetime import datetime
from urllib.request import Request, urlopen

# Inicializando o logger principal
logger = logging.getLogger(__name__)

# Carrega as configurações e vars
config_file = os.path.join(os.path.dirname(__file__), "voip_config.json")
with open(config_file, "r") as file:
    config = json.load(file)

TDA_FalhaComum = False
Disj_GDE_QLCF_Fechado = False

napikey = config["napikey"]
user_token = config["user_token"]
caller_voip = config["caller_voip"]
voz_habilitado = config["voz_habilitado"]
lista_de_contatos_padrao = [
    ["Diego", "41999111134"],
    #["Henrique", "41999610053"]
    #["Alex", "41996319885"],
    #["Escritorio", "41996570004"],
]

def carrega_contatos():
    phonebook = []

    with open(os.path.join(os.path.dirname(__file__), "contatos.csv")) as fp:
        list_r = fp.readlines()

    for r in list_r:
        r = r.strip().replace(", ", ",").replace(" ,", ",")
        r = r.replace("(", "")
        r = r.replace(")", "")
        r = [i for i in r.split(",") if i != ""]

        try:
            name = str(r[0])
            phone = str(r[1])
            t_start = datetime.strptime(r[2], "%Y-%m-%d %H:%M")
            t_end = datetime.strptime(r[3], "%Y-%m-%d %H:%M")

            phonebook.append({"name": name, "phone": phone, "t_start": t_start, "t_end": t_end})

        except ValueError as e:
            print(f"Exception {e}. Skipped entry.")
            continue
        except AttributeError as e:
            print(f"Exception {e}. Skipped entry.")
            continue
        
    res = []
    now = datetime.now()
    for addres in phonebook:
        if now < addres["t_start"]:
            print(f"Not yet: {now.time()} < {addres['t_start']}")
            continue
        elif now > addres["t_end"]:
            print(f"Too late: {now.time()} > {addres['t_end']}")
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
    """
    Esta função exemplifica como o envio de um torpedo d voz deve ser feio.
    :param lista_de_contatos: lista de contatos para ligar no formato: [["DEBUG MOA", "41988591567"],]
    :return: None
    """

    # Verifica se esta funcionalidade está habilitada, evitando ligações em momentos de testes.
    if voz_habilitado:
        logger.debug("Enviando Voz Emergencia")

        # Se a lista de conta não for fornecida, usa-se a lista padrão.
        if lista_de_contatos is None:
            try:
                lista_de_contatos = carrega_contatos()
                if len(lista_de_contatos) < 1:
                    raise ValueError("Lista de contatos com problema")
            except Exception as e:
                logger.exception(e)
                lista_de_contatos = lista_de_contatos_padrao

        # Para cada contato na lista de contatos deve-se fazer uma chamada a web api
        for contato in lista_de_contatos:
            logger.info("Disparando torpedo de voz para {} ({})".format(contato[0], contato[1]))

            # Montagem do pacote para chamar a api
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

            headers = {"Content-Type": "application/json", "Authorization": access_token,}

            # pharse/encode para json
            data = json.dumps(data)
            data = str(data).encode()

            # Envia a request para a api e recebe a resposta
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
        logger.debug("Enviando Voz Emergencia")

        # Se a lista de conta não for fornecida, usa-se a lista padrão.
        if lista_de_contatos is None:
            try:
                lista_de_contatos = carrega_contatos()
                if len(lista_de_contatos) < 1:
                    raise ValueError("Lista de contatos com problema")
            except Exception as e:
                logger.exception(e)
                lista_de_contatos = lista_de_contatos_padrao

    if TDA_FalhaComum or Disj_GDE_QLCF_Fechado:
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

    if Disj_GDE_QLCF_Fechado:
        # Para cada contato na lista de contatos deve-se fazer uma chamada a web api
        for contato in lista_de_contatos:
            logger.info("Disparando torpedo de voz para {} ({})".format(contato[0], contato[1]))

            # Montagem do pacote para chamar a api
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

            headers = {"Content-Type": "application/json", "Authorization": access_token,}

            # pharse/encode para json
            data = json.dumps(data)
            data = str(data).encode()

            # Envia a request para a api e recebe a resposta
            request = Request("https://api.nvoip.com.br/v2/torpedo/voice?napikey={}".format(napikey), data=data, headers=headers,)
            try:
                response_body = urlopen(request).read()
            except Exception as e:
                logger.debug("Exception NVOIP: {} ".format(e.read()))
            else:
                logger.debug("response_body: {} ".format(response_body))

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

            try:
                response_body = urlopen(request).read()
            except Exception as e:
                logger.debug("Exception NVOIP: {} ".format(e.read()))
            else:
                logger.debug("response_body: {} ".format(response_body))

if __name__ == "__main__":
   enviar_voz_auxiliar()
