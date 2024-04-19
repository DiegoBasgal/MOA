__version__ = "0.2"
__author__ = "Diego Basgal", "Henrique Pfeifer", "Lucas Lavratti"
__description__ = "Este módulo corresponde a implementação da máquina de estados do Módulo de Operação Autônoma."

import sys
import pytz
import logging
import traceback

import src.usina as usn
import src.subestacao as se
import src.tomada_agua as tda
import src.funcoes.agendamentos as agn
import src.conectores.banco_dados as bd

from time import sleep
from datetime import datetime

from src.dicionarios.const import *


logger = logging.getLogger("logger")
debug_log = logging.getLogger("debug")


class StateMachine:
    def __init__(self, initial_state) -> "None":

        self.state = initial_state


    def exec(self) -> "None":
        """
        Função principal de execução da Máquina de Estados do MOA.
        """

        try:
            if self.state is None:
                raise TypeError
            self.state = self.state.run()

        except Exception:
            logger.exception(f"Erro na execução do Estado: {self.state}")
            logger.exception(f"Traceback: {traceback.format_exc()}")
            self.state = FalhaCritica()


class State:
    def __init__(self, *args, **kwargs) -> "None":

        self.args = args
        self.kwargs = kwargs

        usn.Usina.estado_moa = MOA_SM_NAO_INICIALIZADO


    def get_time(self) -> "datetime":
        """
        Função para obter data e hora atual.
        """

        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    def run(self) -> "object":
        """
        Função abstrata para execução do passo da Máquina de Estados do MOA.
        """

        return self


class FalhaCritica(State):
    def __init__(self) -> "None":

        usn.Usina.estado_moa = MOA_SM_FALHA_CRITICA

        logger.critical("Falha crítica MOA. Interrompendo execução...")
        sys.exit(1)


class Pronto(State):
    def __init__(self, *args, **kwargs)  -> "None":
        super().__init__(*args, **kwargs)

        usn.Usina.estado_moa = MOA_SM_PRONTO


    def run(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Apenas chama a função de leitura de valores de operação da classe Pai e
        depois segue para o estado de Controle de Dados.
        """

        usn.Usina.ler_valores()
        return ControleEstados()


class ControleEstados(State):
    def __init__(self, *args, **kwargs) -> "None":
        super().__init__(*args, **kwargs)

        usn.Usina.estado_moa = MOA_SM_CONTROLE_ESTADOS


    def run(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Primeiramente chama a função de leitura de valores de operação da classe
        Pai, para depois realizar a verificação de condições de troca de estados.
        Caso não haja nenhum comando pendente, realiza a verificação de Condicionadores
        da Usina e determina se deverá indisponibilizar a Usina ou normalizá-la.
        Caso não haja nenhum acionamento, passa para o estado de Controle de
        Reservatório.
        """

        usn.Usina.ler_valores()

        logger.debug("")

        logger.debug("Verificando modo do MOA...")
        if not usn.Usina.modo_autonomo:
            logger.debug("")
            logger.debug("Comando acionado: \"Desabilitar Modo Autônomo\"")
            return ModoManual()

        logger.debug("Verificando status da emergência...")
        if usn.Usina.clp_emergencia or usn.Usina.bd_emergencia:
            logger.debug("")
            logger.debug("Foi identificado o acinoamento da emergência")
            return Emergencia()

        logger.debug("Verificando se há agendamentos...")
        if len(agn.Agendamentos.verificar_agendamentos_pendentes()) > 0:
            logger.debug("")
            logger.debug("Foram identificados agendamentos pendentes!")
            return ControleAgendamentos()

        else:
            logger.debug("Verificando condicionadores...")
            flag_condic = usn.Usina.verificar_condicionadores()

            if flag_condic == CONDIC_INDISPONIBILIZAR:
                return Emergencia()

            elif flag_condic == CONDIC_NORMALIZAR:
                if usn.Usina.normalizar_usina() and usn.Usina.tentativas_normalizar > 2:
                    logger.info("Tentativas de Normalização da Usina excedidas!")
                    usn.Usina.tentativas_normalizar = 0
                    return Emergencia()
                else:
                    return ControleDados()

            logger.debug("Verificando status da Subestação...")
            logger.debug("")
            flag_se = usn.Usina.verificar_se()

            if flag_se == DJS_FALTA_TENSAO:
                return Emergencia() if se.Subestacao.aguardar_tensao() == TENSAO_FORA else ControleDados()

            elif flag_se != DJS_OK:
                usn.Usina.normalizar_usina()
                return ControleDados()

            else:
                logger.debug("Heartbeat...")
                # usn.Usina.heartbeat()

                return ControleReservatorio()


class ControleReservatorio(State):
    def __init__(self, *args, **kwargs) -> "None":
        super().__init__(*args, **kwargs)

        usn.Usina.estado_moa = MOA_SM_CONTROLE_RESERVATORIO


    def run(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Chama a função de leitura de valores de operação para depois, chamar a função
        de controle de resrvatório da classe Pai. Caso a função de controle retorne
        o valor de emergência, passa para o estado de Emergência, senão passa para
        o Controle de Dados.
        """

        usn.Usina.ler_valores()
        flag = tda.TomadaAgua.controlar_reservatorio()

        return Emergencia() if flag == NV_EMERGENCIA else ControleDados()


class ControleDados(State):
    def __init__(self, *args, **kwargs) -> "None":
        super().__init__(*args, **kwargs)

        usn.Usina.estado_moa = MOA_SM_CONTROLE_DADOS


    def run(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Chama a função de leitura de valores de operação da classe pai, para
        depois, chamar a função de escrita dos valores no Banco de Dados.
        """

        logger.debug("Escrevendo valores no Banco...")
        usn.Usina.ler_valores()
        usn.Usina.escrever_valores()
        return ControleEstados()


class ControleAgendamentos(State):
    def __init__(self, *args, **kwargs) -> "None":
        super().__init__(*args, **kwargs)

        usn.Usina.estado_moa = MOA_SM_CONTROLE_AGENDAMENTOS


    def run(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Chama a função de verificação de agendamentos pendentes do módulo de
        Agendamentos. Caso haja algum agendamento pendente, retorna ele mesmo após
        a execução do agendamento, para verificar se há mais pendentes. Caso todos
        os agendamentos sejam executados, passa para o estado de Controle de Dados.
        """

        logger.debug("Tratando agendamentos...")
        agn.Agendamentos.verificar_agendamentos()

        if len(agn.Agendamentos.verificar_agendamentos_pendentes()) > 0:
            return self
        else:
            return ControleEstados() if usn.Usina.modo_autonomo else ModoManual()


class ModoManual(State):
    def __init__(self, *args, **kwargs) -> "None":
        super().__init__(*args, **kwargs)

        usn.Usina.estado_moa = MOA_SM_MODO_MANUAL
        usn.Usina.modo_autonomo = False

        for ug in usn.Usina.ugs:
            ug.temporizar_partida = False

        logger.info("Usina em modo manual. Para retornar a operação autônoma, acionar via painel ou página WEB")


    def run(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Primeiramente chama a função de leitura de valores de operação da classe
        Pai. Logo em seguida, atualiza o Setpoint com a leitura atual de potência
        da Unidade, para depois re-calcular o I e IE e escrever os valores atualizados
        no Banco de Dados.
        Caso o modo autônomo seja ativado, realiza uma nova leitura dos valores de
        operação e segue para o Controle de Dados (Retorna ao ciclo normal).
        Se o modo autônomo não foi ativado, segue para o estado de Controle de
        Agendamentos, caso haja algum pendente, senão retorna ele mesmo.
        """

        usn.Usina.ler_valores()

        logger.debug(f"[TDA] Leitura de Nível:                   {tda.TomadaAgua.nv_montante.valor:0.3f}")
        logger.debug(f"[TDA] Leitura de Nível Jusante:           {tda.TomadaAgua.nv_jusante.valor:0.3f}")
        logger.debug(f"[SE]  Potência no medidor:                {se.Subestacao.potencia_ativa.valor:0.3f}")
        logger.debug("")

        for ug in usn.Usina.ugs:
            logger.debug(f"[UG{ug.id}] Unidade:                            \"{UG_SM_STR_DCT[ug.codigo_state]}\"")
            logger.debug(f"[UG{ug.id}] Etapa:                              \"{UG_STR_DCT_ETAPAS[ug.etapa]}\" (Atual: {ug.etapa_atual} | Alvo: {ug.etapa_alvo})")
            logger.debug(f"[UG{ug.id}] Leitura de Potência:                {ug.potencia}")
            logger.debug("")
            ug.setpoint = ug.potencia

        usn.Usina.controle_ie = (usn.Usina.ug1.potencia + usn.Usina.ug2.potencia) / usn.Usina.cfg["pot_maxima_usina"]
        usn.Usina.controle_i = max(min(usn.Usina.controle_ie - (usn.Usina.controle_i * usn.Usina.cfg["ki"]) - usn.Usina.cfg["kp"] * tda.TomadaAgua.erro_nv - usn.Usina.cfg["kd"] * (tda.TomadaAgua.erro_nv - tda.TomadaAgua.erro_nv_anterior), 0.9), 0)

        usn.Usina.escrever_valores()

        sleep(30)

        if usn.Usina.modo_autonomo:
            logger.debug("Comando acionado: \"Habilitar modo autônomo\"")
            usn.Usina.ler_valores()
            sleep(1)
            return ControleDados()

        return ControleAgendamentos() if len(agn.Agendamentos.verificar_agendamentos_pendentes()) > 0 else self


class Emergencia(State):
    def __init__(self, *args, **kwargs) -> "None":
        super().__init__(*args, **kwargs)

        usn.Usina.estado_moa = MOA_SM_EMERGENCIA
        self.tentativas = 0

        logger.critical(f"ATENÇÃO! Usina entrado em estado de emergência. (Horário: {self.get_time()})")


    def run(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Primeiramente chama a função de leitura de valores de operação da classe
        Pai. Logo em seguida, inicia a verificação de tentativas de normalização
        da Usina. Caso o limite de três tentativas seja ultrapassado, indiponibiliza
        a Usina entrando no estado de Modo Manual. Caso o comando seja acionado
        pela interface WEB, entra em um loop de espera até que o comando seja
        desativado, senão entra em Modo Manual, caso seja desativado.
        Caso a verificação de condicionadores retorna que não há mais nenuma ocorrência,
        retorna para o Estado de Controle de Dados para resumir a operação normal.
        """

        usn.Usina.ler_valores()

        if self.tentativas == 3:
            logger.warning("Tentativas de normalização excedidas, entrando em modo manual.")

            for ug in usn.Usina.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()

            return ModoManual()

        elif usn.Usina.bd_emergencia:
            logger.warning("Comando acionado/agendado via página WEB, aguardando reset pela aba \"Emergência\".")

            while usn.Usina.bd_emergencia:
                logger.debug("Aguardando reset...")
                usn.Usina.atualizar_valores_banco(bd.BancoDados.get_parametros_usina())

                if not usn.Usina.bd_emergencia:
                    usn.Usina.bd_emergencia = False
                    return self

                if not usn.Usina.modo_autonomo:
                    usn.Usina.bd_emergencia = False
                    return ModoManual()

                sleep(5)

        else:
            flag_condic = usn.Usina.verificar_condicionadores()

            if flag_condic == CONDIC_INDISPONIBILIZAR:
                logger.critical("Acionando VOIP e entrando em modo manual")
                return ModoManual()

            elif flag_condic == CONDIC_NORMALIZAR:
                self.tentativas += 1
                logger.info(f"Normalizando usina. (Tentativa {self.tentativas}/3) (Limite entre tentativas: {TIMEOUT_NORMALIZACAO}s)")
                usn.Usina.normalizar_forcado = True
                usn.Usina.normalizar_usina()
                return self

            else:
                logger.debug("Usina normalizada. Retomando operação...")
                return ControleDados()