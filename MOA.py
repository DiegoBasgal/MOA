from time import sleep
from time import time_ns
import logging
import usina

# Inicializando o logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
# LOG to file
fileHandler = logging.FileHandler("MOA.log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
# LOG to console
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

logging.info('Inicializando o MOA')
t0 = time_ns()
nv_montante = 0
while nv_montante == 0:
    try:
        nv_montante = usina.get_nv_montante()
    except Exception as e:
        nv_montante = 0
        logging.warning("{}".format(e))
        pass
nv_montante_anterior = nv_montante
nv_montante_recentes = [nv_montante]
pot_ug1 = 0.0  # MW
pot_ug2 = 0.0  # MW
nv_montante_medio = 0
q_afluente = 0
pot_alvo = 0

logging.info('Executando o MOA')

while True:

    if abs(nv_montante - nv_montante_anterior) > 0.01 or not(usina.USINA_NV_MIN < nv_montante < usina.USINA_NV_MAX):
        nv_montante_anterior = nv_montante
        nv_montante_recentes.append(nv_montante)
        if len(nv_montante_recentes) > 30:
            nv_montante_recentes = nv_montante_recentes[1:31]
        nv_montante_medio = sum(nv_montante_recentes) / len(nv_montante_recentes)

        # fecha o tempo entre ciclos e já começa a gravar novamente
        delta_t = (time_ns() - t0) * (10 ** 9)
        t0 = time_ns()

        # controle da operação
        pot_ug1 = usina.get_pot_ug1()
        pot_ug2 = usina.get_pot_ug2()
        estado_comporta = usina.get_pos_comporta()

        q_afluente = usina.q_afluente(delta_t, 0, 0, nv_montante, nv_montante_anterior, estado_comporta)
        q_turbinada_alvo = q_afluente

        pot_alvo = usina.determina_pot(q_turbinada_alvo, nv_montante_medio)
        usina.distribuir_potencia(pot_alvo)

    logging.debug("nv_montante: {:03.2f} |"
                  " q_afluente_medio: {:03.2f} |"
                  " {:03.3f} pot_alvo |"
                  " {:03.3f} pot_ug1 |"
                  " {:03.3f} pot_ug2".format(nv_montante, q_afluente, pot_alvo, pot_ug1, pot_ug2))

    sleep(0.1)
