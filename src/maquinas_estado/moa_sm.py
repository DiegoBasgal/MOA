import sys
import pytz
import traceback

from time import sleep
from datetime import datetime

from src.usina import *
from src.dicionarios.const import *
from src.dicionarios.reg import MOA
from src.conector import ConectorBancoDados

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
    def __init__(
            self,
            sd: dict | None = ...,
            cfg: dict | None = ...,
            usn: Usina | None = ...,
            db : ConectorBancoDados | None = ...,
            ugs: list[UnidadeDeGeracao] | None = ...,
        ) -> None:

        if None in (sd, cfg, usn, db, ugs):
            logger.error(f"Erro ao instanciar o estado base do MOA. Exception: \"{repr(Exception)}\"")
            self.state = FalhaCritica()
        else:
            self.db = db
            self.cfg = cfg
            self.usn = usn
            self.ugs = ugs
            self.dict = sd

        self.usn.estado_moa = MOA_SM_NAO_INICIALIZADO

    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def run(self) -> object:
        return self

class FalhaCritica(State):
    def __init__(self):
        super().__init__()
        self.usn.estado_moa = MOA_SM_FALHA_CRITICA
        logger.critical("Falha crítica MOA. Interrompendo execução...")
        sys.exit(1)

class Pronto(State):
    def __init__(self, sd, usn):
        State.__init__(sd, cfg, usn, db, ugs)
        self.usn.estado_moa = MOA_SM_PRONTO

    def run(self):
        self.usn.ler_valores()
        return ControleNormal() if not self.dict["GLB"]["tda_offline"] else ControleTdaOffline()


class ControleNormal(State):
    def __init__(self, usn):
        super().__init__(usn)
        self.usn.estado_moa = MOA_SM_CONTROLE_NORMAL
        self.dict["GLB"]["tda_offline"] = False
        self.usn.clp_moa.write_single_coil(MB["MOA"]["PAINEL_LIDO"], [1])

    def run(self):
        self.usn.ler_valores()

        condic_emerg = False
        ler_condicionadores = False

        condic_flag = CONDIC_IGNORAR

        if not self.usn.modo_autonomo:
            logger.info("Comando acionado: Desabilitar modo autônomo.")
            return ControleManual()

        elif self.usn.clp_emergencia or self.usn.db_emergencia:
            return ControleEmergencia()

        elif len(self.usn.get_agendamentos_pendentes()) > 0:
            return ControleAgendamentos()

        else:
            

            if condic_flag == CONDIC_INDISPONIBILIZAR:
                    return ControleEmergencia()

                elif condic_flag == CONDIC_NORMALIZAR:
                    if self.usn.normalizar_usina() == False:
                        return ControleEmergencia() if self.usn.aguardar_tensao() == False else ControleDados()
                    else:
                        return ControleDados()

        if self.usina.clp_emergencia_acionada:
            logger.info("Comando recebido: habilitando modo de ControleEmergencia.")
            sleep(2)
            return ControleEmergencia(self.usina)

        if self.usina.db_emergencia_acionada:
            logger.info("Comando recebido: habilitando modo de ControleEmergencia.")
            sleep(2)
            return ControleEmergencia(self.usina)

        # Verificamos se existem agendamentos
        if len(self.usina.get_agendamentos_pendentes()) > 0:
            return ControleAgendamentos(self.usina)

        # Em seguida com o modo manual (não autonomo)
        if not self.usina.modo_autonomo:
            logger.debug("Comando recebido: desabilitar modo autonomo.")
            sleep(2)
            return ControleManual(self.usina)

        # Se não foi redirecionado ainda,
        # assume-se que o MOA deve executar de modo autônomo

        # Verifica-se então a situação do reservatório
        if self.usina.aguardando_reservatorio:
            if self.usina.nv_montante > self.usina.cfg["nv_alvo"]:
                logger.debug("Reservatorio dentro do nivel de trabalho")
                self.usina.aguardando_reservatorio = 0
                return ReservatorioNormal(self.usina)

        if self.usina.nv_montante < self.usina.cfg["nv_minimo"]:
            self.usina.aguardando_reservatorio = 1
            logger.info("Reservatorio abaixo do nivel de trabalho")
            return ReservatorioAbaixoDoMinimo(self.usina)

        if self.usina.nv_montante >= self.usina.cfg["nv_maximo"]:
            return ReservatorioAcimaDoMaximo(self.usina)

        # Se estiver tudo ok:
        return ReservatorioNormal(self.usina)

class ControleReservatorio(State):
    def __init__(self, usn):
        super().__init__(usn)
        self.usn.estado_moa = MOA_SM_CONTROLE_RESERVATORIO

    def run(self):
        self.usn.ler_valores()
        flag = self.usn.controle_reservatorio()

        if flag == NV_FLAG_EMERGENCIA:
            return ControleEmergencia()
        elif flag == NV_FLAG_TDAOFFLINE:
            return ControleTdaOffline()
        else:
            return ControleDados()

class ControleDados(State):
    def __init__(self, instancia_usina):
        super().__init__()
        self.usina = instancia_usina

    def run(self):
        logger.debug("HB")
        self.usina.heartbeat()
        logger.debug("Escrevendo valores")
        self.usina.escrever_valores()
        return Pronto(self.usina)

class ControleEmergencia(State):
    def __init__(self, instancia_usina):
        super().__init__()
        self.em_sm_acionada = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        logger.warning(
            "Usina entrado em estado de emergência (Timestamp: {})".format(
                self.em_sm_acionada
            )
        )
        self.usina = instancia_usina
        self.n_tentativa = 0
        self.usina.escrever_valores()
        self.usina.heartbeat()
        self.nao_ligou = True

    def run(self):
        self.usina.heartbeat()
        self.n_tentativa += 1
        if self.n_tentativa > 2:
            logger.warning("Numero de tentaivas de normalização excedidas, entrando em modo manual.")
            self.usina.entrar_em_modo_manual()
            self.usina.heartbeat()
            for ug in self.usina.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()
            return ControleManual(self.usina)
        else:
            if self.usina.db_emergencia_acionada:
                logger.warning("ControleEmergencia acionada via Interface WEB/DB, aguardando Reset/Reconhecimento pela interface ou CLP")
                while self.usina.db_emergencia_acionada:
                    self.usina.ler_valores()
                    if not self.usina.clp.em_emergencia():
                        self.usina.db.update_emergencia(0)
                        self.usina.db_emergencia_acionada = 0

            self.usina.ler_valores()
            # Ler condiconadores
            CONDIC_INDISPONIBILIZAR = False
            CONDIC_NORMALIZAR = False
            condicionadores_ativos = []
            
            for condicionador_essencial in self.usina.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade == CONDIC_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    CONDIC_INDISPONIBILIZAR = True
                elif condicionador_essencial.gravidade == CONDIC_NORMALIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    CONDIC_NORMALIZAR = True

            for condicionador in self.usina.condicionadores:
                if condicionador.ativo and condicionador.gravidade == CONDIC_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador)
                    CONDIC_INDISPONIBILIZAR=True
                elif condicionador.gravidade == CONDIC_NORMALIZAR:
                    condicionadores_ativos.append(condicionador)
                    CONDIC_INDISPONIBILIZAR=False

            if (self.usina.clp_emergencia_acionada or CONDIC_NORMALIZAR or CONDIC_INDISPONIBILIZAR):
                try:

                    # Se algum condicionador deve gerar uma indisponibilidade
                    if CONDIC_INDISPONIBILIZAR:
                        # Logar os condicionadores ativos
                        logger.critical(
                            "[USN] USN detectou condicionadores ativos, passando USINA para manual e ligando por VOIP.\nCondicionadores ativos:\n{}".format(
                                [d.descr for d in condicionadores_ativos]
                            )
                        )
                        # Vai para o estado StateIndisponivel
                        self.usina.entrar_em_modo_manual()
                        return ControleManual(self.usina)

                    elif CONDIC_NORMALIZAR:
                        logger.debug("Aguardando antes de tentar normalizar novamente (5s)")
                        sleep(5)
                        logger.info("Normalizando usina. (tentativa{}/2) (limite entre tentaivas: {}s)".format(self.n_tentativa, self.usina.cfg["timeout_normalizacao"]))
                        self.usina.deve_normalizar_forcado=True
                        self.usina.normalizar_emergencia()
                        self.usina.ler_valores()
                        return self

                    else:
                        logger.debug("Nenhum condicionador relevante ativo...")
                        self.usina.ler_valores()
                        return ControleDados(self.usina)

                except Exception as e:
                    logger.error(
                        "Erro durante a comunicação do MOA com a usina. Exception: {}.".format(
                            repr(e)
                        )
                    )
                    logger.debug("Traceback: {}".format(traceback.print_stack))
                return self
            else:
                self.usina.ler_valores()
                logger.info("Usina normalizada")
                return ControleDados(self.usina)


class ControleManual(State):
    def __init__(self, instancia_usina):
        super().__init__()
        self.usina = instancia_usina
        self.usina.modo_autonomo = False
        self.usina.escrever_valores()
        logger.info("Usina em modo manual, deve-se alterar via painel ou interface web.")

    def run(self):
        self.usina.ler_valores()
        DataBank.set_words(REG_MB["MOA"]["PAINEL_LIDO"], [1])
        self.usina.ug1.setpoint = self.usina.ug1.leitura_potencia.valor
        self.usina.ug2.setpoint = self.usina.ug2.leitura_potencia.valor

        self.usina.controle_ie = (self.usina.ug1.setpoint + self.usina.ug2.setpoint) / self.usina.cfg["pot_maxima_alvo"]

        self.usina.heartbeat()
        sleep(1 / ESCALA_DE_TEMPO)
        if self.usina.modo_autonomo:
            logger.debug("Comando recebido: habilitar modo autonomo.")
            sleep(2)
            logger.info("Usina voltou para o modo Autonomo")
            self.usina.db.update_habilitar_autonomo()
            self.usina.ler_valores()
            if (self.usina.clp_emergencia_acionada == 1 or self.usina.db_emergencia_acionada == 1):
                self.usina.normalizar_emergencia()
            self.usina.heartbeat()
            return ControleDados(self.usina)

        if len(self.usina.get_agendamentos_pendentes()) > 0:
            return ControleAgendamentos(self.usina)

        return self


class ControleAgendamentos(State):
    def __init__(self, instancia_usina):
        super().__init__()
        self.usina = instancia_usina

    def run(self):
        logger.info("Tratando agendamentos")
        self.usina.verificar_agendamentos()
        return ControleDados(self.usina)


class ReservatorioAbaixoDoMinimo(State):
    def __init__(self, instancia_usina):
        super().__init__()
        self.usina = instancia_usina

    def run(self):
        self.usina.distribuir_potencia(0)
        if self.usina.nv_montante_recente <= self.usina.cfg["nv_fundo_reservatorio"]:
            if not usina.ping(self.usina.cfg["TDA_slave_ip"]):
                logger.warning("Sem comunicação com CLP TDA, entrando no modo de operação Offline")
                self.usina.TDA_Offline = True
                return ControleTdaOffline(self.usina)
            else:
                logger.critical("Nivel montante ({:3.2f}) atingiu o fundo do reservatorio!".format(self.usina.nv_montante_recente))
                return ControleEmergencia(self.usina)
        for ug in self.usina.ugs:
            print("")
            ug.step()
        return ControleDados(self.usina)


class ReservatorioAcimaDoMaximo(State):
    def __init__(self, instancia_usina):
        super().__init__()
        self.usina = instancia_usina

    def run(self):
        if self.usina.nv_montante_recente >= self.usina.cfg["nv_maximorum"]:
            self.usina.distribuir_potencia(0)
            logger.critical("Nivel montante ({:3.2f}) atingiu o maximorum!".format(self.usina.nv_montante_recente))
            return ControleEmergencia(self.usina)
        else:
            self.usina.distribuir_potencia(self.usina.cfg["pot_maxima_usina"])
            self.usina.controle_ie = 0.5
            self.usina.controle_i = 0.5
            for ug in self.usina.ugs:
                print("")
                ug.step()
            return ControleDados(self.usina)


class ReservatorioNormal(State):
    def __init__(self, instancia_usina):
        super().__init__()
        self.usina = instancia_usina

    def run(self):

        self.usina.controle_normal()
        for ug in self.usina.ugs:
            print("")
            ug.step()
        return ControleDados(self.usina)

class ControleTdaOffline(State):
    def __init__(self, instancia_usina):
        super().__init__()
        self.usina = instancia_usina
        self.deve_ler_condicionadores = False
        self.habilitar_emerg_condic_e = False
        self.habilitar_emerg_condic_c = False

    def run(self):
        global aux
        global CONDIC_NORMALIZAR
        self.usina.TDA_Offline = True

        for condicionador_essencial in self.usina.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.deve_ler_condicionadores=True

        if self.usina.avisado_em_eletrica or self.deve_ler_condicionadores==True:
            for condicionador_essencial in self.usina.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade >= CONDIC_INDISPONIBILIZAR:
                        self.habilitar_emerg_condic_e=True
                elif condicionador_essencial.ativo and condicionador_essencial.gravidade == CONDIC_NORMALIZAR:
                    CONDIC_NORMALIZAR=True
                    self.habilitar_emerg_condic_e=False
                else:
                    CONDIC_NORMALIZAR=False
                    self.habilitar_emerg_condic_e=False
            
            for condicionador in self.usina.condicionadores:
                if condicionador.ativo and condicionador.gravidade >= CONDIC_INDISPONIBILIZAR:
                    self.habilitar_emerg_condic_c=True
                elif condicionador.ativo and condicionador.gravidade == CONDIC_NORMALIZAR:
                    self.habilitar_emerg_condic_c=False
                    CONDIC_NORMALIZAR=True
                else:
                    CONDIC_NORMALIZAR=False
                    self.habilitar_emerg_condic_c=False
            
            if self.habilitar_emerg_condic_e or self.habilitar_emerg_condic_c:
                logger.info("Condicionadores ativos com gravidade alta!")
                return ControleEmergencia(self.usina)

        if CONDIC_NORMALIZAR:
            if (not self.usina.normalizar_emergencia()) and self.usina.tensao_ok==False and aux==0:
                logger.warning("Tensão da linha fora do limite ")
                aux = 1
                threading.Thread(target=lambda: self.usina.aguardar_tensao(20)).start()

            elif self.usina.timer_tensao:
                aux = 0
                CONDIC_NORMALIZAR = None
                self.usina.timer_tensao = None

            elif self.usina.timer_tensao==False:
                aux = 0
                CONDIC_NORMALIZAR = None
                self.usina.timer_tensao = None
                logger.warning("O tempo de normalização da linha excedeu o limite! (10 min)")
                return ControleEmergencia(self.usina)
        
        if not self.usina.modo_autonomo:
            logger.info("Comando recebido: desabilitar modo autonomo.")
            sleep(2)
            return ControleManual(self.usina)

        if len(self.usina.get_agendamentos_pendentes()) > 0:
            return ControleAgendamentos(self.usina)

        for ug in self.usina.ugs:
            print("")
            ug.controle_press_turbina()
            ug.step()

        return ControleDados(self.usina)


