import sys
import pytz
import traceback

import src.dicionarios as d

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

        self.usn.clp["MOA"].write_single_coil(REG["PAINEL_LIDO"], [1])

    def run(self):
        self.usn.ler_valores()

        logger.debug("Verificando modo do MOA...")
        if not self.usn.modo_autonomo:
            logger.debug("")
            logger.info("Comando acionado: \"Desabilitar Modo Autônomo\"")
            return ModoManual(self.usn)

        logger.debug("Verificando status da emergência...")
        if self.usn.clp_emergencia or self.usn.db_emergencia:
            logger.debug("")
            logger.debug("Foi identificado o acinoamento da emergência")
            return Emergencia(self.usn)

        logger.debug("Verificando se há agendamentos...")
        if len(self.usn.agn.verificar_agendamentos_pendentes()) > 0:
            logger.debug("")
            logger.debug("Foram identificados agendamentos pendentes!")
            return ControleAgendamentos(self.usn)

        else:
            logger.debug("Verificando condicionadores...")
            flag = self.usn.oco.verificar_condicionadores()
            if flag == CONDIC_INDISPONIBILIZAR:
                return Emergencia(self.usn)

            elif flag == CONDIC_NORMALIZAR:
                if self.usn.normalizar_usina() == False:
                    return Emergencia(self.usn) if self.usn.aguardar_tensao() == False else self
                else:
                    return self

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
        logger.debug("Escrevendo valores no Banco...")
        self.usn.ler_valores()
        self.usn.escrever_valores()
        return ControleTDAOffline(self.usn) if d.glb["TDA_Offline"] else ControleEstados(self.usn)

class ControleAgendamentos(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usn.estado_moa = MOA_SM_CONTROLE_AGENDAMENTOS

    def run(self):
        logger.info("Tratando agendamentos...")
        self.usn.agn.verificar_agendamentos()
        if len(self.usn.agn.verificar_agendamentos_pendentes()) > 0:
            return self
        else:
            return ControleEstados(self.usn) if self.usn.modo_autonomo else ModoManual(self.usn)

class ModoManual(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        self.usn.estado_moa = MOA_SM_MODO_MANUAL
        logger.info("Usina em modo manual. Para retornar a operação autônoma, acionar via painel ou página WEB")

        self.usn.modo_autonomo = False
        self.usn.clp["MOA"].write_single_coil(REG["PAINEL_LIDO"], [1])

    def run(self):
        self.usn.ler_valores()
        logger.debug(f"[USN] Leitura de Nível:                   {self.usn.nv_montante_recente:0.3f}")
        logger.debug(f"[USN] Potência no medidor:                {self.usn.potencia_ativa:0.3f}")
        logger.debug("")

        for ug in self.usn.ugs:
            logger.debug(f"[UG{ug.id}] Unidade:                            \"{UG_SM_STR_DCT[ug.codigo_state]}\"")
            logger.debug(f"[UG{ug.id}] Etapa atual:                        \"{UG_STR_DCT_ETAPAS[ug.etapa_atual]}\"")
            logger.debug(f"[UG{ug.id}] Leitura de Potência:                {ug.leitura_potencia}")
            logger.debug("")
            ug.setpoint = ug.leitura_potencia

        self.usn.controle_ie = sum(ug.leitura_potencia for ug in self.usn.ugs) / self.usn.cfg["pot_maxima_alvo"]

        self.usn.escrever_valores()
        if self.usn.modo_autonomo:
            logger.debug("Comando acionado: \"Habilitar modo autônomo\"")
            self.usn.ler_valores()
            sleep(2)
            return ControleDados(self.usn)

        return ControleAgendamentos(self.usn) if len(self.usn.agn.verificar_agendamentos_pendentes()) > 0 else self

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


class ControleTDAOffline(State):
    def __init__(self, usina, *args, **kwargs):
        super().__init__(usina, *args, **kwargs)

        self.usn.estado_moa = MOA_SM_CONTROLE_RESERVATORIO

        d.glb["TDA_Offline"] = True

    def run(self):
        self.usn.heartbeat()
        
        logger.debug("Verificando modo do MOA...")
        if not self.usn.modo_autonomo:
            logger.debug("")
            logger.info("Comando acionado: \"Desabilitar modo autônomo\"")
            return ModoManual(self.usn)

        logger.debug("Verificando status da emergência...")
        if self.usn.clp_emergencia or self.usn.db_emergencia:
            logger.debug("")
            logger.debug("Foi identificado o acinoamento da emergência")
            return Emergencia(self.usn)

        logger.debug("Verificando se há agendamentos...")
        if len(self.usn.agn.verificar_agendamentos_pendentes()) > 0:
            logger.debug("")
            logger.debug("Foram identificados agendamentos pendentes!")
            return ControleAgendamentos(self.usn)

        else:
            logger.debug("Verificando condicionadores...")
            condic_flag = self.usn.oco.verificar_condicionadores()
            if condic_flag == CONDIC_INDISPONIBILIZAR:
                return Emergencia(self.usn)

            elif condic_flag == CONDIC_NORMALIZAR:
                if self.usn.normalizar_usina() == False:
                    return Emergencia(self.usn) if self.usn.aguardar_tensao() == False else ControleDados(self.usn)
                else:
                    for ug in self.usn.ugs:
                        ug.controle_cx_espiral()
                        ug.step()

                    return ControleDados(self.usn)