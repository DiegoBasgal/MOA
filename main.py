import os
import sys
import time
import json
import pytz
import logging
import threading
import traceback
import logging.handlers as handlers

import usina as usina

from sys import stderr
from time import sleep, time
from datetime import datetime

from src.dicionarios.dict import *
from src.maquinas_estado.moa_sm import *

from src.clients import ClientsUsn
from src.banco_dados import BancoDados
from src.conversor_protocolo.conversor import NativoParaExterno
from src.mensageiro.mensageiro_log_handler import MensageiroHandler

# Criar pasta para logs
if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

# Método para conversão de data/horário GMT:-03:00 (Brasil)
def timeConverter() -> datetime:
    tz = pytz.timezone("Brazil/East")
    return datetime.now(tz).timetuple()

# Método para criar logger principal
def criar_logger() -> logging:
    logger = logging.getLogger(__name__)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(logging.NOTSET)

    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [MOA-SM] %(message)s")
    logFormatterSimples = logging.Formatter("[%(levelname)-5.5s] %(message)s")
    logFormatter.converter = timeConverter

    ch = logging.StreamHandler(stderr)  # log para sdtout
    ch.setFormatter(logFormatter)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    fh = handlers.TimedRotatingFileHandler(
        os.path.join(os.path.dirname(__file__), "logs", "MOA.log"),
        when="midnight",
        interval=1,
        backupCount=7,
    )  # log para arquivo
    fh.setFormatter(logFormatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    mh = MensageiroHandler()
    mh.setFormatter(logFormatterSimples)
    mh.setLevel(logging.INFO)
    logger.addHandler(mh)

    return logger

# Método de leitura do arquivo de dados json
def leitura_json(nome: str) -> dict:
    arquivo = os.path.join(os.path.dirname(__file__), nome)
    with open(arquivo, "r") as file:
        return json.load(file)

# Método de escrever no arquivo de dados json após mudanças
def escrita_json(valor, nome: str) -> None:
    arquivo = os.path.join(os.path.dirname(__file__), nome)
    with open(arquivo, "w") as file:
        json.dump(valor, file, indent=4)

if __name__ == "__main__":
    ESCALA_DE_TEMPO = 3
    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])

    logger = criar_logger()
    timeout = 10
    prox_estado = 0
    n_tentativa = 0

    logger.debug("Debug is ON")
    logger.info("Iniciando MOA...")
    logger.debug(f"ESCALA_DE_TEMPO: {ESCALA_DE_TEMPO}")

    while prox_estado == 0:
        n_tentativa += 1
        if n_tentativa == 3:
            prox_estado = FalhaCritica
        else:
            try:
                logger.info("Carregando arquivos de configuração, dicionário compartilhado e dados de conversão")

                dct = dicionario
                cfg = leitura_json("cfg.json")
                dcv = leitura_json("dados.json")
                escrita_json(cfg, "cfg.json.bkp")

            except Exception:
                logger.exception(f"Erro ao carregar arquivo de configuração e dicionário compartilhado. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando classe de conexão com o servidor OPC e CLPs da usina.")

                cln = ClientsUsn(dct)
                cln.open_all()

            except Exception:
                logger.exception(f"Erro ao iniciar conexão com os CLPs da usina. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Inicando classe de conversão de dados OPC DA / OPC UA.")
                cnv = NativoParaExterno(dcv)

            except Exception:
                logger.exception(f"Erro ao instanciar a classe de conversão de protocolo. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue
            
            try:
                logger.info("Iniciando classe de conexão com banco de dados.")

                bds = BancoDados()

            except Exception:
                logger.exception(f"Erro ao instanciar a classe do banco de dados. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando instância da classe Usina.")
                usn = Usina(cfg, dct, cln, cnv, bds)

            except Exception:
                logger.exception(f"Erro ao instanciar a classe Usina. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue
            
            try:
                logger.info("Finalizando inicialização com intâncias da máquina de estados e Threads paralelas.")

                sm = StateMachine(initial_state=Pronto(cfg, dct, usn, bds))

                threading.Thread(target=lambda: usn.leitura_temporizada()).start()

            except Exception:
                logger.exception(f"Erro ao finalizar a incialização do MOA. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

    logger.info("Inicialização completa, executando o MOA \U0001F916")

    while True:
        try:
            logger.debug(f"Executando estado: \"{sm.state.__class__.__name__}\"")

            t_i = time()
            sm.exec()
            if usn.estado_moa == MOA_SM_CONTROLE_DADOS:
                t_restante = max(30 - (time() - t_i), 0) / ESCALA_DE_TEMPO

                if t_restante == 0:
                    logger.warning("\n\"ATENÇÃO!\"")
                    logger.warning("O ciclo está demorando mais que o permitido!")
                    logger.warning("\"ATENÇÃO!\"\n")
                sleep(t_restante)

        except Exception as e:
            logger.exception(f"Houve um erro na execução do loop principal da main do MOA. Exception: {repr(e)}")
            logger.exception(f"Traceback: {traceback.print_stack}")
            cln.close_all()
            break

        except KeyboardInterrupt:
            logger.warning("Execução do loop principal da main do MOA interrompido por comando de teclado.")
            cln.close_all()
            break
