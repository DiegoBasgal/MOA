__version__ = "0.2"
__author__ = "Lucas Lavratti", "Henrique Pfeifer", "Diego Basgal"
__description__ = "Este módulo corresponde a implementação das Unidades de Geração."

import pytz
import logging
import traceback
import threading

import src.subestacao as se
import src.tomada_agua as tda
import src.funcoes.leitura as lei
import src.funcoes.escrita as esc
import src.funcoes.condicionadores as c
import src.conectores.banco_dados as bd
import src.conectores.servidores as serv

from time import time, sleep
from datetime import datetime

from src.dicionarios.reg import *
from src.maquinas_estado.ug import *


logger = logging.getLogger("logger")


class UnidadeGeracao:
    def __init__(self, id: "int", cfg: "dict"=None, db: "bd.BancoDados"=None):

        # VERIFICAÇÃO DE ARGUMENTOS

        if id <= 0:
            logger.error(f"[UG{self.id}] A Unidade não pode ser instanciada com o ID <= \"0\" ou vazio.")
            raise ValueError
        else:
            self.__id = id

        self.__db = db
        self.__cfg = cfg

        self.clp = serv.Servidores.clp

        # ATRIBUIÇÃO DE VAIRIÁVEIS

        # PRIVADAS
        self.__leitura_potencia = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"][""],
            descricao=f"[UG{self.id}] Leitura Potência"
        )
        self.__leitura_etapa_atual = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"][""],
            descricao=f"[UG{self.id}] Leitura Etapa"
        )
        self.__leitura_etapa_alvo = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"][""],
            descricao=f"[UG{self.id}] Leitura Etapa"
        )
        self.__leitura_horimetro = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"][""],
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
        self.aguardar_pressao_cp: "bool" = False
        self.normalizacao_agendada: "bool" = False
        self.temporizar_normalizacao: "bool" = False

        self.borda_cp_fechar: "bool" = False

        self.condicionadores_ativos: "list[c.CondicionadorBase]" = []

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
            logger.debug(f"[UG{self.id}]          Etapa:                     \"{UG_STR_DCT_ETAPAS[self.etapa_atual]}\" (Atual: {self.etapa_atual} | Alvo: {self.etapa_alvo})")

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
            self.clp["MOA"].write_single_coil(REG_MOA["MOA"][f"OUT_ETAPA_UG{self.id}"], self.etapa_atual)
            self.clp["MOA"].write_single_coil(REG_MOA["MOA"][f"OUT_STATE_UG{self.id}"], self.codigo_state)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível escrever os valores no CLP MOA.")
            logger.debug(traceback.format_exc())

    def partir(self) -> "None":
        """
        Função para acionamento do comando de partida da Unidade.
        """

        try:
            if self.etapa != UG_SINCRONIZADA:
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARTIDA\"")

                esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], valor=1)
                self.enviar_setpoint(self.setpoint)

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

                esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], valor=1)
                self.enviar_setpoint(0)

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
                res = self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"][""], int(self.setpoint))

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
            self.clp["MOA"].write_single_coil(REG_UG["MOA"]["PAINEL_LIDO"], 0)

            passo = 0
            for x in range(2):
                passo += 1
                logger.debug("")
                logger.debug(f"[UG{self.id}]          Passo: {passo}/3")
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
                sleep(1)

            self.clp["MOA"].write_single_coil(REG_UG["MOA"]["PAINEL_LIDO"], 1)

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
            esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], valor=1)

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
            esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], valor=0)

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
            self.clp["MOA"].write_single_coil(REG_UG["MOA"][f"OUT_BLOCK_UG{self.id}"], 1)

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
            self.clp["MOA"].write_single_coil(REG_UG["MOA"]["PAINEL_LIDO"], 0)
            self.clp["MOA"].write_single_coil(REG_UG["MOA"][f"OUT_BLOCK_UG{self.id}"], 0)
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

        if self.etapa_atual == UG_PARADA:
            self.acionar_trip_eletrico()
            self.acionar_trip_logico()

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
        esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], valor=1)
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

        if self.etapa_atual == UG_PARADA:
            if self.setpoint >= self.__cfg["pot_minima"]:
                self.partir()

        elif self.etapa_atual == UG_PARANDO:
            if self.setpoint >= self.__cfg["pot_minima"]:
                self.enviar_setpoint(self.setpoint)

        elif self.etapa_atual == UG_SINCRONIZANDO:
            if not self.temporizar_partida:
                self.temporizar_partida = True
                threading.Thread(target=lambda: self.verificar_sincronismo()).start()

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        elif self.etapa_atual == UG_SINCRONIZADA:
            self.temporizar_partida = False

            if not self.aux_tempo_sincronizada:
                self.aux_tempo_sincronizada = self.get_time()

            elif (self.get_time() - self.aux_tempo_sincronizada).seconds >= 300:
                self.tentativas_normalizacao = 0

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        if not self.etapa_atual == UG_SINCRONIZADA:
            self.aux_tempo_sincronizada = None

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

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.warning(f"[UG{self.id}] Foram detectados condicionadores ativos na Unidade!")
            else:
                logger.info(f"[UG{self.id}] Ainda há condicionadores ativos na Unidade!")

            for condic in condics_ativos:
                if condic in self.condicionadores_ativos:
                    logger.debug(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    flag = condic.gravidade
                    continue

                elif condic.gravidade == CONDIC_NORMALIZAR:
                    logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_NORMALIZAR
                    # self.__db.update_alarmes([datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr])

                elif condic.gravidade == CONDIC_AGUARDAR:
                    logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_NORMALIZAR
                    # self.__db.update_alarmes([datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr])

                elif condic.gravidade == CONDIC_INDISPONIBILIZAR:
                    logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_INDISPONIBILIZAR
                    # self.__db.update_alarmes([datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr])

            logger.debug("")
            return flag

        else:
            self.condicionadores_ativos = []
            return flag


    def atualizar_limites(self, parametros: "dict") -> "None":
        """
        Função para extração de valores do Banco de Dados da Interface WEB e atribuição
        de novos limites de operação de condicionadores.
        """

        try:
            self.prioridade = int(parametros[f"ug{self.id}_prioridade"])

            self.c_temp_fase_u_ug.valor_base = float(parametros[f"alerta_temperatura_fase_u_ug{self.id}"])
            self.c_temp_fase_v_ug.valor_base = float(parametros[f"alerta_temperatura_fase_v_ug{self.id}"])
            self.c_temp_fase_w_ug.valor_base = float(parametros[f"alerta_temperatura_fase_w_ug{self.id}"])
            self.c_temp_mancal_gerador_la_1_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_gerador_la_1_ug{self.id}"])
            self.c_temp_mancal_gerador_la_2_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_gerador_la_2_ug{self.id}"])
            self.c_temp_mancal_gerador_lna_1_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_gerador_lna_1_ug{self.id}"])
            self.c_temp_mancal_gerador_lna_2_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_gerador_lna_2_ug{self.id}"])
            self.c_temp_mancal_turbina_radial_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_turbina_radial{self.id}"])
            self.c_temp_mancal_turbina_escora_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_turbina_escora{self.id}"])
            self.c_temp_mancal_turbina_contra_escora_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_turbina_contra_escora_ug{self.id}"])
            self.c_pressao_turbina_ug.valor_base = float(parametros[f"alerta_pressao_turbina_ug{self.id}"])

            self.c_temp_fase_u_ug.valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{self.id}"])
            self.c_temp_fase_v_ug.valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{self.id}"])
            self.c_temp_fase_w_ug.valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{self.id}"])
            self.c_temp_mancal_gerador_la_1_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_gerador_la_1_ug{self.id}"])
            self.c_temp_mancal_gerador_la_2_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_gerador_la_2_ug{self.id}"])
            self.c_temp_mancal_gerador_lna_1_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_gerador_lna_1_ug{self.id}"])
            self.c_temp_mancal_gerador_lna_2_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_gerador_lna_2_ug{self.id}"])
            self.c_temp_mancal_turbina_radial_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_turbina_radial{self.id}"])
            self.c_temp_mancal_turbina_escora_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_turbina_escora{self.id}"])
            self.c_temp_mancal_turbina_contra_escora_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_turbina_contra_escora_ugg{self.id}"])
            self.c_pressao_turbina_ug.valor_limite = float(parametros[f"limite_pressao_turbina_ug{self.id}"])

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores.")
            logger.debug(traceback.format_exc())

    def verificar_limites(self) -> "None":
        """
        Função para verificação de limites de operação da Unidade.

        Verifica os valores base e limite da Unidade, pré-determinados na interface
        WEB, e avisa o operador caso algum valor ultrapasse o estipulado.
        """

        if self.l_temp_fase_U.valor >= self.c_temp_fase_u_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase R da UG passou do valor base! ({self.c_temp_fase_u_ug.valor_base}C) | Leitura: {self.l_temp_fase_U.valor}C")
        if self.l_temp_fase_U.valor >= 0.9*(self.c_temp_fase_u_ug.valor_limite - self.c_temp_fase_u_ug.valor_base) + self.c_temp_fase_u_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase R da UG está muito próxima do limite! ({self.c_temp_fase_u_ug.valor_limite}C) | Leitura: {self.l_temp_fase_U.valor}C")

        if self.l_temp_fase_V.valor >= self.c_temp_fase_v_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase S da UG passou do valor base! ({self.c_temp_fase_v_ug.valor_base}C) | Leitura: {self.l_temp_fase_V.valor}C")
        if self.l_temp_fase_V.valor >= 0.9*(self.c_temp_fase_v_ug.valor_limite - self.c_temp_fase_v_ug.valor_base) + self.c_temp_fase_v_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase S da UG está muito próxima do limite! ({self.c_temp_fase_v_ug.valor_limite}C) | Leitura: {self.l_temp_fase_V.valor}C")

        if self.l_temp_fase_W.valor >= self.c_temp_fase_w_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase T da UG passou do valor base! ({self.c_temp_fase_w_ug.valor_base}C) | Leitura: {self.l_temp_fase_W.valor}C")
        if self.l_temp_fase_W.valor >= 0.9*(self.c_temp_fase_w_ug.valor_limite - self.c_temp_fase_w_ug.valor_base) + self.c_temp_fase_w_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase T da UG está muito próxima do limite! ({self.c_temp_fase_w_ug.valor_limite}C) | Leitura: {self.l_temp_fase_W.valor}C")

        if self.l_temp_mancal_gerador_la_1.valor >= self.c_temp_mancal_gerador_la_1_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Gerador LA 1 da UG passou do valor base! ({self.c_temp_mancal_gerador_la_1_ug.valor_base}C) | Leitura: {self.l_temp_mancal_gerador_la_1.valor}C")
        if self.l_temp_mancal_gerador_la_1.valor >= 0.9*(self.c_temp_mancal_gerador_la_1_ug.valor_limite - self.c_temp_mancal_gerador_la_1_ug.valor_base) + self.c_temp_mancal_gerador_la_1_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Gerador LA 1 da UG está muito próxima do limite! ({self.c_temp_mancal_gerador_la_1_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_gerador_la_1.valor}C")

        if self.l_temp_mancal_gerador_la_2.valor >= self.c_temp_mancal_gerador_la_2_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Gerador LA 2 da UG passou do valor base! ({self.c_temp_mancal_gerador_la_2_ug.valor_base}C) | Leitura: {self.l_temp_mancal_gerador_la_2.valor}C")
        if self.l_temp_mancal_gerador_la_2.valor >= 0.9*(self.c_temp_mancal_gerador_la_2_ug.valor_limite - self.c_temp_mancal_gerador_la_2_ug.valor_base) + self.c_temp_mancal_gerador_la_2_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Gerador LA 2 da UG está muito próxima do limite! ({self.c_temp_mancal_gerador_la_2_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_gerador_la_2.valor}C")

        if self.l_temp_mancal_gerador_lna_1.valor >= self.c_temp_mancal_gerador_lna_1_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Gerador LNA 1 da UG passou do valor base! ({self.c_temp_mancal_gerador_lna_1_ug.valor_base}C) | Leitura: {self.l_temp_mancal_gerador_lna_1.valor}C")
        if self.l_temp_mancal_gerador_lna_1.valor >= 0.9*(self.c_temp_mancal_gerador_lna_1_ug.valor_limite - self.c_temp_mancal_gerador_lna_1_ug.valor_base) + self.c_temp_mancal_gerador_lna_1_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Gerador LNA 1 da UG está muito próxima do limite! ({self.c_temp_mancal_gerador_lna_1_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_gerador_lna_1.valor}C")

        if self.l_temp_mancal_gerador_lna_2.valor >= self.c_temp_mancal_gerador_lna_2_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Gerador LNA 2 da UG passou do valor base! ({self.c_temp_mancal_gerador_lna_2_ug.valor_base}C) | Leitura: {self.l_temp_mancal_gerador_lna_2.valor}C")
        if self.l_temp_mancal_gerador_lna_2.valor >= 0.9*(self.c_temp_mancal_gerador_lna_2_ug.valor_limite - self.c_temp_mancal_gerador_lna_2_ug.valor_base) + self.c_temp_mancal_gerador_lna_2_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Gerador LNA 2 da UG está muito próxima do limite! ({self.c_temp_mancal_gerador_lna_2_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_gerador_lna_2.valor}C")

        if self.l_temp_mancal_turbina_radial.valor >= self.c_temp_mancal_turbina_radial_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura dos Patins do Mancal Gerador LNA 2 da UG passou do valor base! ({self.c_temp_mancal_turbina_radial_ug.valor_base}C) | Leitura: {self.l_temp_mancal_turbina_radial.valor}C")
        if self.l_temp_mancal_turbina_radial.valor >= 0.9*(self.c_temp_mancal_turbina_radial_ug.valor_limite - self.c_temp_mancal_turbina_radial_ug.valor_base) + self.c_temp_mancal_turbina_radial_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura dos Patins do Mancal Gerador LNA 2 da UG está muito próxima do limite! ({self.c_temp_mancal_turbina_radial_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_turbina_radial.valor}C")

        if self.l_temp_mancal_turbina_radial.valor >= self.c_temp_mancal_turbina_radial_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura dos Mancal Turbina Radial da UG passou do valor base! ({self.c_temp_mancal_turbina_radial_ug.valor_base}C) | Leitura: {self.l_temp_mancal_turbina_radial.valor}C")
        if self.l_temp_mancal_turbina_radial.valor >= 0.9*(self.c_temp_mancal_turbina_radial_ug.valor_limite - self.c_temp_mancal_turbina_radial_ug.valor_base) + self.c_temp_mancal_turbina_radial_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura dos Mancal Turbina Radial da UG está muito próxima do limite! ({self.c_temp_mancal_turbina_radial_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_turbina_radial.valor}C")

        if self.l_temp_mancal_turbina_escora.valor >= self.c_temp_mancal_turbina_escora_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Turbina Escora da UG passou do valor base! ({self.c_temp_mancal_turbina_escora_ug.valor_base}C) | Leitura: {self.l_temp_mancal_turbina_escora.valor}C")
        if self.l_temp_mancal_turbina_escora.valor >= 0.9*(self.c_temp_mancal_turbina_escora_ug.valor_limite - self.c_temp_mancal_turbina_escora_ug.valor_base) + self.c_temp_mancal_turbina_escora_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Turbina Escora da UG está muito próxima do limite! ({self.c_temp_mancal_turbina_escora_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_turbina_escora.valor}C")

        if self.l_temp_mancal_turbina_contra_escora.valor >= self.c_temp_mancal_turbina_contra_escora_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Turbina Contra Escora da UG passou do valor base! ({self.c_temp_mancal_turbina_contra_escora_ug.valor_base}C) | Leitura: {self.l_temp_mancal_turbina_contra_escora.valor}C")
        if self.l_temp_mancal_turbina_contra_escora.valor >= 0.9*(self.c_temp_mancal_turbina_contra_escora_ug.valor_limite - self.c_temp_mancal_turbina_contra_escora_ug.valor_base) + self.c_temp_mancal_turbina_contra_escora_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Turbina Contra Escora da UG está muito próxima do limite! ({self.c_temp_mancal_turbina_contra_escora_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_turbina_contra_escora.valor}C")

        if self.l_pressao_turbina.valor <= self.c_pressao_turbina_ug.valor_base and self.l_pressao_turbina.valor != 0 and self.etapa_atual == UG_SINCRONIZADA:
            logger.warning(f"[UG{self.id}] A pressão na entrada da turbina da UG passou do valor base! ({self.c_pressao_turbina_ug.valor_base:03.2f} KGf/m2) | Leitura: {self.l_pressao_turbina.valor:03.2f}")
        if self.l_pressao_turbina.valor <= self.c_pressao_turbina_ug.valor_limite+0.9*(self.c_pressao_turbina_ug.valor_base - self.c_pressao_turbina_ug.valor_limite) and self.l_pressao_turbina.valor != 0 and self.etapa_atual == UG_SINCRONIZADA:
            logger.critical(f"[UG{self.id}] A pressão na entrada da turbina da UG está muito próxima do limite! ({self.c_pressao_turbina_ug.valor_limite:03.2f} KGf/m2) | Leitura: {self.l_pressao_turbina.valor:03.2f} KGf/m2")

    def verificar_leituras(self) -> "None":
        """
        Função para consulta de acionamentos da Unidade e avisos através do mecanismo
        de acionamento temporizado.
        """
        return

    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """

        # CONDICIONADORES ESSENCIAIS
        # Temperaturas                                          # TODO -> mudar nomenclatura dos registradores
            # Fase U
        self.l_temp_fase_U = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], descricao=f"[UG{self.id}] Temperatura Fase U")
        self.c_temp_fase_u_ug = c.CondicionadorExponencial(self.l_temp_fase_U)
        self.condicionadores_essenciais.append(self.c_temp_fase_u_ug)

            # Fase V
        self.l_temp_fase_V = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], descricao=f"[UG{self.id}] Temperatura Fase V")
        self.c_temp_fase_v_ug = c.CondicionadorExponencial(self.l_temp_fase_V)
        self.condicionadores_essenciais.append(self.c_temp_fase_v_ug)

            # Fase W
        self.l_temp_fase_W = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], descricao=f"[UG{self.id}] Temperatura Fase W")
        self.c_temp_fase_w_ug = c.CondicionadorExponencial(self.l_temp_fase_W)
        self.condicionadores_essenciais.append(self.c_temp_fase_w_ug)

            # Mancal Gerador LA 1
        self.l_temp_mancal_gerador_la_1 = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], descricao=f"[UG{self.id}] Temperatura Mancal Gerador LA 1")
        self.c_temp_mancal_gerador_la_1_ug = c.CondicionadorExponencial(self.l_temp_mancal_gerador_la_1)
        self.condicionadores_essenciais.append(self.c_temp_mancal_gerador_la_1_ug)

            # Mancal Gerador LA 2
        self.l_temp_mancal_gerador_la_2 = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], descricao=f"[UG{self.id}] Temperatura Mancal Gerador LA 2")
        self.c_temp_mancal_gerador_la_2_ug = c.CondicionadorExponencial(self.l_temp_mancal_gerador_la_2)
        self.condicionadores_essenciais.append(self.c_temp_mancal_gerador_la_2_ug)

            # Mancal Gerador LNA 1
        self.l_temp_mancal_gerador_lna_1 = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], descricao=f"[UG{self.id}] Temperatura Mancal Gerador LNA 1")
        self.c_temp_mancal_gerador_lna_1_ug = c.CondicionadorExponencial(self.l_temp_mancal_gerador_lna_1)
        self.condicionadores_essenciais.append(self.c_temp_mancal_gerador_lna_1_ug)

            #  Mancal Gerador LNA 2
        self.l_temp_mancal_gerador_lna_2 = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], descricao=f"[UG{self.id}] Temperatura Mancal Gerador LNA 2")
        self.c_temp_mancal_gerador_lna_2_ug = c.CondicionadorExponencial(self.l_temp_mancal_gerador_lna_2)
        self.condicionadores_essenciais.append(self.c_temp_mancal_gerador_lna_2_ug)

            # Mancal Turbina Radial
        self.l_temp_mancal_turbina_radial = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], descricao=f"[UG{self.id}] Temperatura Mancal Turbina Radial")
        self.c_temp_mancal_turbina_radial_ug = c.CondicionadorExponencial(self.l_temp_mancal_turbina_radial)
        self.condicionadores_essenciais.append(self.c_temp_mancal_turbina_radial_ug)

            # Mancal Turbina Escora
        self.l_temp_mancal_turbina_escora = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], descricao=f"[UG{self.id}] Temperatura Mancal Turbina Escora")
        self.c_temp_mancal_turbina_escora_ug = c.CondicionadorExponencial(self.l_temp_mancal_turbina_escora)
        self.condicionadores_essenciais.append(self.c_temp_mancal_turbina_escora_ug)

            # Mancal Turbina Radial Contra Escora
        self.l_temp_mancal_turbina_contra_escora = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], descricao=f"[UG{self.id}] Temperatura Mancal Turbina Contra Escora")
        self.c_temp_mancal_turbina_contra_escora_ug = c.CondicionadorExponencial(self.l_temp_mancal_turbina_contra_escora)
        self.condicionadores_essenciais.append(self.c_temp_mancal_turbina_contra_escora_ug)

            # Óleo UHRV
        self.l_temp_oleo_uhrv = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], descricao=f"[UG{self.id}] Temperatura Óleo UHRV")
        self.c_temp_oleo_uhrv_ug = c.CondicionadorExponencial(self.l_temp_oleo_uhrv)
        self.condicionadores_essenciais.append(self.c_temp_oleo_uhrv_ug)

            # Óleo ULHM
        self.l_temp_oleo_uhlm = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], descricao=f"[UG{self.id}] Temperatura Óleo ULHM")
        self.c_temp_oleo_uhlm_ug = c.CondicionadorExponencial(self.l_temp_oleo_uhlm)
        self.condicionadores_essenciais.append(self.c_temp_oleo_uhlm_ug)

        # CONDICIONCADORES ATENUADORES
            # Pressão Entrada Turbina
        self.l_pressao_turbina = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"][""], escala=0.1, descricao=f"[UG{self.id}] Pressão Entrada Turbina")
        self.c_pressao_turbina_ug = c.CondicionadorExponencialReverso(self.l_pressao_turbina, CONDIC_INDISPONIBILIZAR, 1.6, 1.3)
        self.condicionadores_atenuadores.append(self.c_pressao_turbina_ug)

        return