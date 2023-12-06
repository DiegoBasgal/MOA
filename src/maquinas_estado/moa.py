__version__ = "0.2"
__author__ = "Diego Basgal", "Henrique Pfeifer", "Lucas Lavratti"
__description__ = "Este módulo corresponde a implementação da máquina de estados do Módulo de Operação Autônoma."

import sys
import pytz
import logging
import traceback

import src.adufas as ad
import src.usina as usn
import src.subestacao as se
import src.tomada_agua as tda

from time import sleep
from datetime import datetime

from src.dicionarios.const import *


logger = logging.getLogger("logger")


class StateMachine:
    def __init__(self, initial_state) -> "None":

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

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
            logger.error(f"Erro na execução do Estado: {self.state}")
            logger.debug(traceback.format_exc())
            self.state = FalhaCritica()


class State:
    def __init__(self, usina: "usn.Usina"=None, *args, **kwargs) -> "None":

        # VERIFICAÇÃO DE ARGUMENTOS

        if usina is None:
            logger.error(f"Erro ao carregar a classe da Usina na máquina de estados.")
            return FalhaCritica()
        else:
            self.usn = usina

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.args = args
        self.kwargs = kwargs

        self.usn.estado_moa = MOA_SM_NAO_INICIALIZADO


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

        # FINALIZAÇÃO DO __INIT__

        logger.critical("Falha crítica MOA. Interrompendo execução...")
        sys.exit(1)


class Pronto(State):
    def __init__(self, usn, *args, **kwargs)  -> "None":
        super().__init__(usn, *args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_PRONTO


    def run(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Apenas chama a função de leitura de valores de operação da classe Pai e
        depois segue para o estado de Controle de Dados.
        """

        self.usn.ler_valores()
        return ControleEstados(self.usn)


class ControleEstados(State):
    def __init__(self, usn, *args, **kwargs) -> "None":
        super().__init__(usn, *args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_CONTROLE_ESTADOS


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

        self.usn.ler_valores()

        logger.debug("Verificando modo do MOA...")
        if not self.usn.modo_autonomo:
            logger.debug("")
            logger.debug("Comando acionado: \"Desabilitar Modo Autônomo\"")
            return ModoManual(self.usn)

        logger.debug("Verificando status da emergência...")
        if self.usn.clp_emergencia or self.usn.bd_emergencia:
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
            flag_condic = self.usn.verificar_condicionadores()

            if flag_condic == CONDIC_INDISPONIBILIZAR:
                return Emergencia(self.usn)

            elif flag_condic == CONDIC_NORMALIZAR:
                if self.usn.normalizar_usina() and self.usn.tentativas_normalizar > 2:
                    logger.info("Tentativas de Normalização da Usina excedidas!")
                    self.usn.tentativas_normalizar = 0
                    return Emergencia(self.usn)

                else:
                    return ControleDados(self.usn)

            logger.debug("Verificando status da Subestação...")

            if not se.Subestacao.verificar_tensao_trifasica():
                return Emergencia(self.usn) if se.Subestacao.aguardar_tensao() == TENSAO_FORA else self

            elif not se.Subestacao.fechar_dj_linha():
                self.usn.normalizar_forcado = True
                self.usn.normalizar_usina()
                return self

            else:
                return ControleReservatorio(self.usn)


class ControleReservatorio(State):
    def __init__(self, usn, *args, **kwargs) -> "None":
        super().__init__(usn, *args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_CONTROLE_RESERVATORIO


    def run(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Chama a função de leitura de valores de operação para depois, chamar a função
        de controle de resrvatório da classe Pai. Caso a função de controle retorne
        o valor de emergência, passa para o estado de Emergência, senão passa para
        o Controle de Dados.
        """

        self.usn.ler_valores()
        flag = self.usn.controlar_reservatorio()
        self.usn.ad.controlar_comportas()

        return Emergencia(self.usn) if flag == NV_EMERGENCIA else ControleDados(self.usn)


class ControleDados(State):
    def __init__(self, usn, *args, **kwargs) -> "None":
        super().__init__(usn, *args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_CONTROLE_DADOS


    def run(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Chama a função de leitura de valores de operação da classe pai, para
        depois, chamar a função de escrita dos valores no Banco de Dados.
        """

        logger.debug("Escrevendo valores no Banco...")
        self.usn.ler_valores()
        self.usn.escrever_valores()
        return ControleEstados(self.usn)


class ControleAgendamentos(State):
    def __init__(self, *args, **kwargs) -> "None":
        super().__init__(*args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_CONTROLE_AGENDAMENTOS


    def run(self) -> "State":
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Chama a função de verificação de agendamentos pendentes do módulo de
        Agendamentos. Caso haja algum agendamento pendente, retorna ele mesmo após
        a execução do agendamento, para verificar se há mais pendentes. Caso todos
        os agendamentos sejam executados, passa para o estado de Controle de Dados.
        """

        logger.info("Tratando agendamentos...")
        self.usn.agn.verificar_agendamentos()

        if len(self.usn.agn.verificar_agendamentos_pendentes()) > 0:
            return self

        else:
            return ControleEstados(self.usn) if self.usn.modo_autonomo else ModoManual(self.usn)


class ModoManual(State):
    def __init__(self, usn, *args, **kwargs) -> "None":
        super().__init__(usn, *args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_MODO_MANUAL
        self.usn.modo_autonomo = False

        # FINALIZAÇÃO DO __INIT__

        for ug in self.usn.ugs:
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

        self.usn.ler_valores()

        logger.debug(f"[USN] Leitura de Nível:                   {tda.TomadaAgua.nivel_montante.valor:0.3f}")
        logger.debug(f"[USN] Potência no medidor:                {se.Subestacao.medidor_usina.valor:0.3f}")
        logger.debug("")

        for ug in self.usn.ugs:
            logger.debug(f"[UG{ug.id}] Unidade:                            \"{UG_SM_STR_DCT[ug.codigo_state]}\"")
            logger.debug(f"[UG{ug.id}] Etapa atual:                        \"{UG_STR_DCT_ETAPAS[ug.etapa_atual]}\"")
            logger.debug(f"[UG{ug.id}] Leitura de Potência:                {ug.leitura_potencia}")
            logger.debug("")
            ug.setpoint = ug.leitura_potencia

        self.usn.controle_ie = (self.usn.ug1.leitura_potencia + self.usn.ug2.leitura_potencia + self.usn.ug3.leitura_potencia + self.usn.ug4.leitura_potencia) / self.usn.cfg["pot_alvo_usina"]
        self.usn.controle_i = max(min(self.usn.controle_ie - (self.usn.controle_i * self.usn.cfg["ki"]) - self.usn.cfg["kp"] * tda.TomadaAgua.erro_nivel - self.usn.cfg["kd"] * (tda.TomadaAgua.erro_nivel - tda.TomadaAgua.erro_nivel_anterior), 0.8), 0)

        self.usn.escrever_valores()

        sleep(1)

        if self.usn.modo_autonomo:
            logger.debug("Comando acionado: \"Habilitar modo autônomo\"")
            self.usn.ler_valores()
            return ControleDados(self.usn)

        return ControleAgendamentos(self.usn) if len(self.usn.agn.verificar_agendamentos_pendentes()) > 0 else self


class Emergencia(State):
    def __init__(self, usn, *args, **kwargs) -> "None":
        super().__init__(usn, *args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_EMERGENCIA
        self.tentativas = 0

        # FINALIZAÇÃO DO __INIT__

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

        self.usn.ler_valores()

        if self.tentativas == 3:
            logger.warning("Tentativas de normalização excedidas, entrando em modo manual.")

            for ug in self.usn.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()

            return ModoManual(self.usn)

        elif self.usn.bd_emergencia:
            logger.warning("Comando acionado/agendado via página WEB, aguardando reset pela aba \"Emergência\".")

            while self.usn.bd_emergencia:
                logger.debug("Aguardando reset...")
                self.usn.atualizar_valores_banco(self.usn.bd.get_parametros_usina())

                if not self.usn.bd_emergencia:
                    self.usn.bd_emergencia = False
                    return self

                if not self.usn.modo_autonomo:
                    self.usn.bd_emergencia = False
                    return ModoManual(self.usn)

                sleep(5)

        else:
            flag_condic = self.usn.verificar_condicionadores()

            if flag_condic == CONDIC_INDISPONIBILIZAR:
                logger.critical("Acionando VOIP e entrando em modo manual")
                return ModoManual(self.usn)

            elif flag_condic == CONDIC_NORMALIZAR:
                self.tentativas += 1
                logger.info(f"Normalizando usina. (Tentativa {self.tentativas}/3) (Limite entre tentativas: {TIMEOUT_NORMALIZACAO}s)")
                self.usn.normalizar_forcado = True
                self.usn.normalizar_usina()
                return self

            else:
                logger.debug("Usina normalizada. Retomando operação...")
                return ControleDados(self.usn)
