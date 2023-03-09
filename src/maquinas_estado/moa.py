import sys
import pytz
import threading
import traceback

from time import sleep
from datetime import datetime

from src.usina import *
from src.logger import *
from src.conector import *
from src.ocorrencias import *
from src.agendamentos import *
from src.dicionarios.reg import *
from src.dicionarios.const import *


class StateMachine:
    def __init__(self, initial_state):
        self.state = initial_state
        self.em_falha_critica = False

    def exec(self):
        try:
            if self.state is None:
                raise TypeError
            self.state = self.state.run()

        except Exception:
            logger.exception(f"Estado ({self.state}) levantou uma exception: {traceback.print_stack}")
            self.em_falha_critica = True
            self.state = FalhaCritica()

class State:
    def __init__(
            self,
            shared_dict=None,
            usina: Usina=None,
            ocorrencias: Ocorrencias=None,
            agendamentos: Agendamentos=None,
            ugs: list([UnidadeDeGeracao])=None,
            *args,
            **kwargs
        ):

        self.args = args
        self.kwargs = kwargs

        if (shared_dict or usina or ugs or ocorrencias or agendamentos) is None:
            logger.error(f"Erro ao instanciar o estado base do MOA.\nTraceback: {traceback.print_stack}")
            self.state = FalhaCritica()
        else:
            self.ugs = ugs
            self.ug1 = ugs[0]
            self.ug2 = ugs[1]
            self.usina = usina
            self.dict = shared_dict
            self.ocorrencias = ocorrencias
            self.agendamentos = agendamentos

    def run(self) -> object:
        return self

class FalhaCritica(State):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.critical("Falha crítica MOA. Exiting...")
        sys.exit(1)

class Pronto(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_tentativa = 0
        self.usina.state_moa = 3

    def run(self):
        self.usina.ler_valores()

        if self.n_tentativa >= 2:
            return FalhaCritica()
        else:
            try:
                return ControleNormal() if not self.dict.GLB["tda_offline"] else ControleTdaOffline()

            except Exception:
                self.n_tentativa += 1
                logger.exception(f"Erro durante a comunicação do MOA com a usina. Tentando novamente em {self.dict.CFG['timeout_padrao'] * self.n_tentativa}s (tentativa{self.n_tentativa}/3).\nTraceback: {traceback.print_stack}.")
                sleep(self.dict.CFG["timeout_padrao"] * self.n_tentativa)
                return self

class ControleNormal(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dict.GLB["tda_offline"] = False
        self.usina.clp_moa.write_single_coil(MOA["REG_PAINEL_LIDO"], [1])

    def run(self):
        self.usina.ler_valores()
        self.ocorrencias.verificar_condicionadores_usn()

        if self.ocorrencias.deve_normalizar_usn:
            if not self.usina.normalizar_emergencia() and not self.usina.tensao_ok:
                if not self.usina.aguardar_tensao():
                    return Emergencia()

        if self.usina.clp_emergencia_acionada or self.usina.db_emergencia_acionada or self.ocorrencias.deve_indisponibilizar_usn:
            logger.critical("Atenção! Emergência acionada!")
            self.ocorrencias.deve_indisponibilizar_usn=False
            return Emergencia()

        if len(self.agendamentos.agendamentos_pendentes()) > 0:
            return ControleAgendamentos()

        if not self.usina.modo_autonomo:
            logger.debug("Comando recebido: desabilitar modo autonomo.")
            return ModoManual()

        if self.usina.nv_montante < self.dict.CFG["nv_minimo"]:
            self.usina.aguardando_reservatorio = 1
            logger.info("Reservatorio abaixo do nivel de trabalho")
            return ReservatorioMinimo()

        if self.usina.nv_montante >= self.dict.CFG["nv_maximo"]:
            return ReservatorioMaximo()

        if self.usina.aguardando_reservatorio == 1 and (self.usina.nv_montante > self.dict.CFG["nv_alvo"]):
            logger.debug("Reservatorio dentro do nivel de trabalho")
            self.usina.aguardando_reservatorio = 0
            return ReservatorioNormal()

        elif self.usina.aguardando_reservatorio == 1:
            logger.debug("Aguardando reservatório.")
            return ControleDados()

        else:
            return ReservatorioNormal()

class ReservatorioNormal(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.usina.ler_valores()
        self.usina.controle_normal()
        [ug.step() for ug in self.ugs]
        return ControleDados()

class ReservatorioMinimo(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.usina.ler_valores()
        self.usina.distribuir_potencia(0)

        if self.usina.nv_montante_recente <= self.dict.CFG["nv_fundo_reservatorio"]:
            if not self.usina.ping(self.dict.CFG["TDA_slave_ip"]):
                logger.warning("Sem comunicação com CLP TDA, entrando no modo de operação Offline")
                return ControleTdaOffline()
            else:
                logger.critical(f"Nivel montante ({self.usina.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                return Emergencia()

        [ug.step() for ug in self.ugs]
        return ControleDados()

class ReservatorioMaximo(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def run(self):
        self.usina.ler_valores()
        if self.usina.nv_montante_recente >= self.dict.CFG["nv_maximorum"]:
            self.usina.distribuir_potencia(0)
            logger.critical(f"Nivel montante ({self.usina.nv_montante_recente:3.2f}) atingiu o maximorum!")
            return Emergencia()
        else:
            self.usina.distribuir_potencia(self.dict.CFG["pot_maxima_usina"])
            self.usina.controle_ie = 0.5
            self.usina.controle_i = 0.5
            [ug.step() for ug in self.ugs]
            return ControleDados()

class ControleDados(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.usina.ler_valores()
        logger.debug("Escrevendo valores")
        self.usina.escrever_valores()
        return Pronto()

class ControleAgendamentos(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        logger.info("Tratando agendamentos")
        self.agendamentos.verificar_agendamentos()
        return ControleDados()

class ModoManual(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usina.modo_autonomo = False

        self.usina.entrar_em_modo_manual()
        self.usina.clp_moa.write_single_coil(MOA["REG_PAINEL_LIDO"], [1])

        logger.info("Usina em modo manual, deve-se alterar via painel ou interface web.")

    def run(self):
        self.usina.ler_valores()
        for ug in self.ugs: ug.setpoint = ug.leitura_potencia.valor
        self.usina.controle_ie = (self.ug1.setpoint + self.ug2.setpoint) / self.dict.CFG["pot_maxima_alvo"]

        sleep(1 / ESCALA_DE_TEMPO)
        if self.usina.modo_autonomo:
            self.usina.ler_valores()
            logger.debug("Comando recebido: habilitar modo autonomo.")
            sleep(2)
            logger.debug("Usina voltou para o modo Autonomo")
            self.usina.db.update_habilitar_autonomo()
            if self.usina.clp_emergencia_acionada == 1 or self.usina.db_emergencia_acionada == 1:
                self.usina.normalizar_emergencia()
            self.usina.heartbeat()
            return ControleDados()

        return ControleAgendamentos() if len(self.agendamentos.agendamentos_pendentes()) > 0 else self

class Emergencia(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_tentativa = 0
        self.nao_ligou = True
        self.em_sm_acionada = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
        logger.warning(f"Usina entrado em estado de emergência (Timestamp: {self.em_sm_acionada})")

    def run(self):
        self.n_tentativa += 1
        condicionadores_ativos = self.ocorrencias.verificar_condicionadores_usn()

        self.usina.ler_valores()

        if self.n_tentativa > 2:
            logger.warning("Numero de tentaivas de normalização excedidas, entrando em modo manual.")
            [ug.forcar_estado_indisponivel() and ug.step() for ug in self.ugs]
            return ModoManual()

        else:
            if self.usina.db_emergencia_acionada:
                logger.warning("Emergencia acionada via Interface WEB/DB, aguardando Reset/Reconhecimento pela interface ou CLP")
                while self.usina.db_emergencia_acionada:
                    self.usina.ler_valores()
                    if not self.usina.clp_sa.em_emergencia():
                        self.usina.db.update_emergencia(0)
                        self.usina.db_emergencia_acionada = 0

            if self.usina.clp_emergencia_acionada or self.ocorrencias.deve_normalizar_usn or self.ocorrencias.deve_indisponibilizar_usn:
                logger.info(f"Usina detectou condicionadores ativos.\nCondicionadores ativos:\n{[d.descr for d in condicionadores_ativos]}")
                
                if self.ocorrencias.deve_indisponibilizar_usn:
                    logger.critical("Passando para manual e ligando por VOIP.")
                    self.usina.entrar_em_modo_manual()
                    return ModoManual()

                elif self.ocorrencias.deve_normalizar_usn:
                    logger.info(f"Normalizando usina. (tentativa{self.n_tentativa}/2) (limite entre tentaivas: {self.dict.CFG['timeout_normalizacao']}s)")
                    self.usina.deve_normalizar_forcado = True
                    self.usina.normalizar_emergencia()
                    return self

                else:
                    logger.debug("Usina normalizada. Retomando operação...")
                    return ControleDados()

class ControleTdaOffline(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dict.GLB["tda_offline"] = True

    def run(self):
        self.usina.ler_valores()
        self.ocorrencias.verificar_condicionadores_usn()

        if self.ocorrencias.deve_indisponibilizar_usn:
            logger.info("Condicionadores ativos com gravidade alta!")
            return Emergencia()

        if self.ocorrencias.deve_normalizar_usn:
            if not self.usina.normalizar_emergencia() and not self.usina.tensao_ok and not self.dict.GLB["borda_tensao"]:
                logger.warning("Tensão da linha fora do limite ")
                self.dict.GLB["borda_tensao"] = True
                threading.Thread(target=lambda: self.usina.aguardar_tensao(20)).start()

            elif self.usina.timer_tensao:
                self.dict.GLB["borda_tensao"] = False
                self.usina.timer_tensao = None
                self.ocorrencias.deve_normalizar_usn = None

            elif not self.usina.timer_tensao:
                self.dict.GLB["borda_tensao"] = False
                self.usina.timer_tensao = None
                self.ocorrencias.deve_normalizar_usn = None
                logger.warning("O tempo de normalização da linha excedeu o limite! (10 min)")
                return Emergencia()

        if not self.usina.modo_autonomo:
            logger.info("Comando recebido: desabilitar modo autonomo")
            return ModoManual()

        [ug.controle_cx_espiral() and ug.step() for ug in self.ugs]

        return ControleAgendamentos() if len(self.agendamentos.agendamentos_pendentes()) > 0 else ControleDados()