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
t1 = time_ns()
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
saida_PID = 0
saida_PID_int = 0
logging.info('Executando o MOA')

nv_recentes = [usina.get_nv_montante()]*n_movel
nv_recentes2 = [usina.get_nv_montante()]*n_movel
nv_medio = sum(nv_recentes)/len(nv_recentes)
nv_alvo = (usina.USINA_NV_MIN + usina.USINA_NV_MAX)/2
logging.debug("Tempo simulado; Nível montante;Nível médio;Potência alvo;Leitura UG1;Leitura UG2; AfluenteSIMUL")

while True:

    t1 = time_ns()

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


    # Se estiver QUASE vertendo, turbinar um pouco!
    if nv_montante >= usina.USINA_NV_MAX-0.1 and aguardando_reservatorio:
        aguardando_reservatorio = False
        # logging.info("O nv_montante ({:03.2f}) está acima do limite superior. POT:{:02.3f}".format(nv_montante, pot_alvo))

    # Se estiver sem água no reservatorio, travar até o nv_montante subir
    if nv_montante <= usina.USINA_NV_MIN:
        aguardando_reservatorio = True
        pot_alvo = 0
        usina.distribuir_potencia(pot_alvo)
        #logging.info("O nv_montante ({:03.2f}) está abaixo do limite inferior. POT:{:02.3f}".format(nv_montante, pot_alvo))

    # Se não estiver aguardando acompanhar/deplecionar reservatório
    if not aguardando_reservatorio:

        erro_nv = usina.NV_ALVO - nv_medio
        erro_nv_anterior = usina.NV_ALVO - nv_montante_anterior

        controle_p = usina.controle_proporcional(erro_nv)
        controle_i = usina.controle_integral(erro_nv, controle_i)
        controle_d = usina.controle_derivativo(erro_nv, erro_nv_anterior)

        saida_PID = controle_p + controle_i + controle_d

        Kii = 0.001
        saida_PID_int = saida_PID*Kii + saida_PID_int
        saida_PID_int = min(saida_PID_int, 1)
        saida_PID_int = max(saida_PID_int, 0)

        pot_alvo = round(usina.USINA_POTENCIA_NOMINAL * (saida_PID_int + saida_PID), 2)
        pot_alvo = max(pot_alvo, usina.USINA_POTENCIA_MINIMA_UG)
        pot_alvo = min(pot_alvo, usina.USINA_POTENCIA_NOMINAL)

        print("Pot Alvo: {:2.3f} (PID: {:2.3f} {:2.3f}+{:2.3f}+{:2.3f}; Int: {:2.3f})".format(pot_alvo, saida_PID, controle_p, controle_i, controle_d, saida_PID_int))
        usina.distribuir_potencia(pot_alvo)
    else:
        #logging.info("Aguardando reservatório.".format(nv_montante))
        pot_alvo = 0
        usina.distribuir_potencia(pot_alvo)

    q_debbug = usina.get_q_afluente_debbug()
    #logging.debug(("{:03.4f};{:03.4f};{:03.4f};{:03.4f};{:03.4f};{:03.1f}".format(nv_montante, nv_medio, pot_alvo, pot_ug1, pot_ug2, q_debbug)).replace(".", ","))

    sleep(0.05)
