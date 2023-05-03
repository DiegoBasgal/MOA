import os
import json

from src.codes import *
from src.abstracao_usina import *

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
            logger.debug(f"Traceback: {traceback.print_stack}")
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
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        logger.critical("Falha crítica MOA. Exiting...")
        self.usn._state_moa = SM_CRITICAL_FAILURE
        sys.exit(1)


class Pronto(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.n_tentativa = 0
        self.usn._state_moa = SM_READY

    def run(self):
        self.usn._state_moa = SM_READY
        self.usn.heartbeat()
        if self.n_tentativa >= 2:
            return FalhaCritica()
        else:
            try:
                self.usn.ler_valores()
                return OperacaoTDAOffline(self.usn) if self.usn.TDA_Offline else ValoresInternosAtualizados(self.usn)

            except Exception as e:
                self.n_tentativa += 1
                logger.error(f"Erro durante a comunicação do MOA com a usina. Tentando novamente em {self.usn.cfg['timeout_padrao'] * self.n_tentativa}s (tentativa{self.n_tentativa}/3). \
                            Exception: \"{repr(e)}\".")
                logger.debug(f"Traceback: {traceback.print_stack}")
                sleep(self.usn.cfg["timeout_padrao"] * self.n_tentativa)
                return self


class ValoresInternosAtualizados(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.deve_ler_condicionadores=False
        self.habilitar_emerg_condic_e=False
        self.habilitar_emerg_condic_c=False
        self.usn._state_moa = SM_INTERNAL_VALUES_UPDATED

    def run(self):
        self.usn._state_moa = SM_INTERNAL_VALUES_UPDATED

        global aux
        global deve_normalizar

        self.usn.heartbeat()
        self.usn.ler_valores()
        self.usn.clp["MOA"].write_single_coil(self.usn.cfg['REG_PAINEL_LIDO'], [1])

        self.usn.TDA_Offline = False

        with open(os.path.join(os.path.dirname('/opt/operacao-autonoma/'), "config.json"), "w") as file:
            json.dump(self.usn.cfg, file, indent=4)

        for condicionador_essencial in self.usn.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.deve_ler_condicionadores=True

        if self.usn.avisado_em_eletrica or self.deve_ler_condicionadores==True:
            for condicionador_essencial in self.usn.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade >= DEVE_INDISPONIBILIZAR:
                    self.habilitar_emerg_condic_e=True
                elif condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_NORMALIZAR:
                    deve_normalizar=True
                    self.habilitar_emerg_condic_e=False
                else:
                    deve_normalizar=False
                    self.habilitar_emerg_condic_e=False

            for condicionador in self.usn.condicionadores:
                if condicionador.ativo and condicionador.gravidade >= DEVE_INDISPONIBILIZAR:
                    self.habilitar_emerg_condic_c=True
                elif condicionador.ativo and condicionador.gravidade == DEVE_NORMALIZAR:
                    self.habilitar_emerg_condic_c=False
                    deve_normalizar=True
                else:
                    deve_normalizar=False
                    self.habilitar_emerg_condic_c=False

            if self.habilitar_emerg_condic_e or self.habilitar_emerg_condic_c:
                logger.warning("Foram detectados Condicionadores ativos com gravidade: \"Indisponibilizar\"!")
                return Emergencia(self.usn)

        if deve_normalizar:
            if (not self.usn.normalizar_emergencia()) and self.usn.tensao_ok==False and aux==0:
                logger.warning("Tensão da linha fora do limite")
                aux = 1
                threading.Thread(target=lambda: self.usn.aguardar_tensao(600)).start()

            elif self.usn.timer_tensao:
                aux = 0
                deve_normalizar = None
                self.usn.timer_tensao = None

            elif self.usn.timer_tensao==False:
                aux = 0
                deve_normalizar = None
                self.usn.timer_tensao = None
                logger.critical("O tempo de normalização da linha excedeu o limite! (10 min)")
                return Emergencia(self.usn)

        if self.usn.clp_emergencia_acionada or self.usn.db_emergencia_acionada:
            logger.warning("Comando recebido: habilitando modo de emergencia.")
            sleep(2)
            return Emergencia(self.usn)

        if len(self.usn.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usn)

        if not self.usn.modo_autonomo:
            logger.debug("Comando recebido: \"Desabilitar modo autônomo\"")
            sleep(2)
            return ModoManualAtivado(self.usn)

        if self.usn.aguardando_reservatorio:
            if self.usn.nv_montante > self.usn.cfg["nv_alvo"]:
                logger.debug("Reservatorio dentro do nivel de trabalho")
                self.usn.aguardando_reservatorio = 0
                return ReservatorioNormal(self.usn)

        if self.usn.nv_montante < self.usn.cfg["nv_minimo"]:
            self.usn.aguardando_reservatorio = 1
            logger.info("Reservatorio abaixo do nivel de trabalho")
            return ReservatorioAbaixoDoMinimo(self.usn)

        if self.usn.nv_montante >= self.usn.cfg["nv_maximo"]:
            return ReservatorioAcimaDoMaximo(self.usn)

        # Se estiver tudo ok:
        return ReservatorioNormal(self.usn)


class Emergencia(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.em_sm_acionada = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        logger.warning(f"Usina entrado em estado de emergência (Timestamp: {self.em_sm_acionada})")
        self.n_tentativa = 0
        self.nao_ligou = True
        self.usn.escrever_valores()
        self.usn._state_moa = SM_EMERGENCY

    def run(self):
        self.usn._state_moa = SM_EMERGENCY
        self.usn.heartbeat()
        self.n_tentativa += 1
        if self.n_tentativa > 2:
            logger.warning("Numero de tentaivas de normalização excedidas, entrando em modo manual.")
            for ug in self.usn.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()
            return ModoManualAtivado(self.usn)
        else:
            # TODO revisar lógica
            if self.usn.db_emergencia_acionada:
                logger.warning("Emergencia acionada via Interface WEB/DB, aguardando Reset/Reconhecimento pela interface ou CLP")
                while self.usn.db_emergencia_acionada:
                    self.usn.ler_valores()
                    if not self.usn.clp.em_emergencia():
                        self.usn.db.update_emergencia(0)
                        self.usn.db_emergencia_acionada = 0

            self.usn.ler_valores()
            deve_indisponibilizar = False
            deve_normalizar = False
            condicionadores_ativos = []

            for condicionador_essencial in self.usn.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    deve_indisponibilizar = True
                elif condicionador_essencial.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    deve_normalizar = True

            for condicionador in self.usn.condicionadores:
                if condicionador.ativo and condicionador.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador)
                    deve_indisponibilizar=True
                elif condicionador.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condicionador)
                    deve_indisponibilizar=False

            if (self.usn.clp_emergencia_acionada or deve_normalizar or deve_indisponibilizar):
                try:
                    if deve_indisponibilizar:
                        logger.critical(f"[USN] USN detectou condicionadores ativos, passando USINA para manual e ligando por VOIP.\nCondicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
                        return ModoManualAtivado(self.usn)

                    elif deve_normalizar:
                        logger.debug("Aguardando antes de tentar normalizar novamente (5s)")
                        sleep(5)
                        logger.info(f"Normalizando usina. (tentativa{self.n_tentativa}/2) (limite entre tentaivas: {self.usn.cfg['timeout_normalizacao']}s)")
                        self.usn.deve_normalizar_forcado=True
                        self.usn.normalizar_emergencia()
                        self.usn.ler_valores()
                        return self

                    else:
                        logger.debug("Nenhum condicionador relevante ativo...")
                        self.usn.ler_valores()
                        return ControleRealizado(self.usn)

                except Exception as e:
                    logger.error(f"Erro durante a comunicação do MOA com a usina. Exception: {repr(e)}.")
                    logger.debug(f"Traceback: {traceback.print_stack}")
                return self
            else:
                self.usn.ler_valores()
                logger.info("Usina normalizada")
                return ControleRealizado(self.usn)


class ModoManualAtivado(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn._state_moa = SM_MANUAL_MODE_ACTIVE
        self.usn.modo_autonomo = False
        self.usn.escrever_valores()
        logger.info("Usina em modo manual, deve-se alterar via painel ou interface web.")

    def run(self):
        self.usn._state_moa = SM_MANUAL_MODE_ACTIVE
        self.usn.heartbeat()
        self.usn.ler_valores()
        for ug in self.usn.ugs:
            ug.release_timer = True
            ug.setpoint = ug.leitura_potencia.valor

        self.usn.controle_ie = (self.usn.ug1.setpoint + self.usn.ug2.setpoint + self.usn.ug3.setpoint) / self.usn.cfg["pot_maxima_alvo"]
        self.usn.controle_i = max(min(self.usn.controle_ie - (self.usn.controle_i * self.usn.cfg["ki"]) - self.usn.cfg["kp"] * self.usn.erro_nv - self.usn.cfg["kd"] * (self.usn.erro_nv - self.usn.erro_nv_anterior), 0.8), 0)

        logger.debug("Escrevendo valores no banco")
        self.usn.escrever_valores()
        sleep(1 / ESCALA_DE_TEMPO)
        if self.usn.modo_autonomo:
            logger.debug("Comando recebido: \"Habilitar modo autônomo\"")
            sleep(2)
            logger.info("Usina voltou para o modo Autonomo")
            self.usn.ler_valores()
            if 1 in (self.usn.clp_emergencia_acionada, self.usn.db_emergencia_acionada):
                self.usn.normalizar_emergencia()
            return ControleRealizado(self.usn)

        if len(self.usn.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usn)

        return self


class AgendamentosPendentes(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn._state_moa = SM_SCHEDULE_PENDING

    def run(self):
        self.usn._state_moa = SM_SCHEDULE_PENDING
        logger.debug("Tratando agendamentos")
        self.usn.verificar_agendamentos()
        return ControleRealizado(self.usn)

class ReservatorioAbaixoDoMinimo(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn._state_moa = SM_DAM_LEVEL_UNDER_LOW_LIMIT

    def run(self):
        self.usn._state_moa = SM_DAM_LEVEL_UNDER_LOW_LIMIT
        self.usn.heartbeat()
        if self.usn.nv_montante_recente <= self.usn.cfg["nv_fundo_reservatorio"]:
            if not self.usn.ping(self.usn.cfg["TDA_slave_ip"]):
                logger.warning("Sem comunicação com CLP TDA, entrando no modo de operação Offline")
                self.usn.TDA_Offline = True
                return OperacaoTDAOffline(self.usn)
            else:
                self.usn.distribuir_potencia(0)
                for ug in self.usn.ugs:
                    ug.step()
                logger.critical(f"Nivel montante ({self.usn.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                return Emergencia(self.usn)

        return ControleRealizado(self.usn)


class ReservatorioAcimaDoMaximo(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn._state_moa = SM_DAM_LEVEL_OVER_HIGH_LIMIT

    def run(self):
        self.usn._state_moa = SM_DAM_LEVEL_OVER_HIGH_LIMIT
        self.usn.heartbeat()
        if self.usn.nv_montante_recente >= self.usn.cfg["nv_maximorum"]:
            self.usn.distribuir_potencia(0)
            logger.critical(f"Nivel montante ({self.usn.nv_montante_recente:3.2f}) atingiu o maximorum!")
            return Emergencia(self.usn)
        else:
            self.usn.controle_ie = 1
            self.usn.controle_i = 0.8
            self.usn.distribuir_potencia(self.usn.cfg["pot_maxima_alvo"])
            for ug in self.usn.ugs:
                ug.step()
            return ControleRealizado(self.usn)


class ReservatorioNormal(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn._state_moa = SM_DAM_LEVEL_BETWEEN_LIMITS

    def run(self):
        self.usn._state_moa = SM_DAM_LEVEL_BETWEEN_LIMITS
        self.usn.controle_normal()
        for ug in self.usn.ugs:
            ug.step()
        return ControleRealizado(self.usn)

class OperacaoTDAOffline(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.deve_ler_condicionadores = False
        self.habilitar_emerg_condic_e = False
        self.habilitar_emerg_condic_c = False
        self.usn._state_moa = SM_DAM_COMMUNICATION_OFFLINE

    def run(self):
        self.usn._state_moa = SM_DAM_COMMUNICATION_OFFLINE
        self.usn.heartbeat()
        global aux
        global deve_normalizar
        self.usn.TDA_Offline = True

        for condicionador_essencial in self.usn.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.deve_ler_condicionadores=True

        if self.usn.avisado_em_eletrica or self.deve_ler_condicionadores==True:
            for condicionador_essencial in self.usn.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade >= DEVE_INDISPONIBILIZAR:
                    self.habilitar_emerg_condic_e=True
                elif condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_NORMALIZAR:
                    deve_normalizar=True
                    self.habilitar_emerg_condic_e=False
                else:
                    deve_normalizar=False
                    self.habilitar_emerg_condic_e=False

            for condicionador in self.usn.condicionadores:
                if condicionador.ativo and condicionador.gravidade >= DEVE_INDISPONIBILIZAR:
                    self.habilitar_emerg_condic_c=True
                elif condicionador.ativo and condicionador.gravidade == DEVE_NORMALIZAR:
                    self.habilitar_emerg_condic_c=False
                    deve_normalizar=True
                else:
                    deve_normalizar=False
                    self.habilitar_emerg_condic_c=False

            if self.habilitar_emerg_condic_e or self.habilitar_emerg_condic_c:
                logger.warning("Foram detectados Condicionadores ativos com gravidade: \"Indisponibilizar\"!")
                return Emergencia(self.usn)

        if deve_normalizar:
            if (not self.usn.normalizar_emergencia()) and self.usn.tensao_ok==False and aux==0:
                logger.warning("Tensão da linha fora do limite ")
                aux = 1
                threading.Thread(target=lambda: self.usn.aguardar_tensao(20)).start()

            elif self.usn.timer_tensao:
                aux = 0
                deve_normalizar = None
                self.usn.timer_tensao = None

            elif self.usn.timer_tensao==False:
                aux = 0
                deve_normalizar = None
                self.usn.timer_tensao = None
                logger.warning("O tempo de normalização da linha excedeu o limite! (10 min)")
                return Emergencia(self.usn)

        if not self.usn.modo_autonomo:
            logger.info("Comando recebido: \"Desabilitar modo autônomo\"")
            sleep(2)
            return ModoManualAtivado(self.usn)

        if len(self.usn.get_agendamentos_pendentes()) > 0:
            return AgendamentosPendentes(self.usn)

        for ug in self.usn.ugs:
            ug.controle_cx_espiral()
            ug.step()

        return ControleRealizado(self.usn)

class ControleRealizado(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)
        self.usn._state_moa = SM_CONTROL_ACTION_SENT

    def run(self):
        self.usn._state_moa = SM_CONTROL_ACTION_SENT
        logger.debug("Escrevendo valores no Banco")
        self.usn.heartbeat()
        self.usn.escrever_valores()
        return Pronto(self.usn)