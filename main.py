"""
    Módulo de Operação Autônoma (MOA)
"""
__version__ = "2.0"
__status__ = "Produção"
__description__ = "Módulo de Operação Autônoma"

__maintainers__ = "Diego Basgal", "Henrique Pfeifer"
__emails__ = "diego.garcia@ritmoenergia.com.br", "henrique@ritmoenergia.com.br"

__authors__ = "Diego Basgal", "Henrique Pfeifer", "Lucas Lavratti"
__credits__ = ["Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal", "Lucas Specht", ...]

import os
import sys
import time
import json
import logging
import threading
import traceback

import src.usina as u
import src.conectores.servidores as srv
import src.maquinas_estado.moa as moa_sm

from time import time, sleep
from logging.config import fileConfig

from src.dicionarios.const import *


if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))


fileConfig("/opt/operacao-autonoma/logger_config.ini")
logger = logging.getLogger("logger")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])

    t_i = time()
    t_restante = 1
    n_tentativa = 0
    executar = False
    prox_estado = None

    logger.info("Iniciando MOA...                          (DEBUG: \"ON\")")
    logger.debug(f"ESCALA_DE_TEMPO:                          {ESCALA_DE_TEMPO}")

    while not executar:
        n_tentativa += 1
        logger.info(f"Tentativa:                                {n_tentativa}/3")

        if n_tentativa == 3:
            prox_estado = moa_sm.FalhaCritica

        else:
            try:
                logger.debug("")
                logger.info("Carregando arquivo de configuração...")

                arquivo = os.path.join(os.path.dirname("/opt/operacao-autonoma/src/dicionarios/"), "cfg.json")
                with open(arquivo, "r") as file:
                    cfg = json.load(file)

                arquivo = os.path.join(os.path.dirname("/opt/operacao-autonoma/src/dicionarios/"), "cfg.json.bkp")
                with open(arquivo, "w") as file:
                    json.dump(cfg, file, indent=4)

            except Exception:
                logger.exception(f"Erro ao carregar arquivo de configuração. Tentando novamente em \"{TIMEOUT_MAIN}s\"")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(TIMEOUT_MAIN)
                continue

            try:
                logger.debug("")
                logger.info("Iniciando instância e objetos da Usina...")
                usn: "u.Usina" = u.Usina(cfg)

            except Exception:
                logger.exception(f"Erro ao instanciar a classe Usina. Tentando novamente em \"{TIMEOUT_MAIN}s\"")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(TIMEOUT_MAIN)
                continue

            try:
                logger.debug("")
                logger.info("Iniciando intâncias de máquina de estados e Threads...")

                threading.Thread(target=lambda: usn.verificar_leituras_periodicas()).start()
                sm = moa_sm.StateMachine(initial_state=moa_sm.Pronto(usn=usn))

                executar = True

            except Exception:
                logger.exception(f"Erro ao finalizar a incialização do MOA. Tentando novamente em \"{TIMEOUT_MAIN}s\"")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(TIMEOUT_MAIN)
                continue

    logger.debug("")
    logger.info("\U0001F916 Inicialização completa! Executando o Módulo de Operação Autônoma (MOA) \U0001F916")
    logger.debug("")

    while True:
        try:
            logger.debug("")
            logger.debug("")
            logger.debug(f"Executando estado:                        \"{sm.state.__class__.__name__}\"")
            logger.debug("-----------------------------------------------------------------")
            sm.exec()

            if usn.estado_moa in (MOA_SM_CONTROLE_ESTADOS, MOA_SM_MODO_MANUAL):
                t_restante = max(TEMPO_CICLO_TOTAL - (time() - t_i), 0) / ESCALA_DE_TEMPO
                t_i = time()

            elif usn.estado_moa == MOA_SM_MODO_MANUAL:
                sleep(30)

            else:
                t_restante = 1

            if t_restante == 0:
                pass
            else:
                sleep(t_restante)

        except Exception as e:
            logger.debug("")
            logger.error(f"[!!!] \"ATENÇÃO!\" Houve um erro na execução do loop principal -> !! \"main.py\" !!")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            srv.Servidores.close_all()
            logger.debug("MOA encerrado! Até a próxima...")
            break

        except KeyboardInterrupt:
            logger.debug("")
            logger.warning("[!!!] \"ATENÇÃO!\" Execução do loop principal da main do MOA interrompido por comando de teclado.")
            srv.Servidores.close_all()
            logger.debug("MOA encerrado! Até a próxima...")
            break
