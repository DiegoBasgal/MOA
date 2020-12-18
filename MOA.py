from datetime import datetime
from time import sleep
from time import time
import logging
import usina

# Inicializando o logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)
# LOG to file
fileHandler = logging.FileHandler("MOA.log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
# LOG to console
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

logging.info('Inicializando o MOA')

usina.inicializar()

ESCALA_DE_TEMPO = 10

t0 = time()
t1 = time()
n_movel = 30
n_movel2 = 120
nv_montante = 0
nv_montante_anterior = 0
pot_ug1 = 1.0  # MW
pot_ug2 = 0.0  # MW
pot_alvo = 1.0
aguardando_reservatorio = False
erro_nv = 0
erro_nv_anterior = 0
controle_p = 0
controle_i = 0
controle_d = 0
Kii = 0.01/ESCALA_DE_TEMPO

saida_PID = 0
saida_PID_int = 0.5
logging.info('Executando o MOA')

while True:
    try:
        if usina.get_nv_montante() > 0:
            break
    except Exception as e:
        logging.error("MOA Não conectou a CLP! '{}'. Tentando novamente.".format(e))
        sleep(1)
        pass

nv_recentes = [usina.get_nv_montante()]*n_movel
nv_recentes2 = [usina.get_nv_montante()]*n_movel
nv_medio = sum(nv_recentes)/len(nv_recentes)
nv_alvo = (usina.USINA_NV_MIN + usina.USINA_NV_MAX)/2
logging.debug("Tempo simulado; Nível montante;Nível médio;Potência alvo;Leitura UG1;Leitura UG2; AfluenteSIMUL")

while True:
    try:
        t1 = time()

        nv_montante = usina.get_nv_montante()
        nv_recentes.append(nv_montante)
        nv_recentes2.append(nv_montante)
        if len(nv_recentes) > n_movel:
            nv_recentes = nv_recentes[1:-1]
        if len(nv_recentes2) > n_movel2:
            nv_recentes2 = nv_recentes2[1:-1]
        nv_montante_anterior = sum(nv_recentes2) / len(nv_recentes2)
        nv_medio = sum(nv_recentes) / len(nv_recentes)

        pot_ug1 = usina.get_pot_ug1()
        pot_ug2 = usina.get_pot_ug2()
        #estado_comp = usina.get_pos_comporta()

        # Se passar do nv de espera, turbinar!
        if nv_montante >= usina.get_nv_religamento():
            if aguardando_reservatorio:
                logging.info("O nv_montante ({:03.2f}) está acima do limite superior. POT:{:02.3f}".format(nv_montante, pot_alvo))
            aguardando_reservatorio = False

        # Se estiver sem água no reservatorio, travar até o nv_montante subir
        if nv_montante <= usina.USINA_NV_MIN:
            if not aguardando_reservatorio:
                logging.info("O nv_montante ({:03.2f}) está abaixo do limite inferior. POT:{:02.3f}".format(nv_montante, pot_alvo))
            aguardando_reservatorio = True
            nv_alvo = usina.get_nv_religamento()
            pot_alvo = 0
            usina.distribuir_potencia(pot_alvo, 0)

        # Se não estiver aguardando acompanhar/deplecionar reservatório
        if not aguardando_reservatorio:
            nv_alvo = usina.get_nv_alvo()
            erro_nv = nv_alvo - nv_medio
            erro_nv_anterior = nv_alvo - nv_montante_anterior

            controle_p = usina.controle_proporcional(erro_nv)
            controle_i = usina.controle_integral(erro_nv, controle_i)
            controle_d = usina.controle_derivativo(erro_nv, erro_nv_anterior)

            saida_PID = controle_p + controle_i + controle_d

            saida_PID_int = saida_PID*Kii + saida_PID_int
            saida_PID_int = min(saida_PID_int, 1)
            saida_PID_int = max(saida_PID_int, 0)

            pot_alvo = round(usina.USINA_POTENCIA_NOMINAL * (saida_PID_int + saida_PID), 2)
            pot_alvo = max(pot_alvo, usina.USINA_POTENCIA_MINIMA_UG)
            pot_alvo = min(pot_alvo, usina.USINA_POTENCIA_NOMINAL)

            logging.debug("Pot Alvo: {:2.3f} (PID: {:2.3f} {:2.3f}+{:2.3f}+{:2.3f}; Int: {:2.3f})".format(pot_alvo, saida_PID, controle_p, controle_i, controle_d, saida_PID_int))
            usina.distribuir_potencia(pot_alvo, erro_nv)
        else:
            #logging.info("Aguardando reservatório.".format(nv_montante))
            pot_alvo = 0
            usina.distribuir_potencia(pot_alvo, 0)

        q_debbug = usina.get_q_afluente_debbug()
        logging.debug(("{:03.4f};{:03.4f};{:03.4f};{:03.4f};{:03.4f};{:03.1f}"
                       .format(nv_montante, nv_medio, pot_alvo,pot_ug1, pot_ug2, q_debbug)).replace(".", ","))
        print("T{:} Alvo:{:3.2f}m Montante:{:3.2f}m Alvo:{:1.3f}MW Pot:{:1.3f}MW SP1:{:1.3f}MW SP2:{:1.3f}MW"
              .format(datetime.now(), nv_alvo, nv_montante, pot_alvo, pot_ug1+pot_ug2,
                      usina.get_setpoint_ug1(), usina.get_setpoint_ug2()))
        usina.heartbeat()
        sleep(1/ESCALA_DE_TEMPO)

    except Exception as e:
        logging.error("MOA experienciou uma Exception: '{}'".format(e))
        raise e
        continue
    except KeyboardInterrupt as e:
        logging.info("MOA recebeu uma interrupção por teclado: '{}'".format(e))
        break

logging.info("MOA finalizado")