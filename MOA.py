import logging
from datetime import datetime
from pyModbusTCP.server import DataBank, ModbusServer
from sys import stdout
from time import sleep


# Meus imports
import mensageiro as msg
import usina


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
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# LOG to file
fileHandler = logging.FileHandler("MOA.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
# LOG to console
consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

#######################
# Inicializando o MOA #
#######################

logger.info('Inicializando o MOA')
msg.enviar_whatsapp("Inicializando MOA")
# A escala de tempo é utilizada para acelerar as simulações do sistema
# Utilizar 10x para testes sérios e 120x no máximo para testes simples
ESCALA_DE_TEMPO = 60

##############################
# INICIALIZAÇÃO DE VARIAVEIS #
##############################
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
aviso = "Iniciando Servidor/Slave Modbus MOA."
logger.info(aviso)
msg.enviar_whatsapp(aviso)
modbus_server = ModbusServer(host=u.modbus_server_ip, port=u.modbus_server_porta, no_block=True)
while not modbus_server.is_run:
    try:
        modbus_server.start()
        DataBank.set_words(0, [0] * 0x10000)
        aviso = "Servidor/Slave Modbus MOA Iniciado com sucesso. Endereço: {:}:{:}.".format(u.modbus_server_ip,
                                                                                            u.modbus_server_porta)
        logger.info(aviso)
        msg.enviar_whatsapp(aviso)
    except Exception as e:
        aviso = "Erro ao iniciar Modbus MOA: '{:}'. Tentando novamente em 5s.".format(e)
        logger.error(aviso)
        msg.enviar_whatsapp(aviso)
        sleep(5)
        continue


aviso = "Executando o MOA."
logger.info(aviso)
msg.enviar_whatsapp(aviso)

# Espera conexão com o CLP
while True:
    aviso = "Iniciando conexão com a CLP."
    logger.info(aviso)
    msg.enviar_whatsapp(aviso)
    try:
        u.ler_valores()
        if u.clp_online:
            aviso = "Conexão com a CLP ok."
            logger.info(aviso)
            msg.enviar_whatsapp(aviso)
            break
        else:
            aviso = "Não conectou, tentando novamente em {}s.".format(u.timer_erro)
            logger.info(aviso)
            msg.enviar_whatsapp(aviso)
            sleep(u.timer_erro)
    except Exception as e:
        aviso = "MOA Não conectou a CLP! '{}'. Tentando novamente em {}s.".format(e, u.timer_erro)
        logger.error(aviso)
        msg.enviar_whatsapp(aviso)
        sleep(u.timer_erro)


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
            aviso = "A emergência foi acionada! Status MOA: {}".format(u.status_moa)
            logger.warning(aviso)
            msg.enviar_whatsapp(aviso)
            msg.enviar_voz_teste()
        if (not u.emergencia_acionada) and em_emergencia:
            em_emergencia = False
            aviso = "A emergência foi removida! Status MOA: {}".format(u.status_moa)
            logger.warning(aviso)
            msg.enviar_whatsapp(aviso)

        if not em_emergencia:
            if not emergencias_removidas:
                aviso = "Removendo emegências."
                logger.info(aviso)
                msg.enviar_whatsapp(aviso)
                u.normalizar_emergencia_clp()
                emergencias_removidas = True

            if u.modo_autonomo:
                u.status_moa = 5
                if not modo_autonomo_sinalizado:
                    aviso = "Modo autonomo ativado."
                    logger.info(aviso)
                    msg.enviar_whatsapp(aviso)
                    modo_autonomo_sinalizado = True

                ###############################################
                # VERIFICA CONDIÇÕES E EXECUTA COMPORTAMENTOS #
                ###############################################
                # Se passar do nv de espera, turbinar!
                if u.nv_montante > u.nv_religamento:
                    if u.aguardando_reservatorio:
                        aviso = "O nv_montante ({:03.2f}) está acima do limite de religamento.".format(u.nv_montante)
                        logger.info(aviso)
                        msg.enviar_whatsapp(aviso)
                    u.aguardando_reservatorio = False

                # Se estiver sem água no reservatorio, travar até o nv_montante subir
                if u.nv_montante <= u.nv_minimo:
                    if not u.aguardando_reservatorio:
                        aviso = "O nv_montante ({:03.2f}) está abaixo do limite inferior.".format(u.nv_montante)
                        logger.warning(aviso)
                        msg.enviar_whatsapp(aviso)
                    u.aguardando_reservatorio = True
                    pot_alvo = 0

                # Se não estiver aguardando acompanhar/deplecionar reservatório
                if not u.aguardando_reservatorio:

                    # Se estiver vertendo
                    if nv_montante_recente >= u.nv_maximo:
                        pot_alvo = u.pot_nominal

                    # Se não estiver vertendo
                    else:

                        # Calcula o PID
                        controle_p = controle_proporcional(erro_nv)
                        controle_i = controle_integral(erro_nv, controle_i)
                        controle_d = controle_derivativo(erro_nv, erro_nv_anterior)

                        # Verifica/calcula o PID na região alternativa de 1cm prox ao erro
                        if 0.01 < abs(erro_nv) <= 0.025:
                            controle_p = controle_p*0.75
                        if abs(erro_nv) <= 0.01:
                            controle_p = controle_p*0.5
                            controle_d = controle_d*0.01
                        saida_pid = controle_p + controle_i + controle_d

                        # Calcula o integrador de estabilidade e limita
                        saida_ie = saida_pid * (Kie / ESCALA_DE_TEMPO) + saida_ie
                        if u.ug1.sincronizada and u.ug2.sincronizada:
                            saida_ie = max(min(saida_ie, 1), 0)
                        else:
                            saida_ie = max(min(saida_ie, (u.pot_nominal_ug+(1.1*u.margem_pot_critica))/u.pot_nominal),
                                           0)

                        # Calcula a pot alvo e limita
                        pot_alvo = round(u.pot_nominal * saida_ie, 2)
                        pot_alvo = max(min(pot_alvo, u.pot_nominal), u.pot_minima)

                    # Distribui a potência para as UGs
                    logger.debug("Pot Alvo: {:2.3f} (PID: {:2.3f} {:2.3f}+{:2.3f}+{:2.3f}; Int: {:2.3f})".format(
                        pot_alvo, saida_pid, controle_p, controle_i, controle_d, saida_ie))

                else:
                    logger.debug("Aguardando reservatório.".format(u.nv_montante))
                    pot_alvo = 0

                ##################
                # Distribuir POT #
                ##################

                if pot_alvo < u.pot_minima:
                    pot_alvo = 0
                    u.ug1.setpoint = 0
                    u.ug2.setpoint = 0
                else:
                    pot_alvo = min(pot_alvo, u.pot_disp)

                    if u.ug1.sincronizada and u.ug2.sincronizada and pot_alvo > (2 * u.pot_minima):
                        if pot_alvo > ((2 * u.pot_minima) + u.margem_pot_critica):
                            u.ug1.setpoint = pot_alvo / 2
                            u.ug2.setpoint = pot_alvo / 2
                    elif (pot_alvo > (u.pot_nominal_ug + u.margem_pot_critica)) and (abs(erro_nv) > 0.05) \
                            and u.ug1.disponivel and u.ug2.disponivel:
                        u.ug1.setpoint = pot_alvo / 2
                        u.ug2.setpoint = pot_alvo / 2
                    else:
                        pot_alvo = min(pot_alvo, u.pot_nominal_ug)
                        ugs = u.lista_de_ugs_disponiveis()
                        if len(ugs) > 0:
                            ugs[0].setpoint = pot_alvo
                            for ug in ugs[1:]:
                                ug.setpoint = 0
                        else:
                            for ug in ugs:
                                ug.setpoint = 0

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
                    aviso = "Modo autonomo desativado."
                    logger.info(aviso)
                    msg.enviar_whatsapp(aviso)
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
            aviso = "MOA perdeu a conexo com a usina. Tentando novamente em {}s".format(u.timer_erro)
            logger.error(aviso)
            msg.enviar_whatsapp(aviso)
            sleep(u.timer_erro)
            u.ler_valores()
        aviso = "Conexão com a CLP ok."
        logger.info(aviso)
        msg.enviar_whatsapp(aviso)
        continue

    # Parada abrupta pelo teclado (ctrl-c ou equivalente)
    except KeyboardInterrupt as e:
        aviso = "MOA recebeu uma interrupção por teclado: '{}'.".format(e)
        logger.info(aviso)
        msg.enviar_whatsapp(aviso)
        break

    # Exception padrão/sem descritivo
    except Exception as e:
        aviso = "MOA experienciou uma Exception: '{}'.".format(e)
        logger.error(aviso)
        msg.enviar_whatsapp(aviso)
        raise e


aviso = "MOA finalizado."
logger.info(aviso)
msg.enviar_whatsapp(aviso)
