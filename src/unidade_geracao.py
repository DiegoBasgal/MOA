__version__ = "0.2"
__author__ = "Lucas Lavratti", "Henrique Pfeifer", "Diego Basgal"
__description__ = "Este módulo corresponde a implementação das Unidades de Geração."

import pytz
import logging
import traceback

import src.subestacao as se
import src.tomada_agua as tda
import src.funcoes.condicionadores as c

from time import time, sleep
from threading import Thread
from datetime import datetime

from src.funcoes.leitura import *
from src.maquinas_estado.ug import *

from src.conectores.servidores import Servidores
from src.conectores.banco_dados import BancoDados
from src.funcoes.escrita import EscritaModBusBit as EMB


logger = logging.getLogger("logger")

class UnidadeGeracao:
    def __init__(self, id: "int", cfg: "dict"=None, db: "BancoDados"=None):

        # VERIFICAÇÃO DE ARGUMENTOS

        if id <= 0:
            logger.error(f"[UG{self.id}] A Unidade não pode ser instanciada com o ID <= \"0\" ou vazio.")
            raise ValueError
        else:
            self.__id = id

        self.__db = db
        self.__cfg = cfg

        self.cp = tda.TomadaAgua.cp

        self.clp = Servidores.clp
        self.rele = Servidores.rele

        # ATRIBUIÇÃO DE VAIRIÁVEIS

        # PRIVADAS
        self.__leitura_potencia = LeituraModbus(
            self.clp[f"UG{self.id}"],
            int(REG_CLP[f"UG{self.id}"]["P"]),
            descricao=f"[UG{self.id}] Leitura Potência"
        )
        self.__leitura_etapa_atual = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_CLP[f"UG{self.id}"]["RV_ESTADO_OPERACAO"],
            descricao=f"[UG{self.id}] Leitura Etapa"
        )
        self.__leitura_etapa_alvo = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_CLP[f"UG{self.id}"]["RV_ESTADO_OPERACAO_2"],
            descricao=f"[UG{self.id}] Leitura Etapa"
        )
        self.__leitura_horimetro = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_CLP[f"UG{self.id}"]["HORIMETRO"],
            descricao=f"[UG{self.id}] Leitura Horímetro"
        )

        self.__tempo_entre_tentativas: "int" = 0
        self.__limite_tentativas_normalizacao: "int" = 3

        # PROTEGIDAS
        self._setpoint: "int" = 0
        self._prioridade: "int" = 0
        self._codigo_state: "int" = 0
        self._ultima_etapa_alvo: "int" = 0
        self._ultima_etapa_atual: "int" = 0
        self._tentativas_normalizacao: "int" = 0

        self._setpoint_minimo: "float" = self.__cfg["pot_minima"]
        self._setpoint_maximo: "float" = self.__cfg[f"pot_maxima_ug{self.id}"]

        self._condicionadores: "list[c.CondicionadorBase]" = []
        self._condicionadores_essenciais: "list[c.CondicionadorBase]" = []
        self._condicionadores_atenuadores: "list[c.CondicionadorExponencialReverso]" = []

        # PÚBLICAS
        self.tempo_normalizar: "int" = 0

        self.operar_comporta: "bool" = False
        self.temporizar_partida: "bool" = False
        self.normalizacao_agendada: "bool" = False
        self.temporizar_normalizacao: "bool" = False

        self.borda_cp_fechar: "bool" = False

        self.aux_tempo_sincronizada: "datetime" = 0
        self.ts_auxiliar: "datetime" = self.get_time()

        # FINALIZAÇÃO DO __INIT__

        self.__next_state: "State" = StateDisponivel(self)

        self.carregar_leituras()


    @property
    def id(self) -> "int":
        # PROPRIEDADE -> Retrona o ID da Unidade

        return self.__id

    @property
    def leitura_potencia(self) -> "float":
        # PROPRIEDADE -> Retorna a leitura de Potência da Unidade.

        return self.__leitura_potencia.valor

    @property
    def leitura_horimetro(self) -> "float":
        # PROPRIEDADE -> Retorna a leitura de horas de geração da Unidade.

        return self.__leitura_horimetro.valor

    @property
    def manual(self) -> "bool":
        # PROPRIEDADE -> Verifica se a Unidade está em modo Manual.

        return isinstance(self.__next_state, StateManual)

    @property
    def restrito(self) -> "bool":
        # PROPRIEDADE -> Verifica se a Unidade está em modo Restrito.

        return isinstance(self.__next_state, StateRestrito)

    @property
    def disponivel(self) -> "bool":
        # PROPRIEDADE -> Verifica se a Unidade está em modo Disponível.

        return isinstance(self.__next_state, StateDisponivel)

    @property
    def indisponivel(self) -> "bool":
        # PROPRIEDADE -> Verifica se a Unidade está em modo Indisponível.

        return isinstance(self.__next_state, StateIndisponivel)

    @property
    def limite_tentativas_normalizacao(self) -> "int":
        # PROPRIEDADE -> Retorna o limite pré-definido entre tentativas de normalização.

        return self.__limite_tentativas_normalizacao

    @property
    def etapa_atual(self) -> "int":
        try:
            self._etapa_atual = self.__leitura_etapa_atual.valor
            self._ultima_etapa_atual = self._etapa_atual
            return self._etapa_atual

        except Exception:
            logger.error(f"[UG{self.id}] Erro na leitura de \"Etapa Atual\". Mantendo última etapa.")
            return self._ultima_etapa_atual

    @property
    def etapa_alvo(self) -> "int":
        try:
            self._etapa_alvo = self.__leitura_etapa_alvo.valor
            return self._etapa_alvo

        except Exception:
            logger.error(f"[UG{self.id}] Erro na leitura de \"Etapa Alvo\". Mantendo última etapa.")
            self._etapa_alvo = self._ultima_etapa_alvo
            return self._etapa_alvo

    @property
    def etapa(self) -> "int":
        try:
            if self.etapa_atual == UG_PARADA and self.etapa_alvo == UG_PARADA:
                self._ultima_etapa_alvo = self.etapa_alvo
                return UG_PARADA

            elif self.etapa_atual == UG_SINCRONIZADA and self.etapa_alvo == UG_SINCRONIZADA:
                self._ultima_etapa_alvo = self.etapa_alvo
                return UG_SINCRONIZADA

            elif UG_PARADA < self.etapa_atual <= UG_SINCRONIZADA and self.etapa_alvo == UG_PARADA:

                if self._ultima_etapa_alvo != self.etapa_alvo:
                    if self._ultima_etapa_alvo < self.etapa_alvo:
                        self._ultima_etapa_alvo = self.etapa_alvo
                        return UG_SINCRONIZANDO

                    elif self._ultima_etapa_alvo > self.etapa_alvo:
                        self._ultima_etapa_alvo = self.etapa_alvo
                        return UG_PARANDO

                else:
                    self._ultima_etapa_alvo = self.etapa_alvo
                    return UG_PARANDO

            elif UG_PARADA <= self.etapa_atual < UG_SINCRONIZADA and self.etapa_alvo == UG_SINCRONIZADA:
                if self._ultima_etapa_alvo != self.etapa_alvo:
                    if self._ultima_etapa_alvo > self.etapa_alvo:
                        self._ultima_etapa_alvo = self.etapa_alvo
                        return UG_PARANDO

                    elif self._ultima_etapa_alvo < self.etapa_alvo:
                        self._ultima_etapa_alvo = self.etapa_alvo
                        return UG_SINCRONIZANDO

                else:
                    self._ultima_etapa_alvo = self.etapa_alvo
                    return UG_SINCRONIZANDO

            else:
                return self._ultima_etapa_atual

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro no controle de Etapas da Unidade. Mantendo Etapa anterior.")
            logger.debug(traceback.format_exc())
            return self._ultima_etapa_atual



    @property
    def prioridade(self) -> "int":
        # PROPRIEDADE -> Retorna a prioridade da Unidade.

        return self._prioridade

    @prioridade.setter
    def prioridade(self, var: "int") -> "None":
        # SETTER -> Atribui o novo valor de prioridade da Unidade.

        self._prioridade = var

    @property
    def codigo_state(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de estado da Unidade.

        return self._codigo_state

    @codigo_state.setter
    def codigo_state(self, var: "int") -> "None":
        # SETTER -> Atribui o novo valor de estado da Unidade.

        self._codigo_state = var

    @property
    def setpoint(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de setpoint da Unidade.

        return self._setpoint

    @setpoint.setter
    def setpoint(self, var: "int") -> "None":
        # SETTER -> Atribui o novo valor de setpoint da Unidade.

        if var < self.__cfg["pot_minima"]:
            self._setpoint = 0

        elif var > self.__cfg[f"pot_maxima_ug{self.id}"]:
            self._setpoint = self.__cfg[f"pot_maxima_ug{self.id}"]

        else:
            self._setpoint = int(var)

    @property
    def setpoint_minimo(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de setpoint mínimo da Unidade.

        return self._setpoint_minimo

    @setpoint_minimo.setter
    def setpoint_minimo(self, var: "int"):
        # SETTER -> Atribui o novo valor de setpoint mínimo da Unidade.

        self._setpoint_minimo = var

    @property
    def setpoint_maximo(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de setpoint máximo da Unidade.

        return self._setpoint_maximo

    @setpoint_maximo.setter
    def setpoint_maximo(self, var: "int"):
        # SETTER -> Atribui o novo valor de setpoint máximo da Unidade.

        self._setpoint_maximo = var

    @property
    def tentativas_normalizacao(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de tentativas de normalização da Unidade.

        return self._tentativas_normalizacao

    @tentativas_normalizacao.setter
    def tentativas_normalizacao(self, var: "int") -> "None":
        # SETTER -> Atribui o novo valor de tentativas de normalização da Unidade.

        if 0 <= var and var == int(var):
            self._tentativas_de_normalizacao = int(var)

    @property
    def condicionadores(self) -> "list[c.CondicionadorBase]":
        # PROPRIEDADE -> Retorna a lista de Condicionadores da Unidade.

        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[c.CondicionadorBase]") -> "None":
        # SETTER -> Atribui a nova lista de Condicionadores da Unidade.

        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[c.CondicionadorBase]":
        # PROPRIEDADE -> Retorna a lista de Condicionadores Essenciais da Unidade.

        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[c.CondicionadorBase]") -> "None":
        # SETTER -> Atribui a nova lista de Condicionadores Essenciais da Unidade.

        self._condicionadores_essenciais = var

    @property
    def condicionadores_atenuadores(self) -> "list[c.CondicionadorExponencialReverso]":
        # PROPRIEDADE -> Retorna a lista de Condicionadores Atenuadores da Unidade.

        return self._condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: "list[c.CondicionadorExponencialReverso]") -> "None":
        # SETTER -> Atribui a nova lista de Condicionadores Atenuadores da Unidade.

        self._condicionadores_atenuadores = var

    # FUNÇÕES

    @staticmethod
    def get_time() -> "datetime":
        """
        Função para obter data e hora atual.
        """

        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def forcar_estado_manual(self) -> "None":
        """
        Função para forçar o estado manual na Unidade.
        """

        self.__next_state = StateManual(self)

    def forcar_estado_restrito(self) -> "None":
        """
        Função para forçar o estado restrito na Unidade.
        """

        self.__next_state = StateRestrito(self)

    def forcar_estado_indisponivel(self) -> "None":
        """
        Função para forçar o estado indisponível na Unidade.
        """

        self.__next_state = StateIndisponivel(self)

    def forcar_estado_disponivel(self) -> "None":
        """
        Função para forçar o estado disponível na Unidade.
        """

        self.reconhece_reset_alarmes()
        self.__next_state = StateDisponivel(self)

    def iniciar_ultimo_estado(self) -> "None":
        """
        Função para verificar e atribuir o último estado da Unidade, antes
        da interrupção da última execução do MOA.

        Realiza a consulta no Banco de Dados e atribui o último estado comparando
        com o valor das constantes de Estado.
        """

        estado = self.__db.get_ultimo_estado_ug(self.id)[0]

        if estado == None:
            self.__next_state = StateDisponivel(self)
        else:
            if estado == UG_SM_MANUAL:
                self.__next_state = StateManual(self)
            elif estado == UG_SM_DISPONIVEL:
                self.__next_state = StateDisponivel(self)
            elif estado == UG_SM_RESTRITA:
                self.__next_state = StateRestrito(self)
            elif estado == UG_SM_INDISPONIVEL:
                self.__next_state = StateIndisponivel(self)
            else:
                logger.debug("")
                logger.error(f"[UG{self.id}] Não foi possível ler o último estado da Unidade")
                logger.info(f"[UG{self.id}] Acionando estado \"Manual\".")
                self.__next_state = StateManual(self)

    def step(self) -> "None":
        """
        Função principal de passo da Unidade.

        Serve como principal chamada para controle das Unidades da máquina de estados.
        """

        try:
            logger.debug("")
            logger.debug(f"[UG{self.id}] Step  -> Unidade:                   \"{UG_SM_STR_DCT[self.codigo_state]}\"")
            logger.debug(f"[UG{self.id}]          Etapa:                     \"{UG_STR_DCT_ETAPAS[self.etapa]}\" (Atual: {self.etapa_atual} | Alvo: {self.etapa_alvo})")

            if self.etapa == UG_SINCRONIZADA:
                logger.debug(f"[UG{self.id}]          Leituras de Potência:")
                logger.debug(f"[UG{self.id}]          - \"Ativa\":                 {self.leitura_potencia} kW")

            self.atualizar_modbus_moa()
            self.__next_state = self.__next_state.step()

        except Exception:
            logger.error(f"[UG{self.id}] Erro na execução da máquina de estados da Unidade -> \"step\".")
            logger.debug(traceback.format_exc())

    def atualizar_modbus_moa(self) -> "None":
        """
        Função para atualização do estado da Unidade no CLP - MOA.
        """

        try:
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_ETAPA_UG{self.id}"], [self.etapa])
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_STATE_UG{self.id}"], [self.codigo_state])

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível escrever os valores no CLP MOA.")
            logger.debug(traceback.format_exc())

    def partir(self) -> "None":
        """
        Função para acionamento do comando de partida da Unidade.
        """

        try:
            if self.etapa == UG_PARADA:
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARTIDA\"")

                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PASSOS_CMD_RST_FLH"], valor=1)
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86M_CMD_REARME_BLQ"], valor=1)
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86E_CMD_REARME_BLQ"], valor=1)
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86H_CMD_REARME_BLQ"], valor=1)
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_CMD_REARME_FLH"], valor=1)
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_CMD_REARME_FLH"], valor=1)
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARTIDA_CMD_SINCRONISMO"], valor=1)
                self.enviar_setpoint(self.setpoint)

            else:
                logger.debug(f"[UG{self.id}] A Unidade já está sincronizada.")

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível partir a Unidade.")
            logger.debug(traceback.format_exc())

    def parar(self) -> "None":
        """
        Função para acionamento do comando de Parada da Unidade.

        Verifica se a unidade está sincronizada ou sincronizando. Caso esteja, aciona os comandos
        de parada e reconhecimento de alarmes.
        """

        try:
            if self.etapa in (UG_SINCRONIZADA, UG_SINCRONIZANDO):
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARADA\"")

                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARADA_CMD_DESABILITA_UHLM"], valor=1)
                self.enviar_setpoint(0)

            else:
                logger.debug(f"[UG{self.id}] A Unidade já está parada.")

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível parar a Unidade.")
            logger.debug(traceback.format_exc())

    def enviar_setpoint(self, setpoint_kw: "int") -> "bool":
        """
        Função para envio do valor de setpoint para o controle de potência das
        Unidades.

        Controla os limites máximo e mínimo e logo em seguida, envia o valor calculado para a
        Unidade.
        """

        try:
            logger.debug(f"[UG{self.id}]          Enviando setpoint:         {int(setpoint_kw)} kW")

            if setpoint_kw > 1:
                self.setpoint = int(setpoint_kw)
                res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PASSOS_CMD_RST_FLH"], valor=1)
                res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86M_CMD_REARME_BLQ"], valor=1)
                res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86E_CMD_REARME_BLQ"], valor=1)
                res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86H_CMD_REARME_BLQ"], valor=1)
                res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_CMD_REARME_FLH"], valor=1)
                res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_CMD_REARME_FLH"], valor=1)
                res = self.clp[f"UG{self.id}"].write_single_register(REG_CLP[f"UG{self.id}"]["RV_SETPOT_POT_ATIVA_PU"], int(self.setpoint))

                return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o setpoint para a Unidade.")
            logger.debug(traceback.format_exc())
            return False

    def reconhece_reset_alarmes(self) -> "None":
        """
        Função para reset e reconhecimento de TRIPs.

        Realiza três tentativas de executar as funções de remoção de TRIP elétrico e lógico.
        """

        try:
            logger.debug("")
            logger.info(f"[UG{self.id}]          Enviando comando:          \"RECONHECE E RESET\"")
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["PAINEL_LIDO"], [0])

            passo = 0
            for x in range(2):
                passo += 1
                logger.debug("")
                logger.debug(f"[UG{self.id}]          Passo: {passo}/3")
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
                sleep(1)

            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["PAINEL_LIDO"], [1])

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o comando de reconhecer e resetar alarmes.")
            logger.debug(traceback.format_exc())

    def acionar_trip_logico(self) -> "None":
        """
        Função para acionamento de TRIP lógico.

        Aciona o comando de parada de emergência da Unidade.
        """

        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP LÓGICO\"")
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARADA_CMD_EMERGENCIA"], valor=1)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel acionar o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())

    def remover_trip_logico(self) -> "None":
        """
        Função para remoção de TRIP lógico.

        Aciona os comandos de Reset e Rearmes de Relés, Unidades Hidráulicas, Bloqueios e Falhas.
        """

        try:
            logger.debug(f"[UG{self.id}]          Removendo comando:         \"TRIP LÓGICO\"")
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PASSOS_CMD_RST_FLH"], valor=1)
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86M_CMD_REARME_BLQ"], valor=1)
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86E_CMD_REARME_BLQ"], valor=1)
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86H_CMD_REARME_BLQ"], valor=1)
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_CMD_REARME_FLH"], valor=1)
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_CMD_REARME_FLH"], valor=1)
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86H_BLQ_ATUADO"], valor=0)
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RELE_700G_TRP_ATUADO"], valor=0)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())

    def acionar_trip_eletrico(self) -> "None":
        """
        Função para acionamento de TRIP elétrico.

        Aciona o comando de bloqueio da Unidade através do CLP - MOA.
        """

        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP ELÉTRICO\"")
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{self.id}"], [1])

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel acionar o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())

    def remover_trip_eletrico(self) -> "None":
        """
        Função para remoção de TRIP elétrico.

        Remove o comando de bloqueio da Unidade através do CLP - MOA e fecha o
        Disjuntor 52L (Linha) caso esteja aberto.
        """

        try:
            logger.debug(f"[UG{self.id}]          Removendo comando:         \"TRIP ELÉTRICO\"")
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["PAINEL_LIDO"], [0])
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{self.id}"], [0])
            se.Subestacao.fechar_dj_linha()

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())

    def aguardar_normalizacao(self, delay: "int") -> "None":
        """
        Função de temporizador para espera de normalização da Unidade restrita,
        por tempo pré-definido por agendamento na Interface.
        """

        while not self.temporizar_normalizacao:
            sleep(max(0, time() + delay - time()))
            self.temporizar_normalizacao = True
            return

    def normalizar_unidade(self) -> "bool":
        """
        Função para normalização de ocorrências da Unidade de Geração.

        Primeiramente verifica se a Unidade passou do número de tentativas. Caso
        tenha passado, será chamada a função de forçar estado indisponível, senão
        aciona a função de reconhecimento e reset de alarmes da Unidade.
        """

        if self.tentativas_normalizacao > self.limite_tentativas_normalizacao:
            logger.warning(f"[UG{self.id}] A UG estourou as tentativas de normalização, indisponibilizando Unidade.")
            return False

        elif (self.ts_auxiliar - self.get_time()).seconds > self.__tempo_entre_tentativas:
            self.tentativas_normalizacao += 1
            self.ts_auxiliar = self.get_time()
            logger.info(f"[UG{self.id}] Normalizando Unidade (Tentativa {self.tentativas_normalizacao}/{self.limite_tentativas_normalizacao})")
            self.reconhece_reset_alarmes()
            return True

    def bloquear_unidade(self) -> "None":
        """
        Função para Bloqueio da Unidade nos estados Restrito e Indisponível.

        Verfica se a Unidade está parada e caso não esteja, aciona o comando de parar para logo
        em seguida verificar a comporta. Após a parada total da Unidade, verifica se a comporta
        está aberta ou em cracking. Caso esteja, aciona o comando de fechamento da comporta, mas
        caso já esteja fechada, aciona os comandos de TRIP lógico e elétrico. Caso a comporta
        esteja operando, avisa o operador e aguarda o fechamento completo.
        """

        self.temporizar_partida = False

        if self.etapa == UG_PARADA:
            if self.cp[f"CP{self.id}"].etapa in (CP_ABERTA, CP_CRACKING):
                self.cp[f"CP{self.id}"].fechar()

            elif self.cp[f"CP{self.id}"].etapa == CP_FECHADA:
                self.acionar_trip_eletrico()
                self.acionar_trip_logico()

            else:
                logger.debug(f"[UG{self.id}] A comporta {self.id} deve estar completamente fechada para acionar o bloqueio da UG")

        elif not self.borda_parar and self.parar():
            self.borda_parar = True

    def verificar_sincronismo(self) -> "None":
        """
        Função de verificação de partida da Unidade.

        Caso a unidade seja totalmente sincronizada, o timer é encerrado e avisado,
        senão, é enviado o comando de parada de emergência para a Unidade.
        """

        logger.debug(f"[UG{self.id}]          Verificação MOA:           \"Temporização de Sincronismo\"")
        while time() < time() + 600:
            if not self.temporizar_partida:
                return

        logger.warning(f"[UG{self.id}]          Verificação MOA:          \"Acionar emergência por timeout de Sincronismo\"")
        EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARADA_CMD_EMERGENCIA"], valor=1)
        self.temporizar_partida = False
        sleep(1)

    def atenuar_carga(self) -> "None":
        """
        Função para atenuação de carga através de leitura de Pressão na Entrada da Turbina.

        Calcula o ganho e verifica os limites máximo e mínimo para deteminar se
        deve atenuar ou não.
        """

        atenuacao = 0
        for condic in self.condicionadores_atenuadores:
            atenuacao = max(atenuacao, condic.valor)
            logger.debug(f"[UG{self.id}]          Verificando Atenuadores:")
            logger.debug(f"[UG{self.id}]          - \"{condic.descr}\":   Leitura: {condic.leitura.valor} | Atenuação: {atenuacao}")

        ganho = 1 - atenuacao
        aux = self.setpoint
        if (self.setpoint > self.setpoint_minimo) and self.setpoint * ganho > self.setpoint_minimo:
            self.setpoint = self.setpoint * ganho

        elif (self.setpoint * ganho < self.setpoint_minimo) and (self.setpoint > self.setpoint_minimo):
            self.setpoint =  self.setpoint_minimo

        logger.debug(f"[UG{self.id}]                                     SP {aux} * GANHO {ganho} = {self.setpoint} kW")

    def controlar_etapas(self) -> "None":
        """
        Função para controle de etapas da Unidade.

        PARANDO -> Chama a função de controle de comporta caso seja atribuído um valor
        de setpoint, senão aciona o comando de fechamento da Comporta caso o valor da
        potência caia abaixo de 300 kW.
        PARADA -> Chama a função de controle de comporta caso seja atribuído um valor
        de setpoint, senão apenas envia o setpoint (boa prática).
        SINCRONIZANDO -> Chama o comando de enviar setpoint, senão caiona o comando de
        parada caso o setpoint retorne 0.
        SINCRONIZADA -> Controla a variável de tempo sincronizada e envia o comando
        de parada caso seja atribuído o setpoint 0 para a Unidade.
        """

        if self.etapa == UG_PARADA:
            if self.setpoint >= self.__cfg["pot_minima"]:
                self.controlar_comporta()

            elif self.setpoint == 0 and not self.borda_cp_fechar:
                self.borda_cp_fechar = True
                logger.debug(f"[UG{self.id}]          Comando MOA:               \"OPERAR COMPORTA\"")
                if not self.cp[f"CP{self.id}"].fechar():
                    self.borda_cp_fechar = False

        elif self.etapa == UG_PARANDO:
            if self.setpoint >= self.__cfg["pot_minima"]:
                self.controlar_comporta()
            else:
                self.enviar_setpoint(self.setpoint)

        elif self.etapa == UG_SINCRONIZANDO:
            self.borda_cp_fechar = False
            if not self.temporizar_partida:
                self.temporizar_partida = True
                Thread(target=lambda: self.verificar_sincronismo()).start()

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        elif self.etapa == UG_SINCRONIZADA:
            self.temporizar_partida = False

            if not self.aux_tempo_sincronizada:
                self.aux_tempo_sincronizada = self.get_time()

            elif (self.get_time() - self.aux_tempo_sincronizada).seconds >= 300:
                self.tentativas_normalizacao = 0

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        if not self.etapa == UG_SINCRONIZADA:
            self.aux_tempo_sincronizada = None

    def controlar_comporta(self):
        """
        Função para controlar a Comporta equivalente ao ID da Unidade.

        Verifica se a comporta está fechada e caso esteja, aciona o comando de Cracking.
        Se a comporta estiver em Cracking, aciona o comando de aguardar equalização da
        pressão da UH, para que no momento da equalização da pressão, acionar o comando
        de abertura.
        No momento em que a comporta retorne que está totalmente aberta, aciona o comando
        de partida da Unidade, para daí acionar o mecanismo de aguardar sincronismo.
        Caso a comporta esteja em modo Remoto ou Operando, avisa o oeprador e retorna.
        """
        logger.debug(f"[UG{self.id}]          Comando MOA:               \"OPERAR COMPORTA\"")
        logger.debug("")
        logger.debug(f"[CP{self.id}] Step  -> Comporta:                  \"{'Disponível' if not self.cp[f'CP{self.id}'].operando else 'Operando'}\"")
        logger.debug(f"[CP{self.id}]          Etapa:                     \"{CP_STR_DCT[self.cp[f'CP{self.id}'].etapa]}\"")

        try:
            if self.cp[f"CP{self.id}"].etapa == CP_FECHADA:
                self.cp[f"CP{self.id}"].ultima_etapa = CP_FECHADA
                self.cp[f"CP{self.id}"].operar_cracking()

            elif self.cp[f"CP{self.id}"].etapa == CP_CRACKING:
                self.cp[f"CP{self.id}"].ultima_etapa = CP_CRACKING

                if self.cp[f"CP{self.id}"].pressao_equalizada:
                    self.cp[f"CP{self.id}"].abrir()

                elif self.setpoint == 0 and self.leitura_potencia == 0:
                    self.cp[f"CP{self.id}"].fechar()

            elif self.cp[f"CP{self.id}"].etapa == CP_ABERTA:
                self.cp[f"CP{self.id}"].ultima_etapa = CP_ABERTA

                if self.leitura_potencia == 0 and self.setpoint != 0:
                    self.partir()

            elif self.cp[f"CP{self.id}"].etapa == CP_REMOTO:
                logger.debug(f"[CP{self.id}]          Comporta em modo manual")
                pass

        except Exception:
            logger.error(f"[CP{self.id}] Erro ao operar Comporta.")
            logger.debug(traceback.format_exc())

    def verificar_condicionadores(self) -> "int":
        """
        Função para a verificação de acionamento de condicionadores e determinação
        de gravidade.

        Itera sobre a lista de condicionadores da Unidade e verifica se algum está
        ativo. Caso esteja, verifica o nível de gravidade e retorna o valor para
        a determinação do passo seguinte.
        Caso não haja nenhum condicionador ativo, apenas retorna o valor de ignorar.
        """

        flag = CONDIC_IGNORAR
        v = []

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            for condic in condics_ativos:
                if condic.gravidade == CONDIC_NORMALIZAR:
                    flag = CONDIC_NORMALIZAR
                elif condic.gravidade == CONDIC_AGUARDAR:
                    flag = CONDIC_AGUARDAR
                elif condic.gravidade == CONDIC_INDISPONIBILIZAR:
                    flag = CONDIC_INDISPONIBILIZAR

            logger.debug("")
            logger.info(f"[UG{self.id}] Foram detectados condicionadores ativos!")
            [logger.info(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade]}\"") for condic in condics_ativos]
            logger.debug("")

            return flag
        return flag


    def atualizar_limites(self, parametros: "dict") -> "None":
        """
        Função para extração de valores do Banco de Dados da Interface WEB e atribuição
        de novos limites de operação de condicionadores.
        """

        try:
            self.prioridade = int(parametros[f"ug{self.id}_prioridade"])

            self.condicionador_temperatura_fase_r_ug.valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{self.id}"])
            self.condicionador_temperatura_fase_s_ug.valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{self.id}"])
            self.condicionador_temperatura_fase_t_ug.valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{self.id}"])
            self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_1_ug{self.id}"])
            self.condicionador_temperatura_mancal_guia_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_ug{self.id}"])
            self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_interno_1_ug{self.id}"])
            self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_interno_2_ug{self.id}"])
            self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base = float(parametros[f"alerta_temperatura_patins_mancal_comb_1_ug{self.id}"])
            self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base = float(parametros[f"alerta_temperatura_patins_mancal_comb_2_ug{self.id}"])
            self.condicionador_temperatura_mancal_casq_comb_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_casq_comb_ug{self.id}"])
            self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_contra_esc_comb_ug{self.id}"])
            self.condicionador_pressao_turbina_ug.valor_base = float(parametros[f"alerta_pressao_turbina_ug{self.id}"])

            self.condicionador_temperatura_fase_r_ug.valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{self.id}"])
            self.condicionador_temperatura_fase_s_ug.valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{self.id}"])
            self.condicionador_temperatura_fase_t_ug.valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{self.id}"])
            self.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_1_ug{self.id}"])
            self.condicionador_temperatura_mancal_guia_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_ug{self.id}"])
            self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_interno_1_ug{self.id}"])
            self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_interno_2_ug{self.id}"])
            self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_limite = float(parametros[f"limite_temperatura_patins_mancal_comb_1_ug{self.id}"])
            self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_limite = float(parametros[f"limite_temperatura_patins_mancal_comb_2_ug{self.id}"])
            self.condicionador_temperatura_mancal_casq_comb_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_casq_comb_ug{self.id}"])
            self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_contra_esc_comb_ug{self.id}"])
            self.condicionador_pressao_turbina_ug.valor_limite = float(parametros[f"limite_pressao_turbina_ug{self.id}"])

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores.")
            logger.debug(traceback.format_exc())

    def verificar_limites(self) -> "None":
        """
        Função para verificação de limites de operação da Unidade.

        Verifica os valores base e limite da Unidade, pré-determinados na interface
        WEB, e avisa o operador caso algum valor ultrapasse o estipulado.
        """

        if self.leitura_temperatura_fase_R.valor >= self.condicionador_temperatura_fase_r_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase R da UG passou do valor base! ({self.condicionador_temperatura_fase_r_ug.valor_base}C) | Leitura: {self.leitura_temperatura_fase_R.valor}C")
        if self.leitura_temperatura_fase_R.valor >= 0.9*(self.condicionador_temperatura_fase_r_ug.valor_limite - self.condicionador_temperatura_fase_r_ug.valor_base) + self.condicionador_temperatura_fase_r_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase R da UG está muito próxima do limite! ({self.condicionador_temperatura_fase_r_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_fase_R.valor}C")

        if self.leitura_temperatura_fase_S.valor >= self.condicionador_temperatura_fase_s_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase S da UG passou do valor base! ({self.condicionador_temperatura_fase_s_ug.valor_base}C) | Leitura: {self.leitura_temperatura_fase_S.valor}C")
        if self.leitura_temperatura_fase_S.valor >= 0.9*(self.condicionador_temperatura_fase_s_ug.valor_limite - self.condicionador_temperatura_fase_s_ug.valor_base) + self.condicionador_temperatura_fase_s_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase S da UG está muito próxima do limite! ({self.condicionador_temperatura_fase_s_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_fase_S.valor}C")

        if self.leitura_temperatura_fase_T.valor >= self.condicionador_temperatura_fase_t_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase T da UG passou do valor base! ({self.condicionador_temperatura_fase_t_ug.valor_base}C) | Leitura: {self.leitura_temperatura_fase_T.valor}C")
        if self.leitura_temperatura_fase_T.valor >= 0.9*(self.condicionador_temperatura_fase_t_ug.valor_limite - self.condicionador_temperatura_fase_t_ug.valor_base) + self.condicionador_temperatura_fase_t_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase T da UG está muito próxima do limite! ({self.condicionador_temperatura_fase_t_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_fase_T.valor}C")

        if self.leitura_temperatura_nucleo_gerador_1.valor >= self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Núcleo Gerador 1 da UG passou do valor base! ({self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base}C) | Leitura: {self.leitura_temperatura_nucleo_gerador_1.valor}C")
        if self.leitura_temperatura_nucleo_gerador_1.valor >= 0.9*(self.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite - self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base) + self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Núcleo Gerador 1 da UG está muito próxima do limite! ({self.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_nucleo_gerador_1.valor}C")

        if self.leitura_temperatura_mancal_guia.valor >= self.condicionador_temperatura_mancal_guia_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Guia da UG passou do valor base! ({self.condicionador_temperatura_mancal_guia_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mancal_guia.valor}C")
        if self.leitura_temperatura_mancal_guia.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_ug.valor_limite - self.condicionador_temperatura_mancal_guia_ug.valor_base) + self.condicionador_temperatura_mancal_guia_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Guia da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_guia_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mancal_guia.valor}C")

        if self.leitura_temperatura_mancal_guia_interno_1.valor >= self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Guia Interno 1 da UG passou do valor base! ({self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mancal_guia_interno_1.valor}C")
        if self.leitura_temperatura_mancal_guia_interno_1.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_limite - self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base) + self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Guia Interno 1 da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mancal_guia_interno_1.valor}C")

        if self.leitura_temperatura_mancal_guia_interno_2.valor >= self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Guia Interno 2 da UG passou do valor base! ({self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mancal_guia_interno_2.valor}C")
        if self.leitura_temperatura_mancal_guia_interno_2.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_limite - self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base) + self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Guia Interno 2 da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mancal_guia_interno_2.valor}C")

        if self.leitura_temperatura_patins_mancal_comb_1.valor >= self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura dos Patins do Mancal combinado 1 da UG passou do valor base! ({self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base}C) | Leitura: {self.leitura_temperatura_patins_mancal_comb_1.valor}C")
        if self.leitura_temperatura_patins_mancal_comb_1.valor >= 0.9*(self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_limite - self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base) + self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura dos Patins do Mancal combinado 1 da UG está muito próxima do limite! ({self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_patins_mancal_comb_1.valor}C")

        if self.leitura_temperatura_patins_mancal_comb_2.valor >= self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura dos Patins do Mancal combinado 2 da UG passou do valor base! ({self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base}C) | Leitura: {self.leitura_temperatura_patins_mancal_comb_2.valor}C")
        if self.leitura_temperatura_patins_mancal_comb_2.valor >= 0.9*(self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_limite - self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base) + self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura dos Patins do Mancal combinado 2 da UG está muito próxima do limite! ({self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_patins_mancal_comb_2.valor}C")

        if self.leitura_temperatura_mancal_casq_comb.valor >= self.condicionador_temperatura_mancal_casq_comb_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Casquilho combinado da UG passou do valor base! ({self.condicionador_temperatura_mancal_casq_comb_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mancal_casq_comb.valor}C")
        if self.leitura_temperatura_mancal_casq_comb.valor >= 0.9*(self.condicionador_temperatura_mancal_casq_comb_ug.valor_limite - self.condicionador_temperatura_mancal_casq_comb_ug.valor_base) + self.condicionador_temperatura_mancal_casq_comb_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Casquilho combinado da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_casq_comb_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mancal_casq_comb.valor}C")

        if self.leitura_temperatura_mancal_contra_esc_comb.valor >= self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Contra Escora combinado da UG passou do valor base! ({self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mancal_contra_esc_comb.valor}C")
        if self.leitura_temperatura_mancal_contra_esc_comb.valor >= 0.9*(self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_limite - self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base) + self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Contra Escora combinado da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mancal_contra_esc_comb.valor}C")

        if self.leitura_pressao_turbina.valor <= self.condicionador_pressao_turbina_ug.valor_base and self.leitura_pressao_turbina.valor != 0 and self.etapa == UG_SINCRONIZADA:
            logger.warning(f"[UG{self.id}] A pressão na entrada da turbina da UG passou do valor base! ({self.condicionador_pressao_turbina_ug.valor_base:03.2f} KGf/m2) | Leitura: {self.leitura_pressao_turbina.valor:03.2f}")
        if self.leitura_pressao_turbina.valor <= self.condicionador_pressao_turbina_ug.valor_limite+0.9*(self.condicionador_pressao_turbina_ug.valor_base - self.condicionador_pressao_turbina_ug.valor_limite) and self.leitura_pressao_turbina.valor != 0 and self.etapa == UG_SINCRONIZADA:
            logger.critical(f"[UG{self.id}] A pressão na entrada da turbina da UG está muito próxima do limite! ({self.condicionador_pressao_turbina_ug.valor_limite:03.2f} KGf/m2) | Leitura: {self.leitura_pressao_turbina.valor:03.2f} KGf/m2")

    def verificar_leituras(self) -> "None":
        """
        Função para consulta de acionamentos da Unidade e avisos através do mecanismo
        de acionamento temporizado.
        """

        if self.leitura_saidas_digitais_rv_b0.valor:
            logger.warning(f"[UG{self.id}] O alarme do Regulador de Velocidade da UG foi acionado. Favor verificar.")

        if self.leitura_saidas_digitais_rt_b0.valor:
            logger.warning(f"[UG{self.id}] O alarme do Regulador de Tensão da UG foi acionado. Favor verificar.")

        if self.leitura_falha_3_rt_b0.valor:
            logger.warning(f"[UG{self.id}] Houve uma falha na leitura de potência reativa pelo Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b1.valor:
            logger.warning(f"[UG{self.id}] Houve uma falha na leitura da tensão terminal pelo Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b2.valor:
            logger.warning(f"[UG{self.id}] Houve uma falha na leitura principal da corrente de excitação pelo Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b3.valor:
            logger.warning(f"[UG{self.id}] Houve uma falha na leitura retaguarda da corrente de excitação pelo Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b4.valor:
            logger.warning(f"[UG{self.id}] Foi identificado ruído na instrumentação de reativo do Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b5.valor:
            logger.warning(f"[UG{self.id}] Foi identificado ruído na instrumentação de tensão do Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b6.valor:
            logger.warning(f"[UG{self.id}] Foi identificado ruído na instrumentação de excitação principal do Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b7.valor:
            logger.warning(f"[UG{self.id}] Foi identificado ruído na instrumentação de excitação retaguarda do Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_1_rv_b4.valor:
            logger.warning(f"[UG{self.id}] Houve uma falha de leitura de posição do distribuidor pelo Regulador de Velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b5.valor:
            logger.warning(f"[UG{self.id}] Houve uma falha de leitura de posição do rotor pelo Regulador de Velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b6.valor:
            logger.warning(f"[UG{self.id}] Houve uma falha de leitura de potência ativa pelo Regulador de Velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b7.valor:
            logger.warning(f"[UG{self.id}] Houve uma falha de leitura de referência de potência pelo Regulador de Velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b8.valor:
            logger.warning(f"[UG{self.id}] Houve uma falha de leitura de nível montante pelo Regulador de Velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b13.valor:
            logger.warning(f"[UG{self.id}] Foi identificado ruído na medição principal de velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b14.valor:
            logger.warning(f"[UG{self.id}] Foi identificado ruído na medição retaguarda de velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b15.valor:
            logger.warning(f"[UG{self.id}] Foi identificada perda na medição principal de velocidade da UG. Favor verificar.")

        if self.leitura_falha_2_rv_b0.valor:
            logger.warning(f"[UG{self.id}] Foi identificada perda na medição retaguarda de velocidade da UG. Favor verificar.")

        if self.leitura_falha_2_rv_b4.valor:
            logger.warning(f"[UG{self.id}] Foi identificada diferença entre medidor principal e retaguarda da UG. Favor verificar.")

        if self.leitura_unidade_manutencao_uhrv.valor:
            logger.warning(f"[UG{self.id}] UHRV da UG entrou em modo de manutenção")

        if self.leitura_unidade_manutencao_uhlm.valor:
            logger.warning(f"[UG{self.id}] UHLM da UG entrou em modo de manutenção")

        if not self.leitura_filtro_sujo_uhrv.valor:
            logger.warning(f"[UG{self.id}] O filtro da UHRV da UG está sujo. Favor realizar limpeza/troca.")

        if not self.leitura_filtro_sujo_uhrv.valor:
            logger.warning(f"[UG{self.id}] O filtro da UHLM da UG está sujo. Favor realizar limpeza/troca.")

        if not self.leitura_porta_interna_fechada_cpg.valor:
            logger.warning(f"[UG{self.id}] A porta interna do CPG da UG está aberta. Favor fechar.")

        if not self.leitura_porta_traseira_fechada_cpg.valor:
            logger.warning(f"[UG{self.id}] A porta traseira do CPG da UG está aberta. Favor fechar.")

        if not self.leitura_resistencia_falha.valor:
            logger.warning(f"[UG{self.id}] Houve uma falha na resistência da UG. Favor verificar.")

        if self.leitura_escovas_gastas_polo_positivo.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que as escovas do polo positivo da UG estão gastas. Favor verificar.")

        if self.leitura_escovas_gastas_polo_negativo.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que as escovas do polo negativo da UG estão gastas. Favor verificar.")

        if self.leitura_alarme_temp_ponte_fase_a.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura da pote fase A foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_ponte_fase_b.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura da pote fase B foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_ponte_fase_c.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura da pote fase C foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_trafo_excitacao.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do transformador excitação foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_mancal_guia.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do mancal guia foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_oleo_uhrv.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura de óleo da UHRV foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_oleo_uhlm.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura de óleo da UHLM foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_mancal_casq_comb.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do mancal casquilho combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_mancal_con_esc_comb.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do mancal contra escora combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_patins_1_mancal_comb.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do patins 1 mancal combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_patins_2_mancal_comb.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do patins 2 mancal combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_mancal_guia_interno_1.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do mancal guia interno 1 foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_mancal_guia_interno_2.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do mancal guia interno 2 foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_nucleo_estatorico_gerador.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do núcleo estatórico do gerador foi acionado. Favor verificar.")

        if self.leitura_temp_fase_a_gerador.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura de fase A do gerador foi acionado. Favor verificar.")

        if self.leitura_temp_fase_b_gerador.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura de fase B do gerador foi acionado. Favor verificar.")

        if self.leitura_temp_fase_c_gerador.valor:
            logger.warning(f"[UG{self.id}] O alarme de temperatura de fase C do gerador foi acionado. Favor verificar.")

        if self.leitura_alarme_vibra_eixo_x_mancal_comb.valor:
            logger.warning(f"[UG{self.id}] O alarme de vibração do eixo X do mancal combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_vibra_eixo_y_mancal_comb.valor:
            logger.warning(f"[UG{self.id}] O alarme de vibração do eixo Y do mancal combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_vibra_eixo_z_mancal_comb.valor:
            logger.warning(f"[UG{self.id}] O alarme de vibração do eixo Z do mancal combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_vibra_detec_horizontal.valor:
            logger.warning(f"[UG{self.id}] O alarme de vibração detecção horizontal foi acionado. Favor verificar.")

        if self.leitura_alarme_vibra_detec_vertical.valor:
            logger.warning(f"[UG{self.id}] O alarme de vibração detecção vertical foi acionado. Favor verificar.")

    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """

        # LEITURA PERIODICA
        # Transformador Excitação
        self.leitura_alarme_temp_trafo_excitacao = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["TRAFO_EXCITACAO_ALM_TMP"],  descricao=f"[UG{self.id}] Transformador Excitação Alarme Temperatura")

        # UHRV
        self.leitura_unidade_manutencao_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_MANUTENCAO"], descricao=f"[UG{self.id}] UHRV Manutenção")
        self.leitura_alarme_temp_oleo_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_ALM_TMP_OLEO"], descricao=f"[UG{self.id}] UHRV Alarme Temperatura Óleo")
        self.leitura_filtro_sujo_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_FILTRO_SUJO"], invertido=True, descricao=f"[UG{self.id}] UHRV Status Filtro")

        # UHLM
        self.leitura_unidade_manutencao_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_MANUTENCAO"], descricao=f"[UG{self.id}] UHLM Manutenção")
        self.leitura_alarme_temp_oleo_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_ALM_TMP_OLEO"], descricao=f"[UG{self.id}] UHLM Alarme Temperatura Óleo")
        self.leitura_filtro_sujo_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_FILTRO_SUJO"], invertido=True, descricao=f"[UG{self.id}] UHLM Status Filtro")

        # Resistência
        self.leitura_resistencia_falha = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RESISTENCIA_FALHA"], invertido=True, descricao=f"[UG{self.id}] Resistência Falha")

        # Comporta Gerador
        self.leitura_porta_interna_fechada_cpg = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["CPG_PORTA_INTERNA_FECHADA"], invertido=True, descricao=f"[UG{self.id}] Comporta Porta Interna Fechada")
        self.leitura_porta_traseira_fechada_cpg = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["CPG_PORTA_TRASEIRA_FECHADA"], invertido=True, descricao=f"[UG{self.id}] Comporta Porta Traseira Fechada")

        # RV
        self.leitura_falha_1_rv_b6 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B6"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 06")
        self.leitura_falha_1_rv_b7 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B7"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 07")
        self.leitura_falha_1_rv_b8 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B8"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 08")
        self.leitura_falha_1_rv_b14 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B14"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 14")
        self.leitura_falha_1_rv_b15 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B15"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 15")
        self.leitura_falha_2_rv_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_2_B0"], descricao=f"[UG{self.id}] RV Falha 2 - Bit 00")
        self.leitura_falha_2_rv_b4 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_2_B4"], descricao=f"[UG{self.id}] RV Falha 2 - Bit 04")
        self.leitura_saidas_digitais_rv_b0 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_SAIDAS_DIGITAIS"],  descricao=f"[UG{self.id}] RV Saídas Digitais - Bit 00")

        # RT
        self.leitura_falha_3_rt_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B0"], descricao=f"[UG{self.id}] RT Falha 3 - Bit 00")
        self.leitura_falha_3_rt_b1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B1"], descricao=f"[UG{self.id}] RT Falha 3 - Bit 01")
        self.leitura_falha_3_rt_b2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B2"], descricao=f"[UG{self.id}] RT Falha 3 - Bit 02")
        self.leitura_falha_3_rt_b3 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B3"], descricao=f"[UG{self.id}] RT Falha 3 - Bit 03")
        self.leitura_falha_3_rt_b4 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B4"], descricao=f"[UG{self.id}] RT Falha 3 - Bit 04")
        self.leitura_falha_3_rt_b5 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B5"], descricao=f"[UG{self.id}] RT Falha 3 - Bit 05")
        self.leitura_falha_3_rt_b6 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B6"], descricao=f"[UG{self.id}] RT Falha 3 - Bit 06")
        self.leitura_falha_3_rt_b7 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B7"], descricao=f"[UG{self.id}] RT Falha 3 - Bit 07")
        self.leitura_saidas_digitais_rt_b0 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_SAIDAS_DIGITAIS"], descricao=f"[UG{self.id}] RT Saídas Digitais - Bit 00")

        # Leitura Escovas Polo
        self.leitura_escovas_gastas_polo_positivo = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["ESCOVAS_POLO_POS_GASTAS"], descricao=f"[UG{self.id}] Escovas Polo Positivo Gastas")
        self.leitura_escovas_gastas_polo_negativo = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["ESCOVAS_POLO_NEG_GASTAS"], descricao=f"[UG{self.id}] Escovas Polo Negativo Gastas")

        # Leitura Gerador
        self.leitura_temp_fase_a_gerador = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_A_ALM_TMP"], descricao=f"[UG{self.id}] Gerador Fase A Alarme Temperatura")
        self.leitura_temp_fase_b_gerador = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_B_ALM_TMP"], descricao=f"[UG{self.id}] Gerador Fase B Alarme Temperatura")
        self.leitura_temp_fase_c_gerador = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_C_ALM_TMP"], descricao=f"[UG{self.id}] Gerador Fase C Alarme Temperatura")
        self.leitura_alarme_temp_nucleo_estatorico_gerador = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_NUCL_ESTAT_ALM_TMP"], descricao=f"[UG{self.id}] Gerador Núcleo Estatórico Alarme Temperatura")

        # Leitura Ponte Fase
        self.leitura_alarme_temp_ponte_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_A_ALM_TMP"], descricao=f"[UG{self.id}] Ponte Fase A Alarme Temperatura")
        self.leitura_alarme_temp_ponte_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_B_ALM_TMP"], descricao=f"[UG{self.id}] Ponte Fase B Alarme Temperatura")
        self.leitura_alarme_temp_ponte_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_C_ALM_TMP"], descricao=f"[UG{self.id}] Ponte Fase C Alarme Temperatura")

        # Leitura Vibração
        self.leitura_alarme_vibra_detec_vertical = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DETECCAO_VERTICAL_ALM_VIBRA"], descricao=f"[UG{self.id}] Detecção Vibração Vertical Alarme")
        self.leitura_alarme_vibra_detec_horizontal = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DETECCAO_HORIZONTAL_ALM_VIBRA"], descricao=f"[UG{self.id}] Detecção Vibração Horizontal Alarme")
        self.leitura_alarme_vibra_eixo_x_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_X_ALM_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Alarme Vibração Eixo X")
        self.leitura_alarme_vibra_eixo_y_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_Y_ALM_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Alarme Vibração Eixo Y")
        self.leitura_alarme_vibra_eixo_z_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_Z_ALM_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Alarme Vibração Eixo Z")

        # Leituras Mancais
        self.leitura_alarme_temp_mancal_guia = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_ALM_TMP"],  descricao=f"[UG{self.id}] Mancal Guia Alarme Temperatura")
        self.leitura_alarme_temp_mancal_casq_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CASQ_COMB_ALM_TMP"],  descricao=f"[UG{self.id}] Mancal Casquilho Combinado Alarme Temperatura")
        self.leitura_alarme_temp_mancal_guia_interno_1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_1_ALM_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 1 Alarme Temperatura")
        self.leitura_alarme_temp_mancal_guia_interno_2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_2_ALM_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 2 Alarme Temperatura")
        self.leitura_alarme_temp_patins_1_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_1_ALM_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 1 Alarme Temperatura")
        self.leitura_alarme_temp_patins_2_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_2_ALM_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 2 Alarme Temperatura")
        self.leitura_alarme_temp_mancal_con_esc_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CONT_ESCO_COMB_ALM_TMP"], descricao=f"[UG{self.id}] Mancal Combinado Contra Escora Alarme Temperatura")


        # CONDICIONADORES ESSENCIAIS
        # Temperaturas
            # Fase R
        self.leitura_temperatura_fase_R = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_A_TMP"], descricao=f"[UG{self.id}] Fase A Temperatura")
        self.condicionador_temperatura_fase_r_ug = c.CondicionadorExponencial(self.leitura_temperatura_fase_R)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_r_ug)

            # Fase S
        self.leitura_temperatura_fase_S = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_B_TMP"], descricao=f"[UG{self.id}] Fase B Temperatura")
        self.condicionador_temperatura_fase_s_ug = c.CondicionadorExponencial(self.leitura_temperatura_fase_S)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_s_ug)

            # Fase T
        self.leitura_temperatura_fase_T = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_C_TMP"], descricao=f"[UG{self.id}] Fase C Temperatura")
        self.condicionador_temperatura_fase_t_ug = c.CondicionadorExponencial(self.leitura_temperatura_fase_T)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_t_ug)

            # Nucleo Gerador 1
        self.leitura_temperatura_nucleo_gerador_1 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_NUCL_ESTAT_TMP"], descricao=f"[UG{self.id}] Núcleo Gerador Temperatura")
        self.condicionador_temperatura_nucleo_gerador_1_ug = c.CondicionadorExponencial(self.leitura_temperatura_nucleo_gerador_1)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_gerador_1_ug)

            # Mancal Guia
        self.leitura_temperatura_mancal_guia = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_TMP"], descricao=f"[UG{self.id}] Mancal Guia Temperatura")
        self.condicionador_temperatura_mancal_guia_ug = c.CondicionadorExponencial(self.leitura_temperatura_mancal_guia)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_ug)

            # Mancal Guia Interno 1
        self.leitura_temperatura_mancal_guia_interno_1 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_1_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 1 Temperatura")
        self.condicionador_temperatura_mancal_guia_interno_1_ug = c.CondicionadorExponencial(self.leitura_temperatura_mancal_guia_interno_1)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_interno_1_ug)

            # Mancal Guia Interno 2
        self.leitura_temperatura_mancal_guia_interno_2 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_2_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 2 Temperatura")
        self.condicionador_temperatura_mancal_guia_interno_2_ug = c.CondicionadorExponencial(self.leitura_temperatura_mancal_guia_interno_2)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_interno_2_ug)

            # Patins Mancal combinado 1
        self.leitura_temperatura_patins_mancal_comb_1 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_1_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 1 Temperatura")
        self.condicionador_temperatura_patins_mancal_comb_1_ug = c.CondicionadorExponencial(self.leitura_temperatura_patins_mancal_comb_1)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_patins_mancal_comb_1_ug)

            # Patins Mancal combinado 2
        self.leitura_temperatura_patins_mancal_comb_2 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_2_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 2 Temperatura")
        self.condicionador_temperatura_patins_mancal_comb_2_ug = c.CondicionadorExponencial(self.leitura_temperatura_patins_mancal_comb_2)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_patins_mancal_comb_2_ug)

            # Mancal Casquilho combinado
        self.leitura_temperatura_mancal_casq_comb = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CASQ_COMB_TMP"], descricao=f"[UG{self.id}] Mancal Casquilho Combinado Temperatura")
        self.condicionador_temperatura_mancal_casq_comb_ug = c.CondicionadorExponencial(self.leitura_temperatura_mancal_casq_comb)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_casq_comb_ug)

            # Mancal Contra Escora combinado
        self.leitura_temperatura_mancal_contra_esc_comb = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CONT_ESCO_COMB_TMP"], descricao=f"UG{self.id} Mancal Contra Escora Combinado Temperatura")
        self.condicionador_temperatura_mancal_contra_esc_comb_ug = c.CondicionadorExponencial(self.leitura_temperatura_mancal_contra_esc_comb)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_contra_esc_comb_ug)

        # CONDICIONCADORES ATENUADORES
            # Pressão Entrada Turbina
        self.leitura_pressao_turbina = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["ENTRADA_TURBINA_PRESSAO"], escala=0.1, descricao=f"[UG{self.id}] Pressão Entrada Turbina")
        self.condicionador_pressao_turbina_ug = c.CondicionadorExponencialReverso(self.leitura_pressao_turbina, CONDIC_INDISPONIBILIZAR, 1.6, 1.3)
        self.condicionadores_atenuadores.append(self.condicionador_pressao_turbina_ug)

        return
        # CONDICIONADORES ESSENCIAIS - OUTROS
        # Botões
        self.leitura_bt_emerg_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["BT_EMERGENCIA_ATUADO"], invertido=True, descricao=f"[UG{self.id}] Botão Emergência Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.leitura_bt_emerg_atuado, CONDIC_NORMALIZAR))

        # Bloqueios
        self.leitura_bloq_86M_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86M_BLQ_ATUADO"], descricao=f"[UG{self.id}] Bloqueio 86M Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.leitura_bloq_86M_atuado, CONDIC_NORMALIZAR))

        self.leitura_bloq_86E_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86E_BLQ_ATUADO"], descricao=f"[UG{self.id}] Bloqueio 86E Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.leitura_bloq_86E_atuado, CONDIC_NORMALIZAR))

        self.leitura_bloq_86H_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86H_BLQ_ATUADO"], descricao=f"[UG{self.id}] Bloqueio 86H Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.leitura_bloq_86H_atuado, CONDIC_NORMALIZAR))

        # CLP Geral
        self.leitura_clp_geral_sem_bloq_exter = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["CLP_GERAL_SEM_BLQ_EXTERNO"], invertido=True, descricao=f"[UG{self.id}] CLP Geral Sem Bloqueio Externo")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.leitura_clp_geral_sem_bloq_exter, CONDIC_NORMALIZAR))

        # Relé
        self.leitura_trip_rele700G_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RELE_700G_TRP_ATUADO"], descricao=f"[UG{self.id}] Relé 700G Trip Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.leitura_trip_rele700G_atuado, CONDIC_NORMALIZAR))

        self.leitura_rele_bloq_86EH_desatuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RELE_BLQ_86EH_DESATUADO"], invertido=True, descricao=f"[UG{self.id}] Relé Bloqueio 86EH Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.leitura_rele_bloq_86EH_desatuado, CONDIC_NORMALIZAR))

        # RV
        self.leitura_falha_2_rv_b3 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_2_B3"], descricao=f"[UG{self.id}] RV Falha 2 - Bit 03")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.leitura_falha_2_rv_b3, CONDIC_NORMALIZAR))

        self.leitura_trip_rele_rv_naoatuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_RELE_TRP_NAO_ATUADO"], invertido=True, descricao=f"[UG{self.id}] RV Relé Trip Não Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.leitura_trip_rele_rv_naoatuado, CONDIC_NORMALIZAR))

        self.leitura_saidas_digitiais_rv_b0 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_SAIDAS_DIGITAIS"], descricao=f"[UG{self.id}] RV Saídas Digitais - Bit 00")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.leitura_saidas_digitiais_rv_b0, CONDIC_NORMALIZAR))

        # RT
        self.leitura_saidas_digitais_rt_b0 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_SAIDAS_DIGITAIS"], descricao=f"[UG{self.id}] RT Saídas Digitais - Bit 00")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.leitura_saidas_digitais_rt_b0, CONDIC_NORMALIZAR))

        self.leitura_trip_rele_rt_naoatuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_RELE_TRP_NAO_ATUADO"], invertido=True, descricao=f"[UG{self.id}] RV Relé Trip Não Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.leitura_trip_rele_rt_naoatuado, CONDIC_NORMALIZAR))


        # CONDICIONADORES
        # Bloqueios
        self.leitura_bloqueio_86M_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86M_BLQ_ATUADO"], descricao=f"[UG{self.id}] Bloqueio 86M Atuado")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_bloqueio_86M_atuado, CONDIC_INDISPONIBILIZAR))

        # Processo de Parada da Unidade
        # self.leitura_parada_bloq_descarga_pot = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARADA_BLQ_DESCARGA_POT"], descricao=f"[UG{self.id}] Parada Bloqueio Descarga Potência")
        # self.condicionadores.append(c.CondicionadorBase(self.leitura_parada_bloq_descarga_pot, CONDIC_NORMALIZAR))

        self.leitura_parada_bloq_abertura_disj = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARADA_BLQ_ABERTURA_DJ"], descricao=f"[UG{self.id}] Parada Bloqueio Abertura Disjuntor")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_parada_bloq_abertura_disj, CONDIC_NORMALIZAR))

        # Supervisão
        self.leitura_sup_tensao_125vcc = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["SUP_TENSAO_125VCC"], invertido=True, descricao=f"[UG{self.id}] Tensão 125Vcc Supervisão")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_sup_tensao_125vcc, CONDIC_INDISPONIBILIZAR))

        self.leitura_sup_tensao_24vcc = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["SUP_TENSAO_24VCC"], invertido=True, descricao=f"[UG{self.id}] Tensão 24Vcc Supervisão")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_sup_tensao_24vcc, CONDIC_INDISPONIBILIZAR))

        self.leitura_sup_bobina_52g = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["SUP_BOBINA_52G"], invertido=True, descricao=f"[UG{self.id}] Bobina 52G Supervisão")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_sup_bobina_52g, CONDIC_INDISPONIBILIZAR))

        self.leitura_sup_bobina_86eh = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["SUP_BOBINA_86EH"], invertido=True, descricao=f"[UG{self.id}] Bobina 86EH Supervisão")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_sup_bobina_86eh, CONDIC_INDISPONIBILIZAR))

        # Leitura Pressão Entrada da Turbina
        self.leitura_falha_pressao_entrada_turb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["ENTRADA_TURBINA_FLH_LER_PRESSAO"], descricao=f"[UG{self.id}] Pressão Entrada Turbina Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_pressao_entrada_turb, CONDIC_INDISPONIBILIZAR))

        # Leitura Mancal Guia
        # self.leitura_falha_temp_mancal_guia = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_FLH_LER_TMP"], descricao=f"[UG{self.id}] Mancal Guia Falha Leitura Temperatura")
        # self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_mancal_guia, CONDIC_INDISPONIBILIZAR))

        # Leitura Mancal Casquilho Combinado
        self.leitura_trip_temp_mancal_casq_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CASQ_COMB_TRP_TMP"], descricao=f"[UG{self.id}] Mancal Casquilho Combinado Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_mancal_casq_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_mancal_casq_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CASQ_COMB_FLH_LER_TMP"], descricao=f"[UG{self.id}] Mancal Casquilho Combinado Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_mancal_casq_comb, CONDIC_INDISPONIBILIZAR))

        # Leitura Mancal Contra Escora Combinado
        self.leitura_falha_temp_mancal_con_esc_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CONT_ESCO_COMB_FLH_LER_TMP"], descricao=f"[UG{self.id}] Mancal Contra Escora Combinado Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_mancal_con_esc_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_mancal_contra_esc_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CONT_ESCO_COMB_TRP_TMP"], descricao=f"[UG{self.id}] Mancal Contra Escora Combinado Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_mancal_contra_esc_comb, CONDIC_INDISPONIBILIZAR))

        # Leitura Mancal Guia Interno
        self.leitura_trip_temp_mancal_guia_interno_1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_1_TRP_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 1 Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_mancal_guia_interno_1, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_mancal_guia_interno_2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_2_TRP_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 2 Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_mancal_guia_interno_2, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_mancal_guia_interno_1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_1_FLH_LER_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 1 Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_mancal_guia_interno_1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_mancal_guia_interno_2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_2_FLH_LER_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 2 Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_mancal_guia_interno_2, CONDIC_INDISPONIBILIZAR))

        # Leitura Patins Mancal Combinado
        self.leitura_trip_temp_mancal_patins_1_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_1_TRP_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 1 Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_mancal_patins_1_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_mancal_patins_2_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_2_TRP_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 2 Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_mancal_patins_2_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_mancal_pat_1_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_1_FLH_LER_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 1 Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_mancal_pat_1_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_mancal_pat_2_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_2_FLH_LER_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 2 Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_mancal_pat_2_comb, CONDIC_INDISPONIBILIZAR))

        # Leitura Vibração Eixos Mancal Combinado
        self.leitura_trip_vibra_eixo_x_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_X_TRP_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Trip Vibração Eixo X")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_vibra_eixo_x_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_vibra_eixo_y_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_Y_TRP_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Trip Vibração Eixo Y")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_vibra_eixo_y_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_vibra_eixo_z_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_Z_TRP_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Trip Vibração Eixo Z")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_vibra_eixo_z_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_vibra_eixo_x_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_X_FLH_LER_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Falha Leitura Vibração Eixo X")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_vibra_eixo_x_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_vibra_eixo_y_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_Y_FLH_LER_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Falha Leitura Vibração Eixo Y")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_vibra_eixo_y_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_vibra_eixo_z_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_Z_FLH_LER_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Falha Leitura Vibração Eixo Z")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_vibra_eixo_z_mancal_comb, CONDIC_INDISPONIBILIZAR))

        # Leitura Ponte Fase
        self.leitura_falha_temp_ponte_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_A_FLH_LER_TMP"], descricao=f"[UG{self.id}] Ponte Fase A Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_ponte_fase_a, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_ponte_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_B_FLH_LER_TMP"], descricao=f"[UG{self.id}] Ponte Fase B Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_ponte_fase_b, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_ponte_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_C_FLH_LER_TMP"], descricao=f"[UG{self.id}] Ponte Fase C Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_ponte_fase_c, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_ponte_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_A_TRP_TMP"], descricao=f"[UG{self.id}] Ponte Fase A Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_ponte_fase_a, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_ponte_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_B_TRP_TMP"], descricao=f"[UG{self.id}] Ponte Fase B Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_ponte_fase_b, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_ponte_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_C_TRP_TMP"], descricao=f"[UG{self.id}] Ponte Fase C Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_ponte_fase_c, CONDIC_INDISPONIBILIZAR))

        # Leituras Gerador
        self.leitura_trip_temp_gerador_nucleo_estatorico = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_NUCL_ESTAT_TRP_TMP"], descricao=f"[UG{self.id}] Núcleo Estatórico Gerador Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_gerador_nucleo_estatorico, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_gerador_nucleo_esta = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_NUCL_ESTAT_FLH_LER_TMP"], descricao=f"[UG{self.id}] Núcleo Estatórico Gerador Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_gerador_nucleo_esta, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_gerador_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_A_FLH_LER_TMP"], descricao=f"[UG{self.id}] Fase A Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_gerador_fase_a, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_gerador_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_B_FLH_LER_TMP"], descricao=f"[UG{self.id}] Fase B Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_gerador_fase_b, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_gerador_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_C_FLH_LER_TMP"], descricao=f"[UG{self.id}] Fase C Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_gerador_fase_c, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_gerador_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_A_TRP_TMP"], descricao=f"[UG{self.id}] Gerador Fase A Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_gerador_fase_a, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_gerador_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_B_TRP_TMP"], descricao=f"[UG{self.id}] Gerador Fase B Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_gerador_fase_b, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_gerador_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_C_TRP_TMP"], descricao=f"[UG{self.id}] Gerador Fase C Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_gerador_fase_c, CONDIC_INDISPONIBILIZAR))

        # Leitura Disparo Mecanico
        self.leitura_disparo_mecanico_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DISP_MECANICO_ATUADO"], descricao=f"[UG{self.id}] Disparo Mecânico Atuado")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_disparo_mecanico_atuado, CONDIC_NORMALIZAR))

        self.leitura_disparo_mecanico_desatuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DISP_MECANICO_DESATUADO"], invertido=True, descricao=f"[UG{self.id}] Disparo Mecânico Desatuado")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_disparo_mecanico_desatuado, CONDIC_NORMALIZAR))

        # Leitura Detecção Vertical/Horizontal
        self.leitura_falha_vibra_detec_horizontal = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DETECCAO_HORIZONTAL_FLH_LER_VIBRA"], descricao=f"[UG{self.id}] Detecção Horizontal Falha Leitura Vibração")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_vibra_detec_horizontal, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_vibra_detec_horizontal = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DETECCAO_HORIZONTAL_TRP_VIBRA"], descricao=f"[UG{self.id}] Detecção Horizontal Trip Vibração")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_vibra_detec_horizontal, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_vibra_detec_vertical = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DETECCAO_VERTICAL_FLH_LER_VIBRA"], descricao=f"[UG{self.id}] Detecção Vertical Falha Leitura Vibração")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_vibra_detec_vertical, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_vibra_detec_vertical = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DETECCAO_VERTICAL_TRP_VIBRA"], descricao=f"[UG{self.id}] Detecção Vertical Trip Vibração")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_vibra_detec_vertical, CONDIC_INDISPONIBILIZAR))



        # Relé
        self.leitura_rele_700G_bf_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RELE_700G_BF_ATUADO"], descricao=f"[UG{self.id}] Relé 700G BF Atuado")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_rele_700G_bf_atuado, CONDIC_INDISPONIBILIZAR))

        # Sistema Água
        self.leitura_falha_habilitar_sistema_agua = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["SIS_AGUA_FLH_HAB"], descricao=f"[UG{self.id}] Sistema Água Falha Habilitar")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_habilitar_sistema_agua, CONDIC_NORMALIZAR))

        # Disjuntores
        self.leitura_disj_125vcc_fechados = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DJS_125VCC_FECHADOS"], invertido=True, descricao=f"[UG{self.id}] Disjuntores 125Vcc Fechados")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_disj_125vcc_fechados, CONDIC_INDISPONIBILIZAR))

        self.leitura_disj_24vcc_fechados = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DJS_24VCC_FECHADOS"], invertido=True, descricao=f"[UG{self.id}] Disjuntores 24Vcc Fechados")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_disj_24vcc_fechados, CONDIC_INDISPONIBILIZAR))

        # CLP Geral
        self.leitura_sistema_agua_clp_geral_ok = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["CLP_GERAL_SIS_AGUA_OK"], invertido=True, descricao=f"[UG{self.id}] CLP Geral Status Sistema Água")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_sistema_agua_clp_geral_ok, CONDIC_NORMALIZAR))

        # self.leitura_clp_geral_com_tens_barra_essenc = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["CLP_GERAL_COM_TENSAO_BARRA_ESSEN"], invertido=True, descricao=f"[UG{self.id}] CLP Geral Com Tensão Barra Essenciais")
        # self.condicionadores.append(c.CondicionadorBase(self.leitura_clp_geral_com_tens_barra_essenc, CONDIC_NORMALIZAR))

        # Transformador Excitação/Aterramento
        self.leitura_trip_temp_trafo_ateramento = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["TRAFO_ATERRAMENTO_TRP_TMP"], descricao=f"[UG{self.id}] Transformador Aterramento Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_trafo_ateramento, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_trafo_excitacao = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["TRAFO_EXCITACAO_TRP_TMP"], descricao=f"[UG{self.id}] Transformador Excitação Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_trafo_excitacao, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_trafo_excita = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["TRAFO_EXCITACAO_FLH_LER_TMP"], descricao=f"[UG{self.id}] Transformador Excitação Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_trafo_excita, CONDIC_INDISPONIBILIZAR))

        # UHRV
        self.leitura_falha_bomba_1_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_BOMBA_1_FLH"], descricao=f"[UG{self.id}] UHRV Bomba 1 Falha - Bit 00")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_bomba_1_uhrv, CONDIC_NORMALIZAR))

        self.leitura_falha_bomba_2_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_BOMBA_2_FLH"], descricao=f"[UG{self.id}] UHRV Bomba 2 Falha - Bit 02")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_bomba_2_uhrv, CONDIC_NORMALIZAR))

        self.leitura_trip_temp_oleo_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_TRP_TMP_OLEO"], descricao=f"[UG{self.id}] UHRV Trip Temperatura Óleo")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_oleo_uhrv, CONDIC_NORMALIZAR))

        self.leitura_falha_temp_oleo_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_FLH_LER_TMP_OLEO"], descricao=f"[UG{self.id}] UHRV Falha Leitura Temperatura Óleo")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_oleo_uhrv, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_pressao_acum_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_ACUMULADOR_PRESSAO_TRP"], descricao=f"[UG{self.id}] UHRV Trip Acumulador Pressão")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_pressao_acum_uhrv, CONDIC_INDISPONIBILIZAR))

        # UHLM
        self.leitura_falha_bomba_1_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_BOMBA_1_FLH"], descricao=f"[UG{self.id}] UHLM Bomba 1 Falha - Bit 04")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_bomba_1_uhlm, CONDIC_NORMALIZAR))

        self.leitura_falha_bomba_2_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_BOMBA_2_FLH"], descricao=f"[UG{self.id}] UHLM Bomba 2 Falha - Bit 06")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_bomba_2_uhlm, CONDIC_NORMALIZAR))

        self.leitura_falha_pressao_linha_b1_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_FLH_PRESSAO_LINHA_B1"], descricao=f"[UG{self.id}] UHLM Falha Pressão Linha B1")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_pressao_linha_b1_uhlm, CONDIC_NORMALIZAR))

        self.leitura_falha_pressao_linha_b2_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_FLH_PRESSAO_LINHA_B2"], descricao=f"[UG{self.id}] UHLM Falha Pressão Linha B2")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_pressao_linha_b2_uhlm, CONDIC_NORMALIZAR))

        self.leitura_falha_pressostato_linha_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_FLH_PRESSOSTATO_LINHA"], descricao=f"[UG{self.id}] UHLM Falha Pressostato Linha")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_pressostato_linha_uhlm, CONDIC_NORMALIZAR))

        self.leitura_trip_temp_oleo_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_TRP_TMP_OLEO"], descricao=f"[UG{self.id}] UHLM Trip Temperatura Óleo")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_temp_oleo_uhlm, CONDIC_NORMALIZAR))

        self.leitura_falha_temp_oleo_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_FLH_LER_TMP_OLEO"], descricao=f"[UG{self.id}] UHLM Falha Leitura Temperatura Óleo")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_temp_oleo_uhlm, CONDIC_INDISPONIBILIZAR))

        # RV
        self.leitura_falha_partir_rv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_PARTIR"], descricao=f"[UG{self.id}] RV Falha Partida")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_partir_rv, CONDIC_NORMALIZAR))

        self.leitura_falha_habilitar_rv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_HABILITAR"], descricao=f"[UG{self.id}] RV Falha Habilitar")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_habilitar_rv, CONDIC_NORMALIZAR))

        self.leitura_falha_desabilitar_rv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_DESABILITAR"], descricao=f"[UG{self.id}] RV Falha Desabilitar")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_desabilitar_rv, CONDIC_NORMALIZAR))

        self.leitura_alarme_rele_rv_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_RELE_ALM_ATUADO"], descricao=f"[UG{self.id}] RV Relé Alarme Atuado")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_alarme_rele_rv_atuado, CONDIC_NORMALIZAR))

        self.leitura_falha_fechar_distrib_rv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_FECHAR_DISTRIBUIDOR"], descricao=f"[UG{self.id}] RV Falha Fechamento Distribuidor")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_fechar_distrib_rv, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rv_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B0"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 00")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rv_b0, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B1"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 01")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rv_b1, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B2"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 02")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rv_b2, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b3 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B3"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 03")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rv_b3, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b4 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B4"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 04")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rv_b4, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b5 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B5"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 05")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rv_b5, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b10 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B10"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 10")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rv_b10, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b11 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B11"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 11")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rv_b11, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b12 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B12"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 12")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rv_b12, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b13 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B13"], descricao=f"[UG{self.id}] RV Falha 1 - Bit 13")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rv_b13, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rv_b1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_2_B1"], descricao=f"[UG{self.id}] RV Falhas 2 - Bit 01")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rv_b1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rv_b2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_2_B2"], descricao=f"[UG{self.id}] RV Falhas 2 - Bit 02")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rv_b2, CONDIC_INDISPONIBILIZAR))

        # RT
        self.leitura_falha_partir_rt = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_PARTIR"], descricao=f"[UG{self.id}] RT Falha Partida")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_partir_rt, CONDIC_NORMALIZAR))

        self.leitura_falha_habilitar_rt = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_HABILITAR"], descricao=f"[UG{self.id}] RT Falha Habilitar")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_habilitar_rt, CONDIC_NORMALIZAR))

        self.leitura_falha_desbilitar_rt = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_DESABILITAR"], descricao=f"[UG{self.id}] RT Falha Desabilitar")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_desbilitar_rt, CONDIC_INDISPONIBILIZAR))

        self.leitura_alarme_1_rt_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_ALM_1_B0"], descricao=f"[UG{self.id}] RT Alarmes 1 - Bit 00")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_alarme_1_rt_b0, CONDIC_INDISPONIBILIZAR))

        self.leitura_alarme_1_rt_b4 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_ALM_1_B4"], descricao=f"[UG{self.id}] RT Alarmes 1 - Bit 04")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_alarme_1_rt_b4, CONDIC_INDISPONIBILIZAR))

        self.leitura_alarme_1_rt_b5 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_ALM_1_B5"], descricao=f"[UG{self.id}] RT Alarmes 1 - Bit 05")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_alarme_1_rt_b5, CONDIC_INDISPONIBILIZAR))

        self.leitura_alarme_1_rt_b8 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_ALM_1_B8"], descricao=f"[UG{self.id}] RT Alarme 1 - Bit 08")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_alarme_1_rt_b8, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rt_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B0"], descricao=f"[UG{self.id}] RT Falhas 1 - Bit 00")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b0, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B1"], descricao=f"[UG{self.id}] RT Falha 1 - Bit 01")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b1, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rt_b2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B2"], descricao=f"[UG{self.id}] RT Falha 1 - Bit 02")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b2, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rt_b3 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B3"], descricao=f"[UG{self.id}] RT Falha 1 - Bit 03")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b3, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rt_b4 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B4"], descricao=f"[UG{self.id}] RT Falhas 1 - Bit 04")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b4, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b5 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B5"], descricao=f"[UG{self.id}] RT Falhas 1 - Bit 05")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b5, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b6 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B6"], descricao=f"[UG{self.id}] RT Falhas 1 - Bit 06")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b6, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b7 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B7"], descricao=f"[UG{self.id}] RT Falhas 1 - Bit 07")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b7, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b8 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B8"], descricao=f"[UG{self.id}] RT Falhas 1 - Bit 08")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b8, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b9 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B9"], descricao=f"[UG{self.id}] RT Falhas 1 - Bit 09")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b9, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b10 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B10"], descricao=f"[UG{self.id}] RT Falhas 1 - Bit 10")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b10, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b11 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B11"], descricao=f"[UG{self.id}] RT Falhas 1 - Bit 11")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b11, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b12 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B12"], descricao=f"[UG{self.id}] RT Falhas 1 - Bit 12")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b12, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b13 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B13"], descricao=f"[UG{self.id}] RT Falhas 1 - Bit 13")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b13, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b14 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B14"], descricao=f"[UG{self.id}] RT Falhas 1 - Bit 14")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b14, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b15 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B15"], descricao=f"[UG{self.id}] RT Falhas 1 - Bit 15")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_1_rt_b15, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rt_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B0"], descricao=f"[UG{self.id}] RV Falhas 2 - Bit 00")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rt_b0, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rt_b1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B1"], descricao=f"[UG{self.id}] RV Falhas 2 - Bit 01")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rt_b1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rt_b2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B2"], descricao=f"[UG{self.id}] RT Falha 2 - Bit 02")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rt_b2, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rt_b3 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B3"], descricao=f"[UG{self.id}] RV Falhas 2 - Bit 03")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rt_b3, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rt_b4 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B4"], descricao=f"[UG{self.id}] RV Falhas 2 - Bit 04")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rt_b4, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rt_b5 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B5"], descricao=f"[UG{self.id}] RT Falha 2 - Bit 05")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rt_b5, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rt_b6 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B6"], descricao=f"[UG{self.id}] RT Falha 2 - Bit 06")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rt_b6, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rt_b7 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B7"], descricao=f"[UG{self.id}] RT Falha 2 - Bit 07")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rt_b7, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rt_b8 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B8"], descricao=f"[UG{self.id}] RV Falhas 2 - Bit 08")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rt_b8, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rt_b9 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B9"], descricao=f"[UG{self.id}] RV Falhas 2 - Bit 09")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rt_b9, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rt_b10 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B10"], descricao=f"[UG{self.id}] RT Falha 2 - Bit 10")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rt_b10, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rt_b11 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B11"], descricao=f"[UG{self.id}] RT Falha 2 - Bit 11")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rt_b11, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rt_b12 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B12"], descricao=f"[UG{self.id}] RT Falha 2 - Bit 12")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_2_rt_b12, CONDIC_NORMALIZAR))


        # CONDICIONADORES RELÉS
        self.leitura_trip_rele_protecao1 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["RELE_PROTECAO_TRP_B5"], descricao=f"[UG{self.id}][RELE] Trip Relé Proteção 1")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_rele_protecao1, CONDIC_NORMALIZAR))

        self.leitura_trip_rele_protecao2 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["RELE_PROTECAO_TRP_B6"], descricao=f"[UG{self.id}][RELE] Trip Relé Proteção 2")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_trip_rele_protecao2, CONDIC_NORMALIZAR))

        self.leitura_subtensao_geral = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["SUBTEN_GERAL"], descricao=f"[UG{self.id}][RELE] Subtensão Geral")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_subtensao_geral, CONDIC_NORMALIZAR))

        self.leitura_subfreq_ele1 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["ELE_1_SOBREFRE"], descricao=f"[UG{self.id}][RELE] Subfrequência Elemento 1")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_subfreq_ele1, CONDIC_NORMALIZAR))

        self.leitura_subfreq_ele2 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["ELE_2_SOBREFRE"], descricao=f"[UG{self.id}][RELE] Subfrequência Elemento 2")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_subfreq_ele2, CONDIC_NORMALIZAR))

        self.leitura_sobrefreq_ele1 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["ELE_1_SUBFRE"], descricao=f"[UG{self.id}][RELE] Sobrefrequência Elemento 1")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_sobrefreq_ele1, CONDIC_NORMALIZAR))

        self.leitura_sobrefreq_ele2 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["ELE_2_SUBFRE"], descricao=f"[UG{self.id}][RELE] Sobrefrequência Elemento 2")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_sobrefreq_ele2, CONDIC_NORMALIZAR))

        self.leitura_sobrecorr_instant = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["SOBRECO_INST"], descricao=f"[UG{self.id}][RELE] Sobrecorrente Instantânea")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_sobrecorr_instant, CONDIC_NORMALIZAR))

        self.leitura_voltz_hertz = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["VOLTZ_HERTZ"], descricao=f"[UG{self.id}][RELE] Voltz/Hertz")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_voltz_hertz, CONDIC_NORMALIZAR))

        self.leitura_perda_campo_geral = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["PERDA_CAMPO_GERAL"], descricao=f"[UG{self.id}][RELE] Perda Campo Geral")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_perda_campo_geral, CONDIC_NORMALIZAR))

        self.leitura_pot_reversa = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["POT_REVERSA"], descricao=f"[UG{self.id}][RELE] Potência Reversa")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_pot_reversa, CONDIC_NORMALIZAR))


        self.leitura_transf_disp_rele_linha_trafo = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["TE_RELE_LINHA_TRANS_DISP"], descricao=f"[UG{self.id}][RELE] Transferência Disparo Relé Linha Transformador Elevador")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_transf_disp_rele_linha_trafo, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_partida_dj_maq = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["DJ_MAQUINA_FLH_PARTIDA"], descricao=f"[UG{self.id}][RELE] Falha Partir Disjuntor Máquina")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_partida_dj_maq, CONDIC_INDISPONIBILIZAR))

        # self.leitura_atua_rele_86bf = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG"][f"UG{self.id}_ATUA_RELE_86BF"], descricao=f"[UG{self.id}][RELE] Atua Relé 86BF")
        # self.condicionadores.append(c.CondicionadorBase(self.leitura_atua_rele_86bf, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_abretura_dj_maq1 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["DJ_MAQUINA_FLH_ABERTURA_B7"], descricao=f"[UG{self.id}][RELE] Falha Abertura Disjuntor Máquina 1")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_abretura_dj_maq1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_abretura_dj_maq2 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["DJ_MAQUINA_FLH_ABERTURA_B8"], descricao=f"[UG{self.id}][RELE] Falha Abertura Disjuntor Máquina 2")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_falha_abretura_dj_maq2, CONDIC_INDISPONIBILIZAR))

        self.leitura_recibo_transf_disp = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["RECIBO_TRANS_DISP"], descricao=f"[UG{self.id}][RELE] Recebida Transferência Disparo")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_recibo_transf_disp, CONDIC_INDISPONIBILIZAR))

        self.leitura_difer_com_restr = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["DIF_COM_RESTRICAO"], descricao=f"[UG{self.id}][RELE] Diferencial Com Restrição")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_difer_com_restr, CONDIC_INDISPONIBILIZAR))

        self.leitura_difer_sem_restr = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["DIF_SEM_RESTRICAO"], descricao=f"[UG{self.id}][RELE] Diferencial Sem Restrição")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_difer_sem_restr, CONDIC_INDISPONIBILIZAR))

        self.leitura_fuga_sobrecorr_geral = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["FUGA_SOBRECO_GERAL"], descricao=f"[UG{self.id}][RELE] Fuga Sobrecorrente Geral")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_fuga_sobrecorr_geral, CONDIC_INDISPONIBILIZAR))

        self.leitura_sobrecorr_instant_neutro = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["SOBRECO_INST_NEUTRO"], descricao=f"[UG{self.id}][RELE] Sobrecorrente Instantânea Neutro")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_sobrecorr_instant_neutro, CONDIC_INDISPONIBILIZAR))

        self.leitura_sobrecorr_restr_tensao = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["LT_SOBRECO_RESTRICAO"], descricao=f"[UG{self.id}][RELE] Sobrecorrente Restrição Tensão")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_sobrecorr_restr_tensao, CONDIC_INDISPONIBILIZAR))

        self.leitura_sobrecorr_temp_neutro = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["SOBRECO_TEMPO_NEUTRO"], descricao=f"[UG{self.id}][RELE] Sobrecorrente Temporizada Neutro")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_sobrecorr_temp_neutro, CONDIC_INDISPONIBILIZAR))

        self.leitura_sobrecorr_seq_neg = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["SOBRECO_SEQU_NEG"], descricao=f"[UG{self.id}][RELE] Sobrecorrente Sequência Negativa")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_sobrecorr_seq_neg, CONDIC_INDISPONIBILIZAR))

        self.leitura_unidade_fora_passo = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["UNIDADE_FORA_PASSO"], descricao=f"[UG{self.id}][RELE] Unidade Fora Passo")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_unidade_fora_passo, CONDIC_INDISPONIBILIZAR))

        self.leitura_sobretensao_geral = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["SOBRETEN_GERAL"], descricao=f"[UG{self.id}][RELE] Sobretensão Geral")
        self.condicionadores.append(c.CondicionadorBase(self.leitura_sobretensao_geral, CONDIC_INDISPONIBILIZAR))