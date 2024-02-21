__version__ = "0.2"
__author__ = "Lucas Lavratti", "Henrique Pfeifer", "Diego Basgal"
__description__ = "Este módulo corresponde a implementação das Unidades de Geração."

import pytz
import logging
import traceback
import threading

import src.comporta as cp
import src.subestacao as se
import src.funcoes.condicionadores as c

from time import time, sleep
from datetime import datetime

from src.funcoes.leitura import *
from src.maquinas_estado.ug import *

from src.conectores.servidores import Servidores
from src.conectores.banco_dados import BancoDados
from src.funcoes.escrita import EscritaModBusBit as EMB


logger = logging.getLogger("logger")

class UnidadeGeracao:
    def __init__(self, id: "int", cfg: "dict"=None, db: "BancoDados"=None, cp:"cp.Comporta"=None, serv: "Servidores"=None):

        # VERIFICAÇÃO DE ARGUMENTOS

        if id <= 0:
            logger.error(f"[UG{self.id}] A Unidade não pode ser instanciada com o ID <= \"0\" ou vazio.")
            raise ValueError
        else:
            self.__id = id

        self.__db = db

        self.cfg = cfg

        self.cp = cp
        self.rv = serv.rv
        self.rt = serv.rt
        self.clp = serv.clp
        self.rele = serv.rele


        # ATRIBUIÇÃO DE VAIRIÁVEIS

        # PRIVADAS
        self.__leitura_potencia = LeituraModbus( # LeituraModbusFloat(
            self.clp[f"UG{self.id}"],
            REG_CLP[f"UG{self.id}"]["P"],
            op=3,
            descricao=f"[UG{self.id}] Leitura Potência"
        )
        self.__leitura_etapa_atual = LeituraModbus(
            self.rv[f"UG{self.id}"],
            REG_CLP[f"UG{self.id}"]["RV_ESTADO_OPERACAO"],
            descricao=f"[UG{self.id}] Leitura Etapa"
        )
        self.__leitura_horimetro = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_CLP[f"UG{self.id}"]["HORIMETRO"],
            descricao=f"[UG{self.id}] Leitura Horímetro"
        )

        self.__init_registro_estados: "int" = 0
        self.__tempo_entre_tentativas: "int" = 0
        self.__limite_tentativas_normalizacao: "int" = 3


        # PROTEGIDAS
        self._setpoint: "int" = 0
        self._prioridade: "int" = 0
        self._codigo_state: "int" = 0
        self._ultima_etapa: "int" = 0
        self._tentativas_normalizacao: "int" = 0

        self._setpoint_minimo: "float" = self.cfg["pot_minima"]
        self._setpoint_maximo: "float" = self.cfg[f"pot_maxima_ug{self.id}"]

        self._condicionadores: "list[c.CondicionadorBase]" = []
        self._condicionadores_essenciais: "list[c.CondicionadorBase]" = []
        self._condicionadores_atenuadores: "list[c.CondicionadorBase]" = []


        # PÚBLICAS
        self.atenuacao: "int" = 0
        self.tempo_normalizar: "int" = 0

        self.borda_parar: "bool" = False
        self.manter_unidades: "bool" = False
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

        self.__next_state: "State"

        self.iniciar_ultimo_estado()
        self.carregar_leituras()


    @property
    def id(self) -> "int":
        # PROPRIEDADE -> Retrona o ID da Unidade

        return self.__id

    @property
    def leitura_potencia(self) -> "int":
        # PROPRIEDADE -> Retorna a leitura de Potência da Unidade.

        return int(self.__leitura_potencia.valor)

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
        # PROPRIEDADE -> Retorna a leitura de etapa atual direto do CLP da Unidade.

        return self.__leitura_etapa_atual.valor

    @property
    def etapa(self) -> "int":
        # PROPRIEDADE -> Retorna a etapa atual da Unidade.

        if self.__leitura_etapa_atual.valor == UG_PARADA or self.__leitura_etapa_atual.valor == UG_PARADA2:
            self._ultima_etapa = self.__leitura_etapa_atual.valor
            return UG_PARADA

        elif self.__leitura_etapa_atual.valor == UG_SINCRONIZADA:
            self._ultima_etapa = self.__leitura_etapa_atual.valor
            return UG_SINCRONIZADA

        elif self.__leitura_etapa_atual.valor > UG_SINCRONIZADA and self.__leitura_etapa_atual.valor < UG_PARADA2:
            self._ultima_etapa = self.__leitura_etapa_atual.valor
            return UG_PARANDO

        elif UG_PARADA < self.__leitura_etapa_atual.valor < UG_SINCRONIZADA:
            if self.__leitura_etapa_atual.valor > UG_SINCRONIZADA:
                self._ultima_etapa = self.__leitura_etapa_atual.valor
                return UG_PARANDO
            else:
                self._ultima_etapa = self.__leitura_etapa_atual.valor
                return UG_SINCRONIZANDO


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

        if var < self.cfg["pot_minima"]:
            if self.manter_unidades:
                self._setpoint = self.cfg["pot_minima"]
            else:
                self._setpoint = 0

        elif var > self.cfg[f"pot_maxima_ug{self.id}"]:
            self._setpoint = self.cfg[f"pot_maxima_ug{self.id}"]

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
    def condicionadores_atenuadores(self) -> "list[c.CondicionadorExponencial]":
        # PROPRIEDADE -> Retorna a lista de Condicionadores Atenuadores da Unidade.

        return self._condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: "list[c.CondicionadorExponencial]") -> "None":
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


    def atualizar_registro_estados(self) -> "None":
        """
        Função para registro de troca de estados no banco de dados.

        A função é chamada na inicialização da classe de estado no momento da troca.
        """

        if self.__init_registro_estados == 0:
            self.__init_registro_estados = 1
        else:
            try:
                self.__db.update_controle_estados([
                    self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                    UG_SM_STR_DCT[self.codigo_state] if self.id == 1 else "",
                    UG_SM_STR_DCT[self.codigo_state] if self.id == 2 else "",
                ])

            except Exception:
                logger.error(f"[UG{self.id}] Houve um erro ao inserir os dados para controle de troca de estados no Banco de Dados.")
                logger.debug(traceback.format_exc())


    def step(self) -> "None":
        """
        Função principal de passo da Unidade.

        Serve como principal chamada para controle das Unidades da máquina de estados.
        """

        try:
            logger.debug("")
            logger.debug(f"[UG{self.id}] Step  -> Unidade:                   \"{UG_SM_STR_DCT[self.codigo_state]}\"")
            logger.debug(f"[UG{self.id}]          Etapa:                     \"{UG_STR_DCT_ETAPAS[self.etapa]}\" (Atual: {self.__leitura_etapa_atual.valor})")

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
        return
        try:
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_ETAPA_UG{self.id}"], self.etapa)
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_STATE_UG{self.id}"], self.codigo_state)

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

                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PASSOS_CMD_RST_FLH"], valor=1)
                # EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARTIDA_CMD_SINCRONISMO"], valor=1)
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

                # EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARADA_CMD_DESABILITA_UHLM"], valor=1)
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

            if setpoint_kw > 1:
                self.setpoint_minimo = self.cfg["pot_minima"]
                self.setpoint_maximo = self.cfg[f"pot_maxima_ug{self.id}"]

                self.setpoint = int(setpoint_kw)
                setpoint_porcento = ((self.setpoint / self.cfg[f"pot_maxima_ug"]) * 10000)

                logger.debug(f"[UG{self.id}]          Enviando setpoint:         {self.setpoint} kW ({setpoint_porcento / 100:2.2f} %)")

                res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PASSOS_CMD_RST_FLH"], valor=1)
                res = self.rv[f"UG{self.id}"].write_single_register(REG_CLP[f"UG{self.id}"]["RV_SETPOT_POT_ATIVA_PU"], int(setpoint_porcento))

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
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["PAINEL_LIDO"], 0)

            passo = 0
            for x in range(3):
                passo += 1
                logger.debug("")
                logger.debug(f"[UG{self.id}]          Passo: {passo}/3")
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
                sleep(1)

            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["PAINEL_LIDO"], 1)

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
            # EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARADA_CMD_EMERGENCIA"], valor=1)

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
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{self.id}"], 1)

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
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["PAINEL_LIDO"], 0)
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{self.id}"], 0)

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

        if self.tentativas_normalizacao > self.__limite_tentativas_normalizacao:
            logger.warning(f"[UG{self.id}] A UG estourou as tentativas de normalização, indisponibilizando Unidade.")
            return False

        elif (self.ts_auxiliar - self.get_time()).seconds > self.__tempo_entre_tentativas:
            self.tentativas_normalizacao += 1
            self.ts_auxiliar = self.get_time()
            logger.info(f"[UG{self.id}] Normalizando Unidade (Tentativa {self.tentativas_normalizacao}/{self.__limite_tentativas_normalizacao})")
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
        # EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARADA_CMD_EMERGENCIA"], valor=1)
        self.temporizar_partida = False
        sleep(1)


    def atenuar_carga(self) -> "None":
        """
        Função para atenuação de carga através de leitura de Pressão na Entrada da Turbina.

        Calcula o ganho e verifica os limites máximo e mínimo para deteminar se
        deve atenuar ou não.
        """

        flags = 0
        atenuacao = 0
        logger.debug(f"[UG{self.id}]          Verificando Atenuadores...")

        for condic in self.condicionadores_atenuadores:
            atenuacao = max(atenuacao, condic.valor)
            if atenuacao > 0:
                flags += 1
                logger.debug(f"[UG{self.id}]          - \"{condic.descricao}\":   Leitura: {condic.leitura:3.2f} | Atenuação: {atenuacao}")
                self.atenuacao = atenuacao
                atenuacao = 0

        if flags == 0:
            logger.debug(f"[UG{self.id}]          Não há necessidade de Atenuação.")

        ganho = 1 - self.atenuacao
        aux = self.setpoint
        self.atenuacao = 0
        if (self.setpoint > self.setpoint_minimo) and self.setpoint * ganho > self.setpoint_minimo:
            self.setpoint = self.setpoint * ganho

        elif (self.setpoint * ganho < self.setpoint_minimo) and (self.setpoint > self.setpoint_minimo):
            self.setpoint =  self.setpoint_minimo

        if self.etapa == UG_SINCRONIZADA and ganho < 1:
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
            if self.setpoint >= self.cfg["pot_minima"]:
                self.controlar_comporta()

            elif self.setpoint == 0 and not self.borda_cp_fechar:
                self.borda_cp_fechar = True
                logger.debug(f"[UG{self.id}]          Comando MOA:               \"OPERAR COMPORTA\"")
                if not self.cp[f"CP{self.id}"].fechar():
                    self.borda_cp_fechar = False

        elif self.etapa == UG_PARANDO:
            if self.setpoint >= self.cfg["pot_minima"]:
                self.enviar_setpoint(self.setpoint)

        elif self.etapa == UG_SINCRONIZANDO:
            self.borda_cp_fechar = False
            if not self.temporizar_partida:
                self.temporizar_partida = True
                threading.Thread(target=lambda: self.verificar_sincronismo()).start()

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
                self.cp[f"CP{self.id}"].operar_cracking()

            elif self.cp[f"CP{self.id}"].etapa == CP_CRACKING:

                if self.cp[f"CP{self.id}"].pressao_equalizada:
                    self.cp[f"CP{self.id}"].abrir()

                elif self.setpoint == 0 and self.leitura_potencia == 0:
                    self.cp[f"CP{self.id}"].fechar()

            elif self.cp[f"CP{self.id}"].etapa == CP_ABERTA:

                if self.setpoint >= self.cfg["pot_minima"]:
                    self.partir()

            elif self.cp[f"CP{self.id}"].etapa == CP_MANUAL:
                logger.debug(f"[CP{self.id}]          Comporta em modo Manual")
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

        autor_a = 0
        autor_n = 0
        autor_i = 0

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.debug(f"[UG{self.id}] Foram detectados condicionadores ativos na Unidade!")
            else:
                logger.debug(f"[UG{self.id}] Ainda há condicionadores ativos na Unidade!")

            for condic in condics_ativos:
                if condic.teste:
                    logger.debug(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\", Obs.: \"TESTE\"")
                    continue

                elif condic in self.condicionadores_ativos:
                    logger.debug(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    flag = condic.gravidade
                    continue

                elif condic.gravidade == CONDIC_INDISPONIBILIZAR:
                    logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_INDISPONIBILIZAR
                    self.__db.update_alarmes([
                        self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor_i == 0 else ""
                    ])
                    autor_i += 1
                    sleep(1)

                elif condic.gravidade == CONDIC_AGUARDAR:
                    logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_AGUARDAR
                    self.__db.update_alarmes([
                        self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor_i == 0 and autor_a == 0 else ""
                    ])
                    autor_a += 1
                    sleep(1)

                elif condic.gravidade == CONDIC_NORMALIZAR:
                    logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_NORMALIZAR
                    self.__db.update_alarmes([
                        self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor_i == 0 and autor_a == 0 and autor_n == 0 else ""
                    ])
                    autor_n += 1
                    sleep(1)

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
            # self.manter_unidades = bool(parametros["manter_unidades"])
            self.condic_temp_fase_r_ug.valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{self.id}"])
            self.condic_temp_fase_s_ug.valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{self.id}"])
            self.condic_temp_fase_t_ug.valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{self.id}"])
            self.condic_temp_oleo_uhrv.valor_base = float(parametros[f"alerta_temperatura_oleo_uhrv_ug{self.id}"])
            self.condic_temp_nucleo_gerador_1_ug.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_1_ug{self.id}"])
            self.condic_temp_mancal_guia_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_ug{self.id}"])
            self.condic_temp_mancal_guia_interno_1_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_interno_1_ug{self.id}"])
            self.condic_temp_mancal_guia_interno_2_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_interno_2_ug{self.id}"])
            self.condic_temp_patins_mancal_comb_1_ug.valor_base = float(parametros[f"alerta_temperatura_patins_mancal_comb_1_ug{self.id}"])
            self.condic_temp_patins_mancal_comb_2_ug.valor_base = float(parametros[f"alerta_temperatura_patins_mancal_comb_2_ug{self.id}"])
            self.condic_temp_mancal_casq_comb_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_casq_comb_ug{self.id}"])
            self.condic_temp_mancal_contra_esc_comb_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_contra_esc_comb_ug{self.id}"])
            self.condic_pressao_turbina_ug.valor_base = float(parametros[f"alerta_pressao_turbina_ug{self.id}"])

            self.condic_temp_fase_r_ug.valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{self.id}"])
            self.condic_temp_fase_s_ug.valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{self.id}"])
            self.condic_temp_fase_t_ug.valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{self.id}"])
            self.condic_temp_oleo_uhrv.valor_limite = float(parametros[f"limite_temperatura_oleo_uhrv_ug{self.id}"])
            self.condic_temp_nucleo_gerador_1_ug.valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_1_ug{self.id}"])
            self.condic_temp_mancal_guia_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_ug{self.id}"])
            self.condic_temp_mancal_guia_interno_1_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_interno_1_ug{self.id}"])
            self.condic_temp_mancal_guia_interno_2_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_interno_2_ug{self.id}"])
            self.condic_temp_patins_mancal_comb_1_ug.valor_limite = float(parametros[f"limite_temperatura_patins_mancal_comb_1_ug{self.id}"])
            self.condic_temp_patins_mancal_comb_2_ug.valor_limite = float(parametros[f"limite_temperatura_patins_mancal_comb_2_ug{self.id}"])
            self.condic_temp_mancal_casq_comb_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_casq_comb_ug{self.id}"])
            self.condic_temp_mancal_contra_esc_comb_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_contra_esc_comb_ug{self.id}"])
            self.condic_pressao_turbina_ug.valor_limite = float(parametros[f"limite_pressao_turbina_ug{self.id}"])

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores.")
            logger.debug(traceback.format_exc())


    def verificar_limites(self) -> "None":
        """
        Função para verificação de limites de operação da Unidade.

        Verifica os valores base e limite da Unidade, pré-determinados na interface
        WEB, e avisa o operador caso algum valor ultrapasse o estipulado.
        """

        if self.l_temp_oleo_uhrv.valor >= self.condic_temp_oleo_uhrv.valor_base and self.brd_t_oleo_uhrv == 0:
            self.brd_t_oleo_uhrv = 1
            logger.debug(f"[UG{self.id}] A temperatura do Óleo da UHRV da UG passou do valor base! ({self.condic_temp_oleo_uhrv.valor_base}C) | Leitura: {self.l_temp_oleo_uhrv.valor:0.2f}C")

        if (self.l_temp_oleo_uhrv.valor >= 0.9*(self.condic_temp_oleo_uhrv.valor_limite - self.condic_temp_oleo_uhrv.valor_base) + self.condic_temp_oleo_uhrv.valor_base) and self.brd_t_oleo_uhrv in (0,1):
            self.brd_t_oleo_uhrv = 2
            logger.debug(f"[UG{self.id}] A temperatura do Óleo da UHRV da UG está muito próxima do limite! ({self.condic_temp_oleo_uhrv.valor_limite}C) | Leitura: {self.l_temp_oleo_uhrv.valor:0.2f}C")

        if self.l_temp_oleo_uhrv.valor < self.condic_temp_oleo_uhrv.valor_base and self.brd_t_oleo_uhrv in (1,2):
            self.brd_t_oleo_uhrv = 0
            logger.debug(f"[UG{self.id}] A temperatura do óleo da UHRV voltou ao Normal. Leitura: {self.l_temp_oleo_uhrv.valor:0.2f}C")



        if self.l_temp_fase_R.valor >= self.condic_temp_fase_r_ug.valor_base and self.brd_t_fase_r == 0:
            self.brd_t_fase_r = 1
            logger.debug(f"[UG{self.id}] A temperatura de Fase R da UG passou do valor base! ({self.condic_temp_fase_r_ug.valor_base}C) | Leitura: {self.l_temp_fase_R.valor:0.2f}C")

        if (self.l_temp_fase_R.valor >= 0.9*(self.condic_temp_fase_r_ug.valor_limite - self.condic_temp_fase_r_ug.valor_base) + self.condic_temp_fase_r_ug.valor_base) and self.brd_t_fase_r in (0,1):
            self.brd_t_fase_r = 2
            logger.debug(f"[UG{self.id}] A temperatura de Fase R da UG está muito próxima do limite! ({self.condic_temp_fase_r_ug.valor_limite}C) | Leitura: {self.l_temp_fase_R.valor:0.2f}C")

        if self.l_temp_fase_R.valor <= self.condic_temp_fase_r_ug.valor_base and self.brd_t_fase_r in (1,2):
            self.brd_t_fase_r = 0
            logger.info(f"[UG{self.id}] A temperatura de Fase R da UG voltou ao Normal. Leitura: {self.l_temp_fase_R.valor:0.2f}C")



        if self.l_temp_fase_S.valor >= self.condic_temp_fase_s_ug.valor_base and self.brd_t_fase_s == 0:
            self.brd_t_fase_s = 1
            logger.debug(f"[UG{self.id}] A temperatura de Fase S da UG passou do valor base! ({self.condic_temp_fase_s_ug.valor_base}C) | Leitura: {self.l_temp_fase_S.valor:0.2f}C")

        if (self.l_temp_fase_S.valor >= 0.9*(self.condic_temp_fase_s_ug.valor_limite - self.condic_temp_fase_s_ug.valor_base) + self.condic_temp_fase_s_ug.valor_base) and self.brd_t_fase_s in (0,1):
            self.brd_t_fase_s = 2
            logger.debug(f"[UG{self.id}] A temperatura de Fase S da UG está muito próxima do limite! ({self.condic_temp_fase_s_ug.valor_limite}C) | Leitura: {self.l_temp_fase_S.valor:0.2f}C")

        if self.l_temp_fase_S.valor >= self.condic_temp_fase_s_ug.valor_base and self.brd_t_fase_s in (1,2):
            self.brd_t_fase_s = 0
            logger.info(f"[UG{self.id}] A temperatura de Fase S da UG voltou ao Normal. Leitura: {self.l_temp_oleo_uhrv.valor:0.2f}C")



        if self.l_temp_fase_T.valor >= self.condic_temp_fase_t_ug.valor_base and self.brd_t_fase_t == 0:
            self.brd_t_fase_t = 1
            logger.debug(f"[UG{self.id}] A temperatura de Fase T da UG passou do valor base! ({self.condic_temp_fase_t_ug.valor_base}C) | Leitura: {self.l_temp_fase_T.valor:0.2f}C")

        if (self.l_temp_fase_T.valor >= 0.9*(self.condic_temp_fase_t_ug.valor_limite - self.condic_temp_fase_t_ug.valor_base) + self.condic_temp_fase_t_ug.valor_base) and self.brd_t_fase_t in (0,1):
            self.brd_t_fase_t = 2
            logger.debug(f"[UG{self.id}] A temperatura de Fase T da UG está muito próxima do limite! ({self.condic_temp_fase_t_ug.valor_limite}C) | Leitura: {self.l_temp_fase_T.valor:0.2f}C")

        if self.l_temp_fase_T.valor <= self.condic_temp_fase_t_ug.valor_base and self.brd_t_fase_t in (1,2):
            self.brd_t_fase_t = 0
            logger.info(f"[UG{self.id}] A temperatura de Fase T da UG voltou ao Normal. Leitura: {self.l_temp_fase_T.valor:0.2f}C")



        if self.l_temp_nucleo_gerador_1.valor >= self.condic_temp_nucleo_gerador_1_ug.valor_base and self.brd_t_nuc_gera == 0:
            self.brd_t_nuc_gera = 1
            logger.debug(f"[UG{self.id}] A temperatura do Núcleo Gerador 1 da UG passou do valor base! ({self.condic_temp_nucleo_gerador_1_ug.valor_base}C) | Leitura: {self.l_temp_nucleo_gerador_1.valor:0.2f}C")

        if (self.l_temp_nucleo_gerador_1.valor >= 0.9*(self.condic_temp_nucleo_gerador_1_ug.valor_limite - self.condic_temp_nucleo_gerador_1_ug.valor_base) + self.condic_temp_nucleo_gerador_1_ug.valor_base) and self.brd_t_nuc_gera in (0,1):
            self.brd_t_nuc_gera = 2
            logger.debug(f"[UG{self.id}] A temperatura do Núcleo Gerador 1 da UG está muito próxima do limite! ({self.condic_temp_nucleo_gerador_1_ug.valor_limite}C) | Leitura: {self.l_temp_nucleo_gerador_1.valor:0.2f}C")

        if self.l_temp_nucleo_gerador_1.valor <= self.condic_temp_nucleo_gerador_1_ug.valor_base and self.brd_t_nuc_gera in (1,2):
            self.brd_t_nuc_gera = 0
            logger.debug(f"[UG{self.id}] A temperatura do Núcleo Gerador 1 da UG voltou ao Normal. Leitura: {self.l_temp_nucleo_gerador_1.valor:0.2f}C")



        if self.l_temp_mancal_guia.valor >= self.condic_temp_mancal_guia_ug.valor_base and self.brd_t_manc_guia == 0:
            self.brd_t_manc_guia = 1
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Guia da UG passou do valor base! ({self.condic_temp_mancal_guia_ug.valor_base}C) | Leitura: {self.l_temp_mancal_guia.valor:0.2f}C")

        if (self.l_temp_mancal_guia.valor >= 0.9*(self.condic_temp_mancal_guia_ug.valor_limite - self.condic_temp_mancal_guia_ug.valor_base) + self.condic_temp_mancal_guia_ug.valor_base) and self.brd_t_manc_guia in (0,1):
            self.brd_t_manc_guia = 2
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Guia da UG está muito próxima do limite! ({self.condic_temp_mancal_guia_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_guia.valor:0.2f}C")

        if self.l_temp_mancal_guia.valor <= self.condic_temp_mancal_guia_ug.valor_base and self.brd_t_manc_guia in (1,2):
            self.brd_t_manc_guia = 0
            logger.info(f"[UG{self.id}] A temperatura do Mancal Guia da UG voltou ao Normal. Leitura: {self.l_temp_mancal_guia.valor:0.2f}C")



        if self.l_temp_mancal_guia_interno_1.valor >= self.condic_temp_mancal_guia_interno_1_ug.valor_base and self.brd_t_manc_guia_in_1 == 0:
            self.brd_t_manc_guia_in_1 = 1
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Guia Interno 1 da UG passou do valor base! ({self.condic_temp_mancal_guia_interno_1_ug.valor_base}C) | Leitura: {self.l_temp_mancal_guia_interno_1.valor:0.2f}C")

        if (self.l_temp_mancal_guia_interno_1.valor >= 0.9*(self.condic_temp_mancal_guia_interno_1_ug.valor_limite - self.condic_temp_mancal_guia_interno_1_ug.valor_base) + self.condic_temp_mancal_guia_interno_1_ug.valor_base) and self.brd_t_manc_guia_in_1 in (0,1):
            self.brd_t_manc_guia_in_1 = 2
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Guia Interno 1 da UG está muito próxima do limite! ({self.condic_temp_mancal_guia_interno_1_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_guia_interno_1.valor:0.2f}C")

        if self.l_temp_mancal_guia_interno_1.valor <= self.condic_temp_mancal_guia_interno_1_ug.valor_base and self.brd_t_manc_guia_in_1 in (1,2):
            self.brd_t_manc_guia_in_1 = 0
            logger.info(f"[UG{self.id}] A temperatura do Mancal Guia Interno 1 da UG voltou ao Normal. Leitura {self.l_temp_mancal_guia_interno_1.valor:0.2f}C")



        if self.l_temp_mancal_guia_interno_2.valor >= self.condic_temp_mancal_guia_interno_2_ug.valor_base and self.brd_t_manc_guia_in_2 == 0:
            self.brd_t_manc_guia_in_2 = 1
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Guia Interno 2 da UG passou do valor base! ({self.condic_temp_mancal_guia_interno_2_ug.valor_base}C) | Leitura: {self.l_temp_mancal_guia_interno_2.valor:0.2f}C")

        if (self.l_temp_mancal_guia_interno_2.valor >= 0.9*(self.condic_temp_mancal_guia_interno_2_ug.valor_limite - self.condic_temp_mancal_guia_interno_2_ug.valor_base) + self.condic_temp_mancal_guia_interno_2_ug.valor_base) and self.brd_t_manc_guia_in_2 in (0,1):
            self.brd_t_manc_guia_in_2 = 2
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Guia Interno 2 da UG está muito próxima do limite! ({self.condic_temp_mancal_guia_interno_2_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_guia_interno_2.valor:0.2f}C")

        if self.l_temp_mancal_guia_interno_2.valor <= self.condic_temp_mancal_guia_interno_2_ug.valor_base and self.brd_t_manc_guia_in_2 in (1,2):
            self.brd_t_manc_guia_in_2 = 0
            logger.info(f"[UG{self.id}] A temperatura do Mancal Guia Interno 2 voltou ao Normal. Leitura: {self.l_temp_mancal_guia_interno_2.valor:0.2f}C")



        if self.l_temp_patins_mancal_comb_1.valor >= self.condic_temp_patins_mancal_comb_1_ug.valor_base and self.brd_t_pat_manc_comb_1 == 0:
            self.brd_t_pat_manc_comb_1 = 1
            logger.debug(f"[UG{self.id}] A temperatura dos Patins do Mancal combinado 1 da UG passou do valor base! ({self.condic_temp_patins_mancal_comb_1_ug.valor_base}C) | Leitura: {self.l_temp_patins_mancal_comb_1.valor:0.2f}C")

        if (self.l_temp_patins_mancal_comb_1.valor >= 0.9*(self.condic_temp_patins_mancal_comb_1_ug.valor_limite - self.condic_temp_patins_mancal_comb_1_ug.valor_base) + self.condic_temp_patins_mancal_comb_1_ug.valor_base) and self.brd_t_pat_manc_comb_1 in (0,1):
            self.brd_t_pat_manc_comb_1 = 2
            logger.debug(f"[UG{self.id}] A temperatura dos Patins do Mancal combinado 1 da UG está muito próxima do limite! ({self.condic_temp_patins_mancal_comb_1_ug.valor_limite}C) | Leitura: {self.l_temp_patins_mancal_comb_1.valor:0.2f}C")

        if self.l_temp_patins_mancal_comb_1.valor <= self.condic_temp_patins_mancal_comb_1_ug.valor_base and self.brd_t_pat_manc_comb_1 in (1,2):
            self.brd_t_pat_manc_comb_1 = 0
            logger.info(f"[UG{self.id}] A temperatura do Patins do Mancal Combinado 1 voltou ao Normal. Leitura: {self.l_temp_patins_mancal_comb_1.valor:0.2f}C")



        if self.l_temp_patins_mancal_comb_2.valor >= self.condic_temp_patins_mancal_comb_2_ug.valor_base and self.brd_t_pat_manc_comb_2 == 0:
            self.brd_t_pat_manc_comb_2 = 1
            logger.debug(f"[UG{self.id}] A temperatura dos Patins do Mancal combinado 2 da UG passou do valor base! ({self.condic_temp_patins_mancal_comb_2_ug.valor_base}C) | Leitura: {self.l_temp_patins_mancal_comb_2.valor:0.2f}C")

        if (self.l_temp_patins_mancal_comb_2.valor >= 0.9*(self.condic_temp_patins_mancal_comb_2_ug.valor_limite - self.condic_temp_patins_mancal_comb_2_ug.valor_base) + self.condic_temp_patins_mancal_comb_2_ug.valor_base) and self.brd_t_pat_manc_comb_2 in (0,1):
            self.brd_t_pat_manc_comb_2 = 2
            logger.debug(f"[UG{self.id}] A temperatura dos Patins do Mancal combinado 2 da UG está muito próxima do limite! ({self.condic_temp_patins_mancal_comb_2_ug.valor_limite}C) | Leitura: {self.l_temp_patins_mancal_comb_2.valor:0.2f}C")

        if self.l_temp_patins_mancal_comb_2.valor <= self.condic_temp_patins_mancal_comb_2_ug.valor_base and self.brd_t_pat_manc_comb_2 in (1,2):
            self.brd_t_pat_manc_comb_2 = 0
            logger.info(f"[UG{self.id}] A temperatura do Patins do Mancal Combinado 2 voltou ao Normal. Leitura: {self.l_temp_patins_mancal_comb_2.valor:0.2f}C")



        if self.l_temp_mancal_casq_comb.valor >= self.condic_temp_mancal_casq_comb_ug.valor_base and self.brd_t_manc_casq_comb == 0:
            self.brd_t_manc_casq_comb = 1
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Casquilho Combinado da UG passou do valor base! ({self.condic_temp_mancal_casq_comb_ug.valor_base}C) | Leitura: {self.l_temp_mancal_casq_comb.valor:0.2f}C")

        if (self.l_temp_mancal_casq_comb.valor >= 0.9*(self.condic_temp_mancal_casq_comb_ug.valor_limite - self.condic_temp_mancal_casq_comb_ug.valor_base) + self.condic_temp_mancal_casq_comb_ug.valor_base) and self.brd_t_manc_casq_comb in (0,1):
            self.brd_t_manc_casq_comb = 2
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Casquilho Combinado da UG está muito próxima do limite! ({self.condic_temp_mancal_casq_comb_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_casq_comb.valor:0.2f}C")

        if self.l_temp_mancal_casq_comb.valor <= self.condic_temp_mancal_casq_comb_ug.valor_base and self.brd_t_manc_casq_comb in (1,2):
            self.brd_t_manc_casq_comb = 0
            logger.info(f"[UG{self.id}] A temperatura do Mancal Casquilho Combinado voltou ao Normal. Leitura: {self.l_temp_patins_mancal_comb_2.valor:0.2f}C")



        if self.l_temp_mancal_contra_esc_comb.valor >= self.condic_temp_mancal_contra_esc_comb_ug.valor_base and self.brd_t_manc_con_esc_comb == 0:
            self.brd_t_manc_con_esc_comb = 1
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Contra Escora Combinado da UG passou do valor base! ({self.condic_temp_mancal_contra_esc_comb_ug.valor_base}C) | Leitura: {self.l_temp_mancal_contra_esc_comb.valor:0.2f}C")

        if (self.l_temp_mancal_contra_esc_comb.valor >= 0.9*(self.condic_temp_mancal_contra_esc_comb_ug.valor_limite - self.condic_temp_mancal_contra_esc_comb_ug.valor_base) + self.condic_temp_mancal_contra_esc_comb_ug.valor_base) and self.brd_t_manc_con_esc_comb in (0,1):
            self.brd_t_manc_con_esc_comb = 2
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Contra Escora Combinado da UG está muito próxima do limite! ({self.condic_temp_mancal_contra_esc_comb_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_contra_esc_comb.valor:0.2f}C")

        if self.l_temp_mancal_contra_esc_comb.valor >= self.condic_temp_mancal_contra_esc_comb_ug.valor_base and self.brd_t_manc_con_esc_comb in (1,2):
            self.brd_t_manc_con_esc_comb = 0
            logger.info(f"[UG{self.id}] A temperatura do Mancal Contra Escora Combinado voltou ao Normal. Leitura: {self.l_temp_patins_mancal_comb_2.valor:0.2f}C")



        if self.l_pressao_turbina.valor <= self.condic_pressao_turbina_ug.valor_base and self.l_pressao_turbina.valor != 0 and self.etapa == UG_SINCRONIZADA and self.brd_p_ent_turb == 0:
            self.brd_p_ent_turb = 1
            logger.debug(f"[UG{self.id}] A pressão na entrada da turbina da UG passou do valor base! ({self.condic_pressao_turbina_ug.valor_base:03.2f} KGf/m2) | Leitura: {self.l_pressao_turbina.valor:03.2f}")

        if self.l_pressao_turbina.valor <= self.condic_pressao_turbina_ug.valor_limite+0.9*(self.condic_pressao_turbina_ug.valor_base - self.condic_pressao_turbina_ug.valor_limite) and self.l_pressao_turbina.valor != 0 and self.etapa == UG_SINCRONIZADA and self.brd_p_ent_turb in (0,1):
            self.brd_p_ent_turb = 2
            logger.debug(f"[UG{self.id}] A pressão na entrada da turbina da UG está muito próxima do limite! ({self.condic_pressao_turbina_ug.valor_limite:03.2f} KGf/m2) | Leitura: {self.l_pressao_turbina.valor:03.2f} KGf/m2")

        if self.l_pressao_turbina.valor >= self.condic_pressao_turbina_ug.valor_base and self.l_pressao_turbina.valor != 0 and self.etapa == UG_SINCRONIZADA and self.brd_p_ent_turb in (1,2):
            self.brd_p_ent_turb = 0
            logger.info(f"[UG{self.id}] A Pressão na Entrada da Turbina voltou ao Normal. Leitura: {self.l_pressao_turbina.valor:03.2f} KGf/m2")



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
        # Temperaturas
            # Fase R
        self.brd_t_fase_r = 0
        self.l_temp_fase_R = LeituraModbusFloat(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_A_TMP"], descricao=f"[UG{self.id}] Fase A Temperatura")
        self.condic_temp_fase_r_ug = c.CondicionadorExponencial(self.l_temp_fase_R, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.condic_temp_fase_r_ug)
        self.condicionadores_atenuadores.append(self.condic_temp_fase_r_ug)

            # Fase S
        self.brd_t_fase_s = 0
        self.l_temp_fase_S = LeituraModbusFloat(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_B_TMP"], descricao=f"[UG{self.id}] Fase B Temperatura")
        self.condic_temp_fase_s_ug = c.CondicionadorExponencial(self.l_temp_fase_S, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.condic_temp_fase_s_ug)
        self.condicionadores_atenuadores.append(self.condic_temp_fase_s_ug)

            # Fase T
        self.brd_t_fase_t = 0
        self.l_temp_fase_T = LeituraModbusFloat(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_C_TMP"], descricao=f"[UG{self.id}] Fase C Temperatura")
        self.condic_temp_fase_t_ug = c.CondicionadorExponencial(self.l_temp_fase_T, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.condic_temp_fase_t_ug)
        self.condicionadores_atenuadores.append(self.condic_temp_fase_t_ug)

            # Óleo UHRV
        self.brd_t_oleo_uhrv = 0
        self.l_temp_oleo_uhrv = LeituraModbusFloat(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["OLEO_UHRV_TMP"], descricao=f"[UG{self.id}] Óleo UHRV Temperatura")
        self.condic_temp_oleo_uhrv = c.CondicionadorExponencial(self.l_temp_oleo_uhrv, CONDIC_INDISPONIBILIZAR, valor_base=39, valor_limite=42)
        self.condicionadores_essenciais.append(self.condic_temp_oleo_uhrv)
        self.condicionadores_atenuadores.append(self.condic_temp_oleo_uhrv)

            # Nucleo Gerador 1
        self.brd_t_nuc_gera = 0
        self.l_temp_nucleo_gerador_1 = LeituraModbusFloat(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_NUCL_ESTAT_TMP"], descricao=f"[UG{self.id}] Núcleo Gerador Temperatura")
        self.condic_temp_nucleo_gerador_1_ug = c.CondicionadorExponencial(self.l_temp_nucleo_gerador_1, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.condic_temp_nucleo_gerador_1_ug)
        self.condicionadores_atenuadores.append(self.condic_temp_nucleo_gerador_1_ug)

            # Mancal Guia
        self.brd_t_manc_guia = 0
        self.l_temp_mancal_guia = LeituraModbusFloat(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_TMP"], descricao=f"[UG{self.id}] Mancal Guia Temperatura")
        self.condic_temp_mancal_guia_ug = c.CondicionadorExponencial(self.l_temp_mancal_guia, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.condic_temp_mancal_guia_ug)
        self.condicionadores_atenuadores.append(self.condic_temp_mancal_guia_ug)

            # Mancal Guia Interno 1
        self.brd_t_manc_guia_in_1 = 0
        self.l_temp_mancal_guia_interno_1 = LeituraModbusFloat(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_1_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 1 Temperatura")
        self.condic_temp_mancal_guia_interno_1_ug = c.CondicionadorExponencial(self.l_temp_mancal_guia_interno_1, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.condic_temp_mancal_guia_interno_1_ug)
        self.condicionadores_atenuadores.append(self.condic_temp_mancal_guia_interno_1_ug)

            # Mancal Guia Interno 2
        self.brd_t_manc_guia_in_2 = 0
        self.l_temp_mancal_guia_interno_2 = LeituraModbusFloat(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_2_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 2 Temperatura")
        self.condic_temp_mancal_guia_interno_2_ug = c.CondicionadorExponencial(self.l_temp_mancal_guia_interno_2, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.condic_temp_mancal_guia_interno_2_ug)
        self.condicionadores_atenuadores.append(self.condic_temp_mancal_guia_interno_2_ug)

            # Patins Mancal combinado 1
        self.brd_t_pat_manc_comb_1 = 0
        self.l_temp_patins_mancal_comb_1 = LeituraModbusFloat(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_1_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 1 Temperatura")
        self.condic_temp_patins_mancal_comb_1_ug = c.CondicionadorExponencial(self.l_temp_patins_mancal_comb_1, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.condic_temp_patins_mancal_comb_1_ug)
        self.condicionadores_atenuadores.append(self.condic_temp_patins_mancal_comb_1_ug)

            # Patins Mancal combinado 2
        self.brd_t_pat_manc_comb_2 = 0
        self.l_temp_patins_mancal_comb_2 = LeituraModbusFloat(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_2_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 2 Temperatura")
        self.condic_temp_patins_mancal_comb_2_ug = c.CondicionadorExponencial(self.l_temp_patins_mancal_comb_2, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.condic_temp_patins_mancal_comb_2_ug)
        self.condicionadores_atenuadores.append(self.condic_temp_patins_mancal_comb_2_ug)

            # Mancal Casquilho combinado
        self.brd_t_manc_casq_comb = 0
        self.l_temp_mancal_casq_comb = LeituraModbusFloat(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CASQ_COMB_TMP"], descricao=f"[UG{self.id}] Mancal Casquilho Combinado Temperatura")
        self.condic_temp_mancal_casq_comb_ug = c.CondicionadorExponencial(self.l_temp_mancal_casq_comb, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.condic_temp_mancal_casq_comb_ug)
        self.condicionadores_atenuadores.append(self.condic_temp_mancal_casq_comb_ug)

            # Mancal Contra Escora combinado
        self.brd_t_manc_con_esc_comb = 0
        self.l_temp_mancal_contra_esc_comb = LeituraModbusFloat(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CONT_ESCO_COMB_TMP"], descricao=f"[UG{self.id}] Mancal Contra Escora Combinado Temperatura")
        self.condic_temp_mancal_contra_esc_comb_ug = c.CondicionadorExponencial(self.l_temp_mancal_contra_esc_comb, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.condic_temp_mancal_contra_esc_comb_ug)
        self.condicionadores_atenuadores.append(self.condic_temp_mancal_contra_esc_comb_ug)

        # CONDICIONCADORES ATENUADORES
            # Pressão Entrada Turbina
        self.brd_p_ent_turb = 0
        self.l_pressao_turbina = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["ENTRADA_TURBINA_PRESSAO"], escala=0.1, descricao=f"[UG{self.id}] Pressão Entrada Turbina")
        self.condic_pressao_turbina_ug = c.CondicionadorExponencialReverso(self.l_pressao_turbina, CONDIC_INDISPONIBILIZAR, 1.6, 1.3)
        self.condicionadores_atenuadores.append(self.condic_pressao_turbina_ug)