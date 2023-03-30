__version__ = "0.2"
__authors__ = "Lucas Lavratti", " Henrique Pfeifer"
__credits__ = ["Diego Basgal" , ...]
__description__ = "Este módulo corresponde a implementação das Unidades de Geração."

from Usina import *
from maquinas_estado.ug_sm import *

logger = logging.getLogger("__main__")

class UnidadeGeracao(Usina):
    def __init__(self, id: int | None = ...) -> ...:
        # VERIFICAÇÃO DE ARGUMENTOS
        if not id or id < 1:
            raise ValueError(f"[UG{self.id}] A Unidade deve ser instanciada com um valor maior que \"0\".")
        else:
            self.__id: int = id


        # ATRIBUIÇÃO DE VAIRÁVEIS
        # Privadas
        self.__tempo_entre_tentativas: int = 0
        self.__limite_tentativas_de_normalizacao: int = 3

        self.__etapa_atual: LeituraModbus = LeituraModbus(self.clp, MB["UG"][f"UG{self.id}_RV_ESTADO_OPERACAO"])

        self.__leitura_potencia: LeituraOpc = LeituraOpc(OPC_UA["UG"][f"UG{self.id}_UG_P"])
        self.__leitura_horimetro: LeituraOpc = LeituraOpc(OPC_UA["UG"][f"UG{self.id}_UG_HORIMETRO"])
        self.__leitura_dj52l: LeituraOpcBit = LeituraOpcBit(OPC_UA["SE"]["CMD_SE_FECHA_52L"], 4, True)

        self.__next_state: State = StateDisponivel(self)

        # Protegidas
        self._codigo_state: int = 0

        self._prioridade: int = 0

        self._etapa_atual: int = 0
        self._ultima_etapa_atual: int = 0

        self._setpoint: int = 0

        self._tentativas_de_normalizacao: int = 0

        self._condicionadores: list[CondicionadorBase] = []
        self._condicionadores_essenciais: list[CondicionadorBase] = []
        self._condicionadores_atenuadores: list[CondicionadorExponencialReverso] = []

        # Públicas
        self.tempo_normalizar: int = 0

        self.parar_timer: bool = False
        self.timer_press: bool = False
        self.limpeza_grade: bool = False
        self.norma_agendada: bool = False
        self.aux_tempo_sincronizada: bool = None
        self.deve_ler_condicionadores: bool = False

        self.ts_auxiliar: datetime = self.get_time()


        # FINALIZAÇÃO DO __INIT__
        self.iniciar_leituras_condicionadores()


    @property
    def id(self) -> int:
        return self.__id

    @property
    def leitura_potencia(self) -> float:
        return self.__leitura_potencia.valor

    @property
    def leitura_horimetro(self) -> float:
        return self.__leitura_horimetro.valor

    @property
    def leitura_dj52l(self) -> int:
        return self.__leitura_dj52l.valor

    @property
    def disponivel(self) -> bool:
        return isinstance(self.__next_state, StateDisponivel)

    @property
    def manual(self) -> bool:
        return isinstance(self.__next_state, StateManual)

    @property
    def tempo_entre_tentativas(self) -> int:
        return self.__tempo_entre_tentativas

    @property
    def limite_tentativas_de_normalizacao(self) -> int:
        return self.__limite_tentativas_de_normalizacao

    @property
    def etapa_atual(self) -> int:
        try:
            if response := self.__etapa_atual > 0:
                self._ultima_etapa_atual = response
                return response
            else:
                return self._ultima_etapa_atual
        except Exception as e:
            logger.exception(f"[USN] Houve um erro na leitura de etapa atual da UG. Exception: \"{repr(e)}\"")
            logger.exception(f"[USN] Traceback: {traceback.print_stack}")
            return 99


    @property
    def setpoint(self) -> int:
        return self._setpoint

    @setpoint.setter
    def setpoint(self, var: int):
        if var < self.cfg["pot_minima"]:
            self._setpoint = 0
        elif var > self.cfg[f"pot_maxima_ug{self.id}"]:
            self._setpoint = self.cfg[f"pot_maxima_ug{self.id}"]
        else:
            self._setpoint = int(var)
        logger.debug(f"[UG{self.id}] SP<-{var}")

    @property
    def prioridade(self) -> int:
        return self._prioridade

    @prioridade.setter
    def prioridade(self, var) -> None:
        self._prioridade = var

    @property
    def codigo_state(self) -> int:
        return self._codigo_state

    @codigo_state.setter
    def codigo_state(self, var) -> None:
        self._codigo_state = var

    @property
    def lista_ugs(self) -> list[UnidadeGeracao]:
        return self._lista_ugs

    @lista_ugs.setter
    def lista_ugs(self, var: list[UnidadeGeracao]) -> None:
        self._lista_ugs = var

    @property
    def condicionadores(self) -> list[CondicionadorBase]:
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: list[CondicionadorBase]):
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> list[CondicionadorBase]:
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: list[CondicionadorBase]):
        self._condicionadores_essenciais = var

    @property
    def condicionadores_atenuadores(self) -> list[CondicionadorBase]:
        return self._condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: list[CondicionadorBase]):
        self._condicionadores_atenuadores = var

    @property
    def tentativas_de_normalizacao(self) -> int:
        return self._tentativas_de_normalizacao

    @tentativas_de_normalizacao.setter
    def tentativas_de_normalizacao(self, var: int):
        if 0 <= var and var == int(var) and self.tentativas_de_normalizacao <= self.limite_tentativas_de_normalizacao:
            self.tentativas_de_normalizacao = int(var)
        if self.tentativas_de_normalizacao == self.limite_tentativas_de_normalizacao:
            logger.debug(f"[UG{self.id}] Última tentativa de normalização...")


    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def acionar_trips(self) -> None:
        self.acionar_trip_eletrico()
        self.acionar_trip_logico()

    def forcar_estado_manual(self) -> None:
        try:
            self.__next_state = StateManual(self)

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel forçar o estado manual. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")

    def forcar_estado_restrito(self) -> None:
        try:
            self.__next_state = StateRestrito(self)

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel forçar o estado restrito. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")

    def forcar_estado_indisponivel(self) -> None:
        try:
            self.__next_state = StateIndisponivel(self)

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel forçar o estado indisponível. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")

    def forcar_estado_disponivel(self) -> None:
        try:
            self.reconhece_reset_alarmes()
            self.__next_state = StateDisponivel(self)

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel forçar o estado disponível. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")

    def step(self) -> None:
        try:
            logger.debug(f"[UG{self.id}] Step -> (Tentativas de normalização: {self.tentativas_de_normalizacao}/{self.limite_tentativas_de_normalizacao}).")
            self.__next_state = self.__next_state.step()
            self.atualizar_modbus_moa()

        except Exception as e:
            logger.exception(f"[UG{self.id}] Erro na execução da máquina de estados -> step. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")

    def atualizar_modbus_moa(self) -> None:
        try:
            self.clp_moa.write_single_coil(MB["MOA"][f"OUT_ETAPA_UG{self.id}"], [self.etapa_atual])
            self.clp_moa.write_single_coil(MB["MOA"][f"OUT_STATE_UG{self.id}"], [self.codigo_state])

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível escrever os valores no CLP MOA. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")

    def partir(self) -> bool:
        try:
            if self.etapa_atual == UG_PARADA:
                logger.info(f"[UG{self.id}] Enviando comando de partida.")
                res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_RESET_FALHAS_PASSOS"], valor=1, bit=0)
                res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86M"], valor=1, bit=1)
                res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86E"], valor=1, bit=2)
                res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86H"], valor=1, bit=3)
                res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_UHRV_REARME_FALHAS"], valor=1, bit=0)
                res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_UHLM_REARME_FALHAS"], valor=1, bit=16)
                res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_PARTIDA_CMD_SINCRONISMO"], valor=1, bit=10)
                self.enviar_setpoint(self.setpoint)
            else:
                logger.debug(f"[UG{self.id}] A Unidade já está sincronizada.")
            return res

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível partir a Unidade. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def parar(self) -> bool:
        try:
            if self.etapa_atual == (UG_SINCRONIZADA or UG_SINCRONIZANDO):
                logger.info(f"[UG{self.id}] Enviando comando de parada.")
                self.enviar_setpoint(0)
                return self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_PARADA_CMD_DESABILITA_UHLM"], valor=1, bit=15)
            else:
                logger.debug(f"[UG{self.id}] A Unidade já está parada.")

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível parar a Unidade. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def enviar_setpoint(self, setpoint_kw: int) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Enviando setpoint {int(self.setpoint)} kW.")
            if setpoint_kw > 1:
                self.setpoint = int(setpoint_kw)
                res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_RESET_FALHAS_PASSOS"], valor=1, bit=0)
                res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86M"], valor=1, bit=1)
                res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86E"], valor=1, bit=2)
                res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86H"], valor=1, bit=3)
                res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_UHRV_REARME_FALHAS"], valor=1, bit=0)
                res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_UHLM_REARME_FALHAS"], valor=1, bit=16)
                res = self.clp.write_single_register(MB["UG"][f"UG{self.id}_RV_SETPOINT_POTENCIA_ATIVA_PU"], self.setpoint)
                return res

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel enviar o setpoint para a Unidade. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def reconhece_reset_alarmes(self) -> bool:
        try:
            logger.info(f"[UG{self.id}] Enviando comando de reconhecer e resetar alarmes.")
            for x in range(3):
                logger.debug(f"[UG{self.id}] Passo: {x}/3")
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
                sleep(1)
                self.clp_moa.write_single_coil(MB["MOA"]["PAINEL_LIDO"], [0])
                sleep(1)
            return True

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel enviar o comando de reconhecer e resetar alarmes. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def acionar_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Acionando TRIP -> Lógico.")
            return self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_PARADA_EMERGENCIA"], 4, 1)

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel acionar o TRIP lógico. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def remover_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Removendo TRIP -> Lógico.")
            res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_RESET_FALHAS_PASSOS"], valor=1, bit=0)
            res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86M"], valor=1, bit=1)
            res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86E"], valor=1, bit=2)
            res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86H"], valor=1, bit=3)
            res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_UHRV_REARME_FALHAS"], valor=1, bit=0)
            res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_UHLM_REARME_FALHAS"], valor=1, bit=16)
            res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_BLOQUEIO_86H_ATUADO"], valor=0, bit=31)
            res = self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_RELE_700G_TRIP_ATUADO"], valor=0, bit=31)
            return res

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível remover o TRIP lógico. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def acionar_trip_eletrico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Acionando TRIP -> Elétrico.")
            return self.clp_moa.write_single_coil(MB["MOA"][f"OUT_BLOCK_UG{self.id}"], [1])

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível acionar o TRIP elétrico. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def remover_trip_eletrico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Removendo TRIP -> Elétrico.")
            self.clp_moa.write_single_coil(MB["MOA"][f"OUT_BLOCK_UG{self.id}"], [0])
            self.clp_moa.write_single_coil(MB["MOA"]["PAINEL_LIDO"], [0])

            if not self.leitura_dj52l:
                logger.debug(f"[UG{self.id}] Comando recebido - Fechando Dj52L")
                return self.escrita_opc.escrever_bit(OPC_UA["SE"]["CMD_SE_FECHA_52L"], valor=1, bit=4)

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível remover o TRIP elétrico. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def resetar_emergencia(self) -> bool:
        try:
            res = self.escrita_opc.escrever_bit(OPC_UA["UG"][f"UG{self.id}_CMD_RESET_FALHAS_PASSOS"], valor=1, bit=0)
            res = self.escrita_opc.escrever_bit(OPC_UA["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86M"], valor=1, bit=1)
            res = self.escrita_opc.escrever_bit(OPC_UA["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86E"], valor=1, bit=2)
            res = self.escrita_opc.escrever_bit(OPC_UA["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86H"], valor=1, bit=3)
            res = self.escrita_opc.escrever_bit(OPC_UA["UG"][f"UG{self.id}_CMD_UHRV_REARME_FALHAS"], valor=1, bit=0)
            res = self.escrita_opc.escrever_bit(OPC_UA["UG"][f"UG{self.id}_CMD_UHLM_REARME_FALHAS"], valor=1, bit=16)
            return res

        except Exception as e:
            logger.exception(f"[UG{self.id}] Houve um erro ao realizar o reset geral. Exception: \"{repr(e)}\"")
            logger.exception(f"[SE{self.id}] Traceback: {traceback.print_stack}")
            return False

    def verificar_partindo(self) -> None:
        logger.debug(f"[UG{self.id}] Iniciando o timer de verificação de partida")
        while time() < (time() + 600):
            if self.etapa_atual == UG_SINCRONIZADA or self.parar_timer:
                logger.debug(f"[UG{self.id}] {'Modo manual ativado' if self.parar_timer else 'Unidade Sincronizada'}. Verificação de partida encerrada.")
                return

        logger.debug(f"[UG{self.id}] A Unidade estourou o timer de verificação de partida, adicionando condição para normalizar")
        self.escrita_opc.escrever_bit(self.opc, OPC_UA["UG"][f"UG{self.id}_CMD_PARADA_EMERGENCIA"], 4, 1)
        self.borda_partindo = False
        self.parar_timer = True

    def atualizar_limites_condicionadores(self, parametros) -> None:
        try:
            self.prioridade = int(parametros[f"ug{self.id}_prioridade"])
            self.condicionador_temperatura_fase_r_ug.valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{self.id}"])
            self.condicionador_temperatura_fase_r_ug.valor_limite = float(parametros[f"flimite_temperatura_fase_r_ug{self.id}"])
            self.condicionador_temperatura_fase_s_ug.valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{self.id}"])
            self.condicionador_temperatura_fase_s_ug.valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{self.id}"])
            self.condicionador_temperatura_fase_t_ug.valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{self.id}"])
            self.condicionador_temperatura_fase_t_ug.valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{self.id}"])
            self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_1_ug{self.id}"])
            self.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_1_ug{self.id}"])
            self.condicionador_temperatura_mancal_guia_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_ug{self.id}"])
            self.condicionador_temperatura_mancal_guia_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_ug{self.id}"])
            self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_interno_1_ug{self.id}"])
            self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_interno_1_ug{self.id}"])
            self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_guia_interno_2_ug{self.id}"])
            self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_guia_interno_2_ug{self.id}"])
            self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base = float(parametros[f"alerta_temperatura_patins_mancal_comb_1_ug{self.id}"])
            self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_limite = float(parametros[f"limite_temperatura_patins_mancal_comb_1_ug{self.id}"])
            self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base = float(parametros[f"alerta_temperatura_patins_mancal_comb_2_ug{self.id}"])
            self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_limite = float(parametros[f"limite_temperatura_patins_mancal_comb_2_ug{self.id}"])
            self.condicionador_temperatura_mancal_casq_comb_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_casq_comb_ug{self.id}"])
            self.condicionador_temperatura_mancal_casq_comb_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_casq_comb_ug{self.id}"])
            self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_contra_esc_comb_ug{self.id}"])
            self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_contra_esc_comb_ug{self.id}"])
            self.condicionador_pressao_turbina_ug.valor_base = float(parametros[f"alerta_pressao_turbina_ug{self.id}"])
            self.condicionador_pressao_turbina_ug.valor_limite = float(parametros[f"limite_pressao_turbina_ug{self.id}"])

        except Exception as e:
            logger.exception(f"[UG{self.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")

    def controle_limites_operacao(self) -> None:
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
            logger.warning(f"[UG{self.id}] A temperatura dos Patins do Mancal Combinado 1 da UG passou do valor base! ({self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base}C) | Leitura: {self.leitura_temperatura_patins_mancal_comb_1.valor}C")
        if self.leitura_temperatura_patins_mancal_comb_1.valor >= 0.9*(self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_limite - self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base) + self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura dos Patins do Mancal Combinado 1 da UG está muito próxima do limite! ({self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_patins_mancal_comb_1.valor}C")

        if self.leitura_temperatura_patins_mancal_comb_2.valor >= self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura dos Patins do Mancal Combinado 2 da UG passou do valor base! ({self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base}C) | Leitura: {self.leitura_temperatura_patins_mancal_comb_2.valor}C")
        if self.leitura_temperatura_patins_mancal_comb_2.valor >= 0.9*(self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_limite - self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base) + self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura dos Patins do Mancal Combinado 2 da UG está muito próxima do limite! ({self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_patins_mancal_comb_2.valor}C")

        if self.leitura_temperatura_mancal_casq_comb.valor >= self.condicionador_temperatura_mancal_casq_comb_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Casquilho Combinado da UG passou do valor base! ({self.condicionador_temperatura_mancal_casq_comb_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mancal_casq_comb.valor}C")
        if self.leitura_temperatura_mancal_casq_comb.valor >= 0.9*(self.condicionador_temperatura_mancal_casq_comb_ug.valor_limite - self.condicionador_temperatura_mancal_casq_comb_ug.valor_base) + self.condicionador_temperatura_mancal_casq_comb_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Casquilho Combinado da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_casq_comb_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mancal_casq_comb.valor}C")

        if self.leitura_temperatura_mancal_contra_esc_comb.valor >= self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Contra Escora Combinado da UG passou do valor base! ({self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base}C) | Leitura: {self.leitura_temperatura_mancal_contra_esc_comb.valor}C")
        if self.leitura_temperatura_mancal_contra_esc_comb.valor >= 0.9*(self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_limite - self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base) + self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Contra Escora Combinado da UG está muito próxima do limite! ({self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_limite}C) | Leitura: {self.leitura_temperatura_mancal_contra_esc_comb.valor}C")

        if self.leitura_pressao_turbina.valor <= self.condicionador_pressao_turbina_ug.valor_base and self.leitura_pressao_turbina.valor != 0 and self.etapa_atual == UG_SINCRONIZADA:
            logger.warning(f"[UG{self.id}] A pressão na entrada da turbina da UG passou do valor base! ({self.condicionador_pressao_turbina_ug.valor_base:03.2f} KGf/m2) | Leitura: {self.leitura_pressao_turbina.valor:03.2f}")
        if self.leitura_pressao_turbina.valor <= self.condicionador_pressao_turbina_ug.valor_limite+0.9*(self.condicionador_pressao_turbina_ug.valor_base - self.condicionador_pressao_turbina_ug.valor_limite) and self.leitura_pressao_turbina.valor != 0 and self.etapa_atual == UG_SINCRONIZADA:
            logger.critical(f"[UG{self.id}] A pressão na entrada da turbina da UG está muito próxima do limite! ({self.condicionador_pressao_turbina_ug.valor_limite:03.2f} KGf/m2) | Leitura: {self.leitura_pressao_turbina.valor:03.2f} KGf/m2")

    # TODO Organizar ordem de leituras e condicionadores
    def leitura_periodica(self) -> None:
        # Telegram
        if self.leitura_saidas_digitais_rv_b0:
            logger.warning(f"[UG{self.id}] O alarme do Regulador de Velocidade da UG foi acionado. Favor verificar.")

        if self.leitura_saidas_digitais_rt_b0:
            logger.warning(f"[UG{self.id}] O alarme do Regulador de Tensão da UG foi acionado. Favor verificar.")

        if self.leitura_falha_3_rt_b0:
            logger.warning(f"[UG{self.id}] Houve uma falha na leitura de potência reativa pelo Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b1:
            logger.warning(f"[UG{self.id}] Houve uma falha na leitura da tensão terminal pelo Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b2:
            logger.warning(f"[UG{self.id}] Houve uma falha na leitura principal da corrente de excitação pelo Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b3:
            logger.warning(f"[UG{self.id}] Houve uma falha na leitura retaguarda da corrente de excitação pelo Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b4:
            logger.warning(f"[UG{self.id}] Foi identificado ruído na instrumentação de reativo do Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b5:
            logger.warning(f"[UG{self.id}] Foi identificado ruído na instrumentação de tensão do Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b6:
            logger.warning(f"[UG{self.id}] Foi identificado ruído na instrumentação de excitação principal do Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_3_rt_b7:
            logger.warning(f"[UG{self.id}] Foi identificado ruído na instrumentação de excitação retaguarda do Regulador de Tensão da UG. Favor Verificar.")

        if self.leitura_falha_1_rv_b4:
            logger.warning(f"[UG{self.id}] Houve uma falha de leitura de posição do distribuidor pelo Regulador de Velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b5:
            logger.warning(f"[UG{self.id}] Houve uma falha de leitura de posição do rotor pelo Regulador de Velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b6:
            logger.warning(f"[UG{self.id}] Houve uma falha de leitura de potência ativa pelo Regulador de Velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b7:
            logger.warning(f"[UG{self.id}] Houve uma falha de leitura de referência de potência pelo Regulador de Velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b8:
            logger.warning(f"[UG{self.id}] Houve uma falha de leitura de nível montante pelo Regulador de Velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b13:
            logger.warning(f"[UG{self.id}] Foi identificado ruído na medição principal de velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b14:
            logger.warning(f"[UG{self.id}] Foi identificado ruído na medição retaguarda de velocidade da UG. Favor verificar.")

        if self.leitura_falha_1_rv_b15:
            logger.warning(f"[UG{self.id}] Foi identificada perda na medição principal de velocidade da UG. Favor verificar.")

        if self.leitura_falha_2_rv_b0:
            logger.warning(f"[UG{self.id}] Foi identificada perda na medição retaguarda de velocidade da UG. Favor verificar.")

        if self.leitura_falha_2_rv_b4:
            logger.warning(f"[UG{self.id}] Foi identificada diferença entre medidor principal e retaguarda da UG. Favor verificar.")

        if self.leitura_unidade_manutencao_uhrv:
            logger.warning(f"[UG{self.id}] UHRV da UG entrou em modo de manutenção")

        if self.leitura_unidade_manutencao_uhlm:
            logger.warning(f"[UG{self.id}] UHLM da UG entrou em modo de manutenção")

        if not self.leitura_filtro_limpo_uhrv:
            logger.warning(f"[UG{self.id}] O filtro da UHRV da UG está sujo. Favor realizar limpeza/troca.")

        if not self.leitura_filtro_limpo_uhrv:
            logger.warning(f"[UG{self.id}] O filtro da UHLM da UG está sujo. Favor realizar limpeza/troca.")

        if not self.leitura_porta_interna_fechada_cpg:
            logger.warning(f"[UG{self.id}] A porta interna do CPG da UG está aberta. Favor fechar.")

        if not self.leitura_porta_traseira_fechada_cpg:
            logger.warning(f"[UG{self.id}] A porta traseira do CPG da UG está aberta. Favor fechar.")

        if not self.leitura_resistencia_sem_falha:
            logger.warning(f"[UG{self.id}] Houve uma falha na resistência da UG. Favor verificar.")

        if self.leitura_escovas_gastas_polo_positivo:
            logger.warning(f"[UG{self.id}] Foi identificado que as escovas do polo positivo da UG estão gastas. Favor verificar.")

        if self.leitura_escovas_gastas_polo_negativo:
            logger.warning(f"[UG{self.id}] Foi identificado que as escovas do polo negativo da UG estão gastas. Favor verificar.")

        if self.leitura_alarme_temp_ponte_fase_a:
            logger.warning(f"[UG{self.id}] O alarme de temperatura da pote fase A foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_ponte_fase_b:
            logger.warning(f"[UG{self.id}] O alarme de temperatura da pote fase B foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_ponte_fase_c:
            logger.warning(f"[UG{self.id}] O alarme de temperatura da pote fase C foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_trafo_excitacao:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do transformador excitação foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_mancal_guia:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do mancal guia foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_oleo_uhrv:
            logger.warning(f"[UG{self.id}] O alarme de temperatura de óleo da UHRV foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_oleo_uhlm:
            logger.warning(f"[UG{self.id}] O alarme de temperatura de óleo da UHLM foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_mancal_casq_comb:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do mancal casquilho combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_mancal_con_esc_comb:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do mancal contra escora combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_patins_1_mancal_comb:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do patins 1 mancal combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_patins_2_mancal_comb:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do patins 2 mancal combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_mancal_guia_interno_1:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do mancal guia interno 1 foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_mancal_guia_interno_2:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do mancal guia interno 2 foi acionado. Favor verificar.")

        if self.leitura_alarme_temp_nucleo_estatorico_gerador:
            logger.warning(f"[UG{self.id}] O alarme de temperatura do núcleo estatórico do gerador foi acionado. Favor verificar.")

        if self.leitura_temp_fase_a_gerador:
            logger.warning(f"[UG{self.id}] O alarme de temperatura de fase A do gerador foi acionado. Favor verificar.")

        if self.leitura_temp_fase_b_gerador:
            logger.warning(f"[UG{self.id}] O alarme de temperatura de fase B do gerador foi acionado. Favor verificar.")

        if self.leitura_temp_fase_c_gerador:
            logger.warning(f"[UG{self.id}] O alarme de temperatura de fase C do gerador foi acionado. Favor verificar.")

        if self.leitura_alarme_vibra_eixo_x_mancal_comb:
            logger.warning(f"[UG{self.id}] O alarme de vibração do eixo X do mancal combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_vibra_eixo_y_mancal_comb:
            logger.warning(f"[UG{self.id}] O alarme de vibração do eixo Y do mancal combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_vibra_eixo_z_mancal_comb:
            logger.warning(f"[UG{self.id}] O alarme de vibração do eixo Z do mancal combinado foi acionado. Favor verificar.")

        if self.leitura_alarme_vibra_detec_horizontal:
            logger.warning(f"[UG{self.id}] O alarme de vibração detecção horizontal foi acionado. Favor verificar.")

        if self.leitura_alarme_vibra_detec_vertical:
            logger.warning(f"[UG{self.id}] O alarme de vibração detecção vertical foi acionado. Favor verificar.")

    def iniciar_leituras_condicionadores(self) -> None:
        # LEITURAS PARA LEITURA PERIODICA
        # Telegram
            # Bit Invertido
        self.leitura_filtro_limpo_uhrv = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_UHRV_FILTRO_LIMPO"], 24, True)
        self.leitura_filtro_limpo_uhlm = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_UHLM_FILTRO_LIMPO"], 21, True)
        self.leitura_resistencia_sem_falha = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RESISTENCIA_SEM_FALHA"], 28, True)
        self.leitura_porta_interna_fechada_cpg = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_CPG_UG_PORTA_INTERNA_FECHADA"], 12, True)
        self.leitura_porta_traseira_fechada_cpg = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_CPG_UG_PORTA_TRASEIRA_FECHADA"], 13, True)

            # Bit Normal
        self.leitura_falha_1_rv_b4 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 4)
        self.leitura_falha_1_rv_b5 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 5)
        self.leitura_falha_1_rv_b6 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 6)
        self.leitura_falha_1_rv_b7 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 7)
        self.leitura_falha_1_rv_b8 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 8)
        self.leitura_falha_2_rv_b0 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 0)
        self.leitura_falha_2_rv_b4 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 4)
        self.leitura_falha_3_rt_b0 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_3"], 0)
        self.leitura_falha_3_rt_b1 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_3"], 1)
        self.leitura_falha_3_rt_b2 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_3"], 2)
        self.leitura_falha_3_rt_b3 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_3"], 3)
        self.leitura_falha_3_rt_b4 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_3"], 4)
        self.leitura_falha_3_rt_b5 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_3"], 5)
        self.leitura_falha_3_rt_b6 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_3"], 6)
        self.leitura_falha_3_rt_b7 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_3"], 7)
        self.leitura_falha_1_rv_b13 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 13)
        self.leitura_falha_1_rv_b14 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 14)
        self.leitura_falha_1_rv_b15 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 15)
        self.leitura_saidas_digitais_rv_b0 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_SAIDAS_DIGITAIS"], 0)
        self.leitura_saidas_digitais_rt_b0 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_SAIDAS_DIGITAIS"], 0)
        self.leitura_alarme_temp_oleo_uhrv = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_OLEO_UHRV"], 6)
        self.leitura_alarme_temp_oleo_uhlm = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_OLEO_UHLM"], 7)
        self.leitura_alarme_temp_mancal_guia = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_MANCAL_GUIA"], 5)
        self.leitura_temp_fase_a_gerador = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_GERADOR_FASE_A"], 15)
        self.leitura_temp_fase_b_gerador = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_GERADOR_FASE_B"], 16)
        self.leitura_temp_fase_c_gerador = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_GERADOR_FASE_C"], 17)
        self.leitura_alarme_temp_ponte_fase_a = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_PONTE_FASE_A"], 0)
        self.leitura_alarme_temp_ponte_fase_b = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_PONTE_FASE_B"], 1)
        self.leitura_alarme_temp_ponte_fase_c = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_PONTE_FASE_C"], 2)
        self.leitura_unidade_manutencao_uhrv = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_UHRV_UNIDADE_EM_MANUTENCAO"], 0)
        self.leitura_unidade_manutencao_uhlm = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_UHLM_UNIDADE_EM_MANUTENCAO"], 4)
        self.leitura_alarme_temp_trafo_excitacao = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_TRAFO_EXCITACAO"], 4)
        self.leitura_escovas_gastas_polo_positivo = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ESCOVAS_GASTAS_POLO_POSITIVO"], 5)
        self.leitura_escovas_gastas_polo_negativo = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ESCOVAS_GASTAS_POLO_NEGATIVO"], 6)
        self.leitura_alarme_temp_mancal_casq_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_CASQ_MANCAL_COMBINADO"], 8)
        self.leitura_alarme_vibra_detec_vertical = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_VIBRACAO_DETECCAO_VERTICAL"], 29)
        self.leitura_alarme_vibra_detec_horizontal = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_VIBRACAO_DETECCAO_HORIZONTAL"], 28)
        self.leitura_alarme_temp_mancal_guia_interno_1 = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_1_MANCAL_GUIA_INTERNO"], 12)
        self.leitura_alarme_temp_mancal_guia_interno_2 = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_2_MANCAL_GUIA_INTERNO"], 13)
        self.leitura_alarme_temp_patins_1_mancal_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_1_PATINS_MANCAL_COMBINADO"], 10)
        self.leitura_alarme_temp_patins_2_mancal_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_2_PATINS_MANCAL_COMBINADO"], 11)
        self.leitura_alarme_vibra_eixo_x_mancal_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_VIBRACAO_EIXO_X_MANCAL_COMBINADO"], 24)
        self.leitura_alarme_vibra_eixo_y_mancal_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_VIBRACAO_EIXO_Y_MANCAL_COMBINADO"], 25)
        self.leitura_alarme_vibra_eixo_z_mancal_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_VIBRACAO_EIXO_Z_MANCAL_COMBINADO"], 26)
        self.leitura_alarme_temp_mancal_con_esc_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO"], 9)
        self.leitura_alarme_temp_nucleo_estatorico_gerador = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_ALM_TEMP_GERADOR_NUCLEO_ESTATORICO"], 14)


        # CONDICIONADORES ESSENCIAIS
        # Essenciais Temperaturas
            # Fase R
        self.leitura_temperatura_fase_R = LeituraOpc(self.opc, OPC_UA["UG"][f"UG{self.id}_TEMP_GERADOR_FASE_A"])
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_R
        self.condicionador_temperatura_fase_r_ug = CondicionadorExponencial(f"UG{self.id}_TEMP_GERADOR_FASE_A", CONDIC_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_r_ug)

            # Fase S
        self.leitura_temperatura_fase_S = LeituraOpc(self.opc, OPC_UA["UG"][f"UG{self.id}_TEMP_GERADOR_FASE_B"])
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_S
        self.condicionador_temperatura_fase_s_ug = CondicionadorExponencial(f"UG{self.id}_TEMP_GERADOR_FASE_B", CONDIC_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_s_ug)

            # Fase T
        self.leitura_temperatura_fase_T = LeituraOpc(self.opc, OPC_UA["UG"][f"UG{self.id}_TEMP_GERADOR_FASE_C"])
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_T
        self.condicionador_temperatura_fase_t_ug = CondicionadorExponencial(f"UG{self.id}_TEMP_GERADOR_FASE_C", CONDIC_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_t_ug)

            # Nucleo Gerador 1
        self.leitura_temperatura_nucleo_gerador_1 = LeituraOpc(self.opc, OPC_UA["UG"][f"UG{self.id}_TEMP_GERADOR_NUCLEO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_nucleo_gerador_1
        self.condicionador_temperatura_nucleo_gerador_1_ug = CondicionadorExponencial(f"UG{self.id}_TEMP_GERADOR_NUCLEO", CONDIC_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_gerador_1_ug)

            # Mancal Guia
        self.leitura_temperatura_mancal_guia = LeituraOpc(self.opc, OPC_UA["UG"][f"UG{self.id}_TEMP_MANCAL_GUIA_GERADOR"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_guia
        self.condicionador_temperatura_mancal_guia_ug = CondicionadorExponencial(f"UG{self.id}_TEMP_MANCAL_GUIA_GERADOR", CONDIC_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_ug)

            # Mancal Guia Interno 1
        self.leitura_temperatura_mancal_guia_interno_1 = LeituraOpc(self.opc, OPC_UA["UG"][f"UG{self.id}_TEMP_1_MANCAL_GUIA_INTERNO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_guia_interno_1
        self.condicionador_temperatura_mancal_guia_interno_1_ug = CondicionadorExponencial(f"UG{self.id}_TEMP_1_MANCAL_GUIA_INTERNO", CONDIC_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_interno_1_ug)

            # Mancal Guia Interno 2
        self.leitura_temperatura_mancal_guia_interno_2 = LeituraOpc(self.opc, OPC_UA["UG"][f"UG{self.id}_TEMP_2_MANCAL_GUIA_INTERNO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_guia_interno_2
        self.condicionador_temperatura_mancal_guia_interno_2_ug = CondicionadorExponencial(f"UG{self.id}_TEMP_2_MANCAL_GUIA_INTERNO", CONDIC_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_interno_2_ug)

            # Patins Mancal Combinado 1
        self.leitura_temperatura_patins_mancal_comb_1 = LeituraOpc(self.opc, OPC_UA["UG"][f"UG{self.id}_TEMP_1_PATINS_MANCAL_COMBINADO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_patins_mancal_comb_1
        self.condicionador_temperatura_patins_mancal_comb_1_ug = CondicionadorExponencial(f"UG{self.id}_TEMP_1_PATINS_MANCAL_COMBINADO", CONDIC_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_patins_mancal_comb_1_ug)

            # Patins Mancal Combinado 2
        self.leitura_temperatura_patins_mancal_comb_2 = LeituraOpc(self.opc, OPC_UA["UG"][f"UG{self.id}_TEMP_2_PATINS_MANCAL_COMBINADO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_patins_mancal_comb_2
        self.condicionador_temperatura_patins_mancal_comb_2_ug = CondicionadorExponencial(f"UG{self.id}_TEMP_2_PATINS_MANCAL_COMBINADO", CONDIC_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_patins_mancal_comb_2_ug)

            # Mancal Casquilho Combinado
        self.leitura_temperatura_mancal_casq_comb = LeituraOpc(self.opc, OPC_UA["UG"][f"UG{self.id}_TEMP_CASQ_MANCAL_COMBINADO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_casq_comb
        self.condicionador_temperatura_mancal_casq_comb_ug = CondicionadorExponencial(f"UG{self.id}_TEMP_CASQ_MANCAL_COMBINADO", CONDIC_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_casq_comb_ug)

            # Mancal Contra Escora Combinado
        self.leitura_temperatura_mancal_contra_esc_comb = LeituraOpc(self.opc, OPC_UA["UG"][f"UG{self.id}_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO"])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_contra_esc_comb
        self.condicionador_temperatura_mancal_contra_esc_comb_ug = CondicionadorExponencial(f"UG{self.id}_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO", CONDIC_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_contra_esc_comb_ug)

        # Essenciais Pressão Turbina
            # Pressão Entrada Turbina
        self.leitura_pressao_turbina = LeituraOpc(self.opc, OPC_UA["UG"][f"UG{self.id}_PRESSAO_ENTRADA_TURBINA"], escala=0.1)
        base = 16.1
        limite = 15.5
        x = self.leitura_pressao_turbina
        self.condicionador_pressao_turbina_ug = CondicionadorExponencialReverso(f"UG{self.id}_PRESSAO_ENTRADA_TURBINA", CONDIC_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_atenuadores.append(self.condicionador_pressao_turbina_ug)

        # Essenciais Padrão
        self.leitura_saidas_digitiais_rv_b0 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_SAIDAS_DIGITAIS"], 0, True)
        x = self.leitura_alarme_1_rt_b0
        self.condicionadores_essenciais.append(CondicionadorBase(f"UG{self.id}_RV_SAIDAS_DIGITAIS - bit 00", CONDIC_NORMALIZAR, x))

        self.leitura_falha_2_rv_b3 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_2"], 3)
        x = self.leitura_falha_2_rv_b3
        self.condicionadores_essenciais.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_2 - bit 03", CONDIC_NORMALIZAR, x))

        self.leitura_saidas_digitais_rt_b0 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_SAIDAS_DIGITAIS"], 0, True)
        x = self.leitura_saidas_digitais_rt_b0
        self.condicionadores_essenciais.append(CondicionadorBase(f"UG{self.id}_RT_SAIDAS_DIGITAIS - bit 00", CONDIC_NORMALIZAR, x))

        self.leitura_trip_rele700G_atuado = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RELE_700G_TRIP_ATUADO"], 31)
        x = self.leitura_trip_rele700G_atuado
        self.condicionadores_essenciais.append(CondicionadorBase(f"UG{self.id}_RELE_700G_TRIP_ATUADO - bit 31", CONDIC_NORMALIZAR, x))

        self.leitura_rele_bloq_86EH_desatuado = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RELE_BLOQUEIO_86EH_DESATUADO"], 28, True)
        x = self.leitura_rele_bloq_86EH_desatuado
        self.condicionadores_essenciais.append(CondicionadorBase(f"UG{self.id}_RELE_BLOQUEIO_86EH_DESATUADO - bit 28", CONDIC_NORMALIZAR, x))

        self.leitura_trip_rele_rv_naoatuado = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RV_RELE_TRIP_NAO_ATUADO"], 14, True)
        x = self.leitura_trip_rele_rv_naoatuado
        self.condicionadores_essenciais.append(CondicionadorBase(f"UG{self.id}_RV_RELE_TRIP_NAO_ATUADO - bit 14", CONDIC_NORMALIZAR, x))

        self.leitura_trip_rele_rt_naoatuado = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RT_RELE_TRIP_NAO_ATUADO"], 23, True)
        x = self.leitura_trip_rele_rt_naoatuado
        self.condicionadores_essenciais.append(CondicionadorBase(f"UG{self.id}_RT_RELE_TRIP_NAO_ATUADO - bit 23", CONDIC_NORMALIZAR, x))

        self.leitura_bt_emerg_naoatuado = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_BT_EMERGENCIA_NAO_ATUADO"], 11, True)
        x = self.leitura_bt_emerg_naoatuado
        self.condicionadores_essenciais.append(CondicionadorBase(f"UG{self.id}_BT_EMERGENCIA_NAO_ATUADO - bit 11", CONDIC_NORMALIZAR, x))

        self.leitura_clp_geral_sem_bloq_exter = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_CLP_GERAL_SEM_BLOQUEIO_EXTERNO"], 1, True)
        x = self.leitura_clp_geral_sem_bloq_exter
        self.condicionadores_essenciais.append(CondicionadorBase(f"UG{self.id}_CLP_GERAL_SEM_BLOQUEIO_EXTERNO - bit 1", CONDIC_NORMALIZAR, x))

        self.leitura_bloq_86M_atuado = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_BLOQUEIO_86M_ATUADO"], 31)
        x = self.leitura_bloq_86M_atuado
        self.condicionadores_essenciais.append(CondicionadorBase(f"UG{self.id}_BLOQUEIO_86M_ATUADO - bit 31", CONDIC_NORMALIZAR, x))

        self.leitura_bloq_86E_atuado = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_BLOQUEIO_86E_ATUADO"], 31)
        x = self.leitura_bloq_86E_atuado
        self.condicionadores_essenciais.append(CondicionadorBase(f"UG{self.id}_BLOQUEIO_86E_ATUADO - bit 31", CONDIC_NORMALIZAR, x))

        self.leitura_bloq_86H_atuado = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_BLOQUEIO_86H_ATUADO"], 31)
        x = self.leitura_bloq_86H_atuado
        self.condicionadores_essenciais.append(CondicionadorBase(f"UG{self.id}_BLOQUEIO_86H_ATUADO - bit 31", CONDIC_NORMALIZAR, x))


        # CONDICIONADORES
        # Padrão
        self.leitura_falha_1_rv_b0 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 0)
        x = self.leitura_falha_1_rv_b0
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_1 - bit 00", CONDIC_NORMALIZAR, x))

        self.leitura_falha_1_rv_b1 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 1)
        x = self.leitura_falha_1_rv_b1
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_1 - bit 01", CONDIC_NORMALIZAR, x))

        self.leitura_falha_1_rv_b2 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 2)
        x = self.leitura_falha_1_rv_b2
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_1 - bit 02", CONDIC_NORMALIZAR, x))

        self.leitura_falha_1_rv_b3 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 3)
        x = self.leitura_falha_1_rv_b3
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_1 - bit 03", CONDIC_NORMALIZAR, x))

        self.leitura_falha_1_rv_b4 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 4)
        x = self.leitura_falha_1_rv_b4
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_1 - bit 04", CONDIC_NORMALIZAR, x))

        self.leitura_falha_1_rv_b5 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 5)
        x = self.leitura_falha_1_rv_b5
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_1 - bit 05", CONDIC_NORMALIZAR, x))

        self.leitura_falha_1_rv_b10 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 10)
        x = self.leitura_falha_1_rv_b10
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_1 - bit 10", CONDIC_NORMALIZAR, x))

        self.leitura_falha_1_rv_b11 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 11)
        x = self.leitura_falha_1_rv_b11
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_1 - bit 11", CONDIC_NORMALIZAR, x))

        self.leitura_falha_1_rv_b12 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 12)
        x = self.leitura_falha_1_rv_b12
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_1 - bit 12", CONDIC_NORMALIZAR, x))

        self.leitura_falha_1_rv_b13 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_1"], 13)
        x = self.leitura_falha_1_rv_b13
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_1 - bit 13", CONDIC_NORMALIZAR, x))

        self.leitura_alarme_1_rt_b8 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_ALARMES_1"], 8)
        x = self.leitura_alarme_1_rt_b8
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_ALARMES_1 - bit 08", CONDIC_NORMALIZAR, x))

        self.leitura_falha_1_rt_b1 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 1)
        x = self.leitura_falha_1_rt_b1
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 01", CONDIC_NORMALIZAR, x))

        self.leitura_falha_1_rt_b2 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 2)
        x = self.leitura_falha_1_rt_b2
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 02", CONDIC_NORMALIZAR, x))

        self.leitura_falha_1_rt_b3 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 3)
        x = self.leitura_falha_1_rt_b3
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 03", CONDIC_NORMALIZAR, x))

        self.leitura_falha_2_rt_b2 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_2"], 2)
        x = self.leitura_falha_2_rt_b2
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_2 - bit 02", CONDIC_NORMALIZAR, x))

        self.leitura_falha_2_rt_b5 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_2"], 5)
        x = self.leitura_falha_2_rt_b5
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_2 - bit 05", CONDIC_NORMALIZAR, x))

        self.leitura_falha_2_rt_b6 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_2"], 6)
        x = self.leitura_falha_2_rt_b6
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_2 - bit 06", CONDIC_NORMALIZAR, x))

        self.leitura_falha_2_rt_b7 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_2"], 7)
        x = self.leitura_falha_2_rt_b7
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_2 - bit 07", CONDIC_NORMALIZAR, x))

        self.leitura_falha_2_rt_b10 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_2"], 10)
        x = self.leitura_falha_2_rt_b10
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_2 - bit 10", CONDIC_NORMALIZAR, x))

        self.leitura_falha_2_rt_b11 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_2"], 11)
        x = self.leitura_falha_2_rt_b11
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_2 - bit 11", CONDIC_NORMALIZAR, x))

        self.leitura_falha_2_rt_b12 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_2"], 12)
        x = self.leitura_falha_2_rt_b12
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_2 - bit 12", CONDIC_NORMALIZAR, x))

        self.leitura_falha_bomba_1_uhrv = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_UHRV_BOMBA_1_FALHA"], 0)
        x = self.leitura_falha_bomba_1_uhrv
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_UHRV_BOMBA_1_FALHA - bit 00", CONDIC_NORMALIZAR, x))

        self.leitura_falha_bomba_2_uhrv = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_UHRV_BOMBA_2_FALHA"], 2)
        x = self.leitura_falha_bomba_2_uhrv
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_UHRV_BOMBA_2_FALHA - bit 02", CONDIC_NORMALIZAR, x))

        self.leitura_falha_bomba_1_uhlm = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_UHLM_BOMBA_1_FALHA"], 4)
        x = self.leitura_falha_bomba_1_uhlm
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_UHLM_BOMBA_1_FALHA - bit 04", CONDIC_NORMALIZAR, x))

        self.leitura_falha_bomba_2_uhlm = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_UHLM_BOMBA_2_FALHA"], 6)
        x = self.leitura_falha_bomba_2_uhlm
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_UHLM_BOMBA_2_FALHA - bit 06", CONDIC_NORMALIZAR, x))

        self.leitura_alarme_rele_rv_atuado = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RV_RELE_ALARME_ATUADO"], 15)
        x = self.leitura_alarme_rele_rv_atuado
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_RELE_ALARME_ATUADO - bit 15", CONDIC_NORMALIZAR, 15))

        self.leitura_sistema_agua_clp_geral_ok = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_CLP_GERAL_SISTEMA_AGUA_OK"], 2, True)
        x = self.leitura_sistema_agua_clp_geral_ok
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_CLP_GERAL_SISTEMA_AGUA_OK - bit 02", CONDIC_NORMALIZAR, x))

        self.leitura_clp_geral_com_tens_barra_essenc = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_CLP_GERAL_COM_TENSAO_BARRA_ESSENCIAIS"], 3, True)
        x = self.leitura_clp_geral_com_tens_barra_essenc
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_CLP_GERAL_COM_TENSAO_BARRA_ESSENCIAIS - bit 03", CONDIC_NORMALIZAR, x))

        self.leitura_disparo_mecanico_atuado = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_DISPARO_MECANICO_ATUADO"], 9)
        x = self.leitura_disparo_mecanico_atuado
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_DISPARO_MECANICO_ATUADO - bit 09", CONDIC_NORMALIZAR, x))

        self.leitura_disparo_mecanico_desatuado = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_DISPARO_MECANICO_DESATUADO"], 8, True)
        x = self.leitura_disparo_mecanico_desatuado
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_DISPARO_MECANICO_DESATUADO - bit 08", CONDIC_NORMALIZAR, x))

        self.leitura_falha_habilitar_sistema_agua = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_HABILITAR_SISTEMA_AGUA"], 11)
        x = self.leitura_falha_habilitar_sistema_agua
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_HABILITAR_SISTEMA_AGUA - bit 11", CONDIC_NORMALIZAR, x))

        self.leitura_trip_temp_oleo_uhlm = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_OLEO_UHLM"], 4)
        x = self.leitura_trip_temp_oleo_uhlm
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_OLEO_UHLM - bit 04", CONDIC_NORMALIZAR, x))

        self.leitura_trip_temp_oleo_uhrv = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_OLEO_UHRV"], 5)
        x = self.leitura_trip_temp_oleo_uhrv
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_OLEO_UHRV - bit 05", CONDIC_NORMALIZAR, x))

        self.leitura_parada_bloq_abertura_disj = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_PARADA_BLOQUEIO_ABERTURA_DISJUNTOR"], 11)
        x = self.leitura_parada_bloq_abertura_disj
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_PARADA_BLOQUEIO_ABERTURA_DISJUNTOR - bit 11", CONDIC_NORMALIZAR, x))

        self.leitura_parada_bloq_descarga_pot = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_PARADA_BLOQUEIO_DESCARGA_POTENCIA"], 10)
        x = self.leitura_parada_bloq_descarga_pot
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_PARADA_BLOQUEIO_DESCARGA_POTENCIA - bit 10", CONDIC_NORMALIZAR, x))

        self.leitura_falha_pressao_linha_b1_uhlm = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_UHLM_FALHA_PRESSAO_LINHA_B1"], 9)
        x = self.leitura_falha_pressao_linha_b1_uhlm
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_UHLM_FALHA_PRESSAO_LINHA_B1 - bit 09", CONDIC_NORMALIZAR, x))

        self.leitura_falha_pressao_linha_b2_uhlm = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_UHLM_FALHA_PRESSAO_LINHA_B2"], 10)
        x = self.leitura_falha_pressao_linha_b2_uhlm
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_UHLM_FALHA_PRESSAO_LINHA_B2 - bit 10", CONDIC_NORMALIZAR, x))

        self.leitura_falha_pressostato_linha_uhlm = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_UHLM_FALHA_PRESSOSTATO_LINHA"], 11)
        x = self.leitura_falha_pressostato_linha_uhlm
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_UHLM_FALHA_PRESSOSTATO_LINHA - bit 11", CONDIC_NORMALIZAR, x))

        self.leitura_falha_habilitar_rv = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RV_FALHA_HABILITAR_RV"], 0)
        x = self.leitura_falha_habilitar_rv
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_HABILITAR_RV - bit 00", CONDIC_NORMALIZAR, x))

        self.leitura_falha_partir_rv = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RV_FALHA_PARTIR_RV"], 1)
        x = self.leitura_falha_partir_rv
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_PARTIR_RV - bit 01", CONDIC_NORMALIZAR, x))

        self.leitura_falha_desabilitar_rv = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RV_FALHA_DESABILITAR_RV"], 2)
        x = self.leitura_falha_desabilitar_rv
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_DESABILITAR_RV - bit 02", CONDIC_NORMALIZAR, x))

        self.leitura_falha_habilitar_rt = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RT_FALHA_HABILITAR"], 16)
        x = self.leitura_falha_habilitar_rt
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHA_HABILITAR - bit 16", CONDIC_NORMALIZAR, x))

        self.leitura_falha_partir_rt = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RT_FALHA_PARTIR"], 17)
        x = self.leitura_falha_partir_rt
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHA_PARTIR - bit 17", CONDIC_NORMALIZAR, x))

        self.leitura_alarme_1_rt_b0 = LeituraModbusBit(self.clp, OPC_UA["UG"][f"UG{self.id}_RT_ALARMES_1"], 0)
        x = self.leitura_alarme_1_rt_b0
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_ALARMES_1 - bit 00", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_alarme_1_rt_b4 = LeituraModbusBit(self.clp, OPC_UA["UG"][f"UG{self.id}_RT_ALARMES_1"], 4)
        x = self.leitura_alarme_1_rt_b4
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_ALARMES_1 - bit 04", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_alarme_1_rt_b5 = LeituraModbusBit(self.clp, OPC_UA["UG"][f"UG{self.id}_RT_ALARMES_1"], 5)
        x = self.leitura_alarme_1_rt_b5
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_ALARMES_1 - bit 05", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b0 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 0)
        x = self.leitura_falha_1_rt_b0
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 00", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b4 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 4)
        x = self.leitura_falha_1_rt_b4
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 04", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b5 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 5)
        x = self.leitura_falha_1_rt_b5
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 05", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b6 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 6)
        x = self.leitura_falha_1_rt_b6
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 06", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b7 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 7)
        x = self.leitura_falha_1_rt_b7
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 07", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b8 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 8)
        x = self.leitura_falha_1_rt_b8
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 08", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b9 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 9)
        x = self.leitura_falha_1_rt_b9
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 09", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b10 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 10)
        x = self.leitura_falha_1_rt_b10
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 10", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b11 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 11)
        x = self.leitura_falha_1_rt_b11
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 11", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b12 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 12)
        x = self.leitura_falha_1_rt_b12
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 12", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b13 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 13)
        x = self.leitura_falha_1_rt_b13
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 13", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b14 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 14)
        x = self.leitura_falha_1_rt_b14
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 14", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b15 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RT_FALHAS_1"], 15)
        x = self.leitura_falha_1_rt_b15
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHAS_1 - bit 15", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_2_rt_b0 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHAS_2"], 0)
        x = self.leitura_falha_2_rt_b0
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHAS_2 - bit 00", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_2_rt_b1 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHAS_2"], 1)
        x = self.leitura_falha_2_rt_b1
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHAS_2 - bit 01", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_2_rt_b3 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHAS_2"], 3)
        x = self.leitura_falha_2_rt_b3
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHAS_2 - bit 03", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_2_rt_b4 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHAS_2"], 4)
        x = self.leitura_falha_2_rt_b4
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHAS_2 - bit 04", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_2_rt_b8 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHAS_2"], 8)
        x = self.leitura_falha_2_rt_b8
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHAS_2 - bit 08", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_2_rt_b9 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHAS_2"], 9)
        x = self.leitura_falha_2_rt_b9
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHAS_2 - bit 09", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_2_rv_b1 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_2"], 1)
        x = self.leitura_falha_2_rv_b1
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_2 - bit 01", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_2_rv_b2 = LeituraModbusBit(self.clp, MB["UG"][f"UG{self.id}_RV_FALHA_2"], 2)
        x = self.leitura_falha_2_rv_b2
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_2 - bit 02", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_rele_700G_bf_atuado = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RELE_700G_BF_ATUADO"], 0)
        x = self.leitura_rele_700G_bf_atuado
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RELE_700G_BF_ATUADO - bit 00", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_sup_tensao_125vcc = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_SUPERVISAO_TENSAO_125VCC"], 29, True)
        x = self.leitura_sup_tensao_125vcc
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_SUPERVISAO_TENSAO_125VCC - bit 29", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_sup_tensao_24vcc = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_SUPERVISAO_TENSAO_24VCC"], 30, True)
        x = self.leitura_sup_tensao_24vcc
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_SUPERVISAO_TENSAO_24VCC - bit 30", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_sup_bobina_52g = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_SUPERVISAO_BOBINA_52G"], 12, True)
        x = self.leitura_sup_bobina_52g
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_SUPERVISAO_BOBINA_52G - bit 12", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_sup_bobina_86eh = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_SUPERVISAO_BOBINA_86EH"], 13, True)
        x = self.leitura_sup_bobina_86eh
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_SUPERVISAO_BOBINA_86EH - bit 13", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_disj_125vcc_fechados = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_DISJUNTORES_125VCC_FECHADOS"], 31, True)
        x = self.leitura_disj_125vcc_fechados
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_DISJUNTORES_125VCC_FECHADOS - bit 31", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_disj_24vcc_fechados = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_DISJUNTORES_24VCC_FECHADOS"], 0, True)
        x = self.leitura_disj_24vcc_fechados
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_DISJUNTORES_24VCC_FECHADOS - bit 00", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_ponte_fase_a = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_PONTE_FASE_A"], 0)
        x = self.leitura_falha_temp_ponte_fase_a
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_PONTE_FASE_A - bit 00", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_ponte_fase_b = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_PONTE_FASE_B"], 1)
        x = self.leitura_falha_temp_ponte_fase_b
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_PONTE_FASE_B - bit 01", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_ponte_fase_c = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_PONTE_FASE_C"], 2)
        x = self.leitura_falha_temp_ponte_fase_c
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_PONTE_FASE_C - bit 02", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_trafo_excita = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_TRAFO_EXCITACAO"], 4)
        x = self.leitura_falha_temp_trafo_excita
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_TRAFO_EXCITACAO - bit 04", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_guia = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_MANCAL_GUIA"], 5)
        x = self.leitura_falha_temp_mancal_guia
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_MANCAL_GUIA - bit 05", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_oleo_uhrv = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_OLEO_UHRV"], 6)
        x = self.leitura_falha_temp_oleo_uhrv
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_OLEO_UHRV - bit 06", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_oleo_uhlm = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_OLEO_UHLM"], 7)
        x = self.leitura_falha_temp_oleo_uhlm
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_OLEO_UHLM - bit 07", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_casq_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_CASQ_MANCAL_COMBINADO"], 8)
        x = self.leitura_falha_temp_mancal_casq_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_CASQ_MANCAL_COMBINADO - bit 08", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_con_esc_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO"], 9)
        x = self.leitura_falha_temp_mancal_con_esc_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO - bit 09", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_pat_1_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_1_PATINS_MANCAL_COMBINADO"], 10)
        x = self.leitura_falha_temp_mancal_pat_1_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_1_PATINS_MANCAL_COMBINADO - bit 10", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_pat_2_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_2_PATINS_MANCAL_COMBINADO"], 11)
        x = self.leitura_falha_temp_mancal_pat_2_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_2_PATINS_MANCAL_COMBINADO - bit 11", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_guia_interno_1 = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_1_MANCAL_GUIA_INTERNO"], 12)
        x = self.leitura_falha_temp_mancal_guia_interno_1
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_1_MANCAL_GUIA_INTERNO - bit 12", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_guia_interno_2 = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_2_MANCAL_GUIA_INTERNO"], 13)
        x = self.leitura_falha_temp_mancal_guia_interno_2
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_2_MANCAL_GUIA_INTERNO - bit 13", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_gerador_nucleo_esta = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_GERADOR_NUCLEO_ESTATORICO"], 14)
        x = self.leitura_falha_temp_gerador_nucleo_esta
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_GERADOR_NUCLEO_ESTATORICO - bit 14", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_gerador_fase_a = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_GERADOR_FASE_A"], 15)
        x = self.leitura_falha_temp_gerador_fase_a
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_GERADOR_FASE_A - bit 15", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_gerador_fase_b = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_GERADOR_FASE_B"], 16)
        x = self.leitura_falha_temp_gerador_fase_b
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_GERADOR_FASE_B - bit 16", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_gerador_fase_c = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_TEMP_GERADOR_FASE_C"], 17)
        x = self.leitura_falha_temp_gerador_fase_c
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_TEMP_GERADOR_FASE_C - bit 17", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_pressao_entrada_turb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_PRESSAO_ENTRADA_TURBINA"], 20)
        x = self.leitura_falha_pressao_entrada_turb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_PRESSAO_ENTRADA_TURBINA - bit 20", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_eixo_x_mancal_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_VIBRACAO_EIXO_X_MANCAL_COMBINADO"], 24)
        x = self.leitura_falha_vibra_eixo_x_mancal_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_VIBRACAO_EIXO_X_MANCAL_COMBINADO - bit 24", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_eixo_y_mancal_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO"], 25)
        x = self.leitura_falha_vibra_eixo_y_mancal_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO - bit 25", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_eixo_z_mancal_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO"], 26)
        x = self.leitura_falha_vibra_eixo_z_mancal_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO - bit 26", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_detec_horizontal = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_VIBRACAO_DETECCAO_HORIZONTAL"], 28)
        x = self.leitura_falha_vibra_detec_horizontal
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_VIBRACAO_DETECCAO_HORIZONTAL - bit 28", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_detec_vertical = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_FALHA_VIBRACAO_DETECACAO_VERTICAL"], 29)
        x = self.leitura_falha_vibra_detec_vertical
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_FALHA_VIBRACAO_DETECACAO_VERTICAL - bit 29", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_bloqueio_86M_atuado = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_BLOQUEIO_86M_ATUADO"], 31)
        x = self.leitura_bloqueio_86M_atuado
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_BLOQUEIO_86M_ATUADO - bit 31", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_detec_horizontal = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_VIBRACAO_DETECCAO_HORIZONTAL"], 21)
        x = self.leitura_trip_vibra_detec_horizontal
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_VIBRACAO_DETECCAO_HORIZONTAL - bit 21", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_detec_vertical = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_VIBRACAO_DETECACAO_VERTICAL"], 22)
        x = self.leitura_trip_vibra_detec_vertical
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_VIBRACAO_DETECACAO_VERTICAL - bit 22", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_eixo_x_mancal_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_VIBRACAO_EIXO_X_MANCAL_COMBINADO"], 23)
        x = self.leitura_trip_vibra_eixo_x_mancal_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_VIBRACAO_EIXO_X_MANCAL_COMBINADO - bit 23", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_eixo_y_mancal_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_VIBRACAO_EIXO_Y_MANCAL_COMBINADO"], 24)
        x = self.leitura_trip_vibra_eixo_y_mancal_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_VIBRACAO_EIXO_Y_MANCAL_COMBINADO - bit 24", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_eixo_z_mancal_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_VIBRACAO_EIXO_Z_MANCAL_COMBINADO"], 25)
        x = self.leitura_trip_vibra_eixo_z_mancal_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_VIBRACAO_EIXO_Z_MANCAL_COMBINADO - bit 25", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_ponte_fase_a = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_PONTE_FASE_A"], 16)
        x = self.leitura_trip_temp_ponte_fase_a
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_PONTE_FASE_A - bit 16", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_ponte_fase_b = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_PONTE_FASE_B"], 17)
        x = self.leitura_trip_temp_ponte_fase_b
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_PONTE_FASE_B - bit 17", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_ponte_fase_c = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_PONTE_FASE_C"], 18)
        x = self.leitura_trip_temp_ponte_fase_c
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_PONTE_FASE_C - bit 18", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_fase_a = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_GERADOR_FASE_A"], 19)
        x = self.leitura_trip_temp_gerador_fase_a
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_GERADOR_FASE_A - bit 19", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_fase_b = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_GERADOR_FASE_B"], 20)
        x = self.leitura_trip_temp_gerador_fase_b
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_GERADOR_FASE_B - bit 20", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_fase_c = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_GERADOR_FASE_C"], 21)
        x = self.leitura_trip_temp_gerador_fase_c
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_GERADOR_FASE_C - bit 21", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_nucleo_estatorico = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_GERADOR_NUCLEO_ESTATORICO"], 22)
        x = self.leitura_trip_temp_gerador_nucleo_estatorico
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_GERADOR_NUCLEO_ESTATORICO - bit 22", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_saida_ar = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_GERADOR_SAIDA_AR"], 23)
        x = self.leitura_trip_temp_gerador_saida_ar
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_GERADOR_SAIDA_AR - bit 23", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_trafo_ateramento = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_TRAFO_ATERRAMENTO"], 24)
        x = self.leitura_trip_temp_trafo_ateramento
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_TRAFO_ATERRAMENTO - bit 24", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_trafo_excitacao = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_TRAFO_EXCITACAO"], 25)
        x = self.leitura_trip_temp_trafo_excitacao
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_TRAFO_EXCITACAO - bit 25", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_pressao_acum_uhrv = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_PRESSAO_ACUMULADOR_UHRV"], 5)
        x = self.leitura_trip_pressao_acum_uhrv
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_PRESSAO_ACUMULADOR_UHRV - bit 05", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_casq_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_CASQ_MANCAL_COMBINADO"], 18)
        x = self.leitura_trip_temp_mancal_casq_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_CASQ_MANCAL_COMBINADO - bit 18", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_contra_esc_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO"], 19)
        x = self.leitura_trip_temp_mancal_contra_esc_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO - bit 19", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_patins_1_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_1_PATINS_MANCAL_COMBINADO"], 20)
        x = self.leitura_trip_temp_mancal_patins_1_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_1_PATINS_MANCAL_COMBINADO - bit 20", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_patins_2_comb = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_2_PATINS_MANCAL_COMBINADO"], 21)
        x = self.leitura_trip_temp_mancal_patins_2_comb
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_2_PATINS_MANCAL_COMBINADO - bit 21", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_guia_interno_1 = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_1_MANCAL_GUIA_INTERNO"], 22)
        x = self.leitura_trip_temp_mancal_guia_interno_1
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_1_MANCAL_GUIA_INTERNO - bit 22", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_guia_interno_2 = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_TRIP_TEMP_2_MANCAL_GUIA_INTERNO"], 23)
        x = self.leitura_trip_temp_mancal_guia_interno_2
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_TRIP_TEMP_2_MANCAL_GUIA_INTERNO - bit 23", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_fechar_distrib_rv = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RV_FALHA_FECHAR_DISTRIBUIDOR"], 4)
        x = self.leitura_falha_fechar_distrib_rv
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RV_FALHA_FECHAR_DISTRIBUIDOR - bit 04", CONDIC_INDISPONIBILIZAR, x))

        self.leitura_falha_desbilitar_rt = LeituraOpcBit(self.opc, OPC_UA["UG"][f"UG{self.id}_RT_FALHA_DESABILITAR"], 18)
        x = self.leitura_falha_desbilitar_rt
        self.condicionadores.append(CondicionadorBase(f"UG{self.id}_RT_FALHA_DESABILITAR - bit 18", CONDIC_INDISPONIBILIZAR, x))

        return True