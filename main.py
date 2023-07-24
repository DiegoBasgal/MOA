"""
    Módulo de Operação Autônoma (MOA)
"""
__version__ = "2.0"
__status__ = "Desenvolvimento"
__description__ = "Módulo de Operação Autônoma"

__maintainers__ = "Diego Basgal", "Henrique Pfeifer"
__emails__ = "diego.garcia@ritmoenergia.com.br", "henrique@ritmoenergia.com.br"

__author__ = "Diego Basgal", " Henrique Pfeifer", "Lucas Lavratti"
__credits__ = ["Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal", "Lucas Specht", ...]


import os
import sys
import time
import json
import logging
import threading
import traceback

from time import time, sleep
from logging.config import fileConfig

from src.dicionarios.const import *
from src.maquinas_estado.moa import *

from src.conectores.servidores import Servidores

if not os.path.exists(os.path.join(os.path.dirname(__file__), "logs")):
    os.mkdir(os.path.join(os.path.dirname(__file__), "logs"))

fileConfig("/opt/operacao-autonoma/logger_cfg.ini")
logger = logging.getLogger("logger")

if __name__ == "__main__":

    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])

    t_i = time()

    prox_estado = 0
    n_tentativa = 0

    logger.info("Iniciando MOA...                          (DEBUG: \"ON\")")
    logger.debug(f"ESCALA_DE_TEMPO:                          {ESCALA_DE_TEMPO}")


    while prox_estado == 0:
        n_tentativa += 1
        logger.info(f"Tentativa:                                {n_tentativa}/3")

        if n_tentativa == 3:
            prox_estado = FalhaCritica

        else:
            try:
                logger.debug("")
                logger.info("Carregando arquivo de configuração...")


                arquivo = os.path.join(os.path.dirname(__file__), "cfg.json")
                with open(arquivo, "r") as file:
                    cfg = json.load(file)

                arquivo = os.path.join(os.path.dirname(__file__), "cfg.json.bkp")
                with open(arquivo, "w") as file:
                    json.dump(cfg, file, indent=4)

            except Exception:
                logger.error(f"Erro ao carregar arquivo de configuração. Tentando novamente em \"{TIMEOUT_MAIN}s\".")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(TIMEOUT_MAIN)
                continue

            try:
                logger.debug("")
                logger.info("Iniciando conexões com Servidores...")

                Servidores.open_all()

            except Exception:
                logger.error(f"Erro ao iniciar classes de conexão com servidores. Tentando novamente em \"{TIMEOUT_MAIN}s\".")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(TIMEOUT_MAIN)
                continue

            try:
                logger.debug("")
                logger.info("Iniciando instância e objetos da Usina...")

                usn: Usina = Usina(cfg)

            except Exception:
                logger.error(f"Erro ao instanciar a classe Usina. Tentando novamente em \"{TIMEOUT_MAIN}s\".")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(TIMEOUT_MAIN)
                continue

            try:
                logger.debug("")
                logger.info("Iniciando intâncias de máquina de estados e Threads...")

                threading.Thread(target=lambda: usn.verificar_leituras_periodicas()).start()

                sm: StateMachine = StateMachine(initial_state=Pronto(cfg, usn))

            except Exception:
                logger.error(f"Erro ao finalizar a incialização do MOA. Tentando novamente em \"{TIMEOUT_MAIN}s\".")
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

            with open(os.path.join(os.path.dirname('/opt/operacao-autonoma/src/dicionarios/'), "cfg.json"), "w") as file:
                json.dump(usn.cfg, file, indent=4)

            if usn.estado_moa == MOA_SM_CONTROLE_DADOS:
                t_restante = max(TEMPO_CICLO_TOTAL - (time() - t_i), 0) / ESCALA_DE_TEMPO
                t_i = time()

            else:
                t_restarnte = 1

            if t_restante == 0:
                pass

            else:
                sleep(t_restante)

        except Exception:
            logger.debug("")
            logger.error(f"[!!!] \"ATENÇÃO!\" Houve um erro na execução do loop principal -> !! \"main.py\" !!")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            Servidores.close_all()
            logger.debug("MOA encerrado! Até a próxima...")
            break

        except KeyboardInterrupt:
            logger.debug("")
            logger.warning("[!!!] \"ATENÇÃO!\" Execução do loop principal da main do MOA interrompido por comando de teclado.")
            Servidores.close_all()
            logger.debug("MOA encerrado! Até a próxima...")
            break
