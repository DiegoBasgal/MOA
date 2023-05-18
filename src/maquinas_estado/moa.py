import os
import json

from src.usina import *
from src.dicionarios.const import *
from src.usina import Usina

logger = logging.getLogger("__main__")

class StateMachine:
    def __init__(self, initial_state):
        self.state = initial_state
        self.em_falha_critica = False

    def exec(self):
        try:
            if self.state is None:
                raise TypeError
            self.state = self.state.run()

        except Exception as e:
            logger.warning(f"Estado ({self.state}) levantou uma exception: \"{repr(e)}\"")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            self.em_falha_critica = True
            self.state = FalhaCritica()

class State:
    def __init__(self, usina: Usina, *args, **kwargs):
        if not usina:
            raise ValueError("Erro ao carregar classe Usina na máquina de estados.")
        else:
            self.usn = usina

        self.args = args
        self.kwargs = kwargs

    def run(self) -> object:
        return self


class FalhaCritica(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logger.critical("Falha crítica MOA. Exiting...")
        sys.exit(1)


class Pronto(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)

        self.usn._state_moa = MOA_SM_PRONTO

        self.n_tentativa = 0

    def run(self):
        self.usn.heartbeat()
        if self.n_tentativa >= 2:
            return FalhaCritica()
        else:
            try:
                self.usn.ler_valores()
                return ControleTDAOffline(self.usn) if self.usn.TDA_Offline else ControleEstados(self.usn)

            except Exception:
                self.n_tentativa += 1
                logger.error(f"Erro durante a comunicação do MOA com a usina. Tentando novamente em {TIMEOUT_PADRAO * self.n_tentativa}s (tentativa{self.n_tentativa}/3)")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                sleep(TIMEOUT_PADRAO * self.n_tentativa)
                return self


class ControleEstados(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)

        self.usn._state_moa = MOA_SM_CONTROLE_ESTADOS

        self.usn.clp["MOA"].write_single_coil(REG['PAINEL_LIDO'], [1])

    def run(self):
        self.usn.ler_valores()

        if not self.usn.modo_autonomo:
            logger.info("Comando acionado: \"Desabilitar Modo Autônomo\"")
            return ModoManual(self.usn)

        elif self.usn.clp_emergencia_acionada or self.usn.db_emergencia_acionada:
            return Emergencia(self.usn)

        elif len(self.usn.agn.obter_agendamentos()) > 0:
            return ControleAgendamentos(self.usn)

        else:
            condic_flag = self.usn.verificar_condicionadores()
            if condic_flag == DEVE_INDISPONIBILIZAR:
                return Emergencia(self.usn)

            elif condic_flag == DEVE_NORMALIZAR:
                if self.usn.normalizar_emergencia() == False:
                    return Emergencia(self.usn) if self.usn.aguardar_tensao() == False else ControleDados(self.usn)
                else:
                    return ControleDados(self.usn)

            else:
                return ControleReservatorio(self.usn)

class ControleReservatorio(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)

        self.usn._state_moa = MOA_SM_CONTROLE_RESERVATORIO

    def run(self):
        self.usn.ler_valores()
        return Emergencia(self.usn) if self.usn.controle_reservatorio() == NV_FLAG_EMERGENCIA else ControleDados(self.usn)

class ControleDados(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)

        self.usn._state_moa = MOA_SM_CONTROLE_DADOS

    def run(self):
        logger.debug("Escrevendo valores no Banco")

        self.usn.ler_valores()
        self.usn.escrever_valores()

        with open(os.path.join(os.path.dirname('/opt/operacao-autonoma/src/dicionarios/'), "cfg.json"), "w") as file:
            json.dump(self.usn.cfg, file, indent=4)

        return ControleEstados(self.usn)

class ControleAgendamentos(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)

        self.usn._state_moa = MOA_SM_CONTROLE_AGENDAMENTOS

        logger.debug("Tratando agendamentos")

    def run(self):
        self.usn.agn.verificar_agendamentos()
        return ControleDados(self.usn) if self.usn.modo_autonomo else ModoManual(self.usn)

class ControleTDAOffline(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)

        self.usn._state_moa = MOA_SM_CONTROLE_TDA_OFFLINE

        self.usn.TDA_Offline = True

    def run(self):
        self.usn.heartbeat()

        if not self.usn.modo_autonomo:
            logger.info("Comando acionado: Desabilitar modo autônomo.")
            return ModoManual(self.usn)

        elif self.usn.clp_emergencia_acionada or self.usn.db_emergencia_acionada:
            return Emergencia(self.usn)

        elif len(self.usn.agn.obter_agendamentos()) > 0:
            return ControleAgendamentos(self.usn)

        else:
            condic_flag = self.usn.verificar_condicionadores()
            if condic_flag == DEVE_INDISPONIBILIZAR:
                return Emergencia(self.usn)

            elif condic_flag == DEVE_NORMALIZAR:
                if self.usn.normalizar_emergencia() == False:
                    return Emergencia(self.usn) if self.usn.aguardar_tensao() == False else ControleDados(self.usn)
                else:
                    for ug in self.usn.ugs:
                        ug.controle_cx_espiral()
                        ug.step()

                    return ControleDados(self.usn)


class ModoManual(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn._state_moa = MOA_SM_MODO_MANUAL

        self.usn.modo_autonomo = False

        self.usn.escrever_valores()
        logger.info("Usina em modo manual, deve-se alterar via painel ou interface web.")

    def run(self):
        self.usn.ler_valores()

        for ug in self.usn.ugs:
            ug.release = True
            ug.setpoint = ug.leitura_potencia.valor

        self.usn.controle_ie = (self.usn.ug1.setpoint + self.usn.ug2.setpoint + self.usn.ug3.setpoint) / self.usn.cfg["pot_maxima_alvo"]
        self.usn.controle_i = max(min(self.usn.controle_ie - (self.usn.controle_i * self.usn.cfg["ki"]) - self.usn.cfg["kp"] * self.usn.erro_nv - self.usn.cfg["kd"] * (self.usn.erro_nv - self.usn.erro_nv_anterior), 0.8), 0)

        self.usn.escrever_valores()

        if self.usn.modo_autonomo:
            logger.debug("Comando recebido: \"Habilitar modo autônomo\"")
            self.usn.ler_valores()
            sleep(2)
            return ControleDados(self.usn)

        return ControleAgendamentos(self.usn) if len(self.usn.agn.obter_agendamentos()) > 0 else self

class Emergencia(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn._state_moa = MOA_SM_EMERGENCIA

        self.tentativas = 0
        self.nao_ligou = True
        self.em_sm_acionada = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

        logger.warning(f"Usina entrado em estado de emergência (Timestamp: {self.em_sm_acionada})")

    def run(self):
        self.usn.ler_valores()

        if self.tentativas == 3:
            logger.warning("Tentativas de normalização excedidas, entrando em modo manual.")
            for ug in self.usn.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()
            return ModoManual(self.usn)

        elif self.usn.db_emergencia_acionada:
            logger.warning("Emergência acionada via página WEB, aguardando reset pela aba emergência.")
            while self.usn.db_emergencia_acionada:
                self.usn.ler_valores()
                if not self.usn.db_emergencia_acionada:
                    self.usn.db_emergencia_acionada= False
                    return self
                if not self.usn.modo_autonomo:
                    self.usn.db_emergencia_acionada = False
                    return ModoManual(self.usn)

        else:
            flag = self.usn.verificar_condicionadores()
            if flag == DEVE_INDISPONIBILIZAR:
                logger.critical("Acionando VOIP e entrando em modo manual")
                return ModoManual(self.usn)

            elif flag == DEVE_NORMALIZAR:
                self.tentativas += 1
                logger.info(f"Normalizando usina. (Tentativa {self.tentativas}/3) (Limite entre tentaivas: {TIMEOUT_NORMALIZACAO}s)")
                self.usn.normalizar_forcado = True
                self.usn.normalizar_emergencia()
                return self

            else:
                logger.debug("Usina normalizada. Retomando operação...")
                return ControleDados(self.usn)