import os
import sys
import json
import logging
import pytz

from time import sleep
from datetime import datetime
from urllib.request import Request, urlopen

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from banco_dados import BancoDados

logger = logging.getLogger(__name__)

config_file = os.path.join(os.path.dirname(__file__), "voip_config.json")
with open(config_file, "r") as file:
    config = json.load(file)

vars_dict = {
    "LG_FALHA_ATUADA": [False, "Atenção! Houve uma falha com o Limpa Grades na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com o Limpa Grades na PCH Xavantina, favor analisar a situação."],
    "FALHA_NIVEL_MONTANTE": [False, "Atenção! Houve uma falha na leitura de nível montante na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha na leitura de nível montante na PCH Xavantina, favor analisar a situação."],
    "FILTRAGEM_BOMBA_FALHA": [False, "Atenção! Houve uma falha com a bomba de filtragem na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com a bomba de filtragem na PCH Xavantina, favor analisar a situação."],
    "DRENAGEM_UNIDADES_BOMBA_FALHA": [False, "Atenção! Houve uma falha com a bomba de drenagem na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com a bomba de drenagem na PCH Xavantina, favor analisar a situação."],
    "BOMBA_RECALQUE_TUBO_SUCCAO_FALHA": [False, "Atenção! Houve uma falha com o tubo de succção da bomba de recalque, favor analisar a situação. Atenção! Houve uma falha com o tubo de succção da bomba de recalque, favor analisar a situação."],
    "POCO_DRENAGEM_NIVEL_MUITO_ALTO": [False, "Atenção! O nível do poço de drenagem na PCH Xavantina está muito alto, favor analisar a situação. Atenção! O nível do poço de drenagem na PCH Xavantina está muito alto, favor analisar a situação."],
    "POCO_DRENAGEM_NIVEL_ALTO": [False, "Atenção! O nível do poço de drenagem na PCH Xavantina está alto, favor monitorar. Atenção! O nível do poço de drenagem na PCH Xavantina está alto, favor monitorar."],
    "52SA1_SEM_FALHA": [False, "Atenção! Houve uma falha com o disjuntor 52SA1 do transformador do serviço auxiliar na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com o disjuntor 52SA1 do transformador do serviço auxiliarna PCH Xavantina, favor analisar a situação."],
    "52SA2_SEM_FALHA": [False, "Atenção! Houve uma falha com o disjuntor 52SA2 do gerador dieselna PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha com o disjuntor 52SA2 do gerador dieselna PCH Xavantina, favor analisar a situação."],
    "52SA3_SEM_FALHA": [False, "Atenção! Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciais na PCH Xavantina, favor analisar a situação . Atenção! Houve uma falha com o disjuntor 52SA3 do barramento de cargas não essenciaisna PCH Xavantina, favor analisar a situação."],
    "SISTEMA_INCENDIO_ALARME_ATUADO": [False, "Atenção! O alarme de incêndio da PCH Xavantina foi acionado, favor analisar a situação. Atenção! O alarme de incêndio da PCH Xavantina foi acionado, favor analisar a situação."],
    "SISTEMA_SEGURANCA_ALARME_ATUADO": [False, "Atenção! O alarme do sistema de segurança da PCH Xavantina foi acionado, favor verificar a situração. Atenção! O alarme do sistema de segurança da PCH Xavantina foi acionado, favor verificar a situração."],
    "GMG_FALHA_PARTIR": [False, "Atenção! Houve uma falha ao partir o gerador diesel na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha ao partir o gerador diesel na PCH Xavantina, favor analisar a situação."],
    "GMG_FALHA_PARAR": [False, "Atenção! Houve uma falha ao parar o gerador diesel na PCH Xavantina, favor analisar a situação. Atenção! Houve uma falha ao parar o gerador diesel na PCH Xavantina, favor analisar a situação."],
    "GMG_OPERACAO_MANUAL": [False, "Atenção! O gerador diesel saiu do modo remoto, favor analisar a situação. Atenção! O gerador diesel saiu do modo remoto, favor analisar a situação."],
    "TE_ALARME_TEMPERATURA_ENROLAMENTO": [False, "Atenção! A temperatura do enrolamento do transformador elevador na PCH Xavantina está alto, favor monitorar. Atenção! A temperatura do enrolamento do transformador elevador na PCH Xavantina está alto, favor monitorar."],
    "TE_ALM_TEMPERATURA_ENROLAMENTO": [False, "Atenção! A temperatura do enrolamento do transformador elevador na PCH Xavantina está alto, favor monitorar. Atenção! A temperatura do enrolamento do transformador elevador na PCH Xavantina está alto, favor monitorar."],
    "TE_ALARME_TEMPERATURA_OLEO": [False, "Atenção! A temperatura do óleo do transformador elevador na PCH Xavantina está alto, favor monitorar. Atenção! A temperatura do óleo do transformador elevador na PCH Xavantina está alto, favor monitorar."],
    "TE_ALM_TEMPERATURA_OLEO": [False, "Atenção! A temperatura do óleo do transformador elevador na PCH Xavantina está alto, favor monitorar. Atenção! A temperatura do óleo do transformador elevador na PCH Xavantina está alto, favor monitorar."],
    "TE_NIVEL_OLEO_MUITO_ALTO": [False, "Atenção! O nível do óleo do transformador elevador na PCH Xavantina está muito alto, favor analisar a situação. Atenção! O nível do óleo do transformador elevador na PCH Xavantina está muito alto, favor analisar a situação."],
    "TE_NIVEL_OLEO_MUITO_BAIXO": [False, "Atenção! O nível do óleo do transformador elevador a PCH Xavantina está muito baixo, favor analisar a situação. Atenção! O nível do óleo do transformador elevador a PCH Xavantina está muito baixo, favor analisar a situação."]
}

lista_de_contatos_padrao = [
    ["Diego", "41999111134"],
    #["Henrique", "41999610053"]
]

def carrega_contatos():
    phonebook = []
    db = BancoDados()
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
    data = f"username={config['caller_voip']}&password={config['user_token']}&grant_type=password"
    data = str(data).encode()
    request = Request("https://api.nvoip.com.br/v2/oauth/token", data=data, headers=headers)

    try:
        response_body = urlopen(request).read()
        response_body = json.loads(response_body)
        return f"Bearer {response_body['access_token']}"
    except Exception as e:
        logger.debug(f"Exception NVOIP: {e.read()} ")

def enviar_voz_emergencia(lista_de_contatos=None):
    access_token = get_token()
    
    if config["voz_habilitado"]:
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
            logger.info(f"Disparando torpedo de voz para {contato[0]} ({contato[1]})")

            data = {
                "caller": f"{config['caller_voip']}",
                "called": f"{contato[1]}",
                "audios": [
                    {
                        "audio": "Atenção! Houve um acionamento de emergência na PCH Xavantina, por favor analisar a situação. Atenção! Houve um acionamento de emergência na PCH Xavantina, por favor analisar a situação.",
                        "positionAudio": 1,
                    }
                ],
                "dtmfs": [],
            }

            headers = {"Content-Type": "application/json", "Authorization": access_token,}

            data = json.dumps(data)
            data = str(data).encode()

            request = Request(f"https://api.nvoip.com.br/v2/torpedo/voice?napikey={config['napikey']}", data=data, headers=headers,)
            try:
                response_body = urlopen(request).read()
            except Exception as e:
                logger.debug(f"Exception NVOIP: {e.read()}")
            else:
                logger.debug(f"response_body: {response_body}")

def enviar_voz_teste():
    access_token = get_token()

    if config["voz_habilitado"]:
        for contato in lista_de_contatos_padrao:
            data = {
                "caller": f"{config['caller_voip']}",
                "called": f"{contato[1]}",
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
            request = Request(f"https://api.nvoip.com.br/v2/torpedo/voice?napikey={config['napikey']}", data=data, headers=headers)
            try:
                response_body = urlopen(request).read()
            except Exception as e:
                logger.debug(f"Exception NVOIP: {e.read()}")
            else:
                logger.debug(f"response_body: {response_body}")

def enviar_voz_auxiliar(lista_de_contatos=None):
    access_token = get_token()

    if config["voz_habilitado"]:
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
            logger.info(f"Disparando torpedo de voz para {contato[0]} ({contato[1]})")

            for i in vars_dict:
                if vars_dict[i][0]:
                    data = {
                        "caller": f"{config['caller_voip']}",
                        "called": f"{contato[1]}",
                        "audios": [{"audio": f"{vars_dict[i][1]}", "positionAudio": 1,}],
                        "dtmfs": [],
                    }
                    headers = {"Content-Type": "application/json", "Authorization": access_token,}
                    data = json.dumps(data)
                    data = str(data).encode()
                    request = Request(f"https://api.nvoip.com.br/v2/torpedo/voice?napikey={config['napikey']}", data=data, headers=headers,)
                    try:
                        response_body = urlopen(request).read()
                    except Exception as e:
                        logger.debug(f"Exception NVOIP: {e.read()}")
                    else:
                        logger.debug(f"response_body: {response_body}")
                    vars_dict[i][0] = False
                    sleep(15)
