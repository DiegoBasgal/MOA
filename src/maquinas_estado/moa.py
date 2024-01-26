import sys
import pytz
import logging
import traceback

import src.usina as u
import src.subestacao as se
import src.tomada_agua as tda

from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


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
    def __init__(self, usina: "u.Usina"=None, *args, **kwargs):
        if usina is None:
            logger.error(f"Erro ao carregar a classe da Usina na máquina de estados.")
            return FalhaCritica()
        else:
            self.usn = usina

        self.args = args
        self.kwargs = kwargs

        self.usn.estado_moa = MOA_SM_NAO_INICIALIZADO

    def get_time(self) -> "datetime":
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def run(self) -> "object":
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

    def run(self):
        self.usn.ler_valores()

        logger.debug("Verificando modo do MOA...")
        if not self.usn.modo_autonomo:
            return ModoManual(self.usn)

        logger.debug("Verificando status da emergência...")
        if self.usn.clp_emergencia or self.usn.bd_emergencia:
            logger.debug("")
            logger.debug("Foi identificado o acionamento de Emergência!")
            return Emergencia(self.usn)

        logger.debug("Verificando se há agendamentos...")
        if len(self.usn.agn.verificar_agendamentos_pendentes()) > 0:
            logger.debug("")
            logger.debug("Foram identificados agendamentos pendentes!")
            return ControleAgendamentos(self.usn)

        else:
            logger.debug("Verificando condicionadores...")
            flag_condic = self.usn.verificar_condicionadores()

            if flag_condic == CONDIC_INDISPONIBILIZAR:
                return Emergencia(self.usn)

            elif flag_condic == CONDIC_AGUARDAR:
                if se.Subestacao.aguardar_normalizacao_djl():
                    self.usn.normalizar_usina()
                    return ControleDados(self.usn)
                else:
                    self.usn.normalizar_usina()
                    return self

            elif flag_condic == CONDIC_NORMALIZAR:
                flag_norm = self.usn.normalizar_usina()

                if flag_norm == NORM_USN_FALTA_TENSAO:
                    return Emergencia(self.usn) if se.Subestacao.aguardar_tensao() == False else ControleDados(self.usn)

                elif flag_norm == NORM_USN_EXECUTADA and self.usn.tentativas_normalizar > 2:
                    logger.info("Tentativas de Normalização da Usina excedidas!")
                    self.usn.tentativas_normalizar = 0
                    return Emergencia(self.usn)

                else:
                    return ControleDados(self.usn)

            else:
                logger.debug("")
                logger.debug("Heartbeat...")
                self.usn.heartbeat()

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

        self.usn.modo_autonomo = False
        for ug in self.usn.ugs: ug.temporizar_partida = False

        # self.usn.clp["MOA"].write_single_coil(REG_MOA["PAINEL_LIDO"], [1])

        logger.info("Usina em modo manual. Para retornar a operação autônoma, acionar via painel ou página WEB")

    def run(self):
        self.usn.ler_valores()

        logger.debug(f"[USN] Leitura de Nível:                   {tda.TomadaAgua.nv_montante:0.3f}")
        logger.debug(f"[USN] Potência no medidor:                {se.Subestacao.potencia_ativa:0.3f}")
        logger.debug("")

        for ug in self.usn.ugs:
            ug.setpoint = ug.potencia
            logger.debug(f"[UG{ug.id}] Unidade:                            \"{UG_SM_STR_DCT[ug.codigo_state]}\"")
            logger.debug(f"[UG{ug.id}] Etapa :                             \"{UG_STR_DCT_ETAPAS[ug.etapa]}\" (Atual: {ug.etapa_atual} | Alvo: {ug.etapa_alvo})")
            logger.debug(f"[UG{ug.id}] Leitura de Potência:                {ug.potencia} kW")
            logger.debug("")

        self.usn.controle_ie = self.usn.ajustar_ie_padrao()
        self.usn.controle_i = max(min(self.usn.controle_ie - (self.usn.controle_i * self.usn.cfg["ki"]) - self.usn.cfg["kp"] * tda.TomadaAgua.erro_nv - self.usn.cfg["kd"] * (tda.TomadaAgua.erro_nv - tda.TomadaAgua.erro_nv_anterior), 0.8), 0)

        self.usn.escrever_valores()

        if self.usn.modo_autonomo:
            self.usn.ler_valores()
            return ControleDados(self.usn)

        return ControleAgendamentos(self.usn) if len(self.usn.agn.verificar_agendamentos_pendentes()) > 0 else self


class Emergencia(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        self.usn.estado_moa = MOA_SM_EMERGENCIA

        self.tentativas = 0

        logger.critical(f"ATENÇÃO! Usina entrado em estado de emergência. (Horário: {self.get_time()})")

    def run(self):
        self.usn.ler_valores()

        if self.tentativas == 3:
            logger.warning("Tentativas de normalização excedidas, entrando em modo manual.")

            for ug in self.usn.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()

            return ModoManual(self.usn)

        elif self.usn.bd_emergencia:
            logger.warning("Comando acionado via página WEB, aguardando reset pela aba \"Emergência\".")

            while self.usn.bd_emergencia:
                self.usn.atualizar_valores_banco(self.usn.bd.get_parametros_usina())

                if not self.usn.bd_emergencia:
                    self.usn.bd_emergencia = False
                    return self

                if not self.usn.modo_autonomo:
                    self.usn.bd_emergencia = False
                    return ModoManual(self.usn)

        else:
            flag_condic = self.usn.verificar_condicionadores()

            if flag_condic == CONDIC_INDISPONIBILIZAR:
                logger.critical("Acionando VOIP e entrando em modo manual")
                for ug in self.usn.ugs:
                    ug.forcar_estado_indisponivel()
                    ug.step()
                return ModoManual(self.usn)

            elif flag_condic == CONDIC_NORMALIZAR:
                self.tentativas += 1
                self.usn.normalizar_forcado = True
                self.usn.normalizar_usina()
                return self

            else:
                logger.debug("Usina normalizada. Retomando operação...")
                return ControleDados(self.usn)