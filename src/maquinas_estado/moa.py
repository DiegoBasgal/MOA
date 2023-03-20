import sys
import pytz
import traceback

from time import sleep
from datetime import datetime

from src.usina import *
from src.agendamentos import *
from src.dicionarios.const import *
from src.dicionarios.reg import MOA
from src.ocorrencias import OcorrenciasUsn
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
    def __init__(self,
                cfg=None,
                sd: dict=None,
                usn: Usina=None,
                agn: Agendamentos=None,
                oco: OcorrenciasUsn=None,
                db : ConectorBancoDados=None,
                ugs: list[UnidadeDeGeracao]=None,
            ):

        if None in (sd, cfg, usn, agn, oco, db, ugs):
            logger.error(f"Erro ao instanciar o estado base do MOA. Exception: \"{repr(Exception)}\"")
            self.state = FalhaCritica()
        else:
            self.db = db
            self.cfg = cfg
            self.usn = usn
            self.agn = agn
            self.ugs = ugs
            self.oco = oco
            self.dict = sd

        self.usn.estado_moa = MOA_SM_NAO_INICIALIZADO

    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def run(self) -> object:
        return self

class FalhaCritica(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usn.estado_moa = MOA_SM_FALHA_CRITICA
        logger.critical("Falha crítica MOA. Interrompendo execução...")
        sys.exit(1)

class Pronto(State):
    def __init__(self, sd, usn, *args, **kwargs):
        super().__init__(sd, usn, *args, **kwargs)
        self.usn.estado_moa = MOA_SM_PRONTO

    def run(self):
        self.usn.ler_valores()
        return ControleNormal() if not self.dict["GLB"]["tda_offline"] else ControleTdaOffline()

class ControleNormal(State):
    def __init__(self, sd, usn, *args, **kwargs):
        super().__init__(sd, usn, *args, **kwargs)
        self.usn.estado_moa = MOA_SM_CONTROLE_NORMAL
        self.dict["GLB"]["tda_offline"] = False
        self.usn.clp_moa.write_single_coil(MOA["PAINEL_LIDO"], [1])

    def run(self):
        self.usn.ler_valores()

        if not self.usn.modo_autonomo:
            logger.info("Comando acionado: Desabilitar modo autônomo.")
            return ControleManual()

        elif self.usn.clp_emergencia or self.usn.db_emergencia:
            return ControleEmergencia()

        elif len(self.agn.agendamentos_pendentes()) > 0:
            return ControleAgendamentos()

        else:
            flag: int = self.oco.verificar_condicionadores()
            if flag == CONDIC_INDISPONIBILIZAR:
                return ControleEmergencia()

            elif flag == CONDIC_NORMALIZAR:
                if self.usn.normalizar_usina() == False:
                    return ControleEmergencia() if self.usn.aguardar_tensao() == False else ControleDados()
                else:
                    return ControleDados()

            return ControleReservatorio()

class ControleReservatorio(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)
        self.usn.estado_moa = MOA_SM_CONTROLE_RESERVATORIO

    def run(self):
        self.usn.ler_valores()
        flag: int = self.usn.controle_reservatorio()

        if flag == NV_FLAG_EMERGENCIA:
            return ControleEmergencia()
        elif flag == NV_FLAG_TDAOFFLINE:
            return ControleTdaOffline()
        else:
            return ControleDados()

class ControleDados(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)
        self.usn.estado_moa = MOA_SM_CONTROLE_DADOS
        logger.debug("Escrevendo valores.")

    def run(self):
        self.usn.ler_valores()
        self.usn.escrever_valores()
        return ControleNormal() if not self.dict["GLB"]["tda_offline"] else ControleTdaOffline()

class ControleAgendamentos(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usn.estado_moa = MOA_SM_CONTROLE_AGENDAMENTOS
        logger.info("Tratando agendamentos.")

    def run(self):
        self.agn.verificar_agendamentos()
        return ControleDados() if self.usn.modo_autonomo else ControleManual()

class ControleManual(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)
        self.usn.estado_moa = MOA_SM_CONTROLE_MANUAL

        self.usn.modo_autonomo = False
        self.usn.clp_moa.write_single_coil(MOA["PAINEL_LIDO"], [1])

        logger.info("Usina em modo manual. Para retornar a operação autônoma, acionar via painel ou página WEB")

    def run(self):
        self.usn.ler_valores()
        for ug in self.ugs:
            ug.setpoint = ug.leitura_potencia
        self.usn.controle_ie = [sum(ug.leitura_potencia) for ug in self.ugs] / self.cfg["pot_maxima_alvo"]

        if self.usn.modo_autonomo:
            logger.debug("Comando acionado: Habilitar modo autônomo.")
            self.usn.ler_valores()
            self.usn.db.update_modo_moa(self.usn.modo_autonomo)
            sleep(2)
            return ControleDados()

        return ControleAgendamentos() if len(self.agn.agendamentos_pendentes()) > 0 else self

class ControleEmergencia(State):
    def __init__(self, usn, oco, *args, **kwargs):
        super().__init__(usn, oco, *args, **kwargs)
        self.usn.estado_moa = MOA_SM_CONTROLE_EMERGENCIA
        self.tentativas = 0
        logger.critical(f"ATENÇÃO! Usina entrado em estado de emergência. (Horário: {self.get_time()})")

    def run(self):
        self.usn.ler_valores()

        if self.tentativas == 3:
            logger.warning("Tentativas de normalização excedidas, entrando em modo manual.")
            for ug in self.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()
            return ControleManual()

        elif self.usn.db_emergencia:
            logger.warning("Acionado via página WEB, aguardando reset pela aba emergência.")
            while self.usn.db_emergencia:
                self.usn.atualizar_parametros_db(self.usn.db.get_parametros_usina())
                if not self.usn.db_emergencia:
                    self.usn.db_emergencia = False
                    return self
                if not self.usn.modo_autonomo:
                    self.usn.db_emergencia = False
                    return ControleManual()

        else:
            flag = self.oco.verificar_condicionadores()
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

class ControleTdaOffline(State):
    def __init__(self, usn, oco, agn, *args, **kwargs):
        super().__init__(usn, oco, agn, *args, **kwargs)
        self.usn.estado_moa = MOA_SM_CONTROLE_TDAOFFLINE
        self.dict["GLB"]["tda_offline"] = True

    def run(self):
        self.usn.ler_valores()

        if not self.usn.modo_autonomo:
            logger.info("Comando acionado: Desabilitar modo autônomo")
            return ControleManual()

        elif len(self.agn.agendamentos_pendentes()) > 0:
            return ControleAgendamentos()

        else:
            flag = self.oco.verificar_condicionadores()
            if flag == CONDIC_INDISPONIBILIZAR:
                    return ControleEmergencia()

            elif flag == CONDIC_NORMALIZAR:
                if self.usn.normalizar_usina() == False:
                    return ControleEmergencia() if self.usn.aguardar_tensao() == False else ControleDados()
                else:
                    return ControleDados()
            else:
                for ug in self.ugs:
                    ug.controle_cx_espiral()
                    ug.step()
                return ControleDados()