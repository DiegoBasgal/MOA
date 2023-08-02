import pytz
import logging
import traceback

from time import sleep
from datetime import datetime

from src.dicionarios.const import *

from src.usina import *
from src.funcoes.leitura import *
from src.Condicionadores import *
from src.maquinas_estado.ug import *

from src.banco_dados import BancoDados
from src.conector import ClientesUsina
from src.ocorrencias import OcorrenciasUg

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
        self.clp = ClientesUsina.clp
        self.oco = OcorrenciasUg(self, self.clp, self.db)


        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__potencia_ativa_kW = LeituraModbus(
            "[USN] Potência Usina",
            self.clp["SA"],
            1,
            op=4
        )
        self.__leitura_horimetro_hora = LeituraModbus(
            f"[UG{self.id}] Horímetro Hora",
            self.clp[f"UG{self.id}"],
            op=4,
        )
        self.__leitura_horimetro_min = LeituraModbus(
            f"[UG{self.id}] Horímetro Min",
            self.clp[f"UG{self.id}"],
            op=4,
            escala=1/60
        )

        self.__leitura_etapa_atual = LeituraComposta(
            f"ug{self.id}_Operacao_EtapaAtual",
        )

        self.__tempo_entre_tentativas: "int" = 0
        self.__limite_tentativas_de_normalizacao: "int" = 2

        self.__codigo_state: "int" = 0
        self.__ultima_etapa_atual: "int" = 0

        self.__setpoint: "int" = 0
        self.__setpoint_minimo: "int" = 0
        self.__setpoint_maximo: "int" = 0
        self.__tentativas_de_normalizacao: "int" = 0

        self.__condicionadores_atenuadores: "list[CondicionadorBase]" = []


        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS

        self._leitura_potencia: "LeituraModbus" = LeituraModbus(
            f"UG{self.id}_Potência",
            self.clp[f"UG{self.id}"],
            op=4,
        )
        self._leitura_horimetro: "LeituraSoma" = LeituraSoma(
            f"UG{self.id}_Horímetro",
            self.__leitura_horimetro_hora,
            self.__leitura_horimetro_min
        )


        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.pot_alvo_anterior: "int" = -1
        self.ajuste_inicial_cx_esp: "int" = -1

        self.tempo_normalizar: "int" = 0
        self.tentativas_sincronismo: "int" = 0
        self.tentativas_aguardar_rotacao: "int" = 0

        self.setpoint_minimo: "int" = self.cfg["pot_minima"]
        self.setpoint_maximo: "int" = self.cfg[f"pot_maxima_ug{self.id}"]

        self.borda_parar: "bool" = False
        self.normalizacao_agendada: "bool" = False

        self.temporizar_partida: "bool" = False

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
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar a leitura de Etapa Atual.")
            logger.debug(traceback.format_exc())
            return self.__ultima_etapa_atual


    # Property/Setter -> VARIÁVEIS PROTEGIDAS

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

        if var < self.setpoint_minimo:
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

        if self.tentativas_de_normalizacao > self.limite_tentativas_de_normalizacao:
            logger.warning(f"[UG{self.id}] A UG estourou as tentativas de normalização, indisponibilizando Unidade.")
            return False

        elif (self.ts_auxiliar - self.get_time()).seconds > self.tempo_entre_tentativas:
            self.tentativas_de_normalizacao += 1
            self.ts_auxiliar = self.get_time()
            logger.info(f"[UG{self.id}] Normalizando Unidade (Tentativa {self.tentativas_de_normalizacao}/{self.limite_tentativas_de_normalizacao})")
            self.reconhece_reset_alarmes()
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

        elif not self.borda_parar and self.parar():
            self.borda_parar = True

    def step(self) -> "None":
        """
        Função principal de passo da Unidade.

        Serve como principal chamada para controle das Unidades da máquina de estados.
        """

        try:
            logger.debug("")
            logger.debug(f"[UG{self.id}] Step  -> Unidade:                   \"{UG_SM_STR_DCT[self.codigo_state]}\"")
            logger.debug(f"[UG{self.id}]          Etapa atual:               \"{UG_STR_DCT_ETAPAS[self.etapa_atual]}\"")

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
            if not self.etapa_atual == UG_SINCRONIZADA and self.tentativas_sincronismo <= 3:
                self.tentativas_sincronismo += 1

                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARTIDA\"")
                logger.info(f"[UG{self.id}]          Tentativas de Sincronismo:  {self.tentativas_sincronismo}/3")

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

                self.enviar_setpoint(self.setpoint)
            else:
                logger.debug(f"[UG{self.id}] A unidade já está parada.")

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

                return 

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
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP ELÉTRICO\"")
            self.clp["MOA"].write_single_coil(REG[f"MOA_OUT_BLOCK_UG{self.id}"], [1])

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

            self.clp["MOA"].write_single_coil(REG["PAINEL_LIDO"], [0])
            self.clp["MOA"].write_single_coil(REG[f"MOA_OUT_BLOCK_UG{self.id}"], [0])
    
            if self.clp["SA"].read_coils(REG[""])[0] == 1:
                logger.debug(f"[UG{self.id}]          Enviando comando:          \"FECHAR DJ LINHA\".")
                self.clp["SA"].write_single_coil(REG[""], [0])

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())

    def acionar_trip_logico(self) -> "None":
        """
        Função para acionamento de TRIP lógico.

        Aciona o comando de emergência via superviório.
        """

        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP LÓGICO\"")

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel acionar o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())

    def remover_trip_logico(self) -> "None":
        """
        Função para remoção de TRIP lógico.

        Aciona os comandos de reset geral, relés e reconhece.
        """

        try:
            logger.debug(f"[UG{self.id}]          Removendo comando:         \"TRIP LÓGICO\"")

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
            self.clp["MOA"].write_single_coil(REG["PAINEL_LIDO"], [0])

            passo = 0
            for x in range(3):
                passo += 1
                logger.debug("")
                logger.debug(f"[UG{self.id}]          Passo: {passo}/3")
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
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

        self.temporizar_partida = False

    def aguardar_normalizacao(self, delay: "int") -> "None":
        """
        Função de temporizador para espera de normalização da Unidade restrita,
        por tempo pré-definido por agendamento na Interface.
        """

        if not self.temporizar_normalizacao:
            sleep(max(0, time() + delay - time()))
            self.temporizar_normalizacao = True
            return

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
            logger.debug(f"[UG{self.id}]          Verificando Atenuadores:")
            logger.debug(f"[UG{self.id}]          - \"{condic.descr}\":   Leitura: {condic.leitura.valor} | Atenuação: {atenuacao}")

        ganho = 1 - atenuacao
        aux = self.setpoint
        if (self.setpoint > self.setpoint_minimo) and self.setpoint * ganho > self.setpoint_minimo:
            self.setpoint = self.setpoint * ganho

        elif (self.setpoint * ganho < self.setpoint_minimo) and (self.setpoint > self.setpoint_minimo):
            self.setpoint =  self.setpoint_minimo

        logger.debug(f"[UG{self.id}]                                     SP {aux} * GANHO {ganho} = {self.setpoint} kW")

    def ajuste_inicial_cx(self) -> "None":
        """
        Função para ajustar valores de P, I e IE da Unidade na inicialização do MOA.

        Esta função é executada apenas uma vez na inicialização do processo.
        """

        try:
            self.cx_controle_p = (self.oco.leitura_dict[f"pressao_cx_espiral_ug{self.id}"].valor - self.cfg["press_cx_alvo"]) * self.cfg["cx_kp"]
            self.cx_ajuste_ie = self.leitura_potencia / self.cfg["pot_maxima_alvo"]
            self.cx_controle_i = self.cx_ajuste_ie - self.cx_controle_p

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar o ajuste incial do PID para pressão de caixa espiral.")
            logger.debug(traceback.format_exc())

    def controle_cx_espiral(self) -> "None":
        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = pot_alvo

        if self.ajuste_inicial_cx_esp == -1:
            self.ajuste_inicial_cx()
            self.ajuste_inicial_cx_esp = 0

        try:
            self.erro_press_cx = 0
            self.erro_press_cx = self.oco.leitura_dict[f"pressao_cx_espiral_ug{self.id}"].valor - self.cfg["press_cx_alvo"]

            logger.debug(f"[UG{self.id}] Pressão Alvo: {self.cfg['press_cx_alvo']:0.3f}, Recente: {self.oco.leitura_dict[f'pressao_cx_espiral_ug{self.id}'].valor:0.3f}")

            self.cx_controle_p = self.cfg["cx_kp"] * self.erro_press_cx
            self.cx_controle_i = max(min((self.cfg["cx_ki"] * self.erro_press_cx) + self.cx_controle_i, 1), 0)
            saida_pi = self.cx_controle_p + self.cx_controle_i

            logger.debug(f"[UG{self.id}] PI: {saida_pi:0.3f} <-- P:{self.cx_controle_p:0.3f} + I:{self.cx_controle_i:0.3f}; ERRO={self.erro_press_cx}")

            self.cx_controle_ie = max(min(saida_pi + self.cx_ajuste_ie * self.cfg["cx_kie"], 1), 0)
            pot_alvo = max(min(round(self.cfg[f"pot_maxima_ug{self.id}"] * self.cx_controle_ie, 5), self.cfg[f"pot_maxima_ug{self.id}"],),self.cfg["pot_minima"],)

            logger.debug(f"[UG{self.id}] Pot alvo: {pot_alvo:0.3f}")

            pot_medidor = self.__potencia_ativa_kW.valor

            logger.debug(f"Potência alvo = {pot_alvo}")
            logger.debug(f"Potência no medidor = {pot_medidor}")

            pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])

            pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

            if pot_medidor > self.cfg["pot_maxima_alvo"] * 0.97:
                pot_alvo = self.pot_alvo_anterior * (1 - 0.5 * ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))

            self.pot_alvo_anterior = pot_alvo
            self.enviar_setpoint(pot_alvo) if self.oco.leitura_dict[f"pressao_cx_espiral_ug{self.id}"].valor >= 15.5 else self.enviar_setpoint(0)

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro no método de Controle por Caixa Espiral da Unidade.")
            logger.debug(traceback.format_exc())