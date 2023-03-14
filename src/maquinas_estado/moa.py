import sys
import pytz
import traceback

from time import sleep
from datetime import datetime

from src.usina import *
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

        except Exception as e:
            logger.exception(f"Estado ({self.state}) levantou uma exception: \"{repr(e)}\"")
            logger.exception(f"Traceback: {traceback.print_stack}")
            self.em_falha_critica = True
            self.state = FalhaCritica()

class State:
    def __init__(
            self,
            sd=None,
            cfg=None,
            usn: Usina=None,
            agn: Agendamentos=None,
            oco: OcorrenciasUsn=None,
            ugs: list([UnidadeDeGeracao])=None,
            *args,
            **kwargs
        ):

        self.args = args
        self.kwargs = kwargs

        if (sd or cfg or usn or ugs or oco or agn) is None:
            logger.error(f"Erro ao instanciar o estado base do MOA. Exception: \"{repr(Exception)}\"")
            self.state = FalhaCritica()
        else:
            self.cfg = cfg
            self.ugs = ugs
            self.usn = usn
            self.dict = sd
            self.oco = oco
            self.agn = agn

    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def run(self) -> object:
        return self

class FalhaCritica(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.critical("Falha crítica MOA. Exiting...")
        sys.exit(1)

class Pronto(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)
        self.tentativas = 0
        self.usn.state_moa = 3

    def run(self):
        self.usn.ler_valores()

        if self.tentativas >= 2:
            return FalhaCritica()
        else:
            try:
                return ControleNormal() if not self.dict["GLB"]["tda_offline"] else ControleTdaOffline()

            except Exception as e:
                self.tentativas += 1
                logger.exception(f"Erro durante a comunicação do MOA com a usina. Tentando novamente em {TIMEOUT_PADRAO * self.tentativas}s (Tentativa {self.tentativas}/3). Exception: \"{repr(e)}\"")
                logger.exception(f"Traceback: {traceback.print_stack}")
                sleep(TIMEOUT_PADRAO * self.tentativas)
                return self

class ControleNormal(State):
    def __init__(self, usn, agn, oco, *args, **kwargs):
        super().__init__(usn, agn, oco, *args, **kwargs)

        self.dict["GLB"]["tda_offline"] = False
        self.usn.clp_moa.write_single_coil(MOA["REG_PAINEL_LIDO"], [1])

    def run(self):
        self.usn.ler_valores()

        if self.oco.verificar_condicionadores():
            if self.oco.indisponibilizar:
                self.oco.indisponibilizar = False
                logger.critical("Atenção! Emergência acionada!")
                return ControleEmergencia()

            elif self.oco.normalizar:
                self.oco.normalizar = False
                if not self.usn.normalizar_usina() and not self.usn.tensao_ok:
                    if not self.usn.aguardar_tensao():
                        return ControleEmergencia()
            else:
                return ControleDados()

        if self.usn.clp_emergencia or self.usn.db_emergencia:
            logger.critical("Atenção! Emergência acionada!")
            return ControleEmergencia()

        if len(self.agn.agendamentos_pendentes()) > 0:
            return ControleAgendamentos()

        if not self.usn.modo_autonomo:
            logger.debug("Comando recebido: desabilitar modo autonomo.")
            return ControleManual()

        else:
            return ControleReservatorio()

class ControleReservatorio(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

    def run(self):
        self.usn.ler_valores()

        # Reservatório acima do nível máximo
        if self.usn.nv_montante >= self.cfg["nv_maximo"]:
            if self.usn.nv_montante_recente >= NIVEL_MAXIMORUM:
                self.usn.distribuir_potencia(0)
                logger.critical(f"Nivel montante ({self.usn.nv_montante_recente:3.2f}) atingiu o maximorum!")
                return ControleEmergencia()
            else:
                self.usn.distribuir_potencia(self.cfg["pot_maxima_usina"])
                self.usn.controle_ie = 0.5
                self.usn.controle_i = 0.5
                for ug in self.ugs: 
                    ug.step()
                return ControleDados()

        # Reservatório abaixo do nível mínimo
        elif self.usn.nv_montante < self.cfg["nv_minimo"] and not self.usn.aguardando_reservatorio:
            self.usn.aguardando_reservatorio = True
            logger.info("Reservatorio abaixo do nivel de trabalho")

            self.usn.distribuir_potencia(0)
            if self.usn.nv_montante_recente < NIVEL_FUNDO_RESERVATORIO:
                if not self.usn.ping(self.dict["IP"]["TDA_slave_ip"]):
                    logger.warning("Sem comunicação com CLP TDA, entrando no modo de operação Offline")
                    return ControleTdaOffline()
                else:
                    logger.critical(f"Nivel montante ({self.usn.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                    return ControleEmergencia()

            for ug in self.ugs:
                ug.step()
            return ControleDados()

        # Aguardando nível do reservatório
        elif self.usn.aguardando_reservatorio:
            if self.usn.nv_montante > self.cfg["nv_alvo"]:
                logger.debug("Reservatorio dentro do nivel de trabalho")
                self.usn.aguardando_reservatorio = False
                return ControleDados()
            else:
                logger.debug("Aguardando reservatório")
                return ControleDados()

        # Reservatório Normal
        else:
            self.usn.controle_normal()
            for ug in self.ugs:
                ug.step()
            return ControleDados()

class ControleDados(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

    def run(self):
        self.usn.ler_valores()
        logger.debug("Escrevendo valores")
        self.usn.escrever_valores()
        return Pronto()

class ControleAgendamentos(State):
    def __init__(self, agn, *args, **kwargs):
        super().__init__(agn, *args, **kwargs)

    def run(self):
        logger.info("Tratando agendamentos")
        self.agn.verificar_agendamentos()
        return ControleDados()

class ControleManual(State):
    def __init__(self, usn, agn, *args, **kwargs):
        super().__init__(usn, agn, *args, **kwargs)

        self.usn.modo_autonomo = False
        self.usn.clp_moa.write_single_coil(MOA["REG_PAINEL_LIDO"], [1])

        logger.info("Usina em modo manual, deve-se alterar via painel ou interface web.")

    def run(self):
        self.usn.ler_valores()
        for ug in self.ugs: 
            ug.setpoint = ug.leitura_potencia.valor
        self.usn.controle_ie = [sum(ug.leitura_potencia.valor) / self.cfg["pot_maxima_alvo"] for ug in self.ugs]

        if self.usn.modo_autonomo:
            self.usn.ler_valores()
            self.usn.db.update_modo_moa(self.usn.modo_autonomo)
            logger.debug("Comando recebido: habilitar modo autonomo.")
            sleep(2)
            return ControleDados()

        return ControleAgendamentos() if len(self.agn.agendamentos_pendentes()) > 0 else self

class ControleEmergencia(State):
    def __init__(self, usn, oco, *args, **kwargs):
        super().__init__(usn, oco, *args, **kwargs)
        self.tentativas = 0
        logger.warning(f"Usina entrado em estado de emergência (Timestamp: {self.get_time()})")

    def run(self):
        self.usn.ler_valores()

        if self.tentativas > 2:
            logger.warning("Numero de tentaivas de normalização excedidas, entrando em modo manual.")
            for ug in self.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()
            return ControleManual()

        elif self.oco.verificar_condicionadores():
            if self.oco.indisponibilizar:
                logger.critical("Passando para manual e ligando por VOIP.")
                self.usn.modo_autonomo = 0
                return ControleManual()

            elif self.oco.normalizar:
                self.tentativas += 1
                logger.info(f"Normalizando usina. (Tentativa {self.tentativas}/2) (limite entre tentaivas: {TIMEOUT_NORMALIZACAO}s)")
                self.usn.normalizar_forcado = True
                self.usn.normalizar_usina()
                return self

        if self.usn.db_emergencia:
            logger.warning("ControleEmergencia acionada via Interface WEB/DB, aguardando Reset/Reconhecimento pela interface ou CLP")
            while self.usn.db_emergencia:
                self.usn.ler_valores()
                if not self.usn.clp_emergencia:
                    self.usn.db_emergencia = False
                    self.usn.db.update_emergencia(0)

        else:
            logger.debug("Usina normalizada. Retomando operação...")
            return ControleDados()

class ControleTdaOffline(State):
    def __init__(self, usn, oco, agn, *args, **kwargs):
        super().__init__(usn, oco, agn, *args, **kwargs)

        self.dict["GLB"]["tda_offline"] = True

    def run(self):
        self.usn.ler_valores()
        self.oco.verificar_condicionadores()

        if self.oco.verificar_condicionadores():
            if self.oco.indisponibilizar:
                self.oco.indisponibilizar = False
                logger.critical("Atenção! Emergência acionada!")
                return ControleEmergencia()

            elif self.oco.normalizar:
                self.oco.normalizar = False
                if not self.usn.normalizar_usina() and not self.usn.tensao_ok:
                    if not self.usn.aguardar_tensao():
                        return ControleEmergencia()
            else:
                return ControleDados()

        if not self.usn.modo_autonomo:
            logger.info("Comando recebido: desabilitar modo autonomo")
            return ControleManual()

        for ug in self.ugs:
            ug.controle_cx_espiral()
            ug.step()

        return ControleAgendamentos() if len(self.agn.agendamentos_pendentes()) > 0 else ControleDados()