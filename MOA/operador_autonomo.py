import logging
import sys
import traceback
from datetime import datetime
from pyModbusTCP.server import DataBank, ModbusServer
from sys import stdout
from time import sleep
from mensageiro.mensageiro_log_handler import MensageiroHandler

# Meus imports
from MOA import usina


def controle_proporcional(erro_nivel):
    return Kp * erro_nivel


def controle_integral(erro_nivel, ganho_integral_anterior):
    res = (Ki * erro_nivel) + ganho_integral_anterior
    res = min(res, 0.8)
    res = max(res, 0)
    return res


def controle_derivativo(erro_nivel, erro_nivel_anterior):
    return Kd * (erro_nivel - erro_nivel_anterior)


###########################
# Inicializando o logging #
###########################

# SILENCIANDO O LOOGER ROOT
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.CRITICAL)

# Inicializando o logger principal
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("MOA.log")
ch = logging.StreamHandler(stdout)
mh = MensageiroHandler()
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logFormatterSimples = logging.Formatter("[%(levelname)-5.5s]  %(message)s")
fh.setFormatter(logFormatter)
ch.setFormatter(logFormatter)
mh.setFormatter(logFormatterSimples)
fh.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)
mh.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(mh)

#######################
# Inicializando o MOA #
#######################

logger.info('Inicializando o MOA')
# A escala de tempo é utilizada para acelerar as simulações do sistema
# Utilizar 10x para testes sérios e 120x no máximo para testes simples
ESCALA_DE_TEMPO = 60

##############################
# INICIALIZAÇÃO DE VARIAVEIS #
##############################
try:

    u = usina.Usina()
    flags = 0
    Kp = 0
    Ki = 0
    Kd = 0
    Kie = 0
    saida_ie = u.valor_ie_inicial
    saida_pid = 0
    pot_alvo = 0
    controle_p = 0
    controle_i = 0
    controle_d = 0
    erro_nv = 0
    em_emergencia = False
    emergencias_removidas = True
    modo_autonomo_sinalizado = False
    ###########################
    # ANTES DOS CICLOS DO MOA #
    ###########################

    # Inicializando Servidor Modbus (para algumas comunicações com o Elipse)
    logger.debug("Iniciando Servidor/Slave Modbus MOA.")
    modbus_server = ModbusServer(host=u.modbus_server_ip, port=u.modbus_server_porta, no_block=True)
    tentativa = 1
    while not modbus_server.is_run:
        try:
            tentativa += 1
            modbus_server.start()
            DataBank.set_words(0, [0] * 0x10000)
            logger.info("Servidor/Slave Modbus MOA Iniciado com sucesso. Endereço: {:}:{:}.".format(u.modbus_server_ip, u.modbus_server_porta))
        except Exception as e:
            if tentativa < 5:
                logger.error("Erro ao iniciar Modbus MOA: '{:}'. Tentando novamente em 10s. (tentativa {}/5).".format(e, tentativa))
            else:
                logger.error("Tentativas exedidas ao iniciar Modbbus MOA. {}".format(e))
                raise e

except Exception as e:
    logger.error("{}".format(e))
    logger.debug("{}".format(traceback.format_exc()))
    logger.critical("Erro na inicialização do MOA. Finalizando o processo.")
    sys.exit(-1)


logger.info("Executando o MOA.")

# Espera conexão com o CLP
while True:

    logger.debug("Iniciando conexão com a CLP.")
    try:
        u.ler_valores()
        if u.clp_online:
            logger.debug("Conexão com a CLP ok.")
            break

    except Exception as e:
        logger.debug("{}".format(traceback.format_exc()))
        logger.error("Falha na conexão com a CLP. {}. Tentando novamente em {}s.".format(e, u.timer_erro))
        sleep(u.timer_erro)
        continue

# inicializção de vetores
nv_montante_recentes = [u.nv_montante] * u.n_movel_R
nv_montante_anteriores = [u.nv_montante] * u.n_movel_L
nv_montante_recente = sum(nv_montante_recentes) / len(nv_montante_recentes)

# DEBBUG
logger.debug("Tempo simulado; Nível montante;Nível médio;Potência alvo;Leitura UG1;Leitura UG2; AfluenteSIMUL")

while True:

    ##########################
    # INÍCIO DO CICLO DO MOA #
    ##########################
    try:
        ########################
        # ATUALIZAÇÃO DAS VARS #
        ########################

        u.verificar_agendamentos()
        u.ler_valores()

        # Atualiza níveis de referência
        nv_montante_recentes.append(u.nv_montante)
        nv_montante_recentes = nv_montante_recentes[1:]
        nv_montante_recente = sum(nv_montante_recentes) / u.n_movel_R
        nv_montante_anteriores.append(u.nv_montante)
        nv_montante_anteriores = nv_montante_anteriores[1:]
        nv_montante_anterior = sum(nv_montante_anteriores) / u.n_movel_L

        # Atualiza ganhos PID
        Kp = u.kp
        Ki = u.ki
        Kd = u.kd
        Kie = u.kie
        erro_nv = u.nv_alvo - nv_montante_recente
        erro_nv_anterior = u.nv_alvo - nv_montante_anterior

        # Verifica se está em emergência
        if u.emergencia_acionada and (not em_emergencia):
            em_emergencia = True
            u.acionar_emergerncia_clp()
            emergencias_removidas = False
            u.status_moa = 1001
            logger.warning("A emergência foi acionada! Status MOA: {}".format(u.status_moa))
        if (not u.emergencia_acionada) and em_emergencia:
            em_emergencia = False
            logger.warning("A emergência foi removida! Status MOA: {}".format(u.status_moa))

        if not em_emergencia:
            if not emergencias_removidas:
                logger.info("Removendo emegências.")
                u.normalizar_emergencia_clp()
                emergencias_removidas = True

            if u.modo_autonomo:
                u.status_moa = 5
                if not modo_autonomo_sinalizado:
                    logger.info("Modo autonomo ativado.")
                    modo_autonomo_sinalizado = True

                ###############################################
                # VERIFICA CONDIÇÕES E EXECUTA COMPORTAMENTOS #
                ###############################################

                # Acertar as comportas
                u.comporta.atualizar_estado(nv_montante_recente)

                # Se passar do nv de espera, turbinar!
                if u.nv_montante > u.nv_religamento:
                    if u.aguardando_reservatorio:
                        logger.info("O nv_montante ({:03.2f}) está acima do limite de religamento.".format(u.nv_montante))
                    u.aguardando_reservatorio = False

                # Se estiver sem água no reservatorio, travar até o nv_montante subir
                if u.nv_montante <= u.nv_minimo:
                    if not u.aguardando_reservatorio:
                        logger.warning("O nv_montante ({:03.2f}) está abaixo do limite inferior.".format(u.nv_montante))
                    u.aguardando_reservatorio = True
                    pot_alvo = 0

                # Se não estiver aguardando acompanhar/deplecionar reservatório
                if not u.aguardando_reservatorio:

                    # Se estiver vertendo
                    if nv_montante_recente >= u.nv_maximo:
                        pot_alvo = u.pot_maxima

                    # Se não estiver vertendo
                    else:

                        # Calcula o PID
                        controle_p = controle_proporcional(erro_nv)
                        controle_i = controle_integral(erro_nv, controle_i)
                        controle_d = controle_derivativo(erro_nv, erro_nv_anterior)

                        """
                        # Verifica/calcula o PID na região alternativa de 1cm prox ao erro
                        if 0.01 < abs(erro_nv) <= 0.025:
                            controle_p = controle_p*0.75
                        if abs(erro_nv) <= 0.01:
                            controle_p = controle_p*0.5
                            controle_d = controle_d*0.01
                        """

                        saida_pid = controle_p + controle_i + controle_d
                        # Calcula o integrador de estabilidade e limita
                        saida_ie = saida_pid * (Kie / ESCALA_DE_TEMPO) + saida_ie

                        """
                        if u.ug1.sincronizada and u.ug2.sincronizada:
                            saida_ie = max(min(saida_ie, 1), 0)
                        else:
                            saida_ie = max(min(saida_ie, (u.pot_maxima_ug+(1.1*u.margem_pot_critica))/u.pot_maxima),
                                           0)
                        """

                        # Calcula a pot alvo e limita
                        pot_alvo = round(u.pot_maxima * saida_ie, 2)
                        pot_alvo = max(min(pot_alvo, u.pot_maxima), u.pot_minima)

                    # Distribui a potência para as UGs
                    logger.debug("Pot Alvo: {:2.3f} (PID: {:2.3f} {:2.3f}+{:2.3f}+{:2.3f}; Int: {:2.3f})".format(
                        pot_alvo, saida_pid, controle_p, controle_i, controle_d, saida_ie))

                else:
                    logger.debug("Aguardando reservatório.".format(u.nv_montante))
                    pot_alvo = 0

                ##################
                # Distribuir POT #
                ##################

                if u.pot_medidor > u.pot_maxima_alvo and pot_alvo > (u.pot_maxima_alvo*0.95):
                    pot_alvo = pot_alvo * 0.99 * ( u.pot_maxima_alvo / u.pot_medidor )

                if pot_alvo < u.pot_minima:
                    pot_alvo = 0
                    u.ug1.mudar_setpoint(0)
                    u.ug2.mudar_setpoint(0)
                else:
                    pot_alvo = min(pot_alvo, u.pot_disp)
                    if u.ug1.sincronizada and u.ug2.sincronizada and pot_alvo > (2 * u.pot_minima):
                        u.ug1.mudar_setpoint(pot_alvo / 2)
                        u.ug2.mudar_setpoint(pot_alvo / 2)
                    elif (pot_alvo > (u.pot_maxima_ug + u.margem_pot_critica)) and (abs(erro_nv) > 0.05) \
                            and u.ug1.disponivel and u.ug2.disponivel:
                        u.ug1.mudar_setpoint(pot_alvo / 2)
                        u.ug2.mudar_setpoint(pot_alvo / 2)
                    else:
                        pot_alvo = min(pot_alvo, u.pot_maxima_ug)
                        ugs = u.lista_de_ugs_disponiveis()
                        if len(ugs) > 0:
                            ugs[0].mudar_setpoint(pot_alvo)
                            for ug in ugs[1:]:
                                ug.mudar_setpoint(0)
                        else:
                            for ug in ugs:
                                ug.mudar_setpoint(0)

                # DEBBUG!
                # EXCEL
                # logger.debug(("{:03.4f};{:03.4f};{:03.4f};{:03.4f};{:03.4f}"
                # .format(nv_montante, nv_montante_recente, pot_alvo, pot_ug1, pot_ug2)).replace(".", ","))

                logger.debug("T{:} Alv:{:3.2f}m Monte:{:3.2f}m Alvo:{:1.3f}MW Pot:{:1.3f}MW SP1:{:1.3f}MW SP2:{:1.3f}MW"
                             .format(datetime.now(), u.nv_alvo, u.nv_montante, pot_alvo, u.ug1.potencia+u.ug2.potencia,
                                     u.ug1.setpoint, u.ug2.setpoint))

                # Temporizador entre ciclos
                # Valor padrão é de 5 segundos, assim a média móvel rapda do nv_montante representa 1m (e a lenta 5m)
                sleep(5/ESCALA_DE_TEMPO)

            else:
                if modo_autonomo_sinalizado:
                    u.status_moa = 1
                    logger.info("Modo autonomo desativado.")
                    modo_autonomo_sinalizado = False
                # Todo o que fazer quando não está no autônomo ?

        # heartbeat da usina para o E3, ou equivalente...
        logger.debug("HB")
        u.escrever_valores()
        # FINAL DO CICLO

    ############################
    # TRATAMENTO DE EXCEPTIONS #
    ############################

    # Erro na conexão
    except ConnectionError as e:

        while not u.clp_online:
            logger.error("MOA perdeu a conexo com a usina. Tentando novamente em {}s".format(u.timer_erro))
            sleep(u.timer_erro)
            u.ler_valores()
        logger.info("Conexão com a CLP ok.")
        continue

    # Parada abrupta pelo teclado (ctrl-c ou equivalente)
    except KeyboardInterrupt as e:
        logger.info("MOA recebeu uma interrupção por teclado: '{}'.".format(e))
        sys.exit(0)

    # Exception padrão/sem descritivo
    except Exception as e:
        logger.critical("MOA experienciou uma Exception: '{}'.".format(e))
        raise e

logger.info("MOA finalizado.")
