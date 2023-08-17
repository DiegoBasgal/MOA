import pytz
import json
import logging
import os.path
import traceback

from time import sleep
from logging.config import fileConfig
from datetime import datetime, timedelta
from pyModbusTCP.client import ModbusClient

from src.mensageiro.voip import Voip
from src.dicionarios.dict import WATCHDOG
from src.mensageiro.dict import voip_dict
from src.conectores.banco_dados import BancoDados

if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

fileConfig("/opt/operacao-autonoma/logger_config.ini")
logger = logging.getLogger("watchdog")

class Watchdog:
    def __init__(self) -> "None":

        self.timestamp: "datetime" = 0

        self.moa_interrompido: "bool" = False

        self.db = BancoDados("Watchdog")

        self.cliente = ModbusClient(
            host=WATCHDOG["ip"],
            port=WATCHDOG["porta"],
            timeout=5,
            unit_id=1
        )


    def get_time(self) -> "datetime":
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    def exec(self) -> "None":

        while True:
            try:
                data = self.db.get_timestamp_moa()

                ano = data.year
                mes = data.month
                dia = data.day
                hora = data.hour
                minuto = data.minute
                segundo = data.second
                microsegundo = data.microsecond

            except Exception:
                logger.error("Erro na conexão com o Banco de Dados MariaDB do MOA. Executando modo de verificação pelo CLP-MOA...")
                logger.debug(traceback.format_exc())
                sleep(5)

            finally:
                try:
                    if self.cliente.open():
                        data = self.cliente.read_holding_registers(0, 7)
                        self.cliente.close()

                        ano = data[0]
                        mes = data[1]
                        dia = data[2]
                        hora = data[3]
                        minuto = data[4]
                        segundo = data[5]
                        microsegundo = data[6]

                except Exception:
                    logger.error(f"Erro na conexão com o CLP-MOA. Tentando novamente em \"{WATCHDOG['timeout_moa']}s\"...")
                    logger.debug(traceback.format_exc())
                    voip_dict["WATCHDOG"][0] = True
                    Voip.acionar_chamada()

                    self.cliente.close()
                    sleep(WATCHDOG["timeout_moa"])
                    continue

            try:
                self.timestamp = datetime(ano, mes, dia, hora, minuto, segundo, microsegundo)
                logger.debug(f"Horário da última verificação de execução do MOA: {self.timestamp.strftime('%d-%m-%Y %H:%M:%S')}")

                if (self.get_time() - self.timestamp) > timedelta(seconds=WATCHDOG["timeout_moa"]):
                    if not moa_interrompido:
                        moa_interrompido = True

                        logger.warning(f"Verificação de execução do MOA em \"{WATCHDOG['nome_usina']}\" no \"{WATCHDOG['nome_local']}\" Falhou!")
                        logger.info(f"Horário: {self.get_time().strftime('%d-%m-%Y %H:%M:%S')}. Tentando novamente em \"{WATCHDOG['timeout_moa']}s\"...")

                    sleep(WATCHDOG["timeout_moa"])

                else:
                    if moa_interrompido:
                        moa_interrompido = False
                        logger.info(f"Verificação de execução do MOA normalizada. Horário: {self.timestamp.strftime('%d-%m-%Y %H:%M:%S')}")

            except Exception:
                logger.error(f"Erro na verificação de execução do MOA. Tentando novamente em \"{WATCHDOG['timeout_moa']}s\"...")
                logger.debug(traceback.format_exc())
                sleep(WATCHDOG["timeout_moa"])
                continue