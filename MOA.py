from datetime import datetime
from time import sleep
from time import time
import logging
import usina

###########################
# Inicializando o logging #
###########################

# Inicializando o logger principal
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

#######################
# Inicializando o MOA #
#######################

logging.info('Inicializando o MOA')

usina.inicializar()

# A escala de tempo é utilizada para acelerar as simulações do sistema
# Utilizar 10x para testes sérios e 120x no máximo para testes simples
ESCALA_DE_TEMPO = 1


##############
# CONSTANTES #
##############

n_movel_R = 6               # N da média móvel para determinar nv_montante recente/rapdo
KIe = 0.05                  # Ganho do integrador de de estabilidade
saida_Ie = 0.3              # Valor inicial do integrador de estabilidade
nv_alvo_inicial = 643.25    # Valor inicial do nv_alvo


##############################
# INICIALIZAÇÃO DE VARIAVEIS #
##############################

n_movel_L = n_movel_R*5             # N da média móvel para determinar nv_montante anterior/lento
nv_alvo = nv_alvo_inicial           # Unidade: m
nv_montante = 0                     # Unidade: m
nv_montante_anterior = 0            # Unidade: m
pot_ug1 = 0.0                       # Unidade: MW
pot_ug2 = 0.0                       # Unidade: MW
pot_alvo = 0.0                      # Unidade: MW
aguardando_reservatorio = False     # Estado pertinente ao reservatório
erro_nv = 0                         # Utilizado no PID Unidade: m
erro_nv_anterior = 0                # Utilizado no PID Unidade: m
controle_p = 0                      # Controle proporcional do PID
controle_i = 0                      # Controle intregrativo do PID
controle_d = 0                      # Controle derivativo do PID
saida_PID = 0                       # Saída do controle PID


###########################
# ANTES DOS CICLOS DO MOA #
###########################

logging.info('Executando o MOA')

# Verifica a conexão com a usina e não prosseque sem.
while True:
    try:
        if usina.get_nv_montante() > 0:
            break
    except Exception as e:
        logging.error("MOA Não conectou a CLP! '{}'. Tentando novamente.".format(e))
        sleep(1)
        pass

# inicializção de vetores
nv_montante_recentes = [usina.get_nv_montante()] * n_movel_R
nv_montante_anteriores = [usina.get_nv_montante()] * n_movel_L
nv_montante_recente = sum(nv_montante_recentes) / len(nv_montante_recentes)

# DEBBUG
logging.debug("Tempo simulado; Nível montante;Nível médio;Potência alvo;Leitura UG1;Leitura UG2; AfluenteSIMUL")

while True:

    ##########################
    # INÍCIO DO CICLO DO MOA #
    ##########################
    try:

        ########################
        # ATUALIZAÇÃO DAS VARS #
        ########################

        # Atualiza níveis de referência
        nv_montante = usina.get_nv_montante()

        nv_montante_recentes.append(nv_montante)
        nv_montante_recentes = nv_montante_recentes[1:-1] if len(nv_montante_recentes) > n_movel_R else nv_montante_recentes
        nv_montante_recente = sum(nv_montante_recentes) / n_movel_R

        nv_montante_anteriores.append(nv_montante)
        nv_montante_anteriores = nv_montante_anteriores[1:-1] if len(nv_montante_anteriores) > n_movel_L else nv_montante_anteriores
        nv_montante_anterior = sum(nv_montante_anteriores) / n_movel_L


        # Atualiza pot real das ugs e não o setpoint
        pot_ug1 = usina.get_pot_ug1()
        pot_ug2 = usina.get_pot_ug2()

        # Atualiza o estado da comporta
        estado_comp = usina.get_pos_comporta()

        ###############################################
        # VERIFICA CONDIÇÕES E EXECUTA COMPORTAMENTOS #
        ###############################################

        # Se passar do nv de espera, turbinar!
        if nv_montante > usina.get_nv_religamento():
            if aguardando_reservatorio:
                logging.info("O nv_montante ({:03.2f}) está acima do limite de religamento.".format(nv_montante))
            aguardando_reservatorio = False

        # Se estiver sem água no reservatorio, travar até o nv_montante subir
        if nv_montante <= usina.USINA_NV_MIN:
            if not aguardando_reservatorio:
                logging.info("O nv_montante ({:03.2f}) está abaixo do limite inferior.".format(nv_montante))
            aguardando_reservatorio = True
            nv_alvo = usina.get_nv_religamento()
            pot_alvo = 0
            usina.distribuir_potencia(pot_alvo, 0)

        # Se não estiver aguardando acompanhar/deplecionar reservatório
        if not aguardando_reservatorio:

            # Se estiver vertendo
            if nv_montante_recente >= usina.USINA_NV_MAX:
                pot_alvo = usina.USINA_POTENCIA_NOMINAL

            # Se não estiver vertendo
            if nv_montante_recente < usina.USINA_NV_MAX:
                # Atualiza o alvo e o erro
                nv_alvo = usina.get_nv_alvo()
                erro_nv = nv_alvo - nv_montante_recente
                erro_nv_anterior = nv_alvo - nv_montante_anterior

                # Calcula o PID
                controle_p = usina.controle_proporcional(erro_nv)
                controle_i = usina.controle_integral(erro_nv, controle_i)
                controle_d = usina.controle_derivativo(erro_nv, erro_nv_anterior)

                # Verifica/calcula o PID na região alternativa de 1cm prox ao erro
                if abs(erro_nv) <= 0.01:
                    controle_p = controle_p*0.5
                    controle_d = controle_d*0.01
                saida_PID = controle_p + controle_i + controle_d

                # Calcula o integrador de estabilidade e limita
                saida_Ie = saida_PID * (KIe / ESCALA_DE_TEMPO) + saida_Ie
                saida_Ie = max(min(saida_Ie, 1), 0)

                # Calcula a pot alvo e limita
                pot_alvo = round(usina.USINA_POTENCIA_NOMINAL * saida_Ie, 2)
                pot_alvo = max(min(pot_alvo, usina.USINA_POTENCIA_NOMINAL), usina.USINA_POTENCIA_MINIMA_UG)

            # Distribui a potência para as UGs
            # logging.debug("Pot Alvo: {:2.3f} (PID: {:2.3f} {:2.3f}+{:2.3f}+{:2.3f}; Int: {:2.3f})".format(pot_alvo, saida_PID, controle_p, controle_i, controle_d, saida_Ie))
            usina.distribuir_potencia(pot_alvo, erro_nv)

        else:
            logging.debug("Aguardando reservatório.".format(nv_montante))
            pot_alvo = 0
            usina.distribuir_potencia(pot_alvo, 0)

        # DEBBUG!
        # EXCEL
        # logging.debug(("{:03.4f};{:03.4f};{:03.4f};{:03.4f};{:03.4f}".format(nv_montante, nv_montante_recente, pot_alvo, pot_ug1, pot_ug2)).replace(".", ","))
        logging.debug("T{:} Alvo:{:3.2f}m Montante:{:3.2f}m Alvo:{:1.3f}MW Pot:{:1.3f}MW SP1:{:1.3f}MW SP2:{:1.3f}MW"
                      .format(datetime.now(), nv_alvo, nv_montante, pot_alvo, pot_ug1+pot_ug2,
                              usina.get_setpoint_ug1(), usina.get_setpoint_ug2()))

        # heartbeat da usina para o E3, ou equivalente...
        usina.heartbeat()

        # Temporizador entre ciclos
        # Valor padrão é de 5 segundos, assim a média móvel rapda do nv_montante representa 1m (e a lenta 5m)
        sleep(5/ESCALA_DE_TEMPO)

    ############################
    # TRATAMENTO DE EXCEPTIONS #
    ############################

    # Exception padrão/sem descritivo
    except Exception as e:
        logging.error("MOA experienciou uma Exception: '{}'".format(e))
        raise e
        continue

    # Parada abrupta pelo teclado (ctrl-c ou equivalente)
    except KeyboardInterrupt as e:
        logging.info("MOA recebeu uma interrupção por teclado: '{}'".format(e))
        break

logging.info("MOA finalizado")