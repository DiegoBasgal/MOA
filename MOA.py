import os
import sys
import time
import json
import traceback

from threading import Thread
from time import sleep, time

from src.usina import *
from src.logger import *
from src.conector import *
from src.ocorrencias import *
from src.agendamentos import *
from src.dicionarios.const import *
from src.maquinas_estado.moa import *

if __name__ == "__main__":
    timeout = 10
    prox_estado = 0
    n_tentativa = 0

    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])

    logger.info("Iniciando MOA...")
    logger.debug(f"Escala de tempo -> \"{ESCALA_DE_TEMPO}\"")

    while prox_estado == 0:
        n_tentativa += 1

        if n_tentativa == 3:
            prox_estado = FalhaCritica
        else:
            try:
                logger.info("Carregando arquivo de configuração \"dict.json\".")
                config_file = os.path.join(os.path.dirname(__file__), "dict.json")
                with open(config_file, "r") as file:
                    shared_dict = json.load(file)
                config_file = os.path.join(os.path.dirname(__file__), "dict.json.bkp")
                with open(config_file, "w") as file:
                    json.dump(shared_dict, file, indent=4)
            except Exception:
                logger.exception(f"Erro ao carregar arquivo de configuração \"dict.json\".Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3)\nTraceback: {traceback.print_stack}")
                continue

            try:
                logger.info("Iniciando classes de conexão.")
                db = DatabaseConnector()
                con = FieldConnector(shared_dict)
            except Exception:
                logger.exception(f"Erro ao iniciar classes de conexão. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3)\nTraceback: {traceback.print_stack}")
                continue

            try:
                logger.info("Instanciando classes das Unidades de Geração.")
                ug1 = UnidadeDeGeracao(1, shared_dict, con, db)
                ug2 = UnidadeDeGeracao(2, shared_dict, con, db)
                ugs = [ug1, ug2]
                ug1.lista_ugs = ugs
                ug2.lista_ugs = ugs
            except Exception:
                logger.exception(f"Erro ao instanciar classes das Unidades de Geração. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3)\nTraceback: {traceback.print_stack}")
                continue

            try:
                logger.info("Instanciando classe de Ocorrências -> TRIPs e Alarmes da Usina.")
                ocorrencias = Ocorrencias(shared_dict, ugs)
            except Exception:
                logger.exception(f"Erro ao inciar classe Ocorrências. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).\nTraceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Iniciando classe Usina.")
                usina = Usina(shared_dict, con, db, ugs, ocorrencias)
            except Exception:
                logger.exception(f"Erro ao iniciar classe Usina. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).\nTraceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                logger.info("Instanciando classes das Unidades de Geração.")
                agendamentos = Agendamentos(shared_dict, db, usina, ugs)
            except Exception:
                logger.exception(f"Erro ao inciar classe Agendamentos. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).\nTraceback: {traceback.print_stack}")
                sleep(timeout)
                continue

            try:
                to_lt = Thread(target=lambda: ocorrencias.leitura_temporizada(1800)).start()
            except Exception:
                logger.exception(f"Erro ao iniciar Threads de leituras temporizadas e leituras de condcionadores. Tentando novamente em \"{timeout}s\" (Tentativa: {n_tentativa}/3).\nTraceback: {traceback.print_stack}")
                sleep(timeout)
                continue

    sm = StateMachine(initial_state=Pronto(shared_dict, usina, ugs, ocorrencias, agendamentos))
    logger.info("Inicialização completa, executando o MOA \U0001F916")
    while True:
        logger.debug(f"Executando estado: {sm.state.__class__.__name__}")
        t_i = time.time()
        sm.exec()
        t_restante = max(30 - (time.time() - t_i), 0) / ESCALA_DE_TEMPO
        if t_restante == 0:
            print("ATENÇÃO!\nCiclo está demorando mais que o permitido\nATENÇÃO!")
        sleep(t_restante)
