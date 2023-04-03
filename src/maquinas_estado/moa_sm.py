__version__ = "0.2"
__author__ = "Diego Basgal"
__credits__ = ["Lucas Lavratti", " Henrique Pfeifer", ...]
__description__ = "Este módulo corresponde a implementação da máquina de estados do Módulo de Operação Autônoma."

from usina import *
from agendamentos import Agendamentos

class StateMachine:
    def __init__(self, initial_state):
        self.state = initial_state

    def exec(self):
        try:
            if self.state is None:
                raise TypeError
            self.state = self.state.run()

        except Exception as e:
            logger.exception(f"Estado ({self.state}) levantou uma exception: \"{repr(e)}\"")
            logger.exception(f"Traceback: {traceback.print_stack}")
            self.state = FalhaCritica()

class State:
    def __init__(self, usina: Usina | None = ...) -> ...:

        if not usina:
            logger.error(f"Erro ao carregar instância da Usina. Exception: \"{repr(Exception)}\"")
            self.state = FalhaCritica()
        else:
            self.usn = usina

        self.usn.estado_moa = MOA_SM_NAO_INICIALIZADO

    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def run(self) -> object:
        return self

class FalhaCritica(State):
    def __init__(self, usina):
        super().__init__(usina)
        self.usn.estado_moa = MOA_SM_FALHA_CRITICA

        logger.critical("Falha crítica MOA. Interrompendo execução...")
        sys.exit(1)

class Pronto(State):
    def __init__(self, usina):
        super().__init__(usina)
        self.usn.estado_moa = MOA_SM_PRONTO

    def run(self):
        self.usn.ler_valores()
        return ControleNormal() if self.usn.modo_autonomo else ControleManual()

class ControleNormal(State):
    def __init__(self, usina):
        super().__init__(usina)
        self.usn.estado_moa = MOA_SM_CONTROLE_NORMAL

        self.usn.clp["MOA"].write_single_coil(MB["MOA"]["PAINEL_LIDO"], [1])

    def run(self):
        self.usn.ler_valores()

        if not self.usn.modo_autonomo:
            logger.info("Comando acionado: Desabilitar modo autônomo.")
            return ControleManual()

        elif self.usn.clp_emergencia or self.usn.bd_emergencia:
            return ControleEmergencia()

        elif len(self.usn.agn.agendamentos_pendentes()) > 0:
            return ControleAgendamentos()

        else:
            condic_flag = self.usn.verificar_condicionadores()
            if condic_flag == CONDIC_INDISPONIBILIZAR:
                return ControleEmergencia()

            elif condic_flag == CONDIC_NORMALIZAR:
                if self.usn.normalizar_usina() == False:
                    return ControleEmergencia() if self.usn.se.aguardar_tensao() == False else ControleDados()
                else:
                    return ControleDados()

            else:
                return ControleReservatorio()

class ControleReservatorio(State):
    def __init__(self, usina):
        super().__init__(usina)
        self.usn.estado_moa = MOA_SM_CONTROLE_RESERVATORIO

    def run(self):
        self.usn.ler_valores()
        return ControleEmergencia() if self.usn.tda.controle_reservatorio() == NV_FLAG_EMERGENCIA else ControleDados()

class ControleDados(State):
    def __init__(self, usina):
        super().__init__(usina)
        self.usn.estado_moa = MOA_SM_CONTROLE_DADOS

    def run(self):
        self.usn.ler_valores()
        self.usn.escrever_valores()
        return ControleNormal()

class ControleAgendamentos(State):
    def __init__(self, usina):
        super().__init__(usina)
        self.usn.estado_moa = MOA_SM_CONTROLE_AGENDAMENTOS

    def run(self):
        Agendamentos.verificar_agendamentos()
        return ControleDados() if self.usn.modo_autonomo else ControleManual()

class ControleManual(State):
    def __init__(self, usina):
        super().__init__(usina)
        self.usn.estado_moa = MOA_SM_CONTROLE_MANUAL

        self.usn.modo_autonomo = False
        self.usn.clp["MOA"].write_single_coil(MB["MOA"]["PAINEL_LIDO"], [1])

        for ug in self.usn.ugs: ug.parar_timer = True

        logger.info("Usina em modo manual. Para retornar a operação autônoma, acionar via painel ou página WEB")

    def run(self):
        self.usn.ler_valores()
        for ug in self.usn.ugs:
            ug.setpoint = ug.leitura_potencia
        self.usn.ajustar_ie_padrao()

        if self.usn.modo_autonomo:
            logger.debug("Comando acionado: Habilitar modo autonomo.")
            self.usn.ler_valores()
            sleep(2)
            return ControleDados()

        return ControleAgendamentos() if len(self.usn.agn.agendamentos_pendentes()) > 0 else self

class ControleEmergencia(State):
    def __init__(self, usina):
        super().__init__(usina)
        self.usn.estado_moa = MOA_SM_CONTROLE_EMERGENCIA

        self.tentativas = 0
        self.usn.distribuir_potencia(0)
        [ug.step() for ug in self.usn.ugs]

        logger.critical(f"ATENÇÃO! Usina entrado em estado de emergência. (Horário: {self.get_time()})")

    def run(self):
        self.usn.ler_valores()

        if self.tentativas == 3:
            logger.warning("Tentativas de normalização excedidas, entrando em modo manual.")
            for ug in self.usn.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()
            return ControleManual()

        elif self.usn.bd_emergencia:
            logger.warning("Emergência acionada via página WEB, aguardando reset pela aba emergência.")
            while self.usn.bd_emergencia:
                self.usn.atualizar_parametros_db(BancoDados.get_parametros_usina())
                if not self.usn.bd_emergencia:
                    self.usn.bd_emergencia = False
                    return self
                if not self.usn.modo_autonomo:
                    self.usn.bd_emergencia = False
                    return ControleManual()

        else:
            flag = self.usn.verificar_condicionadores()
            if flag == CONDIC_INDISPONIBILIZAR:
                logger.critical("Acionando VOIP e entrando em modo manual")
                return ControleManual()

            elif flag == CONDIC_NORMALIZAR:
                self.tentativas += 1
                logger.info(f"Normalizando usina. (Tentativa {self.tentativas}/3) (Limite entre tentaivas: {TIMEOUT_NORMALIZACAO}s)")
                self.usn.normalizar_forcado = True
                self.usn.normalizar_usina()
                return self

            else:
                logger.debug("Usina normalizada. Retomando operação...")
                return ControleDados()