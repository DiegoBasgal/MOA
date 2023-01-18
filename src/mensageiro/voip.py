"""
voip.py

Este módulo tem como objetivo a efetuar a comunicação por voip.
O serviço de voip é fornecido pela nvoip e é acessado via web api.

Painel Nvoip: http://painel.nvoip.com.br
Acesso feito com as credênciais do Henrique.

"""
import sys
import os
import json
import logging
from sys import stdout
from datetime import datetime
from urllib.request import Request, urlopen
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database_connector


# Inicializando o logger principal
logger = logging.getLogger(__name__)

# Carrega as configurações e vars
config_file = os.path.join(os.path.dirname(__file__), 'voip_config.json')
with open(config_file, 'r') as file:
    config = json.load(file)

caller_voip = config['caller_voip']
voz_habilitado = config['voz_habilitado']
napikey = config['napikey']
user_token = config['user_token']

falha_abertura_comp = False
falha_fechamento_comp = False
alarme_temp_oleo_trafo = False
alarme_temp_enrol_trafo = False
falha_part_grupo_diesel = False
falha_fechamento_DJ52L = False

lista_de_contatos_padrao = [
    #["Diego", "41999111134"], 
    #["Luis", "48991058729"], 
    #["Escritorio", "41996570004"],
    #["Henrique P5", "41999610053"],
]
"""
def carrega_contatos():
    phonebook = []
    db = database_connector.Database()
    parametros = db.get_contato_emergencia()

    for i in range(len(parametros)):
        try:
            name = str(parametros[i][1])
            phone = str(parametros[i][2])
            t_start = str(parametros[i][5]) + " " + str(parametros[i][6])
            t_end = str(parametros[i][4]) + " " + str(parametros[i][5])

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
            print(f"A escala do funcionário {addres['name']}, ainda não começou: {now.time()} < {addres['t_start']}")
            logger.info(f"A escala do funcionário {addres['name']}, ainda não começou: {now.time()} < {addres['t_start']}")
            continue
        elif now > addres["t_end"]:
            print(f"A escala do funcionário {addres['name']}, já passou do horário: {now.time()} > {addres['t_end']}")
            logger.info(f"A escala do funcionário {addres['name']}, já passou do horário: {now.time()} > {addres['t_end']}")
            continue
        else:
            res.append([addres["name"], addres["phone"]])
        
    return res
"""

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
                if len(lista_de_contatos) <= 0:
                    raise ValueError("Lista de contatos com problema")
            except Exception as e:
                logger.exception(e)
                lista_de_contatos = lista_de_contatos_padrao

        # Para cada contato na lista de contatos deve-se fazer uma chamada a web api
        for contato in lista_de_contatos:

            logger.info("Disparando torpedo de voz para {} ({})".format(contato[0], contato[1]))

            # Montagem do pacote para chamar a api
            data = {
                'caller': "{}".format(caller_voip),  # caller fornecido pela nvoip
                'called': "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
                'audios': [{
                    'audio': "Atenção! Houve um acionamento de emergência na PCH Covó, por favor verificar a situação. Atenção! Houve um acionamento de emergência na PCH Covó, por favor verificar a situação.",  # URL do arquivo de audio (api acessa via GET)
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

    
        # Para cada contato na lista de contatos deve-se fazer uma chamada a web api
        for contato in lista_de_contatos:
            logger.info("Disparando torpedo de voz para {} ({})".format(contato[0], contato[1]))

            if falha_abertura_comp:
                # Montagem do pacote para chamar a api
                data = {
                    "caller": "{}".format(caller_voip),  # caller fornecido pela nvoip
                    "called": "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
                    "audios": [
                        {
                            "audio": "Atenção! Houve uma falha na abertura de comportas na PCH Covó, favor verificar. Atenção! Houve uma falha na abertura de comportas na PCH Covó, favor verificar.",
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
                sleep(20)
            
            if falha_fechamento_comp:
                # Montagem do pacote para chamar a api
                data = {
                    "caller": "{}".format(caller_voip),  # caller fornecido pela nvoip
                    "called": "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
                    "audios": [
                        {
                            "audio": "Atenção! Houve uma falha no fechamento das comportas na PCH Covó, favor verificar. Atenção! Houve uma falha no fechamento das comportas na PCH Covó, favor verificar.",
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
                sleep(20)
            
            if alarme_temp_oleo_trafo:
                # Montagem do pacote para chamar a api
                data = {
                    "caller": "{}".format(caller_voip),  # caller fornecido pela nvoip
                    "called": "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
                    "audios": [
                        {
                            "audio": "Atenção! O alarme de temperatura de óleo do transformador elevador na PCH Covó foi ativado, favor verificar. Atenção! O alarme de temperatura de óleo do transformador elevador na PCH Covó foi ativado, favor verificar.",
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
                sleep(20)

            if alarme_temp_enrol_trafo:
                # Montagem do pacote para chamar a api
                data = {
                    "caller": "{}".format(caller_voip),  # caller fornecido pela nvoip
                    "called": "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
                    "audios": [
                        {
                            "audio": "Atenção! O alarme de temperatura de enrolamento do transformador elevador na PCH Covó foi ativado, favor verificar. Atenção! O alarme de temperatura de enrolamento do transformador elevador na PCH Covó foi ativado, favor verificar.",
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
                sleep(20)

            if falha_part_grupo_diesel:
                # Montagem do pacote para chamar a api
                data = {
                    "caller": "{}".format(caller_voip),  # caller fornecido pela nvoip
                    "called": "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
                    "audios": [
                        {
                            "audio": "Atenção! Houve uma falha na partida do grupo diesel na PCH Covó, favor verificar. Atenção! Houve uma falha na partida do grupo diesel na PCH Covó, favor verificar.",
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
                sleep(20)

            if falha_fechamento_DJ52L:
                # Montagem do pacote para chamar a api
                data = {
                    "caller": "{}".format(caller_voip),  # caller fornecido pela nvoip
                    "called": "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
                    "audios": [
                        {
                            "audio": "Atenção! Houve uma falha no fechamento do disjuntor 52L na PCH Covó, favor verificar. Atenção! Houve uma falha no fechamento do disjuntor 52L na PCH Covó, favor verificar.",
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
                sleep(20)

def enviar_voz_teste():

    access_token = get_token()

    logger.debug("Enviando Voz Teste")
    for contato in lista_de_contatos_padrao:
        logger.info("Disparando torpedo de voz teste para {} ({})".format(contato[0], contato[1]))
        data = {
            'caller': "{}".format(caller_voip),  # caller fornecido pela nvoip
            'called': "{}".format(contato[1]),  # O número a ser chamado, no formato dddnnnnnnnnn
            'audios': [{
                'audio': "Esta é apenas uma mensagem de teste. Esta é apenas uma mensagem de teste.",  # URL do arquivo de audio (api acessa via GET)
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


if __name__ == "__main__":
    enviar_voz_emergencia()