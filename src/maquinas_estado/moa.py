import sys
import pytz
import traceback

from time import sleep
from datetime import datetime

from src.usina import *
from src.agendamentos import *
from src.dicionarios.reg import *
from src.dicionarios.const import *

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
    def __init__(self, usina: Usina=None, *args, **kwargs):
        if usina is None:
            logger.error(f"Erro ao carregar a classe da Usina na máquina de estados.")
            return FalhaCritica()
        else:
            self.usn = usina

        self.args = args
        self.kwargs = kwargs

        self.usn.estado_moa = MOA_SM_NAO_INICIALIZADO

    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def run(self) -> object:
        return self

class FalhaCritica(State):
    def __init__(self):

        logger.critical("Falha crítica MOA. Interrompendo execução...")
        sys.exit(1)

class Pronto(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        self.usn.estado_moa = MOA_SM_PRONTO

    def run(self):
        self.usn.ler_valores()
        return ControleEstados(self.usn)

class ControleEstados(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        self.usn.estado_moa = MOA_SM_CONTROLE_ESTADOS

        # self.usn.clp["MOA"].write_single_coil(REG_MOA["PAINEL_LIDO"], [1])

    def run(self):
        self.usn.ler_valores()

        if not self.usn.modo_autonomo:
            logger.info("Comando acionado: \"Desabilitar Modo Autônomo\"")
            return ModoManual(self.usn)

        elif self.usn.clp_emergencia or self.usn.db_emergencia:
            return Emergencia(self.usn)

        elif len(Agendamentos.verificar_agendamentos_pendentes()) > 0:
            return ControleAgendamentos(self.usn)

        else:
            flag = self.usn.oco.verificar_condicionadores()
            if flag == CONDIC_INDISPONIBILIZAR:
                return Emergencia(self.usn)

            elif flag == CONDIC_NORMALIZAR:
                if self.usn.normalizar_usina() == False:
                    return Emergencia(self.usn) if self.usn.aguardar_tensao() == False else ControleDados(self.usn)
                else:
                    return ControleDados(self.usn)

            else:
                return ControleReservatorio(self.usn)

class ControleReservatorio(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        self.usn.estado_moa = MOA_SM_CONTROLE_RESERVATORIO

    def run(self):
        self.usn.ler_valores()
        flag = self.usn.controlar_reservatorio()

        return Emergencia(self.usn) if flag == NV_FLAG_EMERGENCIA else ControleDados(self.usn)

class ControleDados(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        self.usn.estado_moa = MOA_SM_CONTROLE_DADOS

    def run(self):
        logger.debug("Escrevendo valores no Banco")
        self.usn.ler_valores()
        self.usn.escrever_valores()
        return ControleEstados(self.usn)

class ControleAgendamentos(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usn.estado_moa = MOA_SM_CONTROLE_AGENDAMENTOS
        logger.info("Tratando agendamentos")

    def run(self):
        Agendamentos.verificar_agendamentos_pendentes()
        return ControleDados(self.usn) if self.usn.modo_autonomo else ModoManual(self.usn)

class ModoManual(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        self.usn.estado_moa = MOA_SM_MODO_MANUAL
        logger.info("Usina em modo manual. Para retornar a operação autônoma, acionar via painel ou página WEB")

        self.usn.modo_autonomo = False
        # self.usn.clp["MOA"].write_single_coil(REG_MOA["PAINEL_LIDO"], [1])

    def run(self):
        self.usn.ler_valores()
        for ug in self.usn.ugs:
            ug.setpoint = ug.leitura_potencia

        self.usn.controle_ie = sum(ug.leitura_potencia for ug in self.usn.ugs) / self.usn.cfg["pot_maxima_alvo"]

        if self.usn.modo_autonomo:
            logger.debug("Comando acionado: \"Habilitar modo autônomo\".")
            self.usn.ler_valores()
            sleep(2)
            return ControleDados(self.usn)

        return ControleAgendamentos(self.usn) if len(Agendamentos.verificar_agendamentos_pendentes()) > 0 else self

class Emergencia(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        self.usn.estado_moa = MOA_SM_EMERGENCIA
        logger.critical(f"ATENÇÃO! Usina entrado em estado de emergência. (Horário: {self.get_time()})")

        self.tentativas = 0

    def run(self):
        self.usn.ler_valores()

        if self.tentativas == 3:
            logger.warning("Tentativas de normalização excedidas, entrando em modo manual.")

            for ug in self.usn.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()

            return ModoManual(self.usn)

        elif self.usn.db_emergencia:
            logger.warning("Comando acionado via página WEB, aguardando reset pela aba \"Emergência\".")

            while self.usn.db_emergencia:
                self.usn.atualizar_valores_banco(self.usn.db.get_parametros_usina())

                if not self.usn.db_emergencia:
                    self.usn.db_emergencia = False
                    return self

                if not self.usn.modo_autonomo:
                    self.usn.db_emergencia = False
                    return ModoManual(self.usn)

        else:
            flag = self.usn.oco.verificar_condicionadores()

            if flag == CONDIC_INDISPONIBILIZAR:
                logger.critical("Acionando VOIP e entrando em modo manual")
                return ModoManual(self.usn)

            elif flag == CONDIC_NORMALIZAR:
                self.tentativas += 1
                logger.info(f"Normalizando usina. (Tentativa {self.tentativas}/3) (Limite entre tentativas: {TIMEOUT_NORMALIZACAO}s)")
                self.usn.normalizar_forcado = True
                self.usn.normalizar_usina()
                return self

            else:
                logger.debug("Usina normalizada. Retomando operação...")
                return ControleDados(self.usn)