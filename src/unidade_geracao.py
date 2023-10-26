import pytz
import logging
import traceback

from time import sleep, time
from datetime import datetime

from src.dicionarios.const import *

from src.funcoes.leitura import *
from src.maquinas_estado.ug import *
from src.funcoes.condicionador import *

import src.ocorrencias as oco
from src.conectores.servidores import Servidores
from src.conectores.banco_dados import BancoDados

logger = logging.getLogger("logger")

class UnidadeGeracao:
    def __init__(self, id: "int", cfg=None, db: "BancoDados"=None):

        # VERIFICAÇÃO DE ARGUMENTOS

        if id <= 0:
            logger.error(f"[UG{self.id}] A Unidade não pode ser instanciada com o ID <= \"0\" ou vazio.")
            raise ValueError
        else:
            self.__id = id

        self.db = db
        self.cfg = cfg
        self.clp = Servidores.clp
        self.oco = oco.OcorrenciasUnidades(self, self.clp, self.db)


        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__potencia_ativa_kW = LeituraModbus(
            self.clp["SA"],
            REG["SA_EA_PM_810_Potencia_Ativa"],
            1,
            op=4,
            descr="[USN] Potência Usina"
        )
        self.__leitura_pressao_uhrv = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_RA_UHRV_Pressao"],
            escala=0.1,
            op=4,
            descr=f"[UG{self.id}] Leitura Pressão UHRV"
        )
        self.__leitura_rotacao = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_RA_ReferenciaCarga"],
            escala=0.1,
            op=4,
            descr=f"[UG{self.id}] Leitura Rotação"
        )

        self.__leitura_horimetro_hora = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_RA_Horimetro_Gerador"],
            op=4,
            descr=f"[UG{self.id}] Horímetro Hora"
        )
        self.__leitura_horimetro_min = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_RA_Horimetro_Gerador_min"],
            op=4,
            escala=1/60,
            descr=f"[UG{self.id}] Horímetro Min"
        )
        __C1 = LeituraModbusCoil(
            cliente=self.clp[f"UG{self.id}"],
            registrador=REG[f"UG{self.id}_ED_DisjGeradorFechado"],
            descr=f"[UG{self.id}] Sincronizada"
        )
        __C2 = LeituraModbusCoil(
            cliente=self.clp[f"UG{self.id}"],
            registrador=REG[f"UG{self.id}_RD_ParandoEmAuto"],
            descr=f"[UG{self.id}] Parando"
        )
        __C3 = LeituraModbusCoil(
            cliente=self.clp[f"UG{self.id}"],
            registrador=REG[f"UG{self.id}_ED_RV_MaquinaParada"],
            descr=f"[UG{self.id}] Parada"
        )
        __C4 = LeituraModbusCoil(
            cliente=self.clp[f"UG{self.id}"],
            registrador=REG[f"UG{self.id}_RD_PartindoEmAuto"],
            descr=f"[UG{self.id}] Sincronizando"
        )
        self.__leitura_etapa_atual = LeituraComposta(
            leitura1=__C1,
            leitura2=__C2,
            leitura3=__C3,
            leitura4=__C4,
            descr=f"[UG{self.id}] Etapa Atual",
        )

        self.__tempo_entre_tentativas: "int" = 0
        self.__limite_tentativas_de_normalizacao: "int" = 3

        self.__prioridade: "int" = 0
        self.__codigo_state: "int" = 0
        self.__ultima_etapa_atual: "int" = 0

        self.__setpoint: "int" = 0
        self.__tentativas_de_normalizacao: "int" = 0

        self.__setpoint_minimo: "int" = self.cfg["pot_minima"]
        self.__setpoint_maximo: "int" = self.cfg[f"pot_maxima_ug{self.id}"]

        self.__condicionadores_atenuadores: "list[CondicionadorBase]" = []


        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS

        self._leitura_potencia: "LeituraModbus" = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_RA_PM_710_Potencia_Ativa"],
            op=4,
            descr=f"[UG{self.id}] Leitura Potência",
        )
        self._leitura_horimetro: "LeituraSoma" = LeituraSoma(
            self.__leitura_horimetro_hora,
            self.__leitura_horimetro_min,
            descr=f"[UG{self.id}] Horímetro",
        )


        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.pot_alvo_anterior: "int" = -1
        self.ajuste_inicial_cx_esp: "int" = -1

        self.tempo_normalizar: "int" = 0
        self.tentativas_sincronismo: "int" = 0
        self.tentativas_aguardar_rotacao: "int" = 0

        self.borda_parar: "bool" = False
        self.limpeza_grade: "bool" = False
        self.atraso_rotacao: "bool" = False
        self.normalizacao_agendada: "bool" = False

        self.temporizar_rotacao: "bool" = False
        self.temporizar_partida: "bool" = False
        self.temporizar_normalizacao: "bool" = False

        self.aux_tempo_sincronizada: "datetime" = 0

        self.ts_auxiliar: "datetime" = self.get_time()

        self.condicionadores_atenuadores.append(self.oco.condic_dict[f"pressao_cx_espiral_ug{self.id}"])


    # Property -> VARIÁVEIS PRIVADAS

    @property
    def id(self) -> "int":
        # PROPRIEDADE -> Retrona o ID da Unidade.

        return self.__id

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
    def tempo_entre_tentativas(self) -> "int":
        # PROPRIEDADE -> Retorna o tempo pré-dfinido entre tentativas de normalização.

        return self.__tempo_entre_tentativas

    @property
    def limite_tentativas_de_normalizacao(self) -> "int":
        # PROPRIEDADE -> Retorna o limite pré-definido entre tentativas de normalização.

        return self.__limite_tentativas_de_normalizacao

    @property
    def leitura_potencia(self) -> "int | float":
        # PROPRIEDADE -> Retorna a leitura de potência atual da Unidade.

        return self._leitura_potencia.valor

    @property
    def leitura_horimetro(self) -> "int | float":
        # PROPRIEDADE -> Retorna a leitura de horas de geração da Unidade.

        return self._leitura_horimetro.valor

    @property
    def etapa_atual(self) -> "int":
        # PROPRIEDADE -> Retorna a etapa atual da Unidade.

        try:
            response = self.__leitura_etapa_atual.valor
            # TODO descrever os valores do CLP
            if response == 1:
                return UG_SINCRONIZADA
            elif 2 <= response <= 3:
                return UG_PARANDO
            elif 4 <= response <= 7:
                return UG_PARADA
            elif 8 <= response <= 15:
                return UG_SINCRONIZANDO
            else:
                return self.__ultima_etapa_atual

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar a leitura de Etapa Atual.")
            logger.debug(traceback.format_exc())
            return self.__ultima_etapa_atual


    # Property/Setter -> VARIÁVEIS PROTEGIDAS

    @property
    def prioridade(self) -> "int":
        # PROPRIEDADE -> Retorna a prioridade da Unidade.

        return self.__prioridade

    @prioridade.setter
    def prioridade(self, var: "int") -> "None":
        # SETTER -> Atribui o novo valor de prioridade da Unidade.

        self.__prioridade = var

    @property
    def codigo_state(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de estado da Unidade.

        return self.__codigo_state

    @codigo_state.setter
    def codigo_state(self, var: "int") -> "None":
        # SETTER -> Atribui o novo valor de estado da Unidade.

        self.__codigo_state = var

    @property
    def setpoint(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de setpoint da Unidade.

        return self.__setpoint

    @setpoint.setter
    def setpoint(self, var: "int"):
        # SETTER -> Atribui o novo valor de setpoint da Unidade.

        if self.limpeza_grade:
            self.__setpoint = self.cfg["pot_limpeza_grade"]
        elif var < self.setpoint_minimo:
            self.__setpoint = 0
        elif var > self.setpoint_maximo:
            self.__setpoint = self.setpoint_maximo
        else:
            self.__setpoint = int(var)

    @property
    def setpoint_minimo(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de setpoint mínimo da Unidade.

        return self.__setpoint_minimo

    @setpoint_minimo.setter
    def setpoint_minimo(self, var: "int"):
        # SETTER -> Atribui o novo valor de setpoint mínimo da Unidade.

        self.__setpoint_minimo = var

    @property
    def setpoint_maximo(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de setpoint máximo da Unidade.

        return self.__setpoint_maximo

    @setpoint_maximo.setter
    def setpoint_maximo(self, var: "int"):
        # SETTER -> Atribui o novo valor de setpoint máximo da Unidade.

        self.__setpoint_maximo = var

    @property
    def tentativas_de_normalizacao(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de tentativas de normalização da Unidade.

        return self.__tentativas_de_normalizacao

    @tentativas_de_normalizacao.setter
    def tentativas_de_normalizacao(self, var: "int"):
        # SETTER -> Atribui o novo valor de tentativas de normalização da Unidade.

        self.__tentativas_de_normalizacao = var

    @property
    def condicionadores_atenuadores(self) -> "list[CondicionadorBase]":
        # PROPRIEDADE -> Retorna a lista de atenuadores da Unidade.

        return self.__condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: "list[CondicionadorBase]") -> None:
        # SETTER -> Atribui a nova lista de atenuadores da Unidade.

        self.__condicionadores_atenuadores = var

    @property
    def lista_ugs(self) -> "list[UnidadeGeracao]":
        # PROPRIEDADE -> Retorna a lista com todas as instâncias de Unidades de Geração.

        return self._lista_ugs

    @lista_ugs.setter
    def lista_ugs(self, var: "list[UnidadeGeracao]") -> None:
        # SETTER -> Atribui a nova lista com todas as instâncias de Unidades de Geração.

        self._lista_ugs = var


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

        estado = self.db.get_ultimo_estado_ug(self.id)[0]

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

    def atualizar_modbus_moa(self) -> "None":
        """
        Função para atualização do estado da Unidade no CLP - MOA.
        """

        self.clp["MOA"].write_single_register(REG[f"MOA_OUT_STATE_UG{self.id}"], self.codigo_state)
        self.clp["MOA"].write_single_register(REG[f"MOA_OUT_ETAPA_UG{self.id}"], self.etapa_atual)

    def normalizar_unidade(self) -> "bool":
        """
        Função para normalização de ocorrências da Unidade de Geração.

        Primeiramente verifica se a Unidade passou do número de tentativas. Caso
        tenha passado, será chamada a função de forçar estado indisponível, senão
        aciona a função de reconhecimento e reset de alarmes da Unidade.
        """

        if self.etapa_atual == UG_PARADA:
            if self.tentativas_de_normalizacao > self.limite_tentativas_de_normalizacao:
                logger.warning(f"[UG{self.id}] A UG estourou as tentativas de normalização, indisponibilizando Unidade.")
                return False

            elif (self.ts_auxiliar - self.get_time()).seconds > self.tempo_entre_tentativas:
                self.tentativas_de_normalizacao += 1
                self.ts_auxiliar = self.get_time()
                logger.info(f"[UG{self.id}] Normalizando Unidade (Tentativa {self.tentativas_de_normalizacao}/{self.limite_tentativas_de_normalizacao})")
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
            logger.debug(f"[UG{self.id}] Step  -> Unidade:                   \"{UG_SM_STR_DCT[self.codigo_state]}\"")
            logger.debug(f"[UG{self.id}]          Etapa Atual:               \"{UG_STR_DCT_ETAPAS[self.etapa_atual]}\"")

            if self.etapa_atual == UG_SINCRONIZADA:
                logger.debug(f"[UG{self.id}]          Leituras:")
                logger.debug(f"[UG{self.id}]          - \"Potência Ativa\":        {self.leitura_potencia} kW")
                logger.debug(f"[UG{self.id}]          - \"Rotação\":               {self.__leitura_rotacao.valor:0.1f} RPM")
                logger.debug(f"[UG{self.id}]          - \"Pressão UHRV\":          {self.__leitura_pressao_uhrv.valor:0.1f} Bar")

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
            if not self.clp[f"UG{self.id}"].read_discrete_inputs(REG[f"UG{self.id}_ED_CondicaoPartida"], 1)[0]:
                logger.debug(f"[UG{self.id}]          Máquina sem condição de partida. Irá partir quando as condições forem reestabelecidas.")
                return

            elif self.clp["SA"].read_coils(REG["SA_ED_QCAP_Disj52A1Fechado"])[0] != 0:
                logger.info(f"[UG{self.id}]           O Disjuntor 52A1 está aberto. Para partir a máquina, o mesmo deverá ser fechado.")
                return

            elif not self.etapa_atual == UG_SINCRONIZADA and self.tentativas_sincronismo <= 3:
                self.tentativas_sincronismo += 1

                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARTIDA\"")

                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetRV"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleRT"], [1])
                self.remover_trip_logico()
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_IniciaPartida"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])

                logger.debug(f"[UG{self.id}]          Tentativas de Sincronismo: {self.tentativas_sincronismo}/3")

                return

            elif self.tentativas_sincronismo > 3:
                self.temporizar_partida = False
                self.tentativas_sincronismo = 0

                logger.critical(f"[UG{self.id}] A Unidade ultrapassou o limite de tentativas de Sincronismo.")
                logger.info(f"[UG{self.id}] Entrando no estado Indisponível e acionando Voip.")

                self.forcar_estado_indisponivel()

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
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_AbortaPartida"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_AbortaSincronismo"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_IniciaParada"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])
                self.enviar_setpoint(self.setpoint)
            else:
                logger.debug(f"[UG{self.id}] A unidade já está parada.")
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])

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
            self.setpoint_minimo = self.cfg["pot_minima"]
            self.setpoint_maximo = self.cfg[f"pot_maxima_ug{self.id}"]

            logger.debug(f"[UG{self.id}]          Enviando setpoint:         {int(setpoint_kw)} kW")

            if self.setpoint > 1:
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetGeral"], [1])
                response = self.clp[f"UG{self.id}"].write_single_register(REG[f"UG{self.id}_RA_ReferenciaCarga"], int(self.setpoint))
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
            self.clp["MOA"].write_single_coil(REG[f"MOA_OUT_BLOCK_UG{self.id}"], 1)

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

            self.clp["MOA"].write_single_coil(REG["PAINEL_LIDO"], 0)
            self.clp["MOA"].write_single_coil(REG[f"MOA_OUT_BLOCK_UG{self.id}"], 0)
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])

            if self.clp["SA"].read_discrete_inputs(REG["SA_ED_DisjDJ1_Fechado"])[0] != 1:
                logger.debug(f"[UG{self.id}]          Enviando comando:          \"FECHAR DJ LINHA\".")
                self.clp["SA"].write_single_coil(REG["SA_CD_Liga_DJ1"], [1])

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
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_EmergenciaViaSuper"], [1])

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
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetGeral"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetRele700G"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleBloq86H"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleBloq86M"], [1])
            self.clp["SA"].write_single_coil(REG["SA_CD_ResetRele59N"], [1])
            self.clp["SA"].write_single_coil(REG["SA_CD_ResetRele787"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_ED_ReleBloqA86HAtuado"], [0])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_ED_ReleBloqA86MAtuado"], [0])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_RD_700G_Trip"], [0])

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
            self.clp["MOA"].write_single_coil(REG["PAINEL_LIDO"], 0)

            passo = 0
            for x in range(3):
                passo += 1
                logger.debug("")
                logger.debug(f"[UG{self.id}]          Passo: {passo}/3")
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
                sleep(1)
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetGeral"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])
                sleep(1)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o comando de reconhecer e resetar alarmes.")
            logger.debug(traceback.format_exc())

    def verificar_sincronismo(self) -> "None":
        """
        Função de verificação de partida da Unidade.

        Caso a unidade seja totalmente sincronizada, o timer é encerrado e avisado,
        senão, é chamada a função de forçar estado indisponível e aciona o comando
        de emergência via supervisório.
        """

        logger.debug(f"[UG{self.id}]          Comando MOA:               \"Iniciar verificação de partida\"")
        while time() < time() + 600:
            if not self.temporizar_partida:
                logger.debug(f"[UG{self.id}]          Condição verdadeira. Saindo da verificação de sincronismo")
                return

        logger.debug(f"[UG{self.id}]          Comando MOA:               \"Acionar emergência por timeout de verificação de partida\"")
        self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_EmergenciaViaSuper"], [1])
        self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_EmergenciaViaSuper"], [0])
        self.temporizar_partida = False

    def verificar_pressao_uhrv(self) -> "None":
        """
        Função para verificação dos limites de pressão da UHRV.

        Esta função tem como objetivo evitar TRIPs em etapas específicas da Unidade.
        """

        if self.__leitura_pressao_uhrv.valor <= 130:
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleBloq86H"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_ED_ReleBloqA86HAtuado"], [0])

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
            if self.__leitura_rotacao.valor < 500 and not self.temporizar_rotacao:
                self.temporizar_rotacao = True
                Thread(target=lambda: self.aguardar_rotacao()).start()

            elif 300 <= self.__leitura_rotacao.valor <= 500 and not self.atraso_rotacao:
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleBloq86M"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_ED_ReleBloqA86MAtuado"], [0])

            elif self.atraso_rotacao and self.tentativas_aguardar_rotacao <= 3:
                self.tentativas_aguardar_rotacao += 1
                logger.debug("")
                logger.warning(f"[UG{self.id}] A rotação da Unidade está demorando para subir. (Tentativa {self.tentativas_aguardar_rotacao}/3)")
                logger.debug("")

                self.reconhece_reset_alarmes()

                self.atraso_rotacao = False

            elif self.tentativas_aguardar_rotacao == 4:
                logger.debug("")
                logger.critical(f"[UG{self.id}] A Unidade ultrapassou o limite de tentativas de aguardo pela rotação.")
                logger.info(f"[UG{self.id}] Abortando partida para realizar uma nova tentativa de Sincronismo do início.")
                logger.debug("")

                self.parar()

            return

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

        while time() <= time() + 90:
            if self.__leitura_rotacao.valor > 500:
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
                self.tentativas_de_normalizacao = 0

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        # CONTROLE TEMPO SINCRONIZADAS
        if not self.etapa_atual == UG_SINCRONIZADA:
            self.aux_tempo_sincronizada = None


    def ajuste_ganho_cx_espiral(self) -> "None":
        """
        Função para atenuação de carga através de leitura de pressão de caixa espiral.

        Calcula o ganho e verifica os limites máximo e mínimo para deteminar se
        deve atenuar ou não.
        """

        atenuacao = 0
        for condic in self.condicionadores_atenuadores:
            atenuacao = max(atenuacao, condic.valor)
            if self.etapa_atual == UG_SINCRONIZADA:
                logger.debug(f"[UG{self.id}]          Verificando Atenuadores:")
                logger.debug(f"[UG{self.id}]          - \"{condic.descr}\":   Leitura: {condic.leitura} | Atenuação: {atenuacao}")

        ganho = 1 - atenuacao
        aux = self.setpoint
        if (self.setpoint > self.setpoint_minimo) and self.setpoint * ganho > self.setpoint_minimo:
            self.setpoint = self.setpoint * ganho

        elif (self.setpoint * ganho < self.setpoint_minimo) and (self.setpoint > self.setpoint_minimo):
            self.setpoint =  self.setpoint_minimo

        if self.etapa_atual == UG_SINCRONIZADA:
            logger.debug(f"[UG{self.id}]                                     SP {aux} * GANHO {ganho} = {self.setpoint} kW")

    def ajuste_inicial_cx(self) -> "None":
        """
        Função para ajustar valores de P, I e IE da Unidade na inicialização do MOA.

        Esta função é executada apenas uma vez na inicialização do processo.
        """

        try:
            self.cx_controle_p = (self.oco.leitura_dict[f"pressao_cx_espiral_ug{self.id}"].valor - self.cfg["press_cx_alvo"]) * self.cfg["cx_kp"]
            self.cx_ajuste_ie = sum(ug.leitura_potencia for ug in self.lista_ugs) / self.cfg["pot_maxima_alvo"]
            self.cx_controle_i = self.cx_ajuste_ie - self.cx_controle_p

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar o ajuste incial do PID para pressão de caixa espiral.")
            logger.debug(traceback.format_exc())

    def controle_cx_espiral(self) -> "None":
        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = self.leitura_potencia

        if self.ajuste_inicial_cx_esp == -1:
            self.ajuste_inicial_cx()
            self.ajuste_inicial_cx_esp = 0

        try:
            self.erro_press_cx = 0
            self.erro_press_cx = self.oco.leitura_dict[f"pressao_cx_espiral_ug{self.id}"].valor - self.cfg["press_cx_alvo"]
            logger.debug("")
            logger.debug(f"[UG{self.id}] Pressão Caixa Espiral:")
            logger.debug(f"[UG{self.id}]          Alvo:                      {self.cfg['press_cx_alvo']:0.3f}")
            logger.debug(f"[UG{self.id}]          Leitura:                   {self.oco.leitura_dict[f'pressao_cx_espiral_ug{self.id}'].valor:0.3f}")

            self.cx_controle_p = self.cfg["cx_kp"] * self.erro_press_cx
            self.cx_controle_i = max(min((self.cfg["cx_ki"] * self.erro_press_cx) + self.cx_controle_i, 1), 0)
            saida_pi = self.cx_controle_p + self.cx_controle_i

            logger.debug("")
            logger.debug(f"[UG{self.id}] PID   -> P + I:                     {saida_pi:0.3f}")
            logger.debug(f"[UG{self.id}] P:                                  {self.cx_controle_p:0.3f}")
            logger.debug(f"[UG{self.id}] I:                                  {self.cx_controle_i:0.3f}")
            logger.debug(f"[UG{self.id}] ERRO:                               {self.erro_press_cx:0.3f}")

            self.cx_controle_ie = max(min(saida_pi + self.cx_ajuste_ie * self.cfg["cx_kie"], 1), 0)
            pot_alvo = max(min(round(self.cfg[f"pot_maxima_ug{self.id}"] * self.cx_controle_ie, 5), self.cfg[f"pot_maxima_ug{self.id}"],),self.cfg["pot_minima"],)

            pot_medidor = self.__potencia_ativa_kW.valor

            logger.debug(f"[UG{self.id}] Potência alvo após ajuste:          {pot_alvo:0.3f}")
            logger.debug("")

            logger.debug(f"[UG{self.id}] Step  -> Unidade:                   \"{UG_SM_STR_DCT[self.codigo_state]}\"")
            logger.debug(f"[UG{self.id}]          Etapa Atual:               \"{UG_STR_DCT_ETAPAS[self.etapa_atual]}\"")

            if self.etapa_atual == UG_SINCRONIZADA:
                logger.debug(f"[UG{self.id}]          Leituras:")
                logger.debug(f"[UG{self.id}]          - \"Potência Ativa\":        {self.leitura_potencia} kW")
                logger.debug(f"[UG{self.id}]          - \"Rotação\":               {self.__leitura_rotacao.valor:0.1f} RPM")
                logger.debug(f"[UG{self.id}]          - \"Pressão UHRV\":          {self.__leitura_pressao_uhrv.valor:0.1f} Bar")

            pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])

            pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

            if pot_medidor > self.cfg["pot_maxima_alvo"] * 0.97:
                pot_alvo = self.pot_alvo_anterior * (1 - 0.5 * ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))

            self.pot_alvo_anterior = pot_alvo

            if self.etapa_atual == UG_PARADA and pot_alvo >= 1360:
                self.partir()
                self.enviar_setpoint(pot_alvo)
            else:
                self.enviar_setpoint(pot_alvo)

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro no método de Controle por Caixa Espiral da Unidade.")
            logger.debug(traceback.format_exc())