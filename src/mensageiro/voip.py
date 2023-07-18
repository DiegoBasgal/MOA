import os
import pytz
import json
import logging
import src.mensageiro.dict as vd

from time import sleep
from datetime import datetime
from urllib.request import Request, urlopen

from src.banco_dados import BancoDados

logger = logging.getLogger("__main__")

class Voip:

    #ATRIBUIÇÃO DE VARIÁVEIS

    arquivo = os.path.join(os.path.dirname(__file__), "voip_config.json")
    with open(arquivo, "r") as file:
        cfg = json.load(file)

    lista_padrao = [["Diego", "41999111134"]]

    token_data = str(f"username={cfg['caller_voip']}&password={cfg['user_token']}&grant_type=password").encode()
    token_headers =  {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic TnZvaXBBcGlWMjpUblp2YVhCQmNHbFdNakl3TWpFPQ==",
        }

    db = BancoDados("voip")

    @staticmethod
    def verificar_expediente(agenda) -> list:
        """
        Função para verificar se o operador cadastrado na interface, está dentro
        do período de sobre-aviso.
        """

        contatos = []
        now = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

        for contato in agenda:
            if str(now) < contato["inicio"]:
                print(f"O expediente ainda não começou! ({str(now)} < {contato['inicio']})")
                continue
            elif str(now) > contato["fim"]:
                print(f"O expediente já acabou! ({str(now)} > {contato['fim']})")
                continue
            else:
                contatos.append([contato["nome"], contato["telefone"]])

        return contatos

    @classmethod
    def carregar_contatos(cls) -> list:
        """
        Função para extrair lista de contatos cadastrados na interface WEB.
        """

        agenda = []
        parametros = cls.db.get_contato_emergencia()

        for i in range(len(parametros)):
            try:
                nome = str(parametros[i][1])
                telefone = str(parametros[i][2])
                inicio = str(parametros[i][3]) + " " + str(parametros[i][4])
                fim = str(parametros[i][5]) + " " + str(parametros[i][6])

                agenda.append({"nome": nome, "telefone": telefone, "inicio": inicio, "fim": fim})

            except Exception as e:
                logger.exception(f"[VOIP] Não foi possível carregar os parâmetros do banco. Exception: \"{repr(e)}\"")
                return None

        return agenda

    @classmethod
    def carregar_token(cls) -> str:
        """
        Função para carregar token de autenticação NVoip.
        """

        try:
            request = Request("https://api.nvoip.com.br/v2/oauth/token", data=cls.token_data, headers=cls.token_headers)
            response_body = json.loads(urlopen(request).read())

            return f"Bearer {response_body['access_token']}"

        except Exception as e:
            logger.debug(f"[VOIP] Não foi possível carregar a token de acesso Nvoip. Exception: \"{repr(e)}\"")
            return None

    @classmethod
    def codificar_dados(cls, data, headers) -> None:
        """
        Função para codificação do acionamento, para a plataforma da Nvoip.
        """

        encoded = str(json.dumps(data)).encode()
        request = Request(f"https://api.nvoip.com.br/v2/torpedo/voice?napikey={cls.cfg['napikey']}", data=encoded, headers=headers)
        try:
            response_body = urlopen(request).read()
            logger.debug(f"[VOIP] Response Body: {response_body}")

        except Exception as e:
            logger.exception(f"[VOIP] Não foi possível codificar dados de envio de torpedo. Exception: \"{repr(e)}\".")

    @classmethod
    def acionar_chamada(cls):
        """
        Função para envio de tropedos de voz, baseado nas condições de acionamento
        do dicioário Voip.

        Primeiramente, chama a função de carregar contatos e realiza a verificação
        de expediente. Caso não haja nenhum contato cadastrado, ou nenhum operador
        dentro do horário de expediente, passa a chamar a lista de contatos padrão
        para não deixar de avisar.
        Caso a condição de emergência estiver ativada, ignora todas as outras condições
        e passa a disparar o torpedo de emerência para todos os operadores.
        Caso sejam apenas condições específicas, realiza uma iteração pelo dicionário
        de condições e concatena todas as mensagens em uma só, para envio aos
        operadores.
        """

        headers = {"Content-Type": "application/json", "Authorization": cls.carregar_token()}

        if cls.cfg["voz_habilitado"]:
            logger.debug("[VOIP] Enviando voz de Emergencia...")

            if cls.carregar_contatos() is not None:
                agenda = cls.carregar_contatos()
                lista_contatos = cls.verificar_expediente(agenda)
            else:
                logger.info("[VOIP] Lista de contatos vazia! Carregando lista de contatos padrão.")
                lista_contatos = cls.lista_padrao

            if vd.voip_dict["EMERGENCIA"][0]:
                for contato in lista_contatos:
                    logger.info(f"[VOIP] Disparando torpedo de voz para: {contato[0]} ({contato[1]})")
                    data = {
                        "caller": f"{cls.cfg['caller_voip']}",
                        "called": f"{contato[1]}",
                        "audios": [{"audio": f"{vd.voip_dict['EMERGENCIA'][1]}", "positionAudio": 1,}],
                        "dtmfs": [],
                    }
                    cls.codificar_dados(data, headers)
                vd.voip_dict["EMERGENCIA"][0] = False
            else:
                todos = []
                for _, vl in vd.voip_dict.items():
                    if vl[0] and vl[1] == 0:
                        todos.append(vl[2])
                        vl[1] = 1

                mensagem = "".join(i for i in todos)

                for contato in lista_contatos:
                    logger.info(f"[VOIP] Disparando torpedo de voz para: {contato[0]} ({contato[1]})")
                    data = {
                        "caller": f"{cls.cfg['caller_voip']}",
                        "called": f"{contato[1]}",
                        "audios": [{"audio": f"{mensagem}", "positionAudio": 1,}],
                        "dtmfs": [],
                    }
                    cls.codificar_dados(data, headers)

        else:
            logger.info("[VOIP] Torpedo de voz desativado. Para habilitar envio, favor alterar valor \"voz_habilitado = true\" no arquivo \"voip_config.json\".")
