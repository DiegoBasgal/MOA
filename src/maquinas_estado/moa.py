import sys
import pytz
import traceback

import src.dicionarios as d

from time import sleep
from datetime import datetime

from src.usina import *
from src.dicionarios.reg import *
from src.dicionarios.const import *
from src.funcoes.agendamentos import *


class StateMachine:
    def __init__(self, initial_state):

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.state = initial_state


    def exec(self):
        """
        Função principal de execução da Máquina de Estados do MOA.
        """

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


    def get_time(self) -> datetime:
        """
        Função para obter data e hora atual.
        """

        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    def run(self) -> object:
        """
        Função abstrata para execução do passo da Máquina de Estados do MOA.
        """

        return self


class FalhaCritica(State):
    def __init__(self):

        # FINALIZAÇÃO DO __INIT__

        logger.critical("Falha crítica MOA. Interrompendo execução...")
        sys.exit(1)


class Pronto(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_PRONTO


    def run(self):
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Apenas chama a função de leitura de valores de operação da classe Pai e
        depois segue para o estado de Controle de Dados.
        """

        self.usn.ler_valores()
        return ControleEstados(self.usn) if not d.glb["TDA_Offline"] else ControleTDAOffline(self.usn)


class ControleEstados(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_CONTROLE_ESTADOS


    def run(self):
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

        if d.glb["TDA_Offline"]:
            logger.debug("")
            logger.info("Entrando no modo de operação TDA Off-line.")
            return ControleTDAOffline(self.usn)

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
            flag_condic = self.usn.oco.verificar_condicionadores()

            if flag_condic == CONDIC_INDISPONIBILIZAR:
                return Emergencia(self.usn)

            elif flag_condic == CONDIC_NORMALIZAR:
                flag_norm = self.usn.normalizar_usina()

                if flag_norm == NORM_USN_FALTA_TENSAO:
                    return Emergencia(self.usn) if self.usn.aguardar_tensao() == False else ControleDados(self.usn)

                elif flag_norm == NORM_USN_EXECUTADA and self.usn.tentativas_normalizar > 2:
                    logger.info("Tentativas de Normalização da Usina excedidas!")
                    self.usn.tentativas_normalizar = 0
                    return Emergencia(self.usn)

                else:
                    return ControleDados(self.usn)

            else:
                return ControleReservatorio(self.usn)


class ControleReservatorio(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_CONTROLE_RESERVATORIO


    def run(self):
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Chama a função de leitura de valores de operação para depois, chamar a função
        de controle de resrvatório da classe Pai. Caso a função de controle retorne
        o valor de emergência, passa para o estado de Emergência, senão passa para
        o Controle de Dados.
        """

        self.usn.ler_valores()
        flag = self.usn.controlar_reservatorio()

        return Emergencia(self.usn) if flag == NV_FLAG_EMERGENCIA else ControleDados(self.usn)


class ControleDados(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_CONTROLE_DADOS


    def run(self):
        """
        Função para execução do passo da Máquina de Estados do MOA.

        Chama a função de leitura de valores de operação da classe pai, para
        depois, chamar a função de escrita dos valores no Banco de Dados.
        """

        logger.debug("Escrevendo valores no Banco...")
        self.usn.ler_valores()
        self.usn.escrever_valores()
        return ControleEstados(self.usn) if not d.glb["TDA_Offline"] else ControleTDAOffline(self.usn)


class ControleAgendamentos(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_CONTROLE_AGENDAMENTOS


    def run(self):
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
            if self.usn.modo_autonomo:
                return ControleEstados(self.usn) if not d.glb["TDA_Offline"] else ControleTDAOffline(self.usn)
            else:
                return ModoManual(self.usn)


class ModoManual(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_MODO_MANUAL
        self.usn.modo_autonomo = False

        # FINALIZAÇÃO DO __INIT__

        for ug in self.usn.ugs:
            ug.temporizar_partida = False

        logger.info("Usina em modo manual. Para retornar a operação autônoma, acionar via painel ou página WEB")


    def run(self):
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
        logger.debug(f"[USN] Leitura de Nível:                   {self.usn.nv_montante:0.3f}")
        logger.debug(f"[USN] Potência no medidor:                {self.usn.potencia_ativa:0.3f}")
        logger.debug("")

        for ug in self.usn.ugs:
            logger.debug(f"[UG{ug.id}] Unidade:                            \"{UG_SM_STR_DCT[ug.codigo_state]}\"")
            logger.debug(f"[UG{ug.id}] Etapa atual:                        \"{UG_STR_DCT_ETAPAS[ug.etapa_atual]}\"")
            logger.debug(f"[UG{ug.id}] Leitura de Potência:                {ug.leitura_potencia}")
            logger.debug("")
            ug.setpoint = ug.leitura_potencia

        self.usn.controle_ie = (self.usn.ug1.leitura_potencia + self.usn.ug2.leitura_potencia + self.usn.ug3.leitura_potencia) / self.usn.cfg["pot_alvo_usina"]
        self.usn.controle_i = max(min(self.usn.controle_ie - (self.usn.controle_i * self.usn.cfg["ki"]) - self.usn.cfg["kp"] * self.usn.erro_nv - self.usn.cfg["kd"] * (self.usn.erro_nv - self.usn.erro_nv_anterior), 0.8), 0)

        self.usn.escrever_valores()
        if self.usn.modo_autonomo:
            self.usn.ler_valores()
            return ControleDados(self.usn)

        return ControleAgendamentos(self.usn) if len(self.usn.agn.verificar_agendamentos_pendentes()) > 0 else self


class Emergencia(State):
    def __init__(self, usn, *args, **kwargs):
        super().__init__(usn, *args, **kwargs)

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_EMERGENCIA
        self.tentativas = 0

        # FINALIZAÇÃO DO __INIT__

        logger.critical(f"ATENÇÃO! Usina em estado de emergência. (Horário: {self.get_time()})")


    def run(self):
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

        if self.usn.db_emergencia:
            logger.warning("Comando acionado/agendado via página WEB.")

            self.usn.db_emergencia = False

            for ug in self.usn.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()
                sleep(1)

            return ModoManual(self.usn)

        elif self.tentativas == 3:
            logger.warning("Tentativas de normalização excedidas, entrando em modo manual.")

            for ug in self.usn.ugs:
                ug.forcar_estado_indisponivel()
                ug.step()
                sleep(1)

            return ModoManual(self.usn)

        else:
            flag = self.usn.oco.verificar_condicionadores()

            if flag == CONDIC_INDISPONIBILIZAR:
                logger.critical("Acionando VOIP e entrando em modo manual")

                for ug in self.usn.ugs:
                    ug.forcar_estado_indisponivel()
                    ug.step()
                    sleep(1)

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

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.usn.estado_moa = MOA_SM_CONTROLE_RESERVATORIO

        # ATRIBUIÇÃO DE VARIÁVEIS DICT/GLOBAIS

        d.glb["TDA_Offline"] = True

    def run(self):
        """
        Função para execução do passo da Máquina de Estados do MOA.

        O modo de Controle Tomada da Água Offline funciona como o estado de Controle
        de Estados (Estado principal), porém ao final da execução da função, ao
        invés de entrar no estado de Controle de Reservatório, chama a função de
        controle por pressão de caixa espiral, que controla os cálculos de cada
        máquina individualmente.
        """

        self.usn.ler_valores()

        logger.debug("Verificando modo do MOA...")
        if not self.usn.modo_autonomo:
            logger.debug("")
            logger.debug("Comando acionado: \"Desabilitar modo autônomo\"")
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
            flag_condic = self.usn.oco.verificar_condicionadores()

            if flag_condic == CONDIC_INDISPONIBILIZAR:
                return Emergencia(self.usn)

            elif flag_condic == CONDIC_NORMALIZAR:
                flag_norm = self.usn.normalizar_usina()

                if flag_norm == NORM_USN_FALTA_TENSAO:
                    return Emergencia(self.usn) if self.usn.aguardar_tensao() == False else ControleDados(self.usn)

                elif flag_norm == NORM_USN_EXECUTADA and self.usn.tentativas_normalizar > 2:
                    logger.info("Tentativas de Normalização da Usina excedidas!")
                    self.usn.tentativas_normalizar = 0
                    return Emergencia(self.usn)

                else:
                    return ControleDados(self.usn)

            else:
                pot_total_cx = 0

                for ug in self.usn.ugs:
                    pot_total_cx += ug.controle_cx_espiral()

                self.usn.distribuir_potencia(pot_total_cx)

                for ug in self.usn.ugs:
                    ug.step()

                return ControleDados(self.usn)