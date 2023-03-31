import os
import json

from abc import abstractmethod
from urllib.request import Request, urlopen

from usina import *

logger = logging.getLogger("__main__")

class Voip:
    arquivo_cfg = os.path.join(os.path.dirname(__file__), "voip_config.json")
    with open(arquivo_cfg, "r") as file:
        cfg = json.load(file)

    lista_padrao = [["Diego", "41999111134"], """["Henrique", "41999610053"]"""]

    token_data = str(f"username={cfg['caller_voip']}&password={cfg['user_token']}&grant_type=password").encode()
    token_headers =  {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic TnZvaXBBcGlWMjpUblp2YVhCQmNHbFdNakl3TWpFPQ==",
        }

    voip_dict = Dicionarios.voip

    @abstractmethod
    def verifica_expediente(agenda) -> list:
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
                contatos.append([contato["name"], contato["phone"]])

        return contatos

    @abstractmethod
    def carrega_contatos(parametros) -> list:
        agenda = []

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
    def carrega_token(cls) -> str:
        try:
            request = Request("https://api.nvoip.com.br/v2/oauth/token", data=cls.token_data, headers=cls.token_headers)
            response_body = json.loads(urlopen(request).read())

            return f"Bearer {response_body['access_token']}"

        except Exception as e:
            logger.debug(f"[VOIP] Não foi possível carregar a token de acesso Nvoip. Exception: \"{repr(e)}\" ")
            return None

    @classmethod
    def codificar_dados(cls, data, headers) -> None:
        encoded = str(json.dumps(data)).encode()
        request = Request(f"https://api.nvoip.com.br/v2/torpedo/voice?napikey={cls.cfg['napikey']}", data=encoded, headers=headers)
        try:
            response_body = urlopen(request).read()
            logger.debug(f"[VOIP] Response Body: {response_body}")

        except Exception as e:
            logger.exception(f"[VOIP] Não foi possível codificar dados de envio de torpedo. Exception: \"{repr(e)}\".")

    @classmethod
    def acionar_chamada(cls):
        headers = {"Content-Type": "application/json", "Authorization": cls.carrega_token()}

        if cls.cfg["voz_habilitado"]:
            logger.debug("[VOIP] Enviando voz de Emergencia...")

            if agenda := cls.carrega_contatos() is not None:
                lista_contatos = cls.verifica_expediente(agenda)
            else:
                logger.info("[VOIP] Lista de contatos vazia! Carregando lista de contatos padrão.")
                lista_contatos = cls.lista_padrao

            for contato in lista_contatos:
                logger.info(f"[VOIP] Disparando torpedo de voz para: {contato[0]} ({contato[1]})")

            if cls.voip_dict["EMERGENCIA"][0]:
                data = {
                    "caller": f"{cls.cfg['caller_voip']}",
                    "called": f"{contato[1]}",
                    "audios": [{"audio": f"{cls.voip_dict['EMERGENCIA'][1]}", "positionAudio": 1,}],
                    "dtmfs": [],
                }
                cls.codificar_dados(data, headers)
                sleep(5)

            else:
                for _, vl in cls.voip_dict.items():
                    if vl[0]:
                        data = {
                            "caller": f"{cls.cfg['caller_voip']}",
                            "called": f"{contato[1]}",
                            "audios": [{"audio": f"{vl[1]}", "positionAudio": 1,}],
                            "dtmfs": [],
                        }
                        cls.codificar_dados(data, headers)
                        sleep(25)

        else:
            logger.info("[VOIP] Torpedo de voz desativado. Para habilitar envio, favor alterar valor \"voz_habilitado = true\" no arquivo \"voip_config.json\".")
