__version__ = "0.2"
__author__ = "Lucas Lavratti", "Henrique Pfeifer", "Diego Basgal"
__description__ = "Este módulo corresponde a implementação das Unidades de Geração."

import pytz
import logging
import traceback
import threading

import src.comporta as cp
import src.subestacao as se
import src.tomada_agua as tda
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
    def __init__(self, id: "int", cfg: "dict"=None, bd: "BancoDados"=None, cp: "dict[str, cp.Comporta]"=None, serv: "Servidores"=None):

        # VERIFICAÇÃO DE ARGUMENTOS

        if id <= 0:
            logger.error(f"[UG{self.id}] A Unidade não pode ser instanciada com o ID <= \"0\" ou vazio.")
            raise ValueError
        else:
            self.__id = id

        self.bd = bd
        self.cfg = cfg

        self.cp = cp
        self.rv = serv.rv
        self.rt = serv.rt
        self.clp = serv.clp
        self.rele = serv.rele

        # ATRIBUIÇÃO DE VAIRIÁVEIS

        # PRIVADAS
        self.__leitura_potencia = LeituraModbusFloat(
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
        self.__leitura_posicao_distribuidor = LeituraModbus(
            self.rv[f"UG{self.id}"],
            REG_CLP[f"UG{self.id}"]["RV_FEEDBACK_DISTRIBUIDOR_PU"],
            escala=0.01,
            descricao=f"[UG{self.id}][RV] Leitura Posição Distribuidor"
        )
        self.__perda_grade = LeituraModbusFloat(
            self.clp["TDA"],
            REG_CLP["TDA"][f"DIFERENCIAL_GRADE_CP{self.id}"],
            descricao=f"[TDA] Leitura Perda Grade CP{self.id}"
        )

        self.__init_registro_estados: "int" = 0
        self.__tempo_entre_tentativas: "int" = 0
        self.__limite_tentativas_normalizacao: "int" = 2


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
        self.amostras_sp_mppt: "int" = 2
        self.amostras_pot_mppt: "int" = 5

        self.atenuacao: "int" = 0
        self.tempo_normalizar: "int" = 0

        self.sp_anterior: "float" = 0
        self.pot_anterior: "float" = 0
        self.pos_distri_anterior: "float" = 0

        self.borda_parar: "bool" = False
        self.manter_unidades: "bool" = False
        self.operar_comporta: "bool" = False
        self.temporizar_partida: "bool" = False
        self.aguardar_pressao_cp: "bool" = False
        self.normalizacao_agendada: "bool" = False
        self.temporizar_normalizacao: "bool" = False

        self.borda_cp_fechar: "bool" = False

        self.potencias_anteriores: "list[int]" = []
        self.setpoints_anteriores: "list[int]" = []
        self.media_amostras_distribuidor: "list[int]" = []
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
    def leitura_potencia(self) -> "float":
        # PROPRIEDADE -> Retorna a leitura de Potência da Unidade.

        return int(self.__leitura_potencia.valor)

    @property
    def leitura_horimetro(self) -> "float":
        # PROPRIEDADE -> Retorna a leitura de horas de geração da Unidade.

        return self.__leitura_horimetro.valor

    @property
    def leitura_posicao_distribuidor(self) -> "int":
        # PROPRIEDADE -> Retorna a leitura de posição do distribuidor do RV

        return self.__leitura_posicao_distribuidor.valor

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

        self._tentativas_normalizacao = var

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

        estado = self.bd.get_ultimo_estado_ug(self.id)[0]

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
                self.bd.update_controle_estados([
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
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86M_CMD_REARME_BLQ"], valor=1)
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86E_CMD_REARME_BLQ"], valor=1)
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86H_CMD_REARME_BLQ"], valor=1)
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_CMD_REARME_FLH"], valor=1)
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_CMD_REARME_FLH"], valor=1)
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARTIDA_CMD_SINCRONISMO"], valor=1)
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

                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARADA_CMD_DESABILITA_UHLM"], valor=1)
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

        self.coletar_amostras_distribuidor()
        media_distribuidor = sum(l_dist for l_dist in self.media_amostras_distribuidor) / len(self.media_amostras_distribuidor)

        cont_mppt = 0
        for pot in self.potencias_anteriores:
            if pot+50 < setpoint_kw:
                cont_mppt += 1

        debug_log.debug("")
        debug_log.debug("")
        debug_log.debug(f"________________________________________________________________________")
        debug_log.debug(f"[UG{self.id}] Amostras Potência             ->    {self.potencias_anteriores}")
        debug_log.debug("")
        # debug_log.debug(f"[UG{self.id}] Amostras Posição Distribuidor ->    {self.media_amostras_distribuidor}")
        # debug_log.debug(f"[UG{self.id}] Média Amostras Distribuidor:        {media_distribuidor}")
        # debug_log.debug("")

        if cont_mppt == self.amostras_pot_mppt and (self.cfg['pot_maxima_ug'] - 500) <= setpoint_kw <= self.cfg["pot_maxima_ug"]:
            setpoint_kw = self.ajustar_mppt(
                [self.leitura_potencia, self.potencias_anteriores[-1]],
                [self.setpoints_anteriores[-1], self.setpoints_anteriores[-2]],
                [self.leitura_posicao_distribuidor, self.pos_dist_anterior],
            )

            setpoint_kw = self.cfg['pot_minima'] if setpoint_kw <= self.cfg['pot_minima'] else setpoint_kw

            logger.debug(f"[UG{self.id}]          Enviando setpoint:")
            logger.debug(f"[UG{self.id}]          - \"MPPT\":                  {setpoint_kw:0.0f} kW")

        else:
            logger.debug(f"[UG{self.id}]          Enviando setpoint:         {int(setpoint_kw):0.0f} kW ({((setpoint_kw / self.cfg[f'pot_maxima_ug']) * 10000) / 100:2.2f} %)")

        self.setpoint = int(setpoint_kw)
        self.pos_dist_anterior = self.leitura_posicao_distribuidor

        self.popular_listas_sp_pot()
        self.media_amostras_distribuidor = []

        try:
            self.setpoint_minimo = self.cfg["pot_minima"]
            self.setpoint_maximo = self.cfg[f"pot_maxima_ug{self.id}"]

            setpoint_porcento = ((self.setpoint / self.cfg[f"pot_maxima_ug"]) * 10000)

            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PASSOS_CMD_RST_FLH"], valor=1)
            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86M_CMD_REARME_BLQ"], valor=1)
            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86E_CMD_REARME_BLQ"], valor=1)
            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86H_CMD_REARME_BLQ"], valor=1)
            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_CMD_REARME_FLH"], valor=1)
            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_CMD_REARME_FLH"], valor=1)
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

            for x in range(3):
                logger.debug("")
                logger.debug(f"[UG{self.id}]          Passo: {x+1}/3")
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


    def popular_listas_sp_pot(self) -> "None":
        """
        FUnção para popular listas com leituras e cálculos de potência e setpoint,
        para controle do MPPT.
        """

        if self.etapa == UG_PARADA or (self.cfg['pot_minima'] < self.leitura_potencia < self.cfg['pot_minima'] + 500):
            self.potencias_anteriores = []

        elif self.etapa == UG_SINCRONIZADA:
            if len(self.potencias_anteriores) == self.amostras_pot_mppt + 1:
                self.potencias_anteriores.pop(-1)

            if len(self.setpoints_anteriores) == self.amostras_sp_mppt + 1:
                self.setpoints_anteriores.pop(-1)

            if len(self.potencias_anteriores) == self.amostras_pot_mppt and self.cfg['pot_minima'] <= self.leitura_potencia <= self.cfg['pot_maxima_ug']:
                self.potencias_anteriores.pop(0)
                self.potencias_anteriores.append(self.leitura_potencia)

            elif self.cfg['pot_minima'] <= self.leitura_potencia <= self.cfg['pot_maxima_ug']:
                self.potencias_anteriores.append(self.leitura_potencia)

            if len(self.setpoints_anteriores) == self.amostras_sp_mppt and self.cfg['pot_minima'] <= self.setpoint <= self.cfg['pot_maxima_ug']:
                self.setpoints_anteriores.pop(0)
                self.setpoints_anteriores.append(self.setpoint)

            elif self.cfg['pot_minima'] <= self.setpoint <= self.cfg['pot_maxima_ug']:
                self.setpoints_anteriores.append(self.setpoint)


    def coletar_amostras_distribuidor(self) -> "int":
        for n in range(5):
            if self.leitura_posicao_distribuidor in (0, None):
                continue
            self.media_amostras_distribuidor.append(self.leitura_posicao_distribuidor)
            sleep(0.5)


    def ajustar_mppt(self, potencia, setpoint, abertura_dist) -> "float":
        """
        Função para ajuste de setpoint, baseado na entrega máxima de potência,
        por MPPT (Maximum Power Point Tracking)
        """

        setpoint_saida = max(min(setpoint[0], self.cfg['pot_maxima_ug']), self.cfg['pot_minima'])
        delta = 20

        if potencia[0] < potencia[1]:
            if abertura_dist[0] < abertura_dist[1]:
                setpoint_saida += delta
            else:
                setpoint_saida -= delta

        elif potencia[0] == potencia[1]:
            setpoint_saida -= delta

        else:
            if abertura_dist[0] - 0.1 < abertura_dist[1]:
                setpoint_saida -= delta
            else:
                setpoint_saida += delta

        setpoint_saida = max(min(setpoint_saida, self.cfg['pot_maxima_ug']), self.cfg['pot_minima'])
        return setpoint_saida


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
            self._tentativas_normalizacao += 1
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
        EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARADA_CMD_EMERGENCIA"], valor=1)
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
        logger.debug(f"[UG{self.id}]          Verificando Atenuadores...") if self.etapa == UG_SINCRONIZADA else None

        for condic in self.condicionadores_atenuadores:
            atenuacao = max(atenuacao, condic.valor)
            if atenuacao > 0:
                flags += 1
                logger.debug(f"[UG{self.id}]          - \"{condic.descricao}\":")
                logger.debug(f"[UG{self.id}]                                     Leitura: {condic.leitura:3.2f} | Atenuação: {atenuacao:0.4f}")

                if flags == 1:
                    self.atenuacao = atenuacao
                elif atenuacao > self.atenuacao:
                    self.atenuacao = atenuacao
                else:
                    pass
                atenuacao = 0

        if flags == 0 and self.etapa == UG_SINCRONIZADA:
            logger.debug(f"[UG{self.id}]          Não há necessidade de Atenuação.")

        ganho = 1 - self.atenuacao
        aux = self.setpoint
        self.atenuacao = 0
        if (self.setpoint > self.setpoint_minimo) and self.setpoint * ganho > self.setpoint_minimo:
            setpoint_atenuado = self.setpoint - 0.5 * (self.setpoint -  (self.setpoint * ganho))
            self.setpoint = min(max(setpoint_atenuado, self.setpoint_minimo), self.setpoint_maximo)

        elif self.setpoint > self.setpoint_minimo and (self.setpoint * ganho) < self.setpoint_minimo:
            self.setpoint = self.setpoint_minimo

        if self.etapa == UG_SINCRONIZADA and ganho < 1:
            logger.debug(f"[UG{self.id}]                                     SP {aux} * GANHO {ganho:0.4f} = {self.setpoint} kW")


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
        autor_i = autor_a = autor_n = 0

        if True in (condic.ativo for condic in self.condicionadores_essenciais) and self.etapa not in (UG_PARADA, UG_PARADA2):
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

                    flag = CONDIC_INDISPONIBILIZAR if flag in (CONDIC_IGNORAR, CONDIC_NORMALIZAR, CONDIC_INDISPONIBILIZAR) and condic.gravidade == CONDIC_INDISPONIBILIZAR else flag
                    flag = CONDIC_AGUARDAR if flag in (CONDIC_IGNORAR, CONDIC_NORMALIZAR) and condic.gravidade == CONDIC_AGUARDAR else flag
                    flag = CONDIC_NORMALIZAR if flag == CONDIC_IGNORAR and condic.gravidade == CONDIC_NORMALIZAR else flag
                    continue

                else:
                    logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)

                    if condic.gravidade == CONDIC_INDISPONIBILIZAR:
                        flag = CONDIC_INDISPONIBILIZAR
                        self.bd.update_alarmes([
                            self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                            condic.gravidade,
                            condic.descricao,
                            "X" if autor_i == 0 else ""
                        ])
                        autor_i += 1

                    elif condic.gravidade == CONDIC_AGUARDAR:
                        flag = CONDIC_AGUARDAR if flag != CONDIC_INDISPONIBILIZAR else flag
                        self.bd.update_alarmes([
                            self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                            condic.gravidade,
                            condic.descricao,
                            "X" if autor_i == 0 and autor_a == 0 else ""
                        ])
                        autor_a += 1

                    elif condic.gravidade == CONDIC_NORMALIZAR:
                        flag = CONDIC_NORMALIZAR if flag not in (CONDIC_INDISPONIBILIZAR, CONDIC_AGUARDAR) else flag
                        self.bd.update_alarmes([
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
            self.manter_unidades = bool(parametros["manter_unidades"])
            self.condic_perda_grade_ug.valor_base = float(parametros[f"alerta_perda_grade_ug{self.id}"])
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

            self.condic_perda_grade_ug.valor_limite = float(parametros[f"ug{self.id}_perda_grade_maxima"])
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
            logger.debug(f"")
            logger.debug(f"[UG{self.id}] A temperatura do óleo da UHRV voltou ao Normal. Leitura: {self.l_temp_oleo_uhrv.valor:0.2f}C")
            logger.debug(f"")



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

        if self.l_falha_3_rt_b0.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma perda de medição de Potência Reativa no RT da Unidade. Favor Verificar.")

        if self.l_falha_3_rt_b1.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma perda de medição de Tensão Terminal no RT da Unidade. Favor Verificar.")

        if self.l_falha_3_rt_b2.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma perda de medição de Corrente de Excitação Principal no RT da Unidade. Favor Verificar.")

        if self.l_falha_3_rt_b3.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma perda de medição de Corrente de Excitação Retaguarda no RT da Unidade. Favor Verificar.")

        if self.l_falha_3_rt_b4.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Ruído de Instrumentação Reativo no RT da Unidade. Favor Verificar.")

        if self.l_falha_3_rt_b5.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Ruído de Instrumentação Tensão no RT da Unidade. Favor Verificar.")

        if self.l_falha_3_rt_b6.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Ruído de Instrumentação Excitação Principal no RT da Unidade. Favor Verificar.")

        if self.l_falha_3_rt_b7.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Ruído de Instrumentação Excitação Retaguarda no RT da Unidade. Favor Verificar.")

        if self.l_falha_1_rv_b4.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha de Leitura da Posição do Distribuidor no RV da Unidade. Favor verificar.")

        if self.l_falha_1_rv_b5.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha de Leitura na Posição do Rotor no RV da Unidade. Favor verificar.")

        if self.l_falha_1_rv_b6.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha de Leitura de Distribuição do Rotor no RV da Unidade. Favor verificar.")

        if self.l_falha_1_rv_b7.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha de Leitura na Posição do Distribuidor no RV da Unidade. Favor verificar.")

        if self.l_falha_1_rv_b8.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha na Leitura de Nível Montante pelo RV da Unidade. Favor verificar.")

        if self.l_falha_1_rv_b13.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Controle de Posição do Rotor pelo RV da Unidade. Favor verificar.")

        if self.l_falha_1_rv_b14.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Ruído na Medição de Velocidade Principal pelo RV da Unidade. Favor verificar.")

        if self.l_falha_1_rv_b15.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Ruído na Medição de Velocidade Retaguarda pelo RV da Unidade. Favor verificar.")

        if self.l_falha_2_rv_b0.valor:
            logger.warning(f"[UG{self.id}] Foi identificado pelo RV que a Unidade excedeu o tempo de Partida. Favor verificar.")

        if self.l_falha_2_rv_b4.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Diferencial na Medição de Velocidade Principal e Retaguarda pelo RV da Unidade. Favor verificar.")

        if self.l_unidade_manutencao_uhrv.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a UHRV da UG entrou em modo de manutenção. Favor verificar.")

        if self.l_unidade_manutencao_uhlm.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a UHLM da UG entrou em modo de manutenção. Favor verificar.")

        if not self.l_filtro_sujo_uhrv.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o Filtro da UHRV da Unidade está sujo. Favor realizar limpeza/troca.")

        if not self.l_filtro_sujo_uhrv.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o Filtro da UHLM da Unidade está sujo. Favor realizar limpeza/troca.")

        if not self.l_porta_interna_fechada_cpg.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a Porta Interna do CPG da Unidade está aberta. Favor verificar/fechar.")

        if not self.l_porta_traseira_fechada_cpg.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a Porta Traseira do CPG da Unidade está aberta. Favor verificar/fechar.")

        if not self.l_resistencia_falha.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma falha na Resistência do Gerador da Unidade. Favor verificar.")

        if self.l_escovas_gastas_polo_positivo.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que as Escovas do Polo Positivo da Unidade estão gastas. Favor verificar.")

        if self.l_escovas_gastas_polo_negativo.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que as Escovas do Polo Negativo da Unidade estão gastas. Favor verificar.")

        if self.l_alarme_temp_ponte_fase_a.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura de Ponte Fase A. Favor verificar.")

        if self.l_alarme_temp_ponte_fase_b.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura de Ponte Fase B. Favor verificar.")

        if self.l_alarme_temp_ponte_fase_c.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura de Ponte Fase C. Favor verificar.")

        if self.l_alarme_temp_trafo_excitacao.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura do Transformador da Unidade. Favor verificar.")

        if self.l_alarme_temp_mancal_guia.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura do Mancal Guia da Unidade. Favor verificar.")

        if self.l_alarme_temp_oleo_uhrv.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura de Óleo da UHRV da Unidade. Favor verificar.")

        if self.l_alarme_temp_oleo_uhlm.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura de Óleo da UHLM da Unidade. Favor verificar.")

        if self.l_alarme_temp_mancal_casq_comb.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura do Mancal Casquilho Combinado da Unidade. Favor verificar.")

        if self.l_alarme_temp_mancal_con_esc_comb.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura do Mancal Contra Escora Combinado da Unidade. Favor verificar.")

        if self.l_alarme_temp_patins_1_mancal_comb.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura do Patins 1 Mancal Combinado da Unidade. Favor verificar.")

        if self.l_alarme_temp_patins_2_mancal_comb.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura do Patins 2 Mancal Combinado da Unidade. Favor verificar.")

        if self.l_alarme_temp_mancal_guia_interno_1.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura do Mancal Guia Interno 1 da Unidade. Favor verificar.")

        if self.l_alarme_temp_mancal_guia_interno_2.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura do mancal Guia Interno 2 da Unidade. Favor verificar.")

        if self.l_alarme_temp_nucleo_estatorico_gerador.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura do Núcleo Estatórico do Gerador da Unidade. Favor verificar.")

        if self.l_temp_fase_a_gerador.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura de Fase A do Gerador da Unidade. Favor verificar.")

        if self.l_temp_fase_b_gerador.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura de Fase B do Gerador da Unidade. Favor verificar.")

        if self.l_temp_fase_c_gerador.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Temperatura de Fase C do Gerador da Unidade. Favor verificar.")

        if self.l_alarme_vibra_eixo_x_mancal_comb.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Vibração do Eixo X do Mancal Combinado da Unidade. Favor verificar.")

        if self.l_alarme_vibra_eixo_y_mancal_comb.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionameonto do Alarme de Vibração do Eixo Y do Mancal Combinado da Unidade. Favor verificar.")

        if self.l_alarme_vibra_eixo_z_mancal_comb.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Vibração do Eixo Z do Mancal Combinado da Unidade. Favor verificar.")

        if self.l_alarme_vibra_detec_horizontal.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Vibração Detecção Horizontal da Unidade. Favor verificar.")

        if self.l_alarme_vibra_detec_vertical.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento do Alarme de Vibração Detecção Vertical da Unidade. Favor verificar.")


    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """

        # CONDICIONADORES ESSENCIAIS
        self.condic_perda_grade_ug = c.CondicionadorExponencial(self.__perda_grade, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_atenuadores.append(self.condic_perda_grade_ug)

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
        self.condic_temp_oleo_uhrv = c.CondicionadorExponencial(self.l_temp_oleo_uhrv, CONDIC_INDISPONIBILIZAR, ordem=1)
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


        # CONDICIONADORES ESSENCIAIS
        self.l_bt_emerg_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["BT_EMERGENCIA_ATUADO"], descricao=f"[UG{self.id}] Botão Emergência Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_bt_emerg_atuado, CONDIC_NORMALIZAR))

        self.l_bloq_86M_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86M_BLQ_ATUADO"], descricao=f"[UG{self.id}] Bloqueio 86M Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_bloq_86M_atuado, CONDIC_NORMALIZAR))

        self.l_bloq_86E_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86E_BLQ_ATUADO"], descricao=f"[UG{self.id}] Bloqueio 86E Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_bloq_86E_atuado, CONDIC_NORMALIZAR))

        self.l_bloq_86H_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86H_BLQ_ATUADO"], descricao=f"[UG{self.id}] Bloqueio 86H Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_bloq_86H_atuado, CONDIC_NORMALIZAR))

        self.l_clp_geral_sem_bloq_exter = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["CLP_GERAL_SEM_BLQ_EXTERNO"], descricao=f"[UG{self.id}] CLP Geral Sem Bloqueio Externo")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_clp_geral_sem_bloq_exter, CONDIC_NORMALIZAR))

        self.l_trip_rele700G_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RELE_700G_TRP_ATUADO"], descricao=f"[UG{self.id}] Relé 700G Trip Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_trip_rele700G_atuado, CONDIC_NORMALIZAR))

        self.l_rele_bloq_86EH_desatuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RELE_BLQ_86EH_DESATUADO"], descricao=f"[UG{self.id}] Relé Bloqueio 86EH Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_bloq_86EH_desatuado, CONDIC_NORMALIZAR))

        # self.l_falha_2_rv_b3 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_2_B3"], descricao=f"[UG{self.id}][RV] Bloqueio Externo")
        # self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_falha_2_rv_b3, CONDIC_NORMALIZAR))

        # self.l_trip_rele_rv_naoatuado = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_RELE_TRP_NAO_ATUADO"], invertido=True, descricao=f"[UG{self.id}][RV] Relé Trip Não Atuado")
        # self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_trip_rele_rv_naoatuado, CONDIC_NORMALIZAR, teste=True))

        # self.l_saidas_digitiais_rv_b0 = LeituraModbus(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_SAIDAS_DIGITAIS"], descricao=f"[UG{self.id}][RV] Rele Trip Não Atuado")
        # self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_saidas_digitiais_rv_b0, CONDIC_NORMALIZAR))

        # self.l_saidas_digitais_rt_b0 = LeituraModbus(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_SAIDAS_DIGITAIS"], descricao=f"[UG{self.id}][RT] Alarme Atuado")
        # self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_saidas_digitais_rt_b0, CONDIC_NORMALIZAR))


        # CONDICIONADORES
        self.l_bloqueio_86M_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["86M_BLQ_ATUADO"], descricao=f"[UG{self.id}] Bloqueio 86M Atuado")
        self.condicionadores.append(c.CondicionadorBase(self.l_bloqueio_86M_atuado, CONDIC_INDISPONIBILIZAR))

        self.l_parada_bloq_abertura_disj = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PARADA_BLQ_ABERTURA_DJ"], descricao=f"[UG{self.id}] Parada Bloqueio Abertura Disjuntor")
        self.condicionadores.append(c.CondicionadorBase(self.l_parada_bloq_abertura_disj, CONDIC_NORMALIZAR))

        self.l_sup_tensao_125vcc = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["SUP_TENSAO_125VCC"], descricao=f"[UG{self.id}] Tensão 125Vcc Supervisão")
        self.condicionadores.append(c.CondicionadorBase(self.l_sup_tensao_125vcc, CONDIC_INDISPONIBILIZAR))

        self.l_sup_tensao_24vcc = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["SUP_TENSAO_24VCC"], descricao=f"[UG{self.id}] Tensão 24Vcc Supervisão")
        self.condicionadores.append(c.CondicionadorBase(self.l_sup_tensao_24vcc, CONDIC_INDISPONIBILIZAR))

        self.l_sup_bobina_52g = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["SUP_BOBINA_52G"], descricao=f"[UG{self.id}] Bobina 52G Supervisão")
        self.condicionadores.append(c.CondicionadorBase(self.l_sup_bobina_52g, CONDIC_INDISPONIBILIZAR))

        self.l_sup_bobina_86eh = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["SUP_BOBINA_86EH"], descricao=f"[UG{self.id}] Bobina 86EH Supervisão")
        self.condicionadores.append(c.CondicionadorBase(self.l_sup_bobina_86eh, CONDIC_INDISPONIBILIZAR))

        self.l_falha_pressao_entrada_turb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["ENTRADA_TURBINA_FLH_LER_PRESSAO"], descricao=f"[UG{self.id}] Pressão Entrada Turbina Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_pressao_entrada_turb, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_mancal_casq_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CASQ_COMB_TRP_TMP"], descricao=f"[UG{self.id}] Mancal Casquilho Combinado Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_mancal_casq_comb, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_mancal_casq_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CASQ_COMB_FLH_LER_TMP"], descricao=f"[UG{self.id}] Mancal Casquilho Combinado Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_mancal_casq_comb, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_mancal_con_esc_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CONT_ESCO_COMB_FLH_LER_TMP"], descricao=f"[UG{self.id}] Mancal Contra Escora Combinado Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_mancal_con_esc_comb, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_mancal_contra_esc_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CONT_ESCO_COMB_TRP_TMP"], descricao=f"[UG{self.id}] Mancal Contra Escora Combinado Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_mancal_contra_esc_comb, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_mancal_guia_interno_1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_1_TRP_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 1 Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_mancal_guia_interno_1, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_mancal_guia_interno_2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_2_TRP_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 2 Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_mancal_guia_interno_2, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_mancal_guia_interno_1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_1_FLH_LER_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 1 Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_mancal_guia_interno_1, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_mancal_guia_interno_2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_2_FLH_LER_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 2 Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_mancal_guia_interno_2, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_mancal_patins_1_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_1_TRP_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 1 Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_mancal_patins_1_comb, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_mancal_patins_2_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_2_TRP_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 2 Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_mancal_patins_2_comb, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_mancal_pat_1_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_1_FLH_LER_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 1 Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_mancal_pat_1_comb, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_mancal_pat_2_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_2_FLH_LER_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 2 Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_mancal_pat_2_comb, CONDIC_INDISPONIBILIZAR))

        self.l_trip_vibra_eixo_x_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_X_TRP_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Trip Vibração Eixo X")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_vibra_eixo_x_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.l_trip_vibra_eixo_y_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_Y_TRP_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Trip Vibração Eixo Y")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_vibra_eixo_y_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.l_trip_vibra_eixo_z_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_Z_TRP_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Trip Vibração Eixo Z")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_vibra_eixo_z_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.l_falha_vibra_eixo_x_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_X_FLH_LER_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Falha Leitura Vibração Eixo X")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_vibra_eixo_x_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.l_falha_vibra_eixo_y_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_Y_FLH_LER_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Falha Leitura Vibração Eixo Y")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_vibra_eixo_y_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.l_falha_vibra_eixo_z_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_Z_FLH_LER_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Falha Leitura Vibração Eixo Z")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_vibra_eixo_z_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_ponte_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_A_FLH_LER_TMP"], descricao=f"[UG{self.id}] Ponte Fase A Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_ponte_fase_a, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_ponte_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_B_FLH_LER_TMP"], descricao=f"[UG{self.id}] Ponte Fase B Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_ponte_fase_b, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_ponte_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_C_FLH_LER_TMP"], descricao=f"[UG{self.id}] Ponte Fase C Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_ponte_fase_c, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_ponte_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_A_TRP_TMP"], descricao=f"[UG{self.id}] Ponte Fase A Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_ponte_fase_a, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_ponte_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_B_TRP_TMP"], descricao=f"[UG{self.id}] Ponte Fase B Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_ponte_fase_b, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_ponte_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_C_TRP_TMP"], descricao=f"[UG{self.id}] Ponte Fase C Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_ponte_fase_c, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_gerador_nucleo_estatorico = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_NUCL_ESTAT_TRP_TMP"], descricao=f"[UG{self.id}] Núcleo Estatórico Gerador Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_gerador_nucleo_estatorico, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_gerador_nucleo_esta = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_NUCL_ESTAT_FLH_LER_TMP"], descricao=f"[UG{self.id}] Núcleo Estatórico Gerador Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_gerador_nucleo_esta, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_gerador_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_A_FLH_LER_TMP"], descricao=f"[UG{self.id}] Fase A Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_gerador_fase_a, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_gerador_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_B_FLH_LER_TMP"], descricao=f"[UG{self.id}] Fase B Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_gerador_fase_b, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_gerador_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_C_FLH_LER_TMP"], descricao=f"[UG{self.id}] Fase C Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_gerador_fase_c, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_gerador_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_A_TRP_TMP"], descricao=f"[UG{self.id}] Gerador Fase A Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_gerador_fase_a, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_gerador_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_B_TRP_TMP"], descricao=f"[UG{self.id}] Gerador Fase B Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_gerador_fase_b, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_gerador_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_C_TRP_TMP"], descricao=f"[UG{self.id}] Gerador Fase C Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_gerador_fase_c, CONDIC_INDISPONIBILIZAR))

        self.l_disparo_mecanico_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DISP_MECANICO_ATUADO"], descricao=f"[UG{self.id}] Disparo Mecânico Atuado")
        self.condicionadores.append(c.CondicionadorBase(self.l_disparo_mecanico_atuado, CONDIC_NORMALIZAR))

        self.l_disparo_mecanico_desatuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DISP_MECANICO_DESATUADO"], invertido=True, descricao=f"[UG{self.id}] Disparo Mecânico Desatuado")
        self.condicionadores.append(c.CondicionadorBase(self.l_disparo_mecanico_desatuado, CONDIC_NORMALIZAR))

        self.l_falha_vibra_detec_horizontal = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DETECCAO_HORIZONTAL_FLH_LER_VIBRA"], descricao=f"[UG{self.id}] Detecção Horizontal Falha Leitura Vibração")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_vibra_detec_horizontal, CONDIC_INDISPONIBILIZAR))

        self.l_trip_vibra_detec_horizontal = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DETECCAO_HORIZONTAL_TRP_VIBRA"], descricao=f"[UG{self.id}] Detecção Horizontal Trip Vibração")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_vibra_detec_horizontal, CONDIC_INDISPONIBILIZAR))

        self.l_falha_vibra_detec_vertical = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DETECCAO_VERTICAL_FLH_LER_VIBRA"], descricao=f"[UG{self.id}] Detecção Vertical Falha Leitura Vibração")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_vibra_detec_vertical, CONDIC_INDISPONIBILIZAR))

        self.l_trip_vibra_detec_vertical = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DETECCAO_VERTICAL_TRP_VIBRA"], descricao=f"[UG{self.id}] Detecção Vertical Trip Vibração")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_vibra_detec_vertical, CONDIC_INDISPONIBILIZAR))

        self.l_rele_700G_bf_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RELE_700G_BF_ATUADO"], descricao=f"[UG{self.id}] Relé 700G BF Atuado")
        self.condicionadores.append(c.CondicionadorBase(self.l_rele_700G_bf_atuado, CONDIC_INDISPONIBILIZAR))

        self.l_falha_habilitar_sistema_agua = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["SIS_AGUA_FLH_HAB"], descricao=f"[UG{self.id}] Sistema Água Falha Habilitar")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_habilitar_sistema_agua, CONDIC_NORMALIZAR))

        self.l_disj_125vcc_fechados = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DJS_125VCC_FECHADOS"], descricao=f"[UG{self.id}] Disjuntores 125Vcc Fechados")
        self.condicionadores.append(c.CondicionadorBase(self.l_disj_125vcc_fechados, CONDIC_INDISPONIBILIZAR))

        self.l_disj_24vcc_fechados = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DJS_24VCC_FECHADOS"], descricao=f"[UG{self.id}] Disjuntores 24Vcc Fechados")
        self.condicionadores.append(c.CondicionadorBase(self.l_disj_24vcc_fechados, CONDIC_INDISPONIBILIZAR))

        self.l_sistema_agua_clp_geral_ok = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["CLP_GERAL_SIS_AGUA_OK"], invertido=True, descricao=f"[UG{self.id}] CLP Geral Status Sistema Água")
        self.condicionadores.append(c.CondicionadorBase(self.l_sistema_agua_clp_geral_ok, CONDIC_NORMALIZAR))

        self.l_trip_temp_trafo_ateramento = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["TRAFO_ATERRAMENTO_TRP_TMP"], descricao=f"[UG{self.id}] Transformador Aterramento Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_trafo_ateramento, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_trafo_excitacao = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["TRAFO_EXCITACAO_TRP_TMP"], descricao=f"[UG{self.id}] Transformador Excitação Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_trafo_excitacao, CONDIC_INDISPONIBILIZAR))

        self.l_falha_temp_trafo_excita = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["TRAFO_EXCITACAO_FLH_LER_TMP"], descricao=f"[UG{self.id}] Transformador Excitação Falha Leitura Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_trafo_excita, CONDIC_INDISPONIBILIZAR))

        self.l_falha_bomba_1_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_BOMBA_1_FLH"], descricao=f"[UG{self.id}][UHRV] Falha Ligar Bomba 1")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_bomba_1_uhrv, CONDIC_NORMALIZAR))

        self.l_falha_bomba_2_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_BOMBA_2_FLH"], descricao=f"[UG{self.id}][UHRV] Falha Ligar Bomba 2")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_bomba_2_uhrv, CONDIC_NORMALIZAR))

        self.l_trip_temp_oleo_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_TRP_TMP_OLEO"], descricao=f"[UG{self.id}][UHRV] Trip Temperatura Óleo")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_oleo_uhrv, CONDIC_NORMALIZAR))

        self.l_falha_temp_oleo_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_FLH_LER_TMP_OLEO"], descricao=f"[UG{self.id}][UHRV] Falha Leitura Temperatura Óleo")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_oleo_uhrv, CONDIC_INDISPONIBILIZAR))

        self.l_trip_pressao_acum_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_ACUMULADOR_PRESSAO_TRP"], descricao=f"[UG{self.id}][UHRV] Trip Acumulador Pressão")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_pressao_acum_uhrv, CONDIC_INDISPONIBILIZAR))

        self.l_falha_bomba_1_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_BOMBA_1_FLH"], descricao=f"[UG{self.id}][UHLM] Unidade em Manutenção")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_bomba_1_uhlm, CONDIC_NORMALIZAR))

        self.l_falha_bomba_2_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_BOMBA_2_FLH"], descricao=f"[UG{self.id}][UHLM] Falha Ligar Bomba 1")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_bomba_2_uhlm, CONDIC_NORMALIZAR))

        self.l_falha_pressao_linha_b1_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_FLH_PRESSAO_LINHA_B1"], descricao=f"[UG{self.id}][UHLM] Falha Pressão Linha B1")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_pressao_linha_b1_uhlm, CONDIC_NORMALIZAR))

        self.l_falha_pressao_linha_b2_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_FLH_PRESSAO_LINHA_B2"], descricao=f"[UG{self.id}][UHLM] Falha Pressão Linha B2")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_pressao_linha_b2_uhlm, CONDIC_NORMALIZAR))

        self.l_falha_pressostato_linha_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_FLH_PRESSOSTATO_LINHA"], descricao=f"[UG{self.id}][UHLM] Falha Pressostato Linha")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_pressostato_linha_uhlm, CONDIC_NORMALIZAR))

        self.l_trip_temp_oleo_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_TRP_TMP_OLEO"], descricao=f"[UG{self.id}][UHLM] Trip Temperatura Óleo")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_oleo_uhlm, CONDIC_NORMALIZAR))

        self.l_falha_temp_oleo_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_FLH_LER_TMP_OLEO"], descricao=f"[UG{self.id}][UHLM] Falha Leitura Temperatura Óleo")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_temp_oleo_uhlm, CONDIC_INDISPONIBILIZAR))

        self.l_falha_partir_rv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_PARTIR"], descricao=f"[UG{self.id}][RV] Falha Partida")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_partir_rv, CONDIC_NORMALIZAR))

        self.l_falha_habilitar_rv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_HABILITAR"], descricao=f"[UG{self.id}][RV] Falha Habilitar")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_habilitar_rv, CONDIC_NORMALIZAR))

        self.l_falha_desabilitar_rv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_DESABILITAR"], descricao=f"[UG{self.id}][RV] Falha Desabilitar")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_desabilitar_rv, CONDIC_NORMALIZAR))

        self.l_alarme_rele_rv_atuado = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_RELE_ALM_ATUADO"], descricao=f"[UG{self.id}][RV] Relé Alarme Atuado")
        self.condicionadores.append(c.CondicionadorBase(self.l_alarme_rele_rv_atuado, CONDIC_NORMALIZAR))

        self.l_falha_fechar_distrib_rv = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_FECHAR_DISTRIBUIDOR"], descricao=f"[UG{self.id}][RV] Falha Fechamento Distribuidor")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_fechar_distrib_rv, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_1_rv_b0 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B0"], descricao=f"[UG{self.id}][RV] Sobrefrequência Instantânea")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rv_b0, CONDIC_NORMALIZAR))

        self.l_falha_1_rv_b1 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B1"], descricao=f"[UG{self.id}][RV] Sobrefrequência Temporizada")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rv_b1, CONDIC_NORMALIZAR))

        self.l_falha_1_rv_b2 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B2"], descricao=f"[UG{self.id}][RV] Subfrequência Temporizada")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rv_b2, CONDIC_NORMALIZAR))

        self.l_falha_1_rv_b3 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B3"], descricao=f"[UG{self.id}][RV] Girando Sem Regulação ou Giro Indevido")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rv_b3, CONDIC_NORMALIZAR))

        self.l_falha_1_rv_b4 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B4"], descricao=f"[UG{self.id}][RV] Falha Leitura Posição Distribuidor")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rv_b4, CONDIC_NORMALIZAR))

        self.l_falha_1_rv_b5 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B5"], descricao=f"[UG{self.id}][RV] Falha Leitura Posição Rotor")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rv_b5, CONDIC_NORMALIZAR))

        self.l_falha_1_rv_b10 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B10"], descricao=f"[UG{self.id}][RV] Controle Posição Distribuidor")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rv_b10, CONDIC_NORMALIZAR))

        self.l_falha_1_rv_b11 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B11"], descricao=f"[UG{self.id}][RV] Nível Montante Muito Baixo")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rv_b11, CONDIC_NORMALIZAR))

        self.l_falha_1_rv_b12 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B12"], descricao=f"[UG{self.id}][RV] Controle Posição Distribuidor")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rv_b12, CONDIC_NORMALIZAR))

        self.l_falha_1_rv_b13 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B13"], descricao=f"[UG{self.id}][RV] Controle Posição Rotor")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rv_b13, CONDIC_NORMALIZAR))

        self.l_falha_2_rv_b1 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_2_B1"], descricao=f"[UG{self.id}][RV] Tempo Excessivo Partida")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rv_b1, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_2_rv_b2 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_2_B2"], descricao=f"[UG{self.id}][RV] Tempo Excessivo Parada")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rv_b2, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_partir_rt = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_PARTIR"], descricao=f"[UG{self.id}][RT] Falha Partida")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_partir_rt, CONDIC_NORMALIZAR))

        self.l_falha_habilitar_rt = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_HABILITAR"], descricao=f"[UG{self.id}][RT] Falha Habilitar")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_habilitar_rt, CONDIC_NORMALIZAR))

        self.l_falha_desbilitar_rt = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_DESABILITAR"], descricao=f"[UG{self.id}][RT] Falha Desabilitar")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_desbilitar_rt, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_alarme_1_rt_b0 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_ALM_1_B0"], descricao=f"[UG{self.id}][RT] Sobretensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_alarme_1_rt_b0, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_alarme_1_rt_b4 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_ALM_1_B4"], descricao=f"[UG{self.id}][RT] Limite Superior Potência Reativa Ultrapassado")
        self.condicionadores.append(c.CondicionadorBase(self.l_alarme_1_rt_b4, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_alarme_1_rt_b5 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_ALM_1_B5"], descricao=f"[UG{self.id}][RT] Limite Inferior Potência Reativa Ultrapassado")
        self.condicionadores.append(c.CondicionadorBase(self.l_alarme_1_rt_b5, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_alarme_1_rt_b8 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_ALM_1_B8"], descricao=f"[UG{self.id}][RT] Variação de Tensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_alarme_1_rt_b8, CONDIC_NORMALIZAR))

        self.l_falha_1_rt_b0 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B0"], descricao=f"[UG{self.id}][RT] Sobretensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b0, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_1_rt_b1 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B1"], descricao=f"[UG{self.id}][RT] Subtensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b1, CONDIC_NORMALIZAR))

        self.l_falha_1_rt_b2 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B2"], descricao=f"[UG{self.id}][RT] Sobrefrequência")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b2, CONDIC_NORMALIZAR))

        self.l_falha_1_rt_b3 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B3"], descricao=f"[UG{self.id}][RT] Subfrequência")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b3, CONDIC_NORMALIZAR))

        self.l_falha_1_rt_b4 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B4"], descricao=f"[UG{self.id}][RT] Limite Superior Potência Reativa Ultrapassado")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b4, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_1_rt_b5 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B5"], descricao=f"[UG{self.id}][RT] Limite Inferior Potência Reativa Ultrapassado")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b5, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_1_rt_b6 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B6"], descricao=f"[UG{self.id}][RT] Limite Superior Fator Potência Ultrapassado")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b6, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_1_rt_b7 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B7"], descricao=f"[UG{self.id}][RT] Limite Inferior Fator Potência Ultrapassado")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b7, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_1_rt_b8 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B8"], descricao=f"[UG{self.id}][RT] Sobretensão Instantânea")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b8, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_1_rt_b9 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B9"], descricao=f"[UG{self.id}][RT] Variação Tensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b9, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_1_rt_b10 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B10"], descricao=f"[UG{self.id}][RT] Potência Reativa Reversa")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b10, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_1_rt_b11 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B11"], descricao=f"[UG{self.id}][RT] Sobrecorrente Terminal")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b11, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_1_rt_b12 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B12"], descricao=f"[UG{self.id}][RT] Limite Superior Corrente Excitação Ultrapassado")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b12, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_1_rt_b13 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B13"], descricao=f"[UG{self.id}][RT] Limite Inferior Corrente Excitação Ultrapassado")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b13, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_1_rt_b14 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B14"], descricao=f"[UG{self.id}][RT] Limite Superior Tensão Excitação Ultrapassado")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b14, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_1_rt_b15 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_1_B15"], descricao=f"[UG{self.id}][RT] Limite Inferior Tensão Excitação Ultrapassado")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_1_rt_b15, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_2_rt_b0 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B0"], descricao=f"[UG{self.id}][RT] Temperatura Muito Alta Rotor")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rt_b0, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_2_rt_b1 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B1"], descricao=f"[UG{self.id}][RT] Falha Presença Tensão Terminal Com Ausência Corrente Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rt_b1, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_2_rt_b2 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B2"], descricao=f"[UG{self.id}][RT] Falha Presença Corrente Excitação Com Ausência Tensão Terminal")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rt_b2, CONDIC_NORMALIZAR))

        self.l_falha_2_rt_b3 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B3"], descricao=f"[UG{self.id}][RT] Falha Controle Corrente Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rt_b3, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_2_rt_b4 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B4"], descricao=f"[UG{self.id}][RT] Falha Controle Tensão Terminal")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rt_b4, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_2_rt_b5 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B5"], descricao=f"[UG{self.id}][RT] Crowbar Atuado com Regulador Habilitado")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rt_b5, CONDIC_NORMALIZAR))

        self.l_falha_2_rt_b6 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B6"], descricao=f"[UG{self.id}][RT] Falha Habilitar Drive Excitação - Lógica Disparo")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rt_b6, CONDIC_NORMALIZAR))

        self.l_falha_2_rt_b7 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B7"], descricao=f"[UG{self.id}][RT] Alarme Fechar Contator de Campo")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rt_b7, CONDIC_NORMALIZAR))

        self.l_falha_2_rt_b8 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B8"], descricao=f"[UG{self.id}][RT] Falha Corrente Excitação Com Pré-Excitação Ativa")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rt_b8, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_2_rt_b9 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B9"], descricao=f"[UG{self.id}][RT] Tempo Excessivo Pré-Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rt_b9, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_falha_2_rt_b10 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B10"], descricao=f"[UG{self.id}][RT] Tempo Excessivo Parada")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rt_b10, CONDIC_NORMALIZAR))

        self.l_falha_2_rt_b11 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B11"], descricao=f"[UG{self.id}][RT] Tempo Excessivo Partida")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rt_b11, CONDIC_NORMALIZAR))

        self.l_falha_2_rt_b12 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_2_B12"], descricao=f"[UG{self.id}][RT] Falha Bloqueio Externo")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_2_rt_b12, CONDIC_NORMALIZAR))


        # CONDICIONADORES RELÉS
        self.l_trip_rele_protecao1 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["RELE_PROTECAO_TRP_B5"], descricao=f"[UG{self.id}][RELE] Trip Relé Proteção 1")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_rele_protecao1, CONDIC_NORMALIZAR))

        self.l_trip_rele_protecao2 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["RELE_PROTECAO_TRP_B6"], descricao=f"[UG{self.id}][RELE] Trip Relé Proteção 2")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_rele_protecao2, CONDIC_NORMALIZAR))

        # self.l_subtensao_geral = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["SUBTEN_GERAL"], descricao=f"[UG{self.id}][RELE] Subtensão Geral")
        # self.condicionadores.append(c.CondicionadorBase(self.l_subtensao_geral, CONDIC_NORMALIZAR))

        # self.l_subfreq_ele1 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["ELE_1_SOBREFRE"], descricao=f"[UG{self.id}][RELE] Sobrefrequência Elemento 1")
        # self.condicionadores.append(c.CondicionadorBase(self.l_subfreq_ele1, CONDIC_NORMALIZAR))

        # self.l_subfreq_ele2 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["ELE_2_SOBREFRE"], descricao=f"[UG{self.id}][RELE] Sobrefrequência Elemento 2")
        # self.condicionadores.append(c.CondicionadorBase(self.l_subfreq_ele2, CONDIC_NORMALIZAR))

        # self.l_sobrefreq_ele1 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["ELE_1_SUBFRE"], descricao=f"[UG{self.id}][RELE] Subfrequência Elemento 1")
        # self.condicionadores.append(c.CondicionadorBase(self.l_sobrefreq_ele1, CONDIC_NORMALIZAR))

        # self.l_sobrefreq_ele2 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["ELE_2_SUBFRE"], descricao=f"[UG{self.id}][RELE] Subfrequência Elemento 2")
        # self.condicionadores.append(c.CondicionadorBase(self.l_sobrefreq_ele2, CONDIC_NORMALIZAR, teste=True))

        self.l_sobrecorr_instant = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["SOBRECO_INST"], descricao=f"[UG{self.id}][RELE] Sobrecorrente Instantânea")
        self.condicionadores.append(c.CondicionadorBase(self.l_sobrecorr_instant, CONDIC_NORMALIZAR))

        self.l_voltz_hertz = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["VOLTZ_HERTZ"], descricao=f"[UG{self.id}][RELE] Voltz/Hertz")
        self.condicionadores.append(c.CondicionadorBase(self.l_voltz_hertz, CONDIC_NORMALIZAR))

        self.l_perda_campo_geral = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["PERDA_CAMPO_GERAL"], descricao=f"[UG{self.id}][RELE] Perda Campo Geral")
        self.condicionadores.append(c.CondicionadorBase(self.l_perda_campo_geral, CONDIC_NORMALIZAR))

        self.l_pot_reversa = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["POT_REVERSA"], descricao=f"[UG{self.id}][RELE] Potência Reversa")
        self.condicionadores.append(c.CondicionadorBase(self.l_pot_reversa, CONDIC_NORMALIZAR))

        self.l_transf_disp_rele_linha_trafo = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["TE_RELE_LINHA_TRANS_DISP"], descricao=f"[UG{self.id}][RELE] Transferência Disparo Relé Linha Transformador Elevador")
        self.condicionadores.append(c.CondicionadorBase(self.l_transf_disp_rele_linha_trafo, CONDIC_INDISPONIBILIZAR))

        self.l_falha_partida_dj_maq = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["DJ_MAQUINA_FLH_PARTIDA"], descricao=f"[UG{self.id}][RELE] Falha Partir Disjuntor Máquina")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_partida_dj_maq, CONDIC_INDISPONIBILIZAR))

        self.l_falha_abretura_dj_maq1 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["DJ_MAQUINA_FLH_ABERTURA_B7"], descricao=f"[UG{self.id}][RELE] Falha Abertura Disjuntor Máquina 1")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_abretura_dj_maq1, CONDIC_INDISPONIBILIZAR))

        self.l_falha_abretura_dj_maq2 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["DJ_MAQUINA_FLH_ABERTURA_B8"], descricao=f"[UG{self.id}][RELE] Falha Abertura Disjuntor Máquina 2")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_abretura_dj_maq2, CONDIC_INDISPONIBILIZAR))

        self.l_recibo_transf_disp = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["RECIBO_TRANS_DISP"], descricao=f"[UG{self.id}][RELE] Recebida Transferência Disparo")
        self.condicionadores.append(c.CondicionadorBase(self.l_recibo_transf_disp, CONDIC_INDISPONIBILIZAR))

        self.l_difer_com_restr = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["DIF_COM_RESTRICAO"], descricao=f"[UG{self.id}][RELE] Diferencial Com Restrição")
        self.condicionadores.append(c.CondicionadorBase(self.l_difer_com_restr, CONDIC_INDISPONIBILIZAR))

        self.l_difer_sem_restr = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["DIF_SEM_RESTRICAO"], descricao=f"[UG{self.id}][RELE] Diferencial Sem Restrição")
        self.condicionadores.append(c.CondicionadorBase(self.l_difer_sem_restr, CONDIC_INDISPONIBILIZAR))

        self.l_fuga_sobrecorr_geral = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["FUGA_SOBRECO_GERAL"], descricao=f"[UG{self.id}][RELE] Fuga Sobrecorrente Geral")
        self.condicionadores.append(c.CondicionadorBase(self.l_fuga_sobrecorr_geral, CONDIC_INDISPONIBILIZAR, teste=True))

        self.l_sobrecorr_instant_neutro = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["SOBRECO_INST_NEUTRO"], descricao=f"[UG{self.id}][RELE] Sobrecorrente Instantânea Neutro")
        self.condicionadores.append(c.CondicionadorBase(self.l_sobrecorr_instant_neutro, CONDIC_INDISPONIBILIZAR))

        self.l_sobrecorr_restr_tensao = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["LT_SOBRECO_RESTRICAO"], descricao=f"[UG{self.id}][RELE] Sobrecorrente Restrição Tensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_sobrecorr_restr_tensao, CONDIC_INDISPONIBILIZAR))

        self.l_sobrecorr_temp_neutro = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["SOBRECO_TEMPO_NEUTRO"], descricao=f"[UG{self.id}][RELE] Sobrecorrente Temporizada Neutro")
        self.condicionadores.append(c.CondicionadorBase(self.l_sobrecorr_temp_neutro, CONDIC_INDISPONIBILIZAR))

        self.l_sobrecorr_seq_neg = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["SOBRECO_SEQU_NEG"], descricao=f"[UG{self.id}][RELE] Sobrecorrente Sequência Negativa")
        self.condicionadores.append(c.CondicionadorBase(self.l_sobrecorr_seq_neg, CONDIC_INDISPONIBILIZAR))

        self.l_unidade_fora_passo = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["UNIDADE_FORA_PASSO"], descricao=f"[UG{self.id}][RELE] Unidade Fora Passo")
        self.condicionadores.append(c.CondicionadorBase(self.l_unidade_fora_passo, CONDIC_INDISPONIBILIZAR))

        self.l_sobretensao_geral = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG{self.id}"]["SOBRETEN_GERAL"], descricao=f"[UG{self.id}][RELE] Sobretensão Geral")
        self.condicionadores.append(c.CondicionadorBase(self.l_sobretensao_geral, CONDIC_INDISPONIBILIZAR))


        # LEITURA PERIODICA
        self.l_alarme_temp_trafo_excitacao = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["TRAFO_EXCITACAO_ALM_TMP"],  descricao=f"[UG{self.id}] Transformador Excitação Alarme Temperatura")

        self.l_unidade_manutencao_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_MANUTENCAO"], descricao=f"[UG{self.id}] UHRV Manutenção")
        self.l_alarme_temp_oleo_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_ALM_TMP_OLEO"], descricao=f"[UG{self.id}] UHRV Alarme Temperatura Óleo")
        self.l_filtro_sujo_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHRV_FILTRO_SUJO"], invertido=True, descricao=f"[UG{self.id}] UHRV Status Filtro")

        self.l_unidade_manutencao_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_MANUTENCAO"], descricao=f"[UG{self.id}] UHLM Manutenção")
        self.l_alarme_temp_oleo_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_ALM_TMP_OLEO"], descricao=f"[UG{self.id}] UHLM Alarme Temperatura Óleo")
        self.l_filtro_sujo_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["UHLM_FILTRO_SUJO"], invertido=True, descricao=f"[UG{self.id}] UHLM Status Filtro")

        self.l_resistencia_falha = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RESISTENCIA_FALHA"], invertido=True, descricao=f"[UG{self.id}] Resistência Falha")

        self.l_porta_interna_fechada_cpg = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["CPG_PORTA_INTERNA_FECHADA"], invertido=True, descricao=f"[UG{self.id}] Comporta Porta Interna Fechada")
        self.l_porta_traseira_fechada_cpg = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["CPG_PORTA_TRASEIRA_FECHADA"], invertido=True, descricao=f"[UG{self.id}] Comporta Porta Traseira Fechada")

        self.l_falha_1_rv_b6 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B6"], descricao=f"[UG{self.id}][RV] Falha Leitura Distribuição Rotor")
        self.l_falha_1_rv_b7 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B7"], descricao=f"[UG{self.id}][RV] Falha Leitura Posição Distribuidor")
        self.l_falha_1_rv_b8 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B8"], descricao=f"[UG{self.id}][RV] Falha Leitura Nível Montante")
        self.l_falha_1_rv_b14 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B14"], descricao=f"[UG{self.id}][RV] Ruído Medição Velocidade Principal")
        self.l_falha_1_rv_b15 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_1_B15"], descricao=f"[UG{self.id}][RV] Ruído Medição Velocidade Retaguarda")
        self.l_falha_2_rv_b0 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_2_B0"], descricao=f"[UG{self.id}][RV] Tempo Excessivo Partida")
        self.l_falha_2_rv_b4 = LeituraModbusBit(self.rv[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RV_FLH_2_B4"], descricao=f"[UG{self.id}][RV] Diferencial Medição Velocidade Principal e Retaguarda")

        self.l_falha_3_rt_b0 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B0"], descricao=f"[UG{self.id}][RT] Perda Medição Potência Reativa")
        self.l_falha_3_rt_b1 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B1"], descricao=f"[UG{self.id}][RT] Perda Medição Tensão Terminal")
        self.l_falha_3_rt_b2 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B2"], descricao=f"[UG{self.id}][RT] Perda Medição Corrente Excitação Principal")
        self.l_falha_3_rt_b3 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B3"], descricao=f"[UG{self.id}][RT] Perda Medição Corrente Excitação Retaguarda")
        self.l_falha_3_rt_b4 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B4"], descricao=f"[UG{self.id}][RT] Ruído Intrumentação Reativo")
        self.l_falha_3_rt_b5 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B5"], descricao=f"[UG{self.id}][RT] Ruído Instrumentação Tensão")
        self.l_falha_3_rt_b6 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B6"], descricao=f"[UG{self.id}][RT] Ruído Instrumentação Excitação Principal")
        self.l_falha_3_rt_b7 = LeituraModbusBit(self.rt[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["RT_FLH_3_B7"], descricao=f"[UG{self.id}][RT] Ruído Instrumentação Excitação Retaguarda")

        self.l_escovas_gastas_polo_positivo = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["ESCOVAS_POLO_POS_GASTAS"], descricao=f"[UG{self.id}] Escovas Polo Positivo Gastas")
        self.l_escovas_gastas_polo_negativo = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["ESCOVAS_POLO_NEG_GASTAS"], descricao=f"[UG{self.id}] Escovas Polo Negativo Gastas")

        self.l_temp_fase_a_gerador = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_A_ALM_TMP"], descricao=f"[UG{self.id}] Gerador Fase A Alarme Temperatura")
        self.l_temp_fase_b_gerador = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_B_ALM_TMP"], descricao=f"[UG{self.id}] Gerador Fase B Alarme Temperatura")
        self.l_temp_fase_c_gerador = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_FASE_C_ALM_TMP"], descricao=f"[UG{self.id}] Gerador Fase C Alarme Temperatura")
        self.l_alarme_temp_nucleo_estatorico_gerador = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["GERADOR_NUCL_ESTAT_ALM_TMP"], descricao=f"[UG{self.id}] Gerador Núcleo Estatórico Alarme Temperatura")

        self.l_alarme_temp_ponte_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_A_ALM_TMP"], descricao=f"[UG{self.id}] Ponte Fase A Alarme Temperatura")
        self.l_alarme_temp_ponte_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_B_ALM_TMP"], descricao=f"[UG{self.id}] Ponte Fase B Alarme Temperatura")
        self.l_alarme_temp_ponte_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["PONTE_FASE_C_ALM_TMP"], descricao=f"[UG{self.id}] Ponte Fase C Alarme Temperatura")

        self.l_alarme_vibra_detec_vertical = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DETECCAO_VERTICAL_ALM_VIBRA"], descricao=f"[UG{self.id}] Detecção Vibração Vertical Alarme")
        self.l_alarme_vibra_detec_horizontal = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["DETECCAO_HORIZONTAL_ALM_VIBRA"], descricao=f"[UG{self.id}] Detecção Vibração Horizontal Alarme")
        self.l_alarme_vibra_eixo_x_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_X_ALM_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Alarme Vibração Eixo X")
        self.l_alarme_vibra_eixo_y_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_Y_ALM_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Alarme Vibração Eixo Y")
        self.l_alarme_vibra_eixo_z_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_EIXO_Z_ALM_VIBR"], descricao=f"[UG{self.id}] Mancal Combinado Alarme Vibração Eixo Z")

        self.l_alarme_temp_mancal_guia = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_ALM_TMP"],  descricao=f"[UG{self.id}] Mancal Guia Alarme Temperatura")
        self.l_alarme_temp_mancal_casq_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CASQ_COMB_ALM_TMP"],  descricao=f"[UG{self.id}] Mancal Casquilho Combinado Alarme Temperatura")
        self.l_alarme_temp_mancal_guia_interno_1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_1_ALM_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 1 Alarme Temperatura")
        self.l_alarme_temp_mancal_guia_interno_2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_GUIA_INTE_2_ALM_TMP"], descricao=f"[UG{self.id}] Mancal Guia Interno 2 Alarme Temperatura")
        self.l_alarme_temp_patins_1_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_1_ALM_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 1 Alarme Temperatura")
        self.l_alarme_temp_patins_2_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_COMB_PATINS_2_ALM_TMP"], descricao=f"[UG{self.id}] Patins Mancal Combinado 2 Alarme Temperatura")
        self.l_alarme_temp_mancal_con_esc_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP[f"UG{self.id}"]["MANCAL_CONT_ESCO_COMB_ALM_TMP"], descricao=f"[UG{self.id}] Mancal Combinado Contra Escora Alarme Temperatura")
