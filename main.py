"""
    Módulo de Operação Autônoma (MOA)
"""
__version__ = "2.0"
__status__ = "Desenvolvimento"
__description__ = "Módulo de Operação Autônoma"

__maintainers__ = "Diego Basgal", "Henrique Pfeifer"
__emails__ = "diego.garcia@ritmoenergia.com.br", "henrique@ritmoenergia.com.br"

__authors__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal"
__credits__ = ["Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal", ...]


import os
import sys
import time
import json
import threading
import traceback

from time import time, sleep

from src.dicionarios.const import *
from src.maquinas_estado.moa_sm import *

from conector import ClientesUsina

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ESCALA_DE_TEMPO = int(sys.argv[1])

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
                logger.info("Carregando arquivo de configuração.")

                arquivo = os.path.join(os.path.dirname(__file__), "cfg.json")
                with open(arquivo, "r") as file:
                    cfg = json.load(file)

                arquivo = os.path.join(os.path.dirname(__file__), "cfg.json.bkp")
                with open(arquivo, "w") as file:
                    json.dump(cfg, file, indent=4)

            except Exception:
                logger.exception(f"Erro ao carregar arquivo de configuração. Tentando novamente em \"{TIMEOUT_MAIN}s\" (Tentativa: {n_tentativa}/3).")
                logger.debug(f"Traceback: {traceback.print_stack}")
                sleep(TIMEOUT_MAIN)
                continue

            try:
                logger.info("Iniciando conexões com o servidores \"OPC\" e \"ModBus\".")

                ClientesUsina.open_all()

            except Exception:
                logger.exception(f"Erro ao iniciar classes de conexão com servidores. Tentando novamente em \"{TIMEOUT_MAIN}s\" (Tentativa: {n_tentativa}/3).")
                logger.debug(f"Traceback: {traceback.print_stack}")
                sleep(TIMEOUT_MAIN)
                continue

            try:
                logger.info("Iniciando instância da classe Usina.")
                usn: Usina = Usina(cfg)

            except Exception:
                logger.exception(f"Erro ao instanciar a classe Usina. Tentando novamente em \"{TIMEOUT_MAIN}s\" (Tentativa: {n_tentativa}/3).")
                logger.debug(f"Traceback: {traceback.print_stack}")
                sleep(TIMEOUT_MAIN)
                continue

            try:
                logger.info("Finalizando inicialização com intâncias da máquina de estados e Threads paralelas.")

                sm: StateMachine = StateMachine(initial_state=Pronto(cfg, usn))

                threading.Thread(target=lambda: usn.leitura_temporizada()).start()

            except Exception:
                logger.exception(f"Erro ao finalizar a incialização do MOA. Tentando novamente em \"{TIMEOUT_MAIN}s\" (Tentativa: {n_tentativa}/3).")
                logger.debug(f"Traceback: {traceback.print_stack}")
                sleep(TIMEOUT_MAIN)
                continue

    logger.info("Inicialização completa, executando o MOA \U0001F916")

    while True:
        try:
            logger.debug(f"Executando estado: \"{sm.state.__class__.__name__}\"")
            t_inicio = time()
            sm.exec()
            logger.debug(f"\nTempo de ciclo: {float(time() - t_inicio)}s\n")

            if usn.estado_moa == MOA_SM_CONTROLE_DADOS:
                t_restante = max(30 - (time() - t_inicio), 0) / ESCALA_DE_TEMPO

                if t_restante == 0:
                    logger.warning("\n\"ATENÇÃO!\"")
                    logger.warning("O ciclo está demorando mais que o permitido!")
                    logger.warning("\"ATENÇÃO!\"\n")
                sleep(t_restante)

        except Exception as e:
            logger.exception(f"Houve um erro na execução do loop principal da main do MOA. Exception: {repr(e)}")
            logger.debug(f"Traceback: {traceback.print_stack}")
            ClientesUsina.close_all()
            break

        except KeyboardInterrupt:
            logger.warning("Execução do loop principal da main do MOA interrompido por comando de teclado.")
            ClientesUsina.close_all()
            break
