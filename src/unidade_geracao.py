import pytz
import logging
import traceback

import src.subestacao as se
import src.funcoes.leitura as lei
import src.maquinas_estado.ug as sm
import src.funcoes.condicionador as c
import src.conectores.banco_dados as bd
import src.conectores.servidores as srv

from time import sleep, time
from threading import Thread
from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")
debug_log = logging.getLogger("debug")


class UnidadeGeracao:
    def __init__(self, id: "int", cfg=None, db: "bd.BancoDados"=None):

        # VERIFICAÇÃO DE ARGUMENTOS
        if id <= 0:
            logger.error(f"[UG{self.id}] A Unidade não pode ser instanciada com o ID <= \"0\" ou vazio.")
            raise ValueError
        else:
            self.__id = id

        self.db = db
        self.cfg = cfg
        self.clp = srv.Servidores.clp

        # PRIVADAS
        self.__l_potencia: "lei.LeituraModbus" = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["PM710_POTENCIA_ATIVA"],
            op=4,
            descricao=f"[UG{self.id}] Leitura Potência",
        )
        self.__l_pressao_uhrv = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["UHRV_PRESSAO"],
            escala=0.1,
            op=4,
            descricao=f"[UG{self.id}] Leitura Pressão UHRV"
        )
        self.__l_rotacao = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["REFERENCIA_CARGA"],
            escala=0.1,
            op=4,
            descricao=f"[UG{self.id}] Leitura Rotação"
        )
        # self.__l_etapa_atual = lei.LeituraComposta(
        #     [lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["DJ_GERADOR_FECHADO"]),
        #     lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["PARANDO_AUTO"]),
        #     lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_MAQ_PARADA"]),
        #     lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["PARTINDO_AUTO"])],
        #     descricao=f"[UG{self.id}] Etapa Atual",
        # )

        self.__l_etapa_atual = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["ETAPA_SIM"],
            descricao=f"[UG{self.id}] Leitura Etapa Simulador"
        )

        self.__l_horimetro_h = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["HORIMETRO_GERADOR"],
            op=4,
            descricao=f"[UG{self.id}] Horímetro Horas"
        )
        self.__l_horimetro_m = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["HORIMETRO_GERADOR_MIN"],
            escala=1/60,
            op=4,
            descricao=f"[UG{self.id}] Horímetro Minutos"
        )
        self.__l_horimetro: "lei.LeituraSoma" = lei.LeituraSoma(
            self.__l_horimetro_h,
            self.__l_horimetro_m,
            descricao=f"[UG{self.id}] Horímetro",
        )

        self.__iniciar_cx_esp: "int" = -1
        self.__init_registro_estados: "int" = -1

        self.__limite_tentativas: "int" = 3
        self.__tempo_entre_tentativas: "int" = 0

        # PROTEGIDAS
        self._estado: "int" = 0
        self._setpoint: "int" = 0
        self._prioridade: "int" = 0
        self._tentativas_normalizacao: "int" = 0

        self._setpoint_minimo: "int" = self.cfg["pot_minima_ugs"]
        self._setpoint_maximo: "int" = self.cfg[f"pot_maxima_ug{self.id}"]

        # PÚBLICAS
        self.pot_alvo_anterior: "int" = -1

        self.atenuacao: "int" = 0
        self.tempo_normalizar: "int" = 0
        self.ultima_etapa_atual: "int" = 0
        self.tentativas_sincronismo: "int" = 0
        self.tentativas_aguardar_rotacao: "int" = 0

        self.borda_parar: "bool" = False
        self.limpeza_grade: "bool" = False
        self.atraso_rotacao: "bool" = False
        self.manter_unidade: "bool" = False
        self.normalizacao_agendada: "bool" = False

        self.temporizar_rotacao: "bool" = False
        self.temporizar_partida: "bool" = False
        self.temporizar_normalizacao: "bool" = False

        self.condicionadores: "list[c.CondicionadorBase]" = []
        self.condicionadores_essenciais: "list[c.CondicionadorBase]" = []
        self.condicionadores_atenuadores: "list[c.CondicionadorBase]" = []

        self.aux_tempo_sincronizada: "datetime" = 0
        self.ts_auxiliar: "datetime" = self.get_time()

        self.carregar_leituras()


    @property
    def id(self) -> "int":
        # PROPRIEDADE -> Retrona o ID da Unidade.
        return self.__id

    @property
    def manual(self) -> "bool":
        # PROPRIEDADE -> Verifica se a Unidade está em modo Manual.
        return isinstance(self.__next_state, sm.StateManual)

    @property
    def restrito(self) -> "bool":
        # PROPRIEDADE -> Verifica se a Unidade está em modo Restrito.
        return isinstance(self.__next_state, sm.StateRestrito)

    @property
    def disponivel(self) -> "bool":
        # PROPRIEDADE -> Verifica se a Unidade está em modo Disponível.
        return isinstance(self.__next_state, sm.StateDisponivel)

    @property
    def indisponivel(self) -> "bool":
        # PROPRIEDADE -> Verifica se a Unidade está em modo Indisponível.
        return isinstance(self.__next_state, sm.StateIndisponivel)

    @property
    def potencia(self) -> "int | float":
        # PROPRIEDADE -> Retorna a leitura de potência atual da Unidade.
        return self.__l_potencia.valor

    @property
    def leitura_horimetro(self) -> "int | float":
        # PROPRIEDADE -> Retorna a leitura de horas de geração da Unidade.
        return self.__l_horimetro.valor

    @property
    def limite_tentativas(self) -> "int":
        # PROPRIEDADE -> Retorna o limite de tentativas de normalização
        return self.__limite_tentativas

    @property
    def etapa_atual(self) -> "int":
        # PROPRIEDADE -> Retorna a etapa atual da Unidade.
        try:
            response = self.__l_etapa_atual.valor
            return response
            if response == 1:
                return UG_SINCRONIZADA
            elif 2 <= response <= 3:
                return UG_PARANDO
            elif 4 <= response <= 7:
                return UG_PARADA
            elif 8 <= response <= 15:
                return UG_SINCRONIZANDO
        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar a leitura de Etapa Atual.")
            logger.debug(traceback.format_exc())
            return self.ultima_etapa_atual


    @property
    def estado(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de estado da Unidade.
        return self._estado

    @estado.setter
    def estado(self, var: "int") -> "None":
        # SETTER -> Atribui o novo valor de estado da Unidade.
        self._estado = var

    @property
    def prioridade(self) -> "int":
        # PROPRIEDADE -> Retorna a prioridade da Unidade.
        return self._prioridade

    @prioridade.setter
    def prioridade(self, var: "int") -> "None":
        # SETTER -> Atribui o novo valor de prioridade da Unidade.
        self._prioridade = var

    @property
    def setpoint(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de setpoint da Unidade.
        return self._setpoint

    @setpoint.setter
    def setpoint(self, var: "int"):
        # SETTER -> Atribui o novo valor de setpoint da Unidade.
        if self.limpeza_grade:
            self._setpoint = self.cfg["pot_limpeza_grade"]
        elif var < self.setpoint_minimo:
            self._setpoint = 0
        elif var > self.setpoint_maximo:
            self._setpoint = self.setpoint_maximo
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
    def tentativas_normalizacao(self, var: "int"):
        # SETTER -> Atribui o novo valor de tentativas de normalização da Unidade.
        self._tentativas_normalizacao = var

    @property
    def lista_ugs(self) -> "list[UnidadeGeracao]":
        # PROPRIEDADE -> Retorna a lista com todas as instâncias de Unidades de Geração.
        return self._lista_ugs

    @lista_ugs.setter
    def lista_ugs(self, var: "list[UnidadeGeracao]") -> None:
        # SETTER -> Atribui a nova lista com todas as instâncias de Unidades de Geração.
        self._lista_ugs = var


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

        self.__next_state = sm.StateManual(self)


    def forcar_estado_restrito(self) -> "None":
        """
        Função para forçar o estado restrito na Unidade.
        """

        self.__next_state = sm.StateRestrito(self)


    def forcar_estado_indisponivel(self) -> "None":
        """
        Função para forçar o estado indisponível na Unidade.
        """

        self.__next_state = sm.StateIndisponivel(self)


    def forcar_estado_disponivel(self) -> "None":
        """
        Função para forçar o estado disponível na Unidade.
        """

        self.reconhece_reset_alarmes()
        self.__next_state = sm.StateDisponivel(self)


    def iniciar_ultimo_estado(self) -> "None":
        """
        Função para verificar e atribuir o último estado da Unidade, antes
        da interrupção da última execução do MOA.

        Realiza a consulta no Banco de Dados e atribui o último estado comparando
        com o valor das constantes de Estado.
        """

        estado = self.db.get_ultimo_estado_ug(self.id)[0]

        if estado == None:
            self.__next_state = sm.StateDisponivel(self)
        else:
            if estado == UG_SM_MANUAL:
                self.__next_state = sm.StateManual(self)
            elif estado == UG_SM_DISPONIVEL:
                self.__next_state = sm.StateDisponivel(self)
            elif estado == UG_SM_RESTRITA:
                self.__next_state = sm.StateRestrito(self)
            elif estado == UG_SM_INDISPONIVEL:
                self.__next_state = sm.StateIndisponivel(self)
            else:
                logger.debug("")
                logger.error(f"[UG{self.id}] Não foi possível ler o último estado da Unidade.")
                self.__next_state = sm.StateManual(self)


    def atualizar_registro_estados(self) -> "None":
        """
        Função para registro de troca de estados no banco de dados.

        A função é chamada na inicialização da classe de estado no momento da troca.
        """

        if self.__init_registro_estados == -1:
            self.__init_registro_estados = 0
        else:
            try:
                self.db.update_controle_estados([
                    time(),
                    UG_SM_STR_DCT[self.estado] if self.id == 1 else "",
                    UG_SM_STR_DCT[self.estado] if self.id == 2 else "",
                    UG_SM_STR_DCT[self.estado] if self.id == 3 else "",
                ])

            except Exception:
                logger.error(f"[UG{self.id}] Houve um erro ao inserir os dados para controle de troca de estados no Banco de Dados.")
                logger.debug(traceback.format_exc())


    def atualizar_modbus_moa(self) -> "None":
        """
        Função para atualização do estado da Unidade no CLP - MOA.
        """
        return

        self.clp["MOA"].write_single_register(REG_MOA[f"MOA_OUT_STATE_UG{self.id}"], self.estado)
        self.clp["MOA"].write_single_register(REG_MOA[f"MOA_OUT_ETAPA_UG{self.id}"], self.etapa_atual)


    def normalizar_unidade(self) -> "bool":
        """
        Função para normalização de ocorrências da Unidade de Geração.

        Primeiramente verifica se a Unidade passou do número de tentativas. Caso
        tenha passado, será chamada a função de forçar estado indisponível, senão
        aciona a função de reconhecimento e reset de alarmes da Unidade.
        """

        if self.etapa_atual == UG_PARADA:
            if self.tentativas_normalizacao > self.__limite_tentativas:
                logger.warning(f"[UG{self.id}] A UG estourou as tentativas de normalização, indisponibilizando Unidade.")
                return False

            elif (self.ts_auxiliar - self.get_time()).seconds > self.__tempo_entre_tentativas:
                self.tentativas_normalizacao += 1
                self.ts_auxiliar = self.get_time()
                logger.info(f"[UG{self.id}] Normalizando Unidade (Tentativa {self.tentativas_normalizacao}/{self.__limite_tentativas})")
                self.reconhece_reset_alarmes()
                sleep(1)
                return True

        else:
            logger.debug(f"[UG{self.id}] Aguardando parada total da Unidade para executar a Normalização...")
            return True


    def bloquear_unidade(self) -> "None":
        """
        Função para Bloqueio da Unidade nos estados Restrito e Indisponível.

        Aciona o comando de parada e aguarda a parada total. Logo após, aciona o
        detector de borda para que o comando de parada não seja acionado todo o
        ciclo e depois, chama as funções de acionamento de trips lógicos e elétrico.
        """

        if self.etapa_atual == UG_PARADA:
            self.acionar_trip_logico()
            self.acionar_trip_eletrico()

        elif not self.borda_parar:
            self.parar()
            self.borda_parar = True


    def step(self) -> "None":
        """
        Função principal de passo da Unidade.

        Serve como principal chamada para controle das Unidades da máquina de estados.
        """

        try:
            logger.debug("")
            logger.debug(f"[UG{self.id}] Step  -> Unidade:                   \"{UG_SM_STR_DCT[self.estado]}\"")
            logger.debug(f"[UG{self.id}]          Etapa Atual:               \"{UG_STR_DCT_ETAPAS[self.etapa_atual]}\"")

            if self.etapa_atual == UG_SINCRONIZADA:
                logger.debug(f"[UG{self.id}]          Leituras:")
                logger.debug(f"[UG{self.id}]          - \"Potência Ativa\":        {self.potencia} kW")
                logger.debug(f"[UG{self.id}]          - \"Rotação\":               {self.__l_rotacao.valor:0.1f} RPM")
                logger.debug(f"[UG{self.id}]          - \"Pressão UHRV\":          {self.__l_pressao_uhrv.valor:0.1f} Bar")

            self.__next_state = self.__next_state.step()
            self.atualizar_modbus_moa()

        except Exception:
            logger.error(f"[UG{self.id}] Erro na execução da máquina de estados da Unidade -> \"step\".")
            logger.debug(traceback.format_exc())


    def partir(self) -> "None":
        """
        Função para acionamento do comando de partida da Unidade.

        Primeiramente verifica se há condição de partida. Caso não haja, avisa o
        operador e retorna falso, senão passa a verificar o status do Dijuntor
        52A1 (SA). Caso o disjuntor esteja aberto, avisa o operador e retorna falso.
        Caso a unidade esteja sincronizada, avisa o operador e retorna, senão,
        são acionados diversos comandos de reconhece e reset, antes de acionar o
        comando de partida.
        Caso a Unidade ultrapasse o limite de tentativas de sincronismo, é chamada
        a função de parada, força o estado restrito para verificar se não há
        condicionadores ativos e avisa o operador para tentar normalizar a Unidade.
        """

        try:
            if self.tentativas_sincronismo > 3:
                logger.critical(f"[UG{self.id}] A Unidade ultrapassou o limite de tentativas de Sincronismo.")
                logger.info(f"[UG{self.id}] Entrando no estado Indisponível e acionando Voip.")

                self.temporizar_partida = False
                self.tentativas_sincronismo = 0
                self.forcar_estado_indisponivel()
                return

            # elif not self.clp[f"UG{self.id}"].read_discrete_inputs(REG_UG[f"UG{self.id}"]["CONDICAO_PARTIDA"])[0]:
            #     logger.debug(f"[UG{self.id}]          Máquina sem condição de partida. Irá partir quando as condições forem reestabelecidas.")
            #     return

            # elif self.clp["SA"].read_coils(REG_SA["QCAP_DJ_52A1_FECHADO"])[0] != 0:
            #     logger.info(f"[UG{self.id}]           O Disjuntor 52A1 está aberto. Para partir a máquina, o mesmo deverá ser fechado.")
            #     return

            elif not self.etapa_atual == UG_SINCRONIZADA:
                self.tentativas_sincronismo += 1
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARTIDA\"")
                logger.debug(f"[UG{self.id}]          Tentativas de Sincronismo: {self.tentativas_sincronismo}/3")

                self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_RESET_RV"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_RESET_RELE_RT"], [1])
                self.remover_trip_logico()
                self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_INICIA_PARTIDA"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_CALA_SIRENE"], [1])
                return

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o comando de partida.")
            logger.debug(traceback.format_exc())


    def parar(self) -> "None":
        """
        Função para acionamento do comando de Parada da Unidade.

        Verifica se a unidade está parada. Caso esteja, avisa o operador e retorna,
        senão aciona os comandos de parada e reconehcimento de alarmes.
        """

        try:
            if not self.etapa_atual == UG_PARADA:
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARADA\"")
                self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_ABORTA_PARTIDA"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_ABORTA_SINCRONISMO"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_INICIA_PARADA"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_CALA_SIRENE"], [1])
                self.enviar_setpoint(0)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o comando de parada.")
            logger.debug(traceback.format_exc())


    def enviar_setpoint(self, setpoint_kw: "int") -> "bool":
        """
        Função para envio do valor de setpoint para o controle de potência das
        Unidades.

        Verifica se foi acionado o comando de limpeza de grades. Caso seja verdadeiro,
        atribui o setpoint mínimo de operação, senão, controla os limites máximo
        e mínimo e logo em seguida, envia o valor calculado para a Unidade.
        """

        try:
            self.setpoint_minimo = self.cfg["pot_minima_ugs"]
            self.setpoint_maximo = self.cfg[f"pot_maxima_ug{self.id}"]

            logger.debug(f"[UG{self.id}]          Enviando setpoint:         {int(setpoint_kw)} kW")

            if self.setpoint > 1:
                response = self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_RESET_GERAL"], [1])
                response = self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["REFERENCIA_CARGA"], int(self.setpoint))
                return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o setpoint.")
            logger.debug(traceback.format_exc())
            return False


    def acionar_trip_eletrico(self) -> "None":
        """
        Função para acionamento de TRIP elétrico.

        Aciona o comando de bloqueio da Unidade através do CLP - MOA.
        """

        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"ACIONAR TRIP ELÉTRICO\"")
            self.clp["MOA"].write_single_coil(REG_MOA[f"MOA_OUT_BLOCK_UG{self.id}"], 1)

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
            logger.info(f"[UG{self.id}]          Enviando comando:          \"REMOVER TRIP ELÉTRICO\"")

            self.clp["MOA"].write_single_coil(REG_MOA["PAINEL_LIDO"], 0)
            self.clp["MOA"].write_single_coil(REG_MOA[f"MOA_OUT_BLOCK_UG{self.id}"], 0)
            self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_CALA_SIRENE"], [1])

            if self.clp["SA"].read_discrete_inputs(REG_SA["DJL_FECHADO"])[0] != 1:
                logger.debug(f"[UG{self.id}]          Enviando comando:          \"FECHAR DJ LINHA\".")
                self.clp["SA"].write_single_coil(REG_UG["CMD_FECHA_DJL"], [1])

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())


    def acionar_trip_logico(self) -> "None":
        """
        Função para acionamento de TRIP lógico.

        Aciona o comando de emergência via superviório.
        """

        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"ACIONAR TRIP LÓGICO\"")
            self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_EMERG_SUPER"], [1])

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel acionar o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())


    def remover_trip_logico(self) -> "None":
        """
        Função para remoção de TRIP lógico.

        Aciona os comandos de reset geral, relés e reconhece.
        """

        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"REMOVER TRIP LÓGICO\"")
            self.clp["SA"].write_single_coil(REG_SA["CMD_RESET_RELE_59N"], [1])
            self.clp["SA"].write_single_coil(REG_SA["CMD_RESET_RELE_787"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_RESET_GERAL"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_RESET_700G"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_RESET_BLOQ_86M"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_RESET_BLOQ_86H"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["BLOQ_A86H_ATUADO"], [0])
            self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["BLOQ_A86M_ATUADO"], [0])
            self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["700G_TRIP"], [0])

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())


    def reconhece_reset_alarmes(self) -> "None":
        """
        Função para reset e reconhecimento de TRIPs.

        Chama três vezes as funções de remoção de TRIP elétrico e lógico, para
        depois acionar os comandos de reset geral e reconhece da Unidade.
        """

        try:
            logger.debug("")
            logger.info(f"[UG{self.id}]          Enviando comando:          \"RECONHECE E RESET\"")

            for x in range(3):
                logger.debug("")
                logger.debug(f"[UG{self.id}]          Passo: {x+1}/3")
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
                sleep(1)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o comando de Reconhece e Reset.")
            logger.debug(traceback.format_exc())


    def verificar_sincronismo(self) -> "None":
        """
        Função de verificação de partida da Unidade.

        Caso a unidade seja totalmente sincronizada, o timer é encerrado e avisado,
        senão, é chamada a função de forçar estado indisponível e aciona o comando
        de emergência via supervisório.
        """

        logger.debug(f"[UG{self.id}]          Comando MOA:               \"Iniciar verificação de Partida\"")

        delay = time() + 600
        while time() < delay:
            if not self.temporizar_partida:
                return

        logger.warning(f"[UG{self.id}]          Comando MOA:               \"Acionar emergência por tempo de Partida excedido!\"")
        self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_EMERG_SUPER"], [1])
        self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_EMERG_SUPER"], [0])
        self.temporizar_partida = False


    def verificar_pressao_uhrv(self) -> "None":
        """
        Função para verificação dos limites de pressão da UHRV.

        Esta função tem como objetivo evitar TRIPs em etapas específicas da Unidade.
        """

        if self.__l_pressao_uhrv.valor <= 130:
            self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_RESET_BLOQ_86H"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["BLOQ_A86H_ATUADO"], [0])


    def verificar_rotacao(self) -> "None":
        """
        Função para verificar a rotação da Unidade, caso haja um atraso no processo
        de sincronismo.

        Chama a função de aguardar rotação, com um tempo pré-definido de aguardo
        no momento que a rotação da Unidade atingir a janela pré-definida.
        Caso o temporizador ultrapasse o tempo, será realizado o Reset Geral, e
        contabilizada uma tentativa de aguardo de rotação. Caso o número de tentativas
        ultrapasse seja maior que três, avisa o operador e aborta a pertida para
        que seja realizada uma nova tentativa do processo de sincronismo do início.
        """

        try:
            if self.tentativas_aguardar_rotacao > 3:
                logger.warning(f"[UG{self.id}] A Unidade ultrapassou o limite de tentativas de aguardo pela rotação.")
                logger.info(f"[UG{self.id}] Abortando partida para realizar uma nova tentativa de Sincronismo do início.")
                self.parar()

            elif self.__l_rotacao.valor < 500 and not self.temporizar_rotacao:
                self.temporizar_rotacao = True
                Thread(target=lambda: self.aguardar_rotacao()).start()

            elif 300 <= self.__l_rotacao.valor <= 500 and not self.atraso_rotacao:
                self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["CMD_RESET_BLOQ_86M"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG_UG[f"UG{self.id}"]["BLOQ_A86M_ATUADO"], [0])

            elif self.atraso_rotacao:
                self.tentativas_aguardar_rotacao += 1
                logger.debug("")
                logger.warning(f"[UG{self.id}] A rotação da Unidade está demorando para subir. (Tentativa {self.tentativas_aguardar_rotacao}/3)")
                logger.debug("")

                self.reconhece_reset_alarmes()

                self.atraso_rotacao = False

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro com a função de verificação de rotação da Unidade.")
            logger.debug(f"Traceback: {traceback.format_exc()}")


    def aguardar_normalizacao(self, delay: "int") -> "None":
        """
        Função de temporizador para espera de normalização da Unidade restrita,
        por tempo pré-definido por agendamento na Interface.
        """

        if not self.temporizar_normalizacao:
            sleep(max(0, time() + delay - time()))
            self.temporizar_normalizacao = True
            return


    def aguardar_rotacao(self) -> "None":
        """
        Função com temporizador de aguardo da rotação da máquina com período
        pré-definido.
        """

        delay = time() + 90
        while time() <= delay:
            if self.__l_rotacao.valor > 500:
                self.temporizar_rotacao = False
                return
            sleep(2)

        self.atraso_rotacao = True
        self.temporizar_rotacao = False


    def controle_etapas(self) -> "None":
        """
        Função para controle de etapas da Unidade.

        PARADA -> Envia comando de partida caso seja atribuído um valor de setpoint.
        PARANDO -> Envia setpoint apenas (boa prática)
        SINCRONIZANDO -> Chama a função de verificação de partida por tempo pré-
        definido. Caso o timer ultrapasse o tempo estipulado, será chamada a função
        de forçar estado indisponível, senão, caso a unidade sincronize, para o
        timer. Caso seja atribuído o valor 0 no setpoint, aciona o comando de parada.
        SINCRONIZADA -> Controla a variável de tempo sincronizada e envia o comando
        de parada caso seja atribuído o setpoint 0 para a Unidade.
        """

        # PARANDO
        if self.etapa_atual == UG_PARANDO:
            if self.setpoint >= self.setpoint_minimo:
                self.enviar_setpoint(self.setpoint)

        # SINCRONIZANDO
        elif self.etapa_atual == UG_SINCRONIZANDO:
            if not self.temporizar_partida:
                self.temporizar_partida = True
                Thread(target=lambda: self.verificar_sincronismo()).start()

            self.verificar_pressao_uhrv()
            self.verificar_rotacao()

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        # PARADA
        elif self.etapa_atual == UG_PARADA:
            if self.setpoint >= self.setpoint_minimo:
                self.partir()
                self.enviar_setpoint(self.setpoint)

        # SINCRONIZADA
        elif self.etapa_atual == UG_SINCRONIZADA:
            self.temporizar_partida = False
            self.tentativas_sincronismo = 0

            if not self.aux_tempo_sincronizada:
                self.aux_tempo_sincronizada = self.get_time()

            elif (self.get_time() - self.aux_tempo_sincronizada).seconds >= 300:
                self.tentativas_normalizacao = 0

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        # CONTROLE TEMPO SINCRONIZADAS
        if not self.etapa_atual == UG_SINCRONIZADA:
            self.aux_tempo_sincronizada = None


    def atenuar_carga(self) -> "None":
        """
        Função para atenuação de carga através de leitura de Pressão na Entrada da Turbina.

        Calcula o ganho e verifica os limites máximo e mínimo para deteminar se
        deve atenuar ou não.
        """

        flags = 0
        atenuacao = 0
        logger.debug(f"[UG{self.id}]          Verificando Atenuadores...") if self.etapa_atual == UG_SINCRONIZADA else None

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

                atenuacao = 0

        if flags == 0 and self.etapa_atual == UG_SINCRONIZADA:
            logger.debug(f"[UG{self.id}]          Não há necessidade de Atenuação.")

        ganho = 1 - self.atenuacao
        aux = self.setpoint
        self.atenuacao = 0
        if (self.setpoint > self.setpoint_minimo) and self.setpoint * ganho > self.setpoint_minimo:
            setpoint_atenuado = self.setpoint - 0.5 * (self.setpoint -  (self.setpoint * ganho))
            self.setpoint = min(max(setpoint_atenuado, self.setpoint_minimo), self.setpoint_maximo)

        elif self.setpoint > self.setpoint_minimo and (self.setpoint * ganho) < self.setpoint_minimo:
            self.setpoint =  self.setpoint_minimo

        if self.etapa_atual == UG_SINCRONIZADA and ganho < 1:
            logger.debug(f"[UG{self.id}]                                     SP {aux} * GANHO {ganho:0.4f} = {self.setpoint} kW")


    def ajuste_inicial_cx(self) -> "None":
        """
        Função para ajustar valores de P, I e IE da Unidade na inicialização do MOA.

        Esta função é executada apenas uma vez na inicialização do processo.
        """

        try:
            self.cx_controle_p = (self.l_pressao_cx_espiral.valor - self.cfg[f"pressao_alvo_ug2"]) * self.cfg["cx_kp"]
            self.cx_ajuste_ie = sum(ug.potencia for ug in self.lista_ugs) / self.cfg["pot_alvo_usina"]
            self.cx_controle_i = self.cx_ajuste_ie - self.cx_controle_p

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar o ajuste incial do PID para pressão de caixa espiral.")
            logger.debug(traceback.format_exc())


    def controle_cx_espiral(self) -> "float":
        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = self.potencia

        if self.__iniciar_cx_esp == -1:
            self.ajuste_inicial_cx()
            self.__iniciar_cx_esp = 0

        try:
            logger.debug(f"[UG{self.id}] Pressão Caixa Espiral:")
            logger.debug(f"[UG{self.id}]          Alvo:                      {self.cfg[f'pressao_alvo_ug2']:0.3f}")
            logger.debug(f"[UG{self.id}]          Leitura:                   {self.l_pressao_cx_espiral.valor:0.3f}")
            logger.debug("")

            self.erro_press_cx = 0
            self.erro_press_cx = self.l_pressao_cx_espiral.valor - self.cfg[f"pressao_alvo_ug2"]

            self.cx_controle_p = self.cfg["cx_kp"] * self.erro_press_cx
            self.cx_controle_i = max(min((self.cfg["cx_ki"] * self.erro_press_cx) + self.cx_controle_i, 1), 0)

            saida_pi = self.cx_controle_p + self.cx_controle_i

            self.cx_controle_ie = max(min(saida_pi + self.cx_ajuste_ie * self.cfg["cx_kie"], 1), 0)

            pot_alvo = max(min(round(self.cfg[f"pot_maxima_ug{self.id}"] * self.cx_controle_ie, 5), self.cfg[f"pot_maxima_ug{self.id}"],),self.cfg["pot_minima_ugs"],)
            pot_medidor = se.Subestacao.l_potencia_medidor.valor

            logger.debug(f"[UG{self.id}] Potência calculada:                 {pot_alvo:0.3f}")
            logger.debug("")

            pot_aux = self.cfg["pot_alvo_usina"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_alvo_usina"])
            pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

            if pot_medidor > self.cfg["pot_alvo_usina"] * 0.97:
                pot_alvo = self.pot_alvo_anterior * (1 - 0.5 * ((pot_medidor - self.cfg["pot_alvo_usina"]) / self.cfg["pot_alvo_usina"]))

            self.pot_alvo_anterior = pot_alvo

            return pot_alvo

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro no método de Controle por Caixa Espiral da Unidade.")
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

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condicionadores_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.warning(f"[UG{self.id}] Foram detectados condicionadores ativos na Unidade!")
            else:
                logger.info(f"[UG{self.id}] Ainda há condicionadores ativos na Unidade!")

            for condic in condicionadores_ativos:
                if condic in self.condicionadores_ativos:
                    logger.debug(f"[UG{self.id}] descricaoição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                elif condic.gravidade == CONDIC_INDISPONIBILIZAR:
                    logger.warning(f"[UG{self.id}] descricaoição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.db.update_alarmes([self.get_time().strftime("%Y-%m-%d %H:%M:%S"), condic.gravidade, condic.descricao, "X" if autor_i == 0 else ""])
                    self.condicionadores_ativos.append(condic)
                    autor_i += 1
                    flag = CONDIC_INDISPONIBILIZAR

                elif condic.gravidade == CONDIC_AGUARDAR:
                    logger.warning(f"[UG{self.id}] descricaoição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.db.update_alarmes([self.get_time().strftime("%Y-%m-%d %H:%M:%S"), condic.gravidade, condic.descricao, "X" if autor_i == 0 and autor_a == 0 else ""])
                    self.condicionadores_ativos.append(condic)
                    autor_a += 1
                    if flag == CONDIC_INDISPONIBILIZAR:
                        continue
                    else:
                        flag = CONDIC_AGUARDAR

                elif condic.gravidade == CONDIC_NORMALIZAR:
                    logger.warning(f"[UG{self.id}] descricaoição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.db.update_alarmes([self.get_time().strftime("%Y-%m-%d %H:%M:%S"), condic.gravidade, condic.descricao, "X" if autor_i == 0 and autor_a == 0 and autor_n == 0 else ""])
                    self.condicionadores_ativos.append(condic)
                    autor_n += 1
                    if flag in (CONDIC_INDISPONIBILIZAR, CONDIC_AGUARDAR):
                        continue
                    else:
                        flag = CONDIC_NORMALIZAR

            logger.debug("")
            return flag

        else:
            self.condicionadores_ativos = []
            return flag


    def atualizar_limites_condicionadores(self, parametros) -> "None":
        """
        Função para extração de valores do Banco de Dados da Interface WEB e atribuição
        de novos limites de operação de condicionadores.
        """

        try:
            self.prioridade = int(parametros[f"ug{self.id}_prioridade"])
            self.aviso_caixa_espiral_ug2 = float(parametros[f"aviso_caixa_espiral_ug2"])

            self.c_tmp_fase_r.valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{self.id}"])
            self.c_tmp_fase_s.valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{self.id}"])
            self.c_tmp_fase_t.valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{self.id}"])
            self.c_tmp_nucleo_estator.valor_base = float(parametros[f"alerta_temperatura_nucleo_estator_ug{self.id}"])
            self.c_tmp_mancal_rad_dia_1.valor_base = float(parametros[f"alerta_temperatura_mancal_rad_dia_1_ug{self.id}"])
            self.c_tmp_mancal_rad_dia_2.valor_base = float(parametros[f"alerta_temperatura_mancal_rad_dia_2_ug{self.id}"])
            self.c_tmp_mancal_rad_tra_1.valor_base = float(parametros[f"alerta_temperatura_mancal_rad_tra_1_ug{self.id}"])
            self.c_tmp_mancal_rad_tra_2.valor_base = float(parametros[f"alerta_temperatura_mancal_rad_tra_2_ug{self.id}"])
            self.c_tmp_saida_de_ar.valor_base = float(parametros[f"alerta_temperatura_saida_de_ar_ug{self.id}"])
            self.c_tmp_mancal_guia_escora.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_escora_ug{self.id}"])
            self.c_tmp_mancal_guia_radial.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_radial_ug{self.id}"])
            self.c_tmp_mancal_guia_contra.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_contra_ug{self.id}"])
            self.c_pressao_cx_espiral.valor_base = float(parametros[f"alerta_caixa_espiral_ug2"])

            self.c_tmp_fase_r.valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{self.id}"])
            self.c_tmp_fase_s.valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{self.id}"])
            self.c_tmp_fase_t.valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{self.id}"])
            self.c_tmp_nucleo_estator.valor_limite = float(parametros[f"limite_temperatura_nucleo_estator_ug{self.id}"])
            self.c_tmp_mancal_rad_dia_1.valor_limite = float(parametros[f"limite_temperatura_mancal_rad_dia_1_ug{self.id}"])
            self.c_tmp_mancal_rad_dia_2.valor_limite = float(parametros[f"limite_temperatura_mancal_rad_dia_2_ug{self.id}"])
            self.c_tmp_mancal_rad_tra_1.valor_limite = float(parametros[f"limite_temperatura_mancal_rad_tra_1_ug{self.id}"])
            self.c_tmp_mancal_rad_tra_2.valor_limite = float(parametros[f"limite_temperatura_mancal_rad_tra_2_ug{self.id}"])
            self.c_tmp_saida_de_ar.valor_limite = float(parametros[f"limite_temperatura_saida_de_ar_ug{self.id}"])
            self.c_tmp_mancal_guia_escora.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_escora_ug{self.id}"])
            self.c_tmp_mancal_guia_radial.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_radial_ug{self.id}"])
            self.c_tmp_mancal_guia_contra.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_contra_ug{self.id}"])
            self.c_pressao_cx_espiral.valor_limite = float(parametros[f"limite_caixa_espiral_ug2"])

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores.")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")


    def controle_limites_operacao(self) -> "None":
        """
        Função para verificação de limites de operação da Unidade.

        Verifica os valores base e limite da Unidade, pré-determinados na interface
        WEB, e avisa o operador caso algum valor ultrapasse o estipulado.
        """

        if self.l_tmp_fase_r.valor >= self.c_tmp_fase_r.valor_base:
            logger.debug(f"[UG{self.id}] A temperatura de Fase R da UG passou do valor base! ({self.c_tmp_fase_r.valor_base} C) | Leitura: {self.l_tmp_fase_r.valor} C")

        if self.l_tmp_fase_r.valor >= 0.9*(self.c_tmp_fase_r.valor_limite - self.c_tmp_fase_r.valor_base) + self.c_tmp_fase_r.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase R da UG está muito próxima do limite! ({self.c_tmp_fase_r.valor_limite} C) | Leitura: {self.l_tmp_fase_r.valor} C")

        if self.l_tmp_fase_s.valor >= self.c_tmp_fase_s.valor_base:
            logger.debug(f"[UG{self.id}] A temperatura de Fase S da UG passou do valor base! ({self.c_tmp_fase_s.valor_base} C) | Leitura: {self.l_tmp_fase_s.valor} C")

        if self.l_tmp_fase_s.valor >= 0.9*(self.c_tmp_fase_s.valor_limite - self.c_tmp_fase_s.valor_base) + self.c_tmp_fase_s.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase S da UG está muito próxima do limite! ({self.c_tmp_fase_s.valor_limite} C) | Leitura: {self.l_tmp_fase_s.valor} C")

        if self.l_tmp_fase_t.valor >= self.c_tmp_fase_t.valor_base:
            logger.debug(f"[UG{self.id}] A temperatura de Fase T da UG passou do valor base! ({self.c_tmp_fase_t.valor_base} C) | Leitura: {self.l_tmp_fase_t.valor} C")

        if self.l_tmp_fase_t.valor >= 0.9*(self.c_tmp_fase_t.valor_limite - self.c_tmp_fase_t.valor_base) + self.c_tmp_fase_t.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase T da UG está muito próxima do limite! ({self.c_tmp_fase_t.valor_limite} C) | Leitura: {self.l_tmp_fase_t.valor} C")

        if self.l_tmp_nucleo_estator.valor >= self.c_tmp_nucleo_estator.valor_base:
            logger.debug(f"[UG{self.id}] A temperatura do Núcleo Gerador Estator da UG passou do valor base! ({self.c_tmp_nucleo_estator.valor_base} C) | Leitura: {self.l_tmp_nucleo_estator.valor} C")

        if self.l_tmp_nucleo_estator.valor >= 0.9*(self.c_tmp_nucleo_estator.valor_limite - self.c_tmp_nucleo_estator.valor_base) + self.c_tmp_nucleo_estator.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Núcleo Gerador Estator da UG está muito próxima do limite! ({self.c_tmp_nucleo_estator.valor_limite} C) | Leitura: {self.l_tmp_nucleo_estator.valor} C")

        if self.l_tmp_mancal_rad_dia_1.valor >= self.c_tmp_mancal_rad_dia_1.valor_base:
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Radial Dianteiro 1 da UG passou do valor base! ({self.c_tmp_mancal_rad_dia_1.valor_base} C) | Leitura: {self.l_tmp_mancal_rad_dia_1.valor} C")

        if self.l_tmp_mancal_rad_dia_1.valor >= 0.9*(self.c_tmp_mancal_rad_dia_1.valor_limite - self.c_tmp_mancal_rad_dia_1.valor_base) + self.c_tmp_mancal_rad_dia_1.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Radial Dianteiro 1 da UG está muito próxima do limite! ({self.c_tmp_mancal_rad_dia_1.valor_limite} C) | Leitura: {self.l_tmp_mancal_rad_dia_1.valor} C")

        if self.l_tmp_mancal_rad_dia_2.valor >= self.c_tmp_mancal_rad_dia_2.valor_base:
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Radial Dianteiro 2 da UG passou do valor base! ({self.c_tmp_mancal_rad_dia_2.valor_base} C) | Leitura: {self.l_tmp_mancal_rad_dia_2.valor} C")

        if self.l_tmp_mancal_rad_dia_2.valor >= 0.9*(self.c_tmp_mancal_rad_dia_2.valor_limite - self.c_tmp_mancal_rad_dia_2.valor_base) + self.c_tmp_mancal_rad_dia_2.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Radial Dianteiro 2 da UG está muito próxima do limite! ({self.c_tmp_mancal_rad_dia_2.valor_limite} C) | Leitura: {self.l_tmp_mancal_rad_dia_2.valor} C")

        if self.l_tmp_mancal_rad_tra_1.valor >= self.c_tmp_mancal_rad_tra_1.valor_base:
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Radial Traseiro 1 da UG passou do valor base! ({self.c_tmp_mancal_rad_tra_1.valor_base} C) | Leitura: {self.l_tmp_mancal_rad_tra_1.valor} C")

        if self.l_tmp_mancal_rad_tra_1.valor >= 0.9*(self.c_tmp_mancal_rad_tra_1.valor_limite - self.c_tmp_mancal_rad_tra_1.valor_base) + self.c_tmp_mancal_rad_tra_1.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Radial Traseiro 1 da UG está muito próxima do limite! ({self.c_tmp_mancal_rad_tra_1.valor_limite} C) | Leitura: {self.l_tmp_mancal_rad_tra_1.valor} C")

        if self.l_tmp_mancal_rad_tra_2.valor >= self.c_tmp_mancal_rad_tra_2.valor_base:
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Radial Traseiro 2 da UG passou do valor base! ({self.c_tmp_mancal_rad_tra_2.valor_base} C) | Leitura: {self.l_tmp_mancal_rad_tra_2.valor} C")

        if self.l_tmp_mancal_rad_tra_2.valor >= 0.9*(self.c_tmp_mancal_rad_tra_2.valor_limite - self.c_tmp_mancal_rad_tra_2.valor_base) + self.c_tmp_mancal_rad_tra_2.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Radial Traseiro 2 da UG está muito próxima do limite! ({self.c_tmp_mancal_rad_tra_2.valor_limite} C) | Leitura: {self.l_tmp_mancal_rad_tra_2.valor} C")

        if self.l_tmp_saida_de_ar.valor >= self.c_tmp_saida_de_ar.valor_base:
            logger.debug(f"[UG{self.id}] A temperatura da Saída de Ar da UG passou do valor base! ({self.c_tmp_saida_de_ar.valor_base} C) | Leitura: {self.l_tmp_saida_de_ar.valor} C")

        if self.l_tmp_saida_de_ar.valor >= 0.9*(self.c_tmp_saida_de_ar.valor_limite - self.c_tmp_saida_de_ar.valor_base) + self.c_tmp_saida_de_ar.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura da Saída de Ar da UG está muito próxima do limite! ({self.c_tmp_saida_de_ar.valor_limite} C) | Leitura: {self.l_tmp_saida_de_ar.valor} C")

        if self.l_tmp_mancal_guia_escora.valor >= self.c_tmp_mancal_guia_escora.valor_base:
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Guia Escora da UG passou do valor base! ({self.c_tmp_mancal_guia_escora.valor_base} C) | Leitura: {self.l_tmp_mancal_guia_escora.valor} C")

        if self.l_tmp_mancal_guia_escora.valor >= 0.9*(self.c_tmp_mancal_guia_escora.valor_limite - self.c_tmp_mancal_guia_escora.valor_base) + self.c_tmp_mancal_guia_escora.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Guia Escora da UG está muito próxima do limite! ({self.c_tmp_mancal_guia_escora.valor_limite} C) | Leitura: {self.l_tmp_mancal_guia_escora.valor} C")

        if self.l_tmp_mancal_guia_radial.valor >= self.c_tmp_mancal_guia_radial.valor_base:
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Guia Radial da UG passou do valor base! ({self.c_tmp_mancal_guia_radial.valor_base} C) | Leitura: {self.l_tmp_mancal_guia_radial.valor} C")

        if self.l_tmp_mancal_guia_radial.valor >= 0.9*(self.c_tmp_mancal_guia_radial.valor_limite - self.c_tmp_mancal_guia_radial.valor_base) + self.c_tmp_mancal_guia_radial.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Guia Radial da UG está muito próxima do limite! ({self.c_tmp_mancal_guia_radial.valor_limite} C) | Leitura: {self.l_tmp_mancal_guia_radial.valor} C")

        if self.l_tmp_mancal_guia_contra.valor >= self.c_tmp_mancal_guia_contra.valor_base:
            logger.debug(f"[UG{self.id}] A temperatura do Mancal Guia Contra Escora da UG passou do valor base! ({self.c_tmp_mancal_guia_contra.valor_base} C) | Leitura: {self.l_tmp_mancal_guia_contra.valor} C")

        if self.l_tmp_mancal_guia_contra.valor >= 0.9*(self.c_tmp_mancal_guia_contra.valor_limite - self.c_tmp_mancal_guia_contra.valor_base) + self.c_tmp_mancal_guia_contra.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Guia Contra Escora da UG está muito próxima do limite! ({self.c_tmp_mancal_guia_contra.valor_limite} C) | Leitura: {self.l_tmp_mancal_guia_contra.valor} C")

        if self.l_pressao_cx_espiral.valor <= self.aviso_caixa_espiral_ug2 and self.etapa_atual == UG_SINCRONIZADA and self.potencia >= 1360 and self.id == 2:
            logger.debug(f"[UG{self.id}] A pressão Caixa Espiral da UG passou do valor estipulado! ({self.aviso_caixa_espiral_ug2:03.2f} KGf/m2) | Leitura: {self.l_pressao_cx_espiral.valor:03.2f}")


    def leitura_temporizada(self) -> "None":
        """
        Função para consulta de acionamentos da Unidade e avisos através do mecanismo
        de acionamento temporizado.
        """

        if self.l_pastilha_freio_gasta.valor != 0:
            logger.warning(f"[UG{self.id}] O sensor de Freio da UG retornou que a Pastilha está gasta, favor considerar troca.")

        if self.l_uhrv_filtro_press_75_sujo.valor != 0:
            logger.warning(f"[UG{self.id}] O sensor do Filtro de Pressão UHRV retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.l_uhrv_filtro_retor_75_sujo.valor != 0:
            logger.warning(f"[UG{self.id}] O sensor do Filtro de Retorno UHRV retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.l_uhlm_filtro_press_1_75_sujo.valor != 0:
            logger.warning(f"[UG{self.id}] O sensor do Filtro 1 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.l_uhlm_filtro_press_2_75_sujo.valor != 0:
            logger.warning(f"[UG{self.id}] O sensor do Filtro 2 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.l_bomba_mec_filtro_press_75_sujo.valor != 0:
            logger.warning(f"[UG{self.id}] O sensor do Filtro de Pressão da Bomba Mecânica retornou que o filtro está 75% sujo, favor considerar troca.")

        if self.l_freio_modo_remoto.valor != 1:
            logger.debug(f"[UG{self.id}] O freio da UG saiu do modo remoto, favor analisar a situação.")

        if self.l_compresor_modo_remoto.valor != 1:
            logger.debug(f"[UG{self.id}] O compressor da UG saiu do modo remoto, favor analisar a situação.")


    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Unidade.
        """

        ### CONDICIONADORES ESSENCIAIS
        # Pressão Caixa Espiral
        self.l_pressao_cx_espiral = lei.LeituraModbus(self.clp[f"UG2"], REG_UG[f"UG2"]["PRESS_K1_CX_ESPIRAL"], escala=0.01, op=4, descricao=f"[UG2] Caixa Espiral")
        self.c_pressao_cx_espiral = c.CondicionadorExponencialReverso(self.l_pressao_cx_espiral, CONDIC_INDISPONIBILIZAR)

        # Fase R
        self.l_tmp_fase_r = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_01"], op=4, descricao=f"[UG{self.id}] Temperatura Fase R")
        self.c_tmp_fase_r = c.CondicionadorExponencial(self.l_tmp_fase_r, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_tmp_fase_r)
        self.condicionadores_atenuadores.append(self.c_tmp_fase_r)

        # Fase S
        self.l_tmp_fase_s = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_02"], op=4, descricao=f"[UG{self.id}] Temperatura Fase S")
        self.c_tmp_fase_s = c.CondicionadorExponencial(self.l_tmp_fase_s, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_tmp_fase_s)
        self.condicionadores_atenuadores.append(self.c_tmp_fase_s)

        # Fase T
        self.l_tmp_fase_t = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_03"], op=4, descricao=f"[UG{self.id}] Temperatura Fase T")
        self.c_tmp_fase_t = c.CondicionadorExponencial(self.l_tmp_fase_t, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_tmp_fase_t)
        self.condicionadores_atenuadores.append(self.c_tmp_fase_t)

        # Nucleo estator
        self.l_tmp_nucleo_estator = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_04"], op=4, descricao=f"[UG{self.id}] Temperatura Núcelo do Estator",)
        self.c_tmp_nucleo_estator = c.CondicionadorExponencial(self.l_tmp_nucleo_estator, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_tmp_nucleo_estator)
        self.condicionadores_atenuadores.append(self.c_tmp_nucleo_estator)

        # MRD 1
        self.l_tmp_mancal_rad_dia_1 = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_05"], op=4, descricao=f"[UG{self.id}] Temperatura Mancal Radial Dianteiro")
        self.c_tmp_mancal_rad_dia_1 = c.CondicionadorExponencial(self.l_tmp_mancal_rad_dia_1, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_tmp_mancal_rad_dia_1)
        self.condicionadores_atenuadores.append(self.c_tmp_mancal_rad_dia_1)

        # MRT 1
        self.l_tmp_mancal_rad_tra_1 = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_06"], op=4, descricao=f"[UG{self.id}] Temperatura Mancal Radial Traseiro",)
        self.c_tmp_mancal_rad_tra_1 = c.CondicionadorExponencial(self.l_tmp_mancal_rad_tra_1, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_tmp_mancal_rad_tra_1)
        self.condicionadores_atenuadores.append(self.c_tmp_mancal_rad_tra_1)

        # MRD 2
        self.l_tmp_mancal_rad_dia_2 = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_07"], op=4, descricao=f"[UG{self.id}] Temperatura Mancal Radial Dianteiro 2")
        self.c_tmp_mancal_rad_dia_2 = c.CondicionadorExponencial(self.l_tmp_mancal_rad_dia_2, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_tmp_mancal_rad_dia_2)
        self.condicionadores_atenuadores.append(self.c_tmp_mancal_rad_dia_2)

        # MRT 2
        self.l_tmp_mancal_rad_tra_2 = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_08"], op=4, descricao=f"[UG{self.id}] Temperatura Mancal Radial Traseiro 2")
        self.c_tmp_mancal_rad_tra_2 = c.CondicionadorExponencial(self.l_tmp_mancal_rad_tra_2, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_tmp_mancal_rad_tra_2)
        self.condicionadores_atenuadores.append(self.c_tmp_mancal_rad_tra_2)

        # Saída de ar
        self.l_tmp_saida_de_ar = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_10"], op=4, descricao=f"[UG{self.id}] Saída de Ar")
        self.c_tmp_saida_de_ar = c.CondicionadorExponencial(self.l_tmp_saida_de_ar, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_tmp_saida_de_ar)
        self.condicionadores_atenuadores.append(self.c_tmp_saida_de_ar)

        # Mancal Guia Radial
        self.l_tmp_mancal_guia_radial = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMP_MC_GUIA_RADIAL"], descricao=f"[UG{self.id}] Mancal Guia Radial",)
        self.c_tmp_mancal_guia_radial = c.CondicionadorExponencial(self.l_tmp_mancal_guia_radial, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_tmp_mancal_guia_radial)
        self.condicionadores_atenuadores.append(self.c_tmp_mancal_guia_radial)

        # Mancal Guia Escora
        self.l_tmp_mancal_guia_escora = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMP_MC_GUIA_ESCORA"], descricao=f"[UG{self.id}] Mancal Guia Escora")
        self.c_tmp_mancal_guia_escora = c.CondicionadorExponencial(self.l_tmp_mancal_guia_escora, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_tmp_mancal_guia_escora)
        self.condicionadores_atenuadores.append(self.c_tmp_mancal_guia_escora)

        # Mancal Guia Contra Escora
        self.l_tmp_mancal_guia_contra = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMP_MC_GUIA_CONTRA_ESCORA"], descricao=f"[UG{self.id}] Mancal Guia Contra Escora")
        self.c_tmp_mancal_guia_contra = c.CondicionadorExponencial(self.l_tmp_mancal_guia_contra, CONDIC_INDISPONIBILIZAR)
        self.condicionadores_essenciais.append(self.c_tmp_mancal_guia_contra)
        self.condicionadores_atenuadores.append(self.c_tmp_mancal_guia_contra)

        return

        self.l_cmd_emerg_via_super = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["EMERGENCIA_SUPER"], descricao=f"[UG{self.id}] Emergência Via Supervisório")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_cmd_emerg_via_super, CONDIC_NORMALIZAR))

        self.l_trip_eletrico = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRIP_ELETRICO"], descricao=f"[UG{self.id}] Trip Elétrico")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_trip_eletrico, CONDIC_NORMALIZAR, [UG_SINCRONIZADA], self.id))
        
        self.l_trip_700G = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["700G_TRIP"], descricao=f"[UG{self.id}] SEL 700G Trip")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_trip_700G, CONDIC_NORMALIZAR, [UG_SINCRONIZADA], self.id))

        self.l_trip_mecanico = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRIP_MECANICO"], descricao=f"[UG{self.id}] Trip Mecâncio")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_trip_mecanico, CONDIC_INDISPONIBILIZAR))

        self.l_trip_rv = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_TRIP"], descricao=f"[UG{self.id}] RV Trip")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_trip_rv, CONDIC_INDISPONIBILIZAR))

        self.l_trip_avr = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["AVR_TRIP"], descricao=f"[UG{self.id}] AVR Trip")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_trip_avr, CONDIC_INDISPONIBILIZAR))

        self.l_SEL700G_atuado = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["SEL700G_ATUADO"], descricao=f"[UG{self.id}] SEL 700G Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_SEL700G_atuado, CONDIC_INDISPONIBILIZAR))

        self.l_bloq_A86M_atuado = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["BLOQ_A86M_ATUADO"], descricao=f"[UG{self.id}] Bloqueio 86M Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_bloq_A86M_atuado, CONDIC_INDISPONIBILIZAR))

        self.l_bloq_A86H_atuado = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["BLOQ_A86H_ATUADO"], descricao=f"[UG{self.id}] Bloqueio 86H Atuado")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_bloq_A86H_atuado, CONDIC_NORMALIZAR, [UG_SINCRONIZADA], self.id))


        ### CONDICIONADORES NORMAIS
        self.l_falha_dj_tps_sinc_G2 = lei.LeituraModbusCoil(self.clp["SA"], REG_SA["FALHA_DJ_TPS_SINCR_G2"], descricao=f"[SA-UG{self.id}] Trasformador Potencial Disjuntor Sincronização Falha")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_dj_tps_sinc_G2, CONDIC_INDISPONIBILIZAR))

        self.l_dj1_alarme_press_baixa = lei.LeituraModbusCoil(self.clp["SA"], REG_SA["DJL_ALM_PRESS_BAIXA"], descricao=f"[SA-UG{self.id}] Disjutor 1 Alarme Pressão Baixa")
        self.condicionadores.append(c.CondicionadorBase(self.l_dj1_alarme_press_baixa, CONDIC_INDISPONIBILIZAR))

        self.l_dj1_bloq_press_baixa = lei.LeituraModbusCoil(self.clp["SA"], REG_SA["DJL_BLOQ_PRESS_BAIXA"], descricao=f"[SA-UG{self.id}] Disjuntor 1 Bloqueio Pressão Baixa")
        self.condicionadores.append(c.CondicionadorBase(self.l_dj1_bloq_press_baixa, CONDIC_INDISPONIBILIZAR))

        self.l_UHRV_trip_bomba_1 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_TRIP_BOMBA_1"], descricao=f"[UG{self.id}] UHRV Bomba 1 Trip")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHRV_trip_bomba_1, CONDIC_INDISPONIBILIZAR))

        self.l_UHRV_Trip_bomba_2 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_TRIP_BOMBA_2"], descricao=f"[UG{self.id}] UHRV Bomba 2 Trip")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHRV_Trip_bomba_2, CONDIC_INDISPONIBILIZAR))

        self.l_UHLM_trip_bomba_1 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_TRIP_BOMBA_1"], descricao=f"[UG{self.id}] UHLM Bomba 1 Trip")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHLM_trip_bomba_1, CONDIC_INDISPONIBILIZAR))

        self.l_UHLM_trip_bomba_2 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_TRIP_BOMBA_2"], descricao=f"[UG{self.id}] UHLM Bomba 2 Trip")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHLM_trip_bomba_2, CONDIC_INDISPONIBILIZAR))

        self.l_trip_dj52A1 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["QCAUG_TRIP_DJ_52A1"], descricao=f"[UG{self.id}] QCAUG Disjuntor 52A1 Trip")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_dj52A1, CONDIC_INDISPONIBILIZAR))

        self.l_trip_alim_painel_freio = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRIP_ALIM_FREIO"], descricao=f"[UG{self.id}] Alimentação Painel Freio Trip")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_alim_painel_freio, CONDIC_INDISPONIBILIZAR))

        self.l_trip_dj_agrup = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["QCAUG_TRIP_DJ_AGRUP"], descricao=f"[UG{self.id}] QCAUG Disjuntor Agrupamento Trip")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_dj_agrup, CONDIC_INDISPONIBILIZAR))

        self.l_AVR_falha_interna = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["AVR_FALHA_INTERNA"], descricao=f"[UG{self.id}] AVR Falha Interna")
        self.condicionadores.append(c.CondicionadorBase(self.l_AVR_falha_interna, CONDIC_INDISPONIBILIZAR))

        self.l_SEL700G_falha_interna = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["SEL700G_FALHA_INTERNA"], descricao=f"[UG{self.id}] SEL 700G Falha Interna")
        self.condicionadores.append(c.CondicionadorBase(self.l_SEL700G_falha_interna, CONDIC_INDISPONIBILIZAR))

        self.l_falha_painel_380Vca = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["QCAUG_FALHA_380VCA"], descricao=f"[UG{self.id}] QCAUG Falha 380 VCA Painel")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_painel_380Vca, CONDIC_NORMALIZAR))

        self.l_falta_125Vcc = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["FALTA_125VCC"], descricao=f"[UG{self.id}] Falta 125 Vcc")
        self.condicionadores.append(c.CondicionadorBase(self.l_falta_125Vcc, CONDIC_INDISPONIBILIZAR))

        self.l_falta_com_125Vcc = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["FALTA_125VCC_COM"], descricao=f"[UG{self.id}] Falta 125 Vcc Com")
        self.condicionadores.append(c.CondicionadorBase(self.l_falta_com_125Vcc, CONDIC_INDISPONIBILIZAR))

        self.l_falta_alim_val_125Vcc = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["FALTA_125VCC_ALIM_VAL"], descricao=f"[UG{self.id}] Falta 125 Vcc Alimentação")
        self.condicionadores.append(c.CondicionadorBase(self.l_falta_alim_val_125Vcc, CONDIC_INDISPONIBILIZAR))

        self.l_falta_fluxo_oleo_mc = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["FALTA_FLUXO_OLEO_MC"], descricao=f"[UG{self.id}] Falta Fluxo Óleo MC")
        self.condicionadores.append(c.CondicionadorBase(self.l_falta_fluxo_oleo_mc, CONDIC_INDISPONIBILIZAR))

        self.l_UHLM_falta_flux_troc = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_FALTA_FLUX_TROC"], descricao=f"[UG{self.id}] UHLM Falta Fluxo")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHLM_falta_flux_troc, CONDIC_INDISPONIBILIZAR))

        self.l_UHLM_falta_press_troc = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_FALTA_PRESS_TROC"], descricao=f"[UG{self.id}] UHLM Falta Pressão") # TODO retornar para DEVE_INDISPONIBILZIA, descricao=R
        self.condicionadores.append(c.CondicionadorBase(self.l_UHLM_falta_press_troc, CONDIC_NORMALIZAR))

        self.l_UHRV_niv_oleo_min_pos36 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_NV_OLEO_MIN_POS36"], descricao=f"[UG{self.id}] UHRV Óleo Nível Mínimo Posição 36")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHRV_niv_oleo_min_pos36, CONDIC_INDISPONIBILIZAR))

        self.l_UHRV_nv_oleo_crit_pos35 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_NV_OLEO_CRIT_POS35"], descricao=f"[UG{self.id}] UHRV Óleo Nível Crítico Posição 35")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHRV_nv_oleo_crit_pos35, CONDIC_INDISPONIBILIZAR))

        self.l_UHLM_fluxo_mc_tras = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_FLUXO_MC_TRAS"], descricao=f"[UG{self.id}] UHLM Fluxo Traseiro MC")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHLM_fluxo_mc_tras, CONDIC_INDISPONIBILIZAR))

        self.l_UHLM_nivel_min_oleo = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_NV_MIN_OLEO"], descricao=f"[UG{self.id}] UHLM Óleo Nível Mínimo")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHLM_nivel_min_oleo, CONDIC_INDISPONIBILIZAR))

        self.l_UHLM_nivel_crit_oleo = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_NV_CRIT_OLEO"], descricao=f"[UG{self.id}] UHLM Óleo Nível Crítico")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHLM_nivel_crit_oleo, CONDIC_INDISPONIBILIZAR))

        self.l_UHLM_fluxo_mc_dianteiro = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_FLUXO_MC_DIANT"], descricao=f"[UG{self.id}] UHLM Fluxo Dianteiro")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHLM_fluxo_mc_dianteiro, CONDIC_INDISPONIBILIZAR))

        self.l_UHLM_filt_press_1_100_sujo = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_FILTR_1_PRES_SUJO_SUJO"], descricao=f"[UG{self.id}] UHLM Filtro 1 Pressão 100% Sujo")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHLM_filt_press_1_100_sujo, CONDIC_INDISPONIBILIZAR))

        self.l_UHLM_filt_press_2_100_sujo = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_FILTR_2_PRES_SUJO_SUJO"], descricao=f"[UG{self.id}] UHLM Filtro 2 Pressão 100% Sujo")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHLM_filt_press_2_100_sujo, CONDIC_INDISPONIBILIZAR))

        self.l_freio_sem_energia = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["FREIO_SEM_ENERGIA"], descricao=f"[UG{self.id}] Freio Sem Energia")
        self.condicionadores.append(c.CondicionadorBase(self.l_freio_sem_energia, CONDIC_INDISPONIBILIZAR))

        self.l_freio_filtro_saturado = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["FREIO_FILTRO_SATURADO"], descricao=f"[UG{self.id}] Freio Filtro Saturado")
        self.condicionadores.append(c.CondicionadorBase(self.l_freio_filtro_saturado, CONDIC_INDISPONIBILIZAR))

        self.l_filtro_retor_100_sujo = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["FILTRO_RET_SUJO_SUJO"], descricao=f"[UG{self.id}] UHRV Filtro Retorno 100% Sujo")
        self.condicionadores.append(c.CondicionadorBase(self.l_filtro_retor_100_sujo, CONDIC_INDISPONIBILIZAR))

        self.l_filtro_press_100_sujo = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["FILTRO_PRESS_SUJO_SUJO"], descricao=f"[UG{self.id}] UHRV Filtro Pressão 100% Sujo")
        self.condicionadores.append(c.CondicionadorBase(self.l_filtro_press_100_sujo, CONDIC_INDISPONIBILIZAR))

        self.l_bomba_mec_filtro_press_100_sujo = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["FILTR_1_PRESS_BOMBA_MEC_SUJO"], descricao=f"[UG{self.id}] UHRV Bomba Filtro Pressão 100% Sujo")
        self.condicionadores.append(c.CondicionadorBase(self.l_bomba_mec_filtro_press_100_sujo, CONDIC_INDISPONIBILIZAR))

        self.l_pas_desalinhadas = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["PAS_DESALINHADAS"], descricao=f"[UG{self.id}] Pás Desalinhadas")
        self.condicionadores.append(c.CondicionadorBase(self.l_pas_desalinhadas, CONDIC_INDISPONIBILIZAR))

        self.l_valv_borb_travada = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["VALV_BORB_TRAVADA_FECHADA"], descricao=f"[UG{self.id}] Válvula Borboleta Travada")
        self.condicionadores.append(c.CondicionadorBase(self.l_valv_borb_travada, CONDIC_INDISPONIBILIZAR))

        self.l_sobre_velo_mec_pos18 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["SOBRE_VELO_MEC_POS18"], descricao=f"[UG{self.id}] Sobre Velocidade Posição 18")
        self.condicionadores.append(c.CondicionadorBase(self.l_sobre_velo_mec_pos18, CONDIC_INDISPONIBILIZAR))

        self.l_nv_mt_alto_poco_dren = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["NV_MUITO_ALTO_POCO_DREN"], descricao=f"[UG{self.id}] Poço Drenagem Nível Alto")
        self.condicionadores.append(c.CondicionadorBase(self.l_nv_mt_alto_poco_dren, CONDIC_INDISPONIBILIZAR))

        self.l_trip_vibr_1 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRIP_VIBR_1"], descricao=f"[UG{self.id}] Vibração 1 Trip")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_vibr_1, CONDIC_INDISPONIBILIZAR))

        self.l_trip_vibr_2 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRIP_VIBR_2"], descricao=f"[UG{self.id}] Vibração 2 Trip")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_vibr_2, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_UHRV = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRIP_TEMP_UHRV"], descricao=f"[UG{self.id}] UHRV Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_UHRV, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_UHLM = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRIP_TEMP_UHLM"], descricao=f"[UG{self.id}] UHLM Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_UHLM, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_gaxeteiro = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRIP_TEMP_GAXETEIRO"], descricao=f"[UG{self.id}] Gaxeteiro Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_gaxeteiro, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_mc_guia_rad = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRIP_TEMP_MC_GUIA_RADIAL"], descricao=f"[UG{self.id}] Mancal Guia Radial Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_mc_guia_rad, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_mc_guia_esc = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRIP_TEMP_MC_GUIA_ESCORA"], descricao=f"[UG{self.id}] Mancal Guia Escora Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_mc_guia_esc, CONDIC_INDISPONIBILIZAR))

        self.l_trip_temp_mc_guia_con_esc = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRIP_TEMP_MC_GUIA_CONTRA_ESCORA"], descricao=f"[UG{self.id}] Mancal Guia Contra Escora Trip Temperatura")
        self.condicionadores.append(c.CondicionadorBase(self.l_trip_temp_mc_guia_con_esc, CONDIC_INDISPONIBILIZAR))

        self.l_falha_CLP = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["FALHA_COMUNICA_CLP"], descricao=f"[UG{self.id}] CLP Falha")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_CLP, CONDIC_INDISPONIBILIZAR))

        self.l_q_negativa = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["IHM_Q_NEGATIVA"], descricao=f"[UG{self.id}] Q Negativa")
        self.condicionadores.append(c.CondicionadorBase(self.l_q_negativa, CONDIC_INDISPONIBILIZAR))

        self.l_falha_remota = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["FALHA_COMUNICA_REMOTA"], descricao=f"[UG{self.id}] Falha Remota")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_remota, CONDIC_INDISPONIBILIZAR))

        self.l_falha_ibnt_dj_ger = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["FALHA_IBNT_DJ_GER"], descricao=f"[UG{self.id}] Dijuntor Gerador Falha")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_ibnt_dj_ger, CONDIC_INDISPONIBILIZAR))

        self.l_UHRV_falha_acion_bba_M1 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_FALHA_ACION_BOMBA_M1"], descricao=f"[UG{self.id}] UHRV Bomba 1 Falha Acionamento")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHRV_falha_acion_bba_M1, CONDIC_INDISPONIBILIZAR))

        self.l_UHRV_falha_acion_bba_M2 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_FALHA_ACION_BOMBA_M2"], descricao=f"[UG{self.id}] UHRV Bomba 2 Falha Acionamento")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHRV_falha_acion_bba_M2, CONDIC_INDISPONIBILIZAR))

        self.l_UHLM_falha_acion_bba_M1 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_FALHA_ACION_BOMBA_M1"], descricao=f"[UG{self.id}] UHLM Bomba 1 Falha Acionamento")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHLM_falha_acion_bba_M1, CONDIC_INDISPONIBILIZAR))

        self.l_UHLM_falha_acion_bba_M2 = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_FALHA_ACION_BOMBA_M2"], descricao=f"[UG{self.id}] UHLM Bomba 2 Falha Acionamento")
        self.condicionadores.append(c.CondicionadorBase(self.l_UHLM_falha_acion_bba_M2, CONDIC_INDISPONIBILIZAR))

        self.l_falha_acion_fecha_valv_borb = lei.LeituraModbusCoil(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["FALHA_ACIONA_FECHA_VALV_BORB"], descricao=f"[UG{self.id}] Válvula Borboleta Falha Acionamento Fechamento")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_acion_fecha_valv_borb, CONDIC_INDISPONIBILIZAR))

        self.l_freio_modo_remoto = lei.LeituraModbusCoil(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["FREIO_CMD_REMOTO"],
            descricao=f"[UG{self.id}] Freio Modo Remoto"
        )
        self.l_pastilha_freio_gasta = lei.LeituraModbusCoil(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["FREIO_PASTILHA_GASTA"],
            descricao=f"[UG{self.id}] Pastilha Freio Gasta"
        )
        self.l_compresor_modo_remoto = lei.LeituraModbusCoil(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"][f"QCAUG{self.id}_REMOTO"],
            descricao=f"[UG{self.id}] Compressor Modo Remoto"
        )
        self.l_uhrv_filtro_press_75_sujo = lei.LeituraModbusCoil(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["FILTRO_PRESS_SUJO_75TROC"],
            descricao=f"[UG{self}] UHRV Filtro Pressão 75% Sujo"
        )
        self.l_uhrv_filtro_retor_75_sujo = lei.LeituraModbusCoil(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["FILTRO_RET_SUJO_75TROC"],
            descricao=f"[UG{self.id}] UHRV Filtro Pressão Retorno 75% Sujo"
        )
        self.l_uhlm_filtro_press_1_75_sujo = lei.LeituraModbusCoil(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["UHLM_FILTR_1_PRES_SUJO_75TROC"],
            descricao=f"[UG{self.id}] UHLM Filtro Pressão 1 75% Sujo"
        )
        self.l_uhlm_filtro_press_2_75_sujo = lei.LeituraModbusCoil(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["UHLM_FILTR_2_PRES_SUJO_75TROC"],
            descricao=f"[UG{self.id}] UHLM Filtro Pressão 2 75% Sujo"
        )
        self.l_bomba_mec_filtro_press_75_sujo = lei.LeituraModbusCoil(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["FILTR_1_PRESS_BOMBA_MEC_75TROC"],
            descricao=f"[UG{self.id}] Filtro Pressão Bomba Mecância 75% Sujo"
        )