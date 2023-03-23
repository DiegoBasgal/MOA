"""
operador_autonomo_sm.py

Implementacao teste de uma versao do moa utilizando SM
"""

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
import conector as conector
import src.mensageiro.voip as voip

from sys import stderr
from time import sleep
from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.dict import *
from src.dicionarios.const import *
from src.maquinas_estado.moa_sm import *

from src.clients import ClientsUsn
from comporta import Comportas
from src.unidade_geracao import UnidadeDeGeracao
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

# Método de leitura por período
def leitura_temporizada():
    delay = 1800
    proxima_leitura = time.time() + delay
    logger.debug("Iniciando o timer de leitura por hora.")
    while True:
        logger.debug("Inciando nova leitura...")
        try:
            if usina.leituras_por_hora() and usina.acionar_voip:
                acionar_voip()
            for ug in usina.ugs:
                ug.leituras_por_hora()
            time.sleep(max(0, proxima_leitura - time.time()))
            
        except Exception:
            logger.debug("Houve um problema ao executar a leitura por hora")

        proxima_leitura += (time.time() - proxima_leitura) // delay * delay + delay

# Método para acionamento voip
def acionar_voip():
    V_VARS = voip.VARS
    try:
        if usina.acionar_voip:
            for i, j in zip(voip, V_VARS):
                if i == j and shared_dict["VOIP"][i]:
                    V_VARS[j][0] = shared_dict["VOIP"][i]
            voip.enviar_voz_auxiliar()

        elif shared_dict["GLB"]["avisado_eletrica"]:
            voip.enviar_voz_emergencia()
            shared_dict["GLB"]["avisado_eletrica"] = False

    except Exception:
        logger.warning("Houve um problema ao ligar por Voip")

if __name__ == "__main__":

    ESCALA_DE_TEMPO = 3
    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])
    
    logger = criar_logger()
    aux = 0
    deve_normalizar = None
    normalizacao_geral_teste = 0
    usina = None
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

                sd = dicionario
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

                cln = ClientsUsn(sd)
                cln.open_all()

            except Exception:
                logger.exception(f"Erro ao iniciar conexão com os CLPs da usina. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue
            
            try:
                logger.info("Iniciando classes de escrita OPC")

                esc_opc = EscritaOpc(cln.opc_client)
                esc_opc_bit = EscritaOpcBit(cln.opc_client)
                esc = [esc_opc, esc_opc_bit]

            except Exception:
                logger.exception(f"Erro ao iniciar classes de escrita. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
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
                logger.info("Iniciando classes de conexão com tda, subestacao, bay e banco de dados.")

                db = BancoDados()
                bay = Bay(cnv, dcv)
                sub = Subestacao(sd, esc, cln)
                tda = TomadaAgua()
                con = [tda, sub, bay]

            except Exception:
                logger.exception(f"Erro ao instanciar as classes de conexão. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando instâncias das classes Unidade de Geração")

                ug1 = UnidadeDeGeracao(1, cfg, cln, con, db, escs)
                ug2 = UnidadeDeGeracao(2, cfg, cln, con, db)
                UnidadeDeGeracao.lista_ugs = [ug1, ug2]

            except Exception:
                logger.exception(f"Erro ao instanciar a classe das Unidades de Geração. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando instância da classe Usina.")
                usn = Usina(cfg, db)

            except Exception:
                logger.exception(f"Erro ao instanciar a classe Usina. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(timeout)
                continue

    logger.info("Inicialização completa, executando o MOA \U0001F916")

    threading.Thread(target=lambda: leitura_temporizada()).start()

    sm = StateMachine(initial_state=prox_estado(usina))
    while True:
        print("")
        t_i = time.time()
        logger.debug("Executando estado: {}".format(sm.state.__class__.__name__))
        sm.exec()
        t_restante = max(30 - (time.time() - t_i), 0) / ESCALA_DE_TEMPO
        if t_restante == 0:
            print("######################################################\n######################################################\nCiclo está demorando mais que o permitido\n######################################################\n######################################################")
        sleep(t_restante)
