__version__ = "0.2"
__authors__ = "Lucas Lavratti", " Henrique Pfeifer"
__credits__ = ["Diego Basgal" , ...]
__description__ = "Este módulo corresponde a implementação das Unidades de Geração."

from usina import *
from condicionador import *
from maquinas_estado.ug_sm import *

logger = logging.getLogger("__main__")

class UnidadeGeracao(Usina):
    def __init__(self, id: int = None):

        # VERIFICAÇÃO DE ARGUMENTOS
        if not id or id < 1:
            raise ValueError(f"[UG{self.id}] A Unidade deve ser instanciada com um valor maior que \"0\".")
        else:
            self.__id: int = id

        # ATRIBUIÇÃO DE VAIRÁVEIS
        # Privadas
        self.__tempo_entre_tentativas: int = 0
        self.__limite_tentativas_de_normalizacao: int = 3

        self.__etapa_atual: LeituraModbus = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_ESTADO_OPERACAO"], descricao=f"UG{self.id}_RV_ESTADO_OPERACAO")

        self.__leitura_potencia: LeituraModbus = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_UG_P"], descricao=f"UG{self.id}_UG_P")
        self.__leitura_horimetro: LeituraModbus = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_UG_HORIMETRO"], descricao=f"UG{self.id}_UG_HORIMETRO")
        self.__leitura_dj52l: LeituraModbusBit = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["SE"]["CMD_SE_FECHA_52L"], bit=4, invertido=True, descricao="CMD_SE_FECHA_52L")

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
        self.borda_pressao: bool = False
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
            logger.exception(f"[UG{self.id}] Houve um erro na leitura de etapa atual da UG. Exception: \"{repr(e)}\"")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
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
    def lista_ugs(self) -> "list[UnidadeGeracao]":
        return self._lista_ugs

    @lista_ugs.setter
    def lista_ugs(self, var: "list[UnidadeGeracao]") -> None:
        self._lista_ugs = var

    @property
    def condicionadores(self) -> "list[CondicionadorBase]":
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[CondicionadorBase]"):
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]"):
        self._condicionadores_essenciais = var

    @property
    def condicionadores_atenuadores(self) -> "list[CondicionadorBase]":
        return self._condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: "list[CondicionadorBase]"):
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


    def forcar_estado_manual(self) -> None:
        self.__next_state = StateManual(self)

    def forcar_estado_restrito(self) -> None:
        self.__next_state = StateRestrito(self)

    def forcar_estado_indisponivel(self) -> None:
        self.__next_state = StateIndisponivel(self)

    def forcar_estado_disponivel(self) -> None:
        self.reconhece_reset_alarmes()
        self.__next_state = StateDisponivel(self)

    def acionar_trips(self) -> None:
        self.acionar_trip_eletrico()
        self.acionar_trip_logico()

    def step(self) -> None:
        logger.debug(f"[UG{self.id}] Step -> (Tentativas de normalização: {self.tentativas_de_normalizacao}/{self.limite_tentativas_de_normalizacao}).")
        self.__next_state = self.__next_state.step()
        self.atualizar_modbus_moa()

    def atualizar_modbus_moa(self) -> None:
        try:
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_ETAPA_UG{self.id}"], [self.etapa_atual])
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_STATE_UG{self.id}"], [self.codigo_state])

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível escrever os valores no CLP MOA. Exception: \"{repr(e)}\".")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")

    def partir(self) -> bool:
        try:
            if self.etapa_atual == UG_PARADA:
                logger.info(f"[UG{self.id}] Enviando comando de partida.")
                res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_RESET_FALHAS_PASSOS"], bit=0, valor=1)
                res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86M"], bit=1, valor=1)
                res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86E"], bit=2, valor=1)
                res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86H"], bit=3, valor=1)
                res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_UHRV_REARME_FALHAS"], bit=0, valor=1)
                res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_UHLM_REARME_FALHAS"], bit=16, valor=1)
                res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_PARTIDA_CMD_SINCRONISMO"], bit=10, valor=1)
                self.enviar_setpoint(self.setpoint)

            else:
                logger.debug(f"[UG{self.id}] A Unidade já está sincronizada.")
            return res

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível partir a Unidade. Exception: \"{repr(e)}\".")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def parar(self) -> bool:
        try:
            if self.etapa_atual == (UG_SINCRONIZADA or UG_SINCRONIZANDO):
                logger.info(f"[UG{self.id}] Enviando comando de parada.")
                self.enviar_setpoint(0)
                return EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_PARADA_CMD_DESABILITA_UHLM"], bit=15, valor=1)

            else:
                logger.debug(f"[UG{self.id}] A Unidade já está parada.")

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível parar a Unidade. Exception: \"{repr(e)}\".")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def enviar_setpoint(self, setpoint_kw: int) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Enviando setpoint {int(self.setpoint)} kW.")

            if setpoint_kw > 1:
                self.setpoint = int(setpoint_kw)
                res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_RESET_FALHAS_PASSOS"], bit=0, valor=1)
                res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86M"], bit=1, valor=1)
                res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86E"], bit=2, valor=1)
                res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86H"], bit=3, valor=1)
                res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_UHRV_REARME_FALHAS"], bit=0, valor=1)
                res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_UHLM_REARME_FALHAS"], bit=16, valor=1)
                res = self.clp[f"UG{self.id}"].write_single_register(REG_CLP["UG"][f"UG{self.id}_RV_SETPOINT_POTENCIA_ATIVA_PU"], self.setpoint)
                return res

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel enviar o setpoint para a Unidade. Exception: \"{repr(e)}\".")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
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
                self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["PAINEL_LIDO"], [0])
                sleep(1)
            return True

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel enviar o comando de reconhecer e resetar alarmes. Exception: \"{repr(e)}\".")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def acionar_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Acionando TRIP -> Lógico.")
            return EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_PARADA_EMERGENCIA"], bit=4, valor=1)

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel acionar o TRIP lógico. Exception: \"{repr(e)}\".")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def remover_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Removendo TRIP -> Lógico.")
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_RESET_FALHAS_PASSOS"], bit=0, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86M"], bit=1, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86E"], bit=2, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86H"], bit=3, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_UHRV_REARME_FALHAS"], bit=0, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_UHLM_REARME_FALHAS"], bit=16, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_BLOQUEIO_86H_ATUADO"], bit=31, valor=0)
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RELE_700G_TRIP_ATUADO"], bit=31, valor=0)
            return res

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível remover o TRIP lógico. Exception: \"{repr(e)}\".")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def acionar_trip_eletrico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Acionando TRIP -> Elétrico.")
            return self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{self.id}"], [1])

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível acionar o TRIP elétrico. Exception: \"{repr(e)}\".")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def remover_trip_eletrico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Removendo TRIP -> Elétrico.")
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{self.id}"], [0])
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["PAINEL_LIDO"], [0])

            if not self.leitura_dj52l:
                logger.debug(f"[UG{self.id}] Comando recebido - Fechando Dj52L")
                return EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["SE"]["CMD_SE_FECHA_52L"], bit=4, valor=1)

        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível remover o TRIP elétrico. Exception: \"{repr(e)}\".")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def resetar_emergencia(self) -> bool:
        try:
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_RESET_FALHAS_PASSOS"], bit=0, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86M"], bit=1, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86E"], bit=2, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_REARME_BLOQUEIO_86H"], bit=3, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_UHRV_REARME_FALHAS"], bit=0, valor=1)
            res = EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_UHLM_REARME_FALHAS"], bit=16, valor=1)
            return res

        except Exception as e:
            logger.exception(f"[UG{self.id}] Houve um erro ao realizar o reset geral. Exception: \"{repr(e)}\".")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def verificar_partindo(self) -> None:
        logger.debug(f"[UG{self.id}] Iniciando o timer de verificação de partida")
        while time() < (time() + 600):
            if self.etapa_atual == UG_SINCRONIZADA or self.parar_timer:
                logger.debug(f"[UG{self.id}] {'Modo manual ativado' if self.parar_timer else 'Unidade Sincronizada'}. Verificação de partida encerrada.")
                return

        logger.debug(f"[UG{self.id}] A Unidade estourou o timer de verificação de partida, adicionando condição para normalizar")
        EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CMD_PARADA_EMERGENCIA"], bit=4, valor=1)
        self.borda_partindo = False
        sleep(1)

    def atenuacao_carga(self) -> None:
        logger.debug(f"[UG{self.id}] Atenuador \"{condic.descr}\" -> Atenuação: {max(0, condic.valor)} / Leitura: {condic.leitura}" for condic in self.condicionadores_atenuadores)

        ganho = 1 - max(0, [sum(condic) for condic in self.condicionadores_atenuadores])
        aux = self.setpoint
        if (self.setpoint > self.cfg["pot_minima"]) and (self.setpoint * ganho) > self.cfg["pot_minima"]:
            self.setpoint = self.setpoint * ganho

        elif (self.setpoint * ganho < self.cfg["pot_minima"]) and (self.setpoint > self.cfg["pot_minima"]):
            self.setpoint = self.cfg["pot_minima"]

        logger.debug(f"[UG{self.id}] SP {aux} * GANHO {ganho} = {self.setpoint}")

    def controle_etapas(self) -> None:
        if self.etapa_atual == UG_PARANDO:
            self.cp[f"CP{self.id}"].fechar_comporta() if self.leitura_potencia < 300 else ...
            self.controle_comportas() if self.setpoint >= self.cfg["pot_minima"] else ...

        elif self.etapa_atual == UG_PARADA:
            self.controle_comportas() if self.setpoint >= self.cfg["pot_minima"] else ...

        elif self.etapa_atual == UG_SINCRONIZANDO:
            self.parar(), logger.warning(f"[UG{self.id}] Parando a UG. (SP enviado = 0).") if self.setpoint == 0 else ...

        elif self.etapa_atual == UG_SINCRONIZADA:
            self.borda_partindo = False

            self.aux_tempo_sincronizada = self.get_time() if not self.aux_tempo_sincronizada else ...
            self.tentativas_de_normalizacao = 0 if (self.get_time() - self.aux_tempo_sincronizada).seconds >= 300 else ...

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        elif self.etapa_atual not in UG_LST_ETAPAS:
            logger.warning(f"[UG{self.id}] UG em etapa inconsistente. (Etapa atual:{self.etapa_atual})")

        if not self.etapa_atual == UG_SINCRONIZADA:
            self.aux_tempo_sincronizada = None

    def controle_comportas(self) -> None:
        if self.cp[f"CP{self.id}"].etapa_comporta == CP_FECHADA:
            self.cp[f"CP{self.id}"].cracking_comporta()

        elif self.cp[f"CP{self.id}"].etapa_comporta == CP_CRACKING:
            if not self.borda_pressao:
                Thread(target=lambda: self.cp[f"CP{self.id}"].verificar_pressao()).start()
                self.borda_pressao = True
            self.cp[f"CP{self.id}"].abrir_comporta() if self.cp[f"CP{self.id}"].press_equalizada.valor else logger.debug(f"[UG{self.id}] Aguardando equalização da pressão da CP{self.id}.")

        elif self.cp[f"CP{self.id}"].etapa_comporta == CP_ABERTA:
            self.partir()
            self.enviar_setpoint(self.setpoint)
            if not self.borda_partindo:
                Thread(target=lambda: self.verificar_partindo()).start()
                self.borda_partindo = True

        elif self.cp[f"CP{self.id}"].etapa_comporta == CP_REMOTO:
            logger.debug(f"[UG{self.id}] Comporta {self.id} em modo manual")
            pass

        else:
            logger.debug(f"[UG{self.id}] Comporta {self.id} entre etapas/etapa inconsistente")

    def verificar_condicionadores(self) -> int:
        if [condic.ativo for condic in self.condicionadores_essenciais]:
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]
            condic_flag = [CONDIC_NORMALIZAR for condic in condics_ativos if condic.gravidade == CONDIC_NORMALIZAR]
            condic_flag = [CONDIC_AGUARDAR for condic in condics_ativos if condic.gravidade == CONDIC_AGUARDAR]
            condic_flag = [CONDIC_INDISPONIBILIZAR for condic in condics_ativos if condic.gravidade == CONDIC_INDISPONIBILIZAR]

            if condic_flag in (CONDIC_NORMALIZAR, CONDIC_AGUARDAR, CONDIC_INDISPONIBILIZAR):
                logger.info(f"[UG{self.id}] Foram detectados condicionadores ativos!")
                [logger.info(f"[UG{self.id}] Condicionador: \"{condic.descricao}\", Gravidade: \"{condic.gravidade}\".") for condic in condics_ativos]
        return condic_flag

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
            logger.exception(f"[UG{self.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores. Exception: \"{repr(e)}\".")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")

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

        if self.leitura_pressao_turbina.valor <= self.condicionador_pressao_turbina_ug.valor_base and self.leitura_pressao_turbina.valor != 0 and self.etapa_atual == UG_SINCRONIZADA:
            logger.warning(f"[UG{self.id}] A pressão na entrada da turbina da UG passou do valor base! ({self.condicionador_pressao_turbina_ug.valor_base:03.2f} KGf/m2) | Leitura: {self.leitura_pressao_turbina.valor:03.2f}")
        if self.leitura_pressao_turbina.valor <= self.condicionador_pressao_turbina_ug.valor_limite+0.9*(self.condicionador_pressao_turbina_ug.valor_base - self.condicionador_pressao_turbina_ug.valor_limite) and self.leitura_pressao_turbina.valor != 0 and self.etapa_atual == UG_SINCRONIZADA:
            logger.critical(f"[UG{self.id}] A pressão na entrada da turbina da UG está muito próxima do limite! ({self.condicionador_pressao_turbina_ug.valor_limite:03.2f} KGf/m2) | Leitura: {self.leitura_pressao_turbina.valor:03.2f} KGf/m2")

    def leitura_periodica(self) -> None:
        # Telegram
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

        if not self.leitura_filtro_limpo_uhrv.valor:
            logger.warning(f"[UG{self.id}] O filtro da UHRV da UG está sujo. Favor realizar limpeza/troca.")

        if not self.leitura_filtro_limpo_uhrv.valor:
            logger.warning(f"[UG{self.id}] O filtro da UHLM da UG está sujo. Favor realizar limpeza/troca.")

        if not self.leitura_porta_interna_fechada_cpg.valor:
            logger.warning(f"[UG{self.id}] A porta interna do CPG da UG está aberta. Favor fechar.")

        if not self.leitura_porta_traseira_fechada_cpg.valor:
            logger.warning(f"[UG{self.id}] A porta traseira do CPG da UG está aberta. Favor fechar.")

        if not self.leitura_resistencia_sem_falha.valor:
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

    def iniciar_leituras_condicionadores(self) -> None:
        # LEITURAS PARA LEITURA PERIODICA
        # Telegram
            # Bit Invertido
        self.leitura_filtro_limpo_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_UHRV_FILTRO_LIMPO"], bit=24, invertido=True, descricao=f"UG{self.id}_UHRV_FILTRO_LIMPO")
        self.leitura_filtro_limpo_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_UHLM_FILTRO_LIMPO"], bit=21, invertido=True, descricao=f"UG{self.id}_UHLM_FILTRO_LIMPO")
        self.leitura_resistencia_sem_falha = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RESISTENCIA_SEM_FALHA"], bit=28, invertido=True, descricao=f"UG{self.id}_RESISTENCIA_SEM_FALHA")
        self.leitura_porta_interna_fechada_cpg = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CPG_UG_PORTA_INTERNA_FECHADA"], bit=12, invertido=True, descricao=f"UG{self.id}_CPG_UG_PORTA_INTERNA_FECHADA")
        self.leitura_porta_traseira_fechada_cpg = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CPG_UG_PORTA_TRASEIRA_FECHADA"], bit=13, invertido=True, descricao=f"UG{self.id}_CPG_UG_PORTA_TRASEIRA_FECHADA")

            # Bit Normal
        self.leitura_falha_1_rv_b4 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=4, descricao=f"UG{self.id}_RV_FALHA_1 - bit 04")
        self.leitura_falha_1_rv_b5 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=5, descricao=f"UG{self.id}_RV_FALHA_1 - bit 05")
        self.leitura_falha_1_rv_b6 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=6, descricao=f"UG{self.id}_RV_FALHA_1 - bit 06")
        self.leitura_falha_1_rv_b7 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=7, descricao=f"UG{self.id}_RV_FALHA_1 - bit 07")
        self.leitura_falha_1_rv_b8 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=8, descricao=f"UG{self.id}_RV_FALHA_1 - bit 08")
        self.leitura_falha_2_rv_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_2"], bit=0, descricao=f"UG{self.id}_RV_FALHA_1 - bit 00")
        self.leitura_falha_2_rv_b4 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_2"], bit=4, descricao=f"UG{self.id}_RV_FALHA_1 - bit 04")
        self.leitura_falha_3_rt_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_3"], bit=0, descricao=f"UG{self.id}_RT_FALHAS_3 - bit 00")
        self.leitura_falha_3_rt_b1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_3"], bit=1, descricao=f"UG{self.id}_RT_FALHAS_3 - bit 01")
        self.leitura_falha_3_rt_b2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_3"], bit=2, descricao=f"UG{self.id}_RT_FALHAS_3 - bit 02")
        self.leitura_falha_3_rt_b3 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_3"], bit=3, descricao=f"UG{self.id}_RT_FALHAS_3 - bit 03")
        self.leitura_falha_3_rt_b4 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_3"], bit=4, descricao=f"UG{self.id}_RT_FALHAS_3 - bit 04")
        self.leitura_falha_3_rt_b5 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_3"], bit=5, descricao=f"UG{self.id}_RT_FALHAS_3 - bit 05")
        self.leitura_falha_3_rt_b6 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_3"], bit=6, descricao=f"UG{self.id}_RT_FALHAS_3 - bit 06")
        self.leitura_falha_3_rt_b7 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_3"], bit=7, descricao=f"UG{self.id}_RT_FALHAS_3 - bit 07")
        self.leitura_falha_1_rv_b13 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=13, descricao=f"UG{self.id}_RV_FALHA_1 - bit 13")
        self.leitura_falha_1_rv_b14 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=14, descricao=f"UG{self.id}_RV_FALHA_1 - bit 14")
        self.leitura_falha_1_rv_b15 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=15, descricao=f"UG{self.id}_RV_FALHA_1 - bit 15")
        self.leitura_saidas_digitais_rv_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_SAIDAS_DIGITAIS"], bit=0, descricao=f"UG{self.id}_RV_SAIDAS_DIGITAIS - bit 00")
        self.leitura_saidas_digitais_rt_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_SAIDAS_DIGITAIS"], bit=0, descricao=f"UG{self.id}_RT_SAIDAS_DIGITAIS - bit 00")

        self.leitura_alarme_temp_oleo_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_OLEO_UHRV"], bit=6, descricao=f"UG{self.id}_ALM_TEMP_OLEO_UHRV")
        self.leitura_alarme_temp_oleo_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_OLEO_UHLM"], bit=7, descricao=f"UG{self.id}_ALM_TEMP_OLEO_UHLM")
        self.leitura_alarme_temp_mancal_guia = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_MANCAL_GUIA"], bit=5, descricao=f"UG{self.id}_ALM_TEMP_MANCAL_GUIA")
        self.leitura_temp_fase_a_gerador = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_GERADOR_FASE_A"], bit=15, descricao=f"UG{self.id}_ALM_TEMP_GERADOR_FASE_A")
        self.leitura_temp_fase_b_gerador = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_GERADOR_FASE_B"], bit=16, descricao=f"UG{self.id}_ALM_TEMP_GERADOR_FASE_B")
        self.leitura_temp_fase_c_gerador = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_GERADOR_FASE_C"], bit=17, descricao=f"UG{self.id}_ALM_TEMP_GERADOR_FASE_C")
        self.leitura_alarme_temp_ponte_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_PONTE_FASE_A"], bit=0, descricao=f"UG{self.id}_ALM_TEMP_PONTE_FASE_A")
        self.leitura_alarme_temp_ponte_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_PONTE_FASE_B"], bit=1, descricao=f"UG{self.id}_ALM_TEMP_PONTE_FASE_B")
        self.leitura_alarme_temp_ponte_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_PONTE_FASE_C"], bit=2, descricao=f"UG{self.id}_ALM_TEMP_PONTE_FASE_C")
        self.leitura_unidade_manutencao_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_UHRV_UNIDADE_EM_MANUTENCAO"], bit=0, descricao=f"UG{self.id}_UHRV_UNIDADE_EM_MANUTENCAO")
        self.leitura_unidade_manutencao_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_UHLM_UNIDADE_EM_MANUTENCAO"], bit=4, descricao=f"UG{self.id}_UHLM_UNIDADE_EM_MANUTENCAO")
        self.leitura_alarme_temp_trafo_excitacao = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_TRAFO_EXCITACAO"], bit=4, descricao=f"UG{self.id}_ALM_TEMP_TRAFO_EXCITACAO")
        self.leitura_escovas_gastas_polo_positivo = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ESCOVAS_GASTAS_POLO_POSITIVO"], bit=5, descricao=f"UG{self.id}_ESCOVAS_GASTAS_POLO_POSITIVO")
        self.leitura_escovas_gastas_polo_negativo = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ESCOVAS_GASTAS_POLO_NEGATIVO"], bit=6, descricao=f"UG{self.id}_ESCOVAS_GASTAS_POLO_NEGATIVO")
        self.leitura_alarme_temp_mancal_casq_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_CASQ_MANCAL_COMBINADO"], bit=8, descricao=f"UG{self.id}_ALM_TEMP_CASQ_MANCAL_COMBINADO")
        self.leitura_alarme_vibra_detec_vertical = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_VIBRACAO_DETECCAO_VERTICAL"], bit=29, descricao=f"UG{self.id}_ALM_VIBRACAO_DETECCAO_VERTICAL")
        self.leitura_alarme_vibra_detec_horizontal = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_VIBRACAO_DETECCAO_HORIZONTAL"], bit=28, descricao=f"UG{self.id}_ALM_VIBRACAO_DETECCAO_HORIZONTAL")
        self.leitura_alarme_temp_mancal_guia_interno_1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_1_MANCAL_GUIA_INTERNO"], bit=12, descricao=f"UG{self.id}_ALM_TEMP_1_MANCAL_GUIA_INTERNO")
        self.leitura_alarme_temp_mancal_guia_interno_2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_2_MANCAL_GUIA_INTERNO"], bit=13, descricao=f"UG{self.id}_ALM_TEMP_2_MANCAL_GUIA_INTERNO")
        self.leitura_alarme_temp_patins_1_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_1_PATINS_MANCAL_COMBINADO"], bit=10, descricao=f"UG{self.id}_ALM_TEMP_1_PATINS_MANCAL_COMBINADO")
        self.leitura_alarme_temp_patins_2_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_2_PATINS_MANCAL_COMBINADO"], bit=11, descricao=f"UG{self.id}_ALM_TEMP_2_PATINS_MANCAL_COMBINADO")
        self.leitura_alarme_vibra_eixo_x_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_VIBRACAO_EIXO_X_MANCAL_COMBINADO"], bit=24, descricao=f"UG{self.id}_ALM_VIBRACAO_EIXO_X_MANCAL_COMBINADO")
        self.leitura_alarme_vibra_eixo_y_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_VIBRACAO_EIXO_Y_MANCAL_COMBINADO"], bit=25, descricao=f"UG{self.id}_ALM_VIBRACAO_EIXO_Y_MANCAL_COMBINADO")
        self.leitura_alarme_vibra_eixo_z_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_VIBRACAO_EIXO_Z_MANCAL_COMBINADO"], bit=26, descricao=f"UG{self.id}_ALM_VIBRACAO_EIXO_Z_MANCAL_COMBINADO")
        self.leitura_alarme_temp_mancal_con_esc_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO"], bit=9, descricao=f"UG{self.id}_ALM_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO")
        self.leitura_alarme_temp_nucleo_estatorico_gerador = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_ALM_TEMP_GERADOR_NUCLEO_ESTATORICO"], bit=14, descricao=f"UG{self.id}_ALM_TEMP_GERADOR_NUCLEO_ESTATORICO")


        # CONDICIONADORES ESSENCIAIS
        # Essenciais Temperaturas
            # Fase R
        self.leitura_temperatura_fase_R = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TEMP_GERADOR_FASE_A"], descricao=f"UG{self.id}_TEMP_GERADOR_FASE_A")
        self.condicionador_temperatura_fase_r_ug = CondicionadorExponencial(self.leitura_temperatura_fase_R, CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_r_ug)

            # Fase S
        self.leitura_temperatura_fase_S = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TEMP_GERADOR_FASE_B"], descricao=f"UG{self.id}_TEMP_GERADOR_FASE_B")
        self.condicionador_temperatura_fase_s_ug = CondicionadorExponencial(self.leitura_temperatura_fase_S, CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_s_ug)

            # Fase T
        self.leitura_temperatura_fase_T = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TEMP_GERADOR_FASE_C"])
        self.condicionador_temperatura_fase_t_ug = CondicionadorExponencial(self.leitura_temperatura_fase_T, CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_t_ug)

            # Nucleo Gerador 1
        self.leitura_temperatura_nucleo_gerador_1 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TEMP_GERADOR_NUCLEO"], descricao=f"UG{self.id}_TEMP_GERADOR_NUCLEO")
        self.condicionador_temperatura_nucleo_gerador_1_ug = CondicionadorExponencial(self.leitura_temperatura_nucleo_gerador_1, CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_gerador_1_ug)

            # Mancal Guia
        self.leitura_temperatura_mancal_guia = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TEMP_MANCAL_GUIA_GERADOR"], descricao=f"UG{self.id}_TEMP_MANCAL_GUIA_GERADOR")
        self.condicionador_temperatura_mancal_guia_ug = CondicionadorExponencial(self.leitura_temperatura_mancal_guia, CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_ug)

            # Mancal Guia Interno 1
        self.leitura_temperatura_mancal_guia_interno_1 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TEMP_1_MANCAL_GUIA_INTERNO"], descricao=f"UG{self.id}_TEMP_1_MANCAL_GUIA_INTERNO")
        self.condicionador_temperatura_mancal_guia_interno_1_ug = CondicionadorExponencial(self.leitura_temperatura_mancal_guia_interno_1, CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_interno_1_ug)

            # Mancal Guia Interno 2
        self.leitura_temperatura_mancal_guia_interno_2 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TEMP_2_MANCAL_GUIA_INTERNO"], descricao=f"UG{self.id}_TEMP_2_MANCAL_GUIA_INTERNO")
        self.condicionador_temperatura_mancal_guia_interno_2_ug = CondicionadorExponencial(self.leitura_temperatura_mancal_guia_interno_2, CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_interno_2_ug)

            # Patins Mancal combinado 1
        self.leitura_temperatura_patins_mancal_comb_1 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TEMP_1_PATINS_MANCAL_COMBINADO"], descricao=f"UG{self.id}_TEMP_1_PATINS_MANCAL_COMBINADO")
        self.condicionador_temperatura_patins_mancal_comb_1_ug = CondicionadorExponencial(self.leitura_temperatura_patins_mancal_comb_1, CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_patins_mancal_comb_1_ug)

            # Patins Mancal combinado 2
        self.leitura_temperatura_patins_mancal_comb_2 = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TEMP_2_PATINS_MANCAL_COMBINADO"], descricao=f"UG{self.id}_TEMP_2_PATINS_MANCAL_COMBINADO")
        self.condicionador_temperatura_patins_mancal_comb_2_ug = CondicionadorExponencial(self.leitura_temperatura_patins_mancal_comb_2, CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_patins_mancal_comb_2_ug)

            # Mancal Casquilho combinado
        self.leitura_temperatura_mancal_casq_comb = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TEMP_CASQ_MANCAL_COMBINADO"], descricao=f"UG{self.id}_TEMP_CASQ_MANCAL_COMBINADO")
        self.condicionador_temperatura_mancal_casq_comb_ug = CondicionadorExponencial(self.leitura_temperatura_mancal_casq_comb, CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_casq_comb_ug)

            # Mancal Contra Escora combinado
        self.leitura_temperatura_mancal_contra_esc_comb = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO"], descricao=f"UG{self.id}_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO")
        self.condicionador_temperatura_mancal_contra_esc_comb_ug = CondicionadorExponencial(self.leitura_temperatura_mancal_contra_esc_comb, CONDIC_INDISPONIBILIZAR, 100, 200)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_contra_esc_comb_ug)

        # Essenciais Pressão Turbina
            # Pressão Entrada Turbina
        self.leitura_pressao_turbina = LeituraModbus(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_PRESSAO_ENTRADA_TURBINA"], escala=0.1, descricao=f"UG{self.id}_PRESSAO_ENTRADA_TURBINA")
        self.condicionador_pressao_turbina_ug = CondicionadorExponencialReverso(self.leitura_pressao_turbina, CONDIC_INDISPONIBILIZAR, 16.1, 15.5)
        self.condicionadores_atenuadores.append(self.condicionador_pressao_turbina_ug)

        # Essenciais Padrão
        self.leitura_saidas_digitiais_rv_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_SAIDAS_DIGITAIS"], bit=0, invertido=True, descricao=f"UG{self.id}_RV_SAIDAS_DIGITAIS - bit 00")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_saidas_digitiais_rv_b0, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rv_b3 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_2"], bit=3, descricao=f"UG{self.id}_RV_FALHA_2 - bit 03")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_falha_2_rv_b3, CONDIC_NORMALIZAR))

        self.leitura_saidas_digitais_rt_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_SAIDAS_DIGITAIS"], bit=0, invertido=True, descricao=f"UG{self.id}_RT_SAIDAS_DIGITAIS - bit 00")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_saidas_digitais_rt_b0, CONDIC_NORMALIZAR))

        self.leitura_trip_rele700G_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RELE_700G_TRIP_ATUADO"], bit=31, descricao=f"UG{self.id}_RELE_700G_TRIP_ATUADO - bit 31")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_trip_rele700G_atuado, CONDIC_NORMALIZAR))

        self.leitura_rele_bloq_86EH_desatuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RELE_BLOQUEIO_86EH_DESATUADO"], bit=28, invertido=True, descricao=f"UG{self.id}_RELE_BLOQUEIO_86EH_DESATUADO - bit 28")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_rele_bloq_86EH_desatuado, CONDIC_NORMALIZAR))

        self.leitura_trip_rele_rv_naoatuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_RELE_TRIP_NAO_ATUADO"], bit=14, invertido=True, descricao=f"UG{self.id}_RV_RELE_TRIP_NAO_ATUADO - bit 14")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_trip_rele_rv_naoatuado, CONDIC_NORMALIZAR))

        self.leitura_trip_rele_rt_naoatuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_RELE_TRIP_NAO_ATUADO"], bit=23, invertido=True, descricao=f"UG{self.id}_RT_RELE_TRIP_NAO_ATUADO - bit 23")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_trip_rele_rt_naoatuado, CONDIC_NORMALIZAR))

        self.leitura_bt_emerg_naoatuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_BT_EMERGENCIA_NAO_ATUADO"], bit=11, invertido=True, descricao=f"UG{self.id}_BT_EMERGENCIA_NAO_ATUADO - bit 11")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_bt_emerg_naoatuado, CONDIC_NORMALIZAR))

        self.leitura_clp_geral_sem_bloq_exter = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CLP_GERAL_SEM_BLOQUEIO_EXTERNO"], bit=1, invertido=True, descricao=f"UG{self.id}_CLP_GERAL_SEM_BLOQUEIO_EXTERNO - bit 1")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_clp_geral_sem_bloq_exter, CONDIC_NORMALIZAR))

        self.leitura_bloq_86M_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_BLOQUEIO_86M_ATUADO"], bit=31, descricao=f"UG{self.id}_BLOQUEIO_86M_ATUADO - bit 31")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_bloq_86M_atuado, CONDIC_NORMALIZAR))

        self.leitura_bloq_86E_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_BLOQUEIO_86E_ATUADO"], bit=31, descricao=f"UG{self.id}_BLOQUEIO_86E_ATUADO - bit 31")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_bloq_86E_atuado, CONDIC_NORMALIZAR))

        self.leitura_bloq_86H_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_BLOQUEIO_86H_ATUADO"], bit=31, descricao=f"UG{self.id}_BLOQUEIO_86H_ATUADO - bit 31")
        self.condicionadores_essenciais.append(CondicionadorBase(self.leitura_bloq_86H_atuado, CONDIC_NORMALIZAR))


        # CONDICIONADORES
        # Padrão
        self.leitura_falha_1_rv_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=0, descricao=f"UG{self.id}_RV_FALHA_1 - bit 00")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rv_b0, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=1, descricao=f"UG{self.id}_RV_FALHA_1 - bit 01")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rv_b1, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=2, descricao=f"UG{self.id}_RV_FALHA_1 - bit 02")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rv_b2, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b3 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=3, descricao=f"UG{self.id}_RV_FALHA_1 - bit 03")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rv_b3, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b4 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=4, descricao=f"UG{self.id}_RV_FALHA_1 - bit 04")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rv_b4, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b5 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=5, descricao=f"UG{self.id}_RV_FALHA_1 - bit 05")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rv_b5, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b10 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=10, descricao=f"UG{self.id}_RV_FALHA_1 - bit 10")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rv_b10, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b11 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=11, descricao=f"UG{self.id}_RV_FALHA_1 - bit 11")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rv_b11, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b12 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=12, descricao=f"UG{self.id}_RV_FALHA_1 - bit 12")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rv_b12, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rv_b13 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_1"], bit=13, descricao=f"UG{self.id}_RV_FALHA_1 - bit 13")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rv_b13, CONDIC_NORMALIZAR))

        self.leitura_alarme_1_rt_b8 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_ALARMES_1"], bit=8, descricao=f"UG{self.id}_RT_ALARMES_1 - bit 08")
        self.condicionadores.append(CondicionadorBase(self.leitura_alarme_1_rt_b8, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rt_b1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=1, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 01")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b1, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rt_b2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=2, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 02")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b2, CONDIC_NORMALIZAR))

        self.leitura_falha_1_rt_b3 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=3, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 03")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b3, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rt_b2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_2"], bit=2, descricao=f"UG{self.id}_RT_FALHAS_2 - bit 02")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rt_b2, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rt_b5 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_2"], bit=5, descricao=f"UG{self.id}_RT_FALHAS_2 - bit 05")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rt_b5, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rt_b6 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_2"], bit=6, descricao=f"UG{self.id}_RT_FALHAS_2 - bit 06")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rt_b6, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rt_b7 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_2"], bit=7, descricao=f"UG{self.id}_RT_FALHAS_2 - bit 07")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rt_b7, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rt_b10 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_2"], bit=10, descricao=f"UG{self.id}_RT_FALHAS_2 - bit 10")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rt_b10, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rt_b11 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_2"], bit=11, descricao=f"UG{self.id}_RT_FALHAS_2 - bit 11")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rt_b11, CONDIC_NORMALIZAR))

        self.leitura_falha_2_rt_b12 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_2"], bit=12, descricao=f"UG{self.id}_RT_FALHAS_2 - bit 12")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rt_b12, CONDIC_NORMALIZAR))

        self.leitura_falha_boREG_CLPa_1_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_UHRV_BOREG_CLPA_1_FALHA"], bit=0, descricao=f"UG{self.id}_UHRV_BOREG_CLPA_1_FALHA - bit 00")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_boREG_CLPa_1_uhrv, CONDIC_NORMALIZAR))

        self.leitura_falha_boREG_CLPa_2_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_UHRV_BOREG_CLPA_2_FALHA"], bit=2, descricao=f"UG{self.id}_UHRV_BOREG_CLPA_2_FALHA - bit 02")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_boREG_CLPa_2_uhrv, CONDIC_NORMALIZAR))

        self.leitura_falha_boREG_CLPa_1_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_UHLM_BOREG_CLPA_1_FALHA"], bit=4, descricao=f"UG{self.id}_UHLM_BOREG_CLPA_1_FALHA - bit 04")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_boREG_CLPa_1_uhlm, CONDIC_NORMALIZAR))

        self.leitura_falha_boREG_CLPa_2_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_UHLM_BOREG_CLPA_2_FALHA"], bit=6, descricao=f"UG{self.id}_UHLM_BOREG_CLPA_2_FALHA - bit 06")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_boREG_CLPa_2_uhlm, CONDIC_NORMALIZAR))

        self.leitura_alarme_rele_rv_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_RELE_ALARME_ATUADO"], bit=15, descricao=f"UG{self.id}_RV_RELE_ALARME_ATUADO - bit 15")
        self.condicionadores.append(CondicionadorBase(self.leitura_alarme_rele_rv_atuado, CONDIC_NORMALIZAR))

        self.leitura_sistema_agua_clp_geral_ok = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CLP_GERAL_SISTEMA_AGUA_OK"], bit=2, invertido=True, descricao=f"UG{self.id}_CLP_GERAL_SISTEMA_AGUA_OK - bit 02")
        self.condicionadores.append(CondicionadorBase(self.leitura_sistema_agua_clp_geral_ok, CONDIC_NORMALIZAR))

        self.leitura_clp_geral_com_tens_barra_essenc = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_CLP_GERAL_COM_TENSAO_BARRA_ESSENCIAIS"], bit=3, invertido=True, descricao=f"UG{self.id}_CLP_GERAL_COM_TENSAO_BARRA_ESSENCIAIS - bit 03")
        self.condicionadores.append(CondicionadorBase(self.leitura_clp_geral_com_tens_barra_essenc, CONDIC_NORMALIZAR))

        self.leitura_disparo_mecanico_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_DISPARO_MECANICO_ATUADO"], bit=9, descricao=f"UG{self.id}_DISPARO_MECANICO_ATUADO - bit 09")
        self.condicionadores.append(CondicionadorBase(self.leitura_disparo_mecanico_atuado, CONDIC_NORMALIZAR))

        self.leitura_disparo_mecanico_desatuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_DISPARO_MECANICO_DESATUADO"], bit=8, invertido=True, descricao=f"UG{self.id}_DISPARO_MECANICO_DESATUADO - bit 08")
        self.condicionadores.append(CondicionadorBase(self.leitura_disparo_mecanico_desatuado, CONDIC_NORMALIZAR))

        self.leitura_falha_habilitar_sistema_agua = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_HABILITAR_SISTEMA_AGUA"], bit=11, descricao=f"UG{self.id}_FALHA_HABILITAR_SISTEMA_AGUA - bit 11")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_habilitar_sistema_agua, CONDIC_NORMALIZAR))

        self.leitura_trip_temp_oleo_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_OLEO_UHLM"], bit=4, descricao=f"UG{self.id}_TRIP_TEMP_OLEO_UHLM - bit 04")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_oleo_uhlm, CONDIC_NORMALIZAR))

        self.leitura_trip_temp_oleo_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_OLEO_UHRV"], bit=5, descricao=f"UG{self.id}_TRIP_TEMP_OLEO_UHRV - bit 05")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_oleo_uhrv, CONDIC_NORMALIZAR))

        self.leitura_parada_bloq_abertura_disj = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_PARADA_BLOQUEIO_ABERTURA_DISJUNTOR"], bit=11, descricao=f"UG{self.id}_PARADA_BLOQUEIO_ABERTURA_DISJUNTOR - bit 11")
        self.condicionadores.append(CondicionadorBase(self.leitura_parada_bloq_abertura_disj, CONDIC_NORMALIZAR))

        self.leitura_parada_bloq_descarga_pot = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_PARADA_BLOQUEIO_DESCARGA_POTENCIA"], bit=10, descricao=f"UG{self.id}_PARADA_BLOQUEIO_DESCARGA_POTENCIA - bit 10")
        self.condicionadores.append(CondicionadorBase(self.leitura_parada_bloq_descarga_pot, CONDIC_NORMALIZAR))

        self.leitura_falha_pressao_linha_b1_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_UHLM_FALHA_PRESSAO_LINHA_B1"], bit=9, descricao=f"UG{self.id}_UHLM_FALHA_PRESSAO_LINHA_B1 - bit 09")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_pressao_linha_b1_uhlm, CONDIC_NORMALIZAR))

        self.leitura_falha_pressao_linha_b2_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_UHLM_FALHA_PRESSAO_LINHA_B2"], bit=10, descricao=f"UG{self.id}_UHLM_FALHA_PRESSAO_LINHA_B2 - bit 10")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_pressao_linha_b2_uhlm, CONDIC_NORMALIZAR))

        self.leitura_falha_pressostato_linha_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_UHLM_FALHA_PRESSOSTATO_LINHA"], bit=11, descricao=f"UG{self.id}_UHLM_FALHA_PRESSOSTATO_LINHA - bit 11")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_pressostato_linha_uhlm, CONDIC_NORMALIZAR))

        self.leitura_falha_habilitar_rv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_HABILITAR_RV"], bit=0, descricao=f"UG{self.id}_RV_FALHA_HABILITAR_RV - bit 00")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_habilitar_rv, CONDIC_NORMALIZAR))

        self.leitura_falha_partir_rv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_PARTIR_RV"], bit=1, descricao=f"UG{self.id}_RV_FALHA_PARTIR_RV - bit 01")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_partir_rv, CONDIC_NORMALIZAR))

        self.leitura_falha_desabilitar_rv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_DESABILITAR_RV"], bit=2, descricao=f"UG{self.id}_RV_FALHA_DESABILITAR_RV - bit 02")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_desabilitar_rv, CONDIC_NORMALIZAR))

        self.leitura_falha_habilitar_rt = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHA_HABILITAR"], bit=16, descricao=f"UG{self.id}_RT_FALHA_HABILITAR - bit 16")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_habilitar_rt, CONDIC_NORMALIZAR))

        self.leitura_falha_partir_rt = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHA_PARTIR"], bit=17, descricao=f"UG{self.id}_RT_FALHA_PARTIR - bit 17")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_partir_rt, CONDIC_NORMALIZAR))

        self.leitura_alarme_1_rt_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_ALARMES_1"], bit=0, descricao=f"UG{self.id}_RT_ALARMES_1 - bit 00")
        self.condicionadores.append(CondicionadorBase(self.leitura_alarme_1_rt_b0, CONDIC_INDISPONIBILIZAR))

        self.leitura_alarme_1_rt_b4 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_ALARMES_1"], bit=4, descricao=f"UG{self.id}_RT_ALARMES_1 - bit 04")
        self.condicionadores.append(CondicionadorBase(self.leitura_alarme_1_rt_b4, CONDIC_INDISPONIBILIZAR))

        self.leitura_alarme_1_rt_b5 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_ALARMES_1"], bit=5, descricao=f"UG{self.id}_RT_ALARMES_1 - bit 05")
        self.condicionadores.append(CondicionadorBase(self.leitura_alarme_1_rt_b5, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=0, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 00")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b0, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b4 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=4, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 04")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b4, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b5 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=5, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 05")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b5, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b6 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=6, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 06")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b6, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b7 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=7, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 07")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b7, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b8 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=8, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 08")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b8, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b9 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=9, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 09")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b9, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b10 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=10, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 10")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b10, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b11 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=11, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 11")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b11, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b12 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=12, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 12")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b12, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b13 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=13, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 13")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b13, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b14 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=14, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 14")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b14, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_1_rt_b15 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHAS_1"], bit=15, descricao=f"UG{self.id}_RT_FALHAS_1 - bit 15")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_1_rt_b15, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rt_b0 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHAS_2"], bit=0, descricao=f"UG{self.id}_RV_FALHAS_2 - bit 00")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rt_b0, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rt_b1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHAS_2"], bit=1, descricao=f"UG{self.id}_RV_FALHAS_2 - bit 01")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rt_b1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rt_b3 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHAS_2"], bit=3, descricao=f"UG{self.id}_RV_FALHAS_2 - bit 03")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rt_b3, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rt_b4 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHAS_2"], bit=4, descricao=f"UG{self.id}_RV_FALHAS_2 - bit 04")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rt_b4, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rt_b8 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHAS_2"], bit=8, descricao=f"UG{self.id}_RV_FALHAS_2 - bit 08")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rt_b8, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rt_b9 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHAS_2"], bit=9, descricao=f"UG{self.id}_RV_FALHAS_2 - bit 09")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rt_b9, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rv_b1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHAS_2"], bit=1, descricao=f"UG{self.id}_RV_FALHAS_2 - bit 01")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rv_b1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_2_rv_b2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHAS_2"], bit=2, descricao=f"UG{self.id}_RV_FALHAS_2 - bit 02")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_2_rv_b2, CONDIC_INDISPONIBILIZAR))

        self.leitura_rele_700G_bf_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RELE_700G_BF_ATUADO"], bit=0, descricao=f"UG{self.id}_RELE_700G_BF_ATUADO - bit 00")
        self.condicionadores.append(CondicionadorBase(self.leitura_rele_700G_bf_atuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_sup_tensao_125vcc = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_SUPERVISAO_TENSAO_125VCC"], bit=29, invertido=True, descricao=f"UG{self.id}_SUPERVISAO_TENSAO_125VCC - bit 29")
        self.condicionadores.append(CondicionadorBase(self.leitura_sup_tensao_125vcc, CONDIC_INDISPONIBILIZAR))

        self.leitura_sup_tensao_24vcc = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_SUPERVISAO_TENSAO_24VCC"], bit=30, invertido=True, descricao=f"UG{self.id}_SUPERVISAO_TENSAO_24VCC - bit 30")
        self.condicionadores.append(CondicionadorBase(self.leitura_sup_tensao_24vcc, CONDIC_INDISPONIBILIZAR))

        self.leitura_sup_bobina_52g = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_SUPERVISAO_BOBINA_52G"], bit=12, invertido=True, descricao=f"UG{self.id}_SUPERVISAO_BOBINA_52G - bit 12")
        self.condicionadores.append(CondicionadorBase(self.leitura_sup_bobina_52g, CONDIC_INDISPONIBILIZAR))

        self.leitura_sup_bobina_86eh = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_SUPERVISAO_BOBINA_86EH"], bit=13, invertido=True, descricao=f"UG{self.id}_SUPERVISAO_BOBINA_86EH - bit 13")
        self.condicionadores.append(CondicionadorBase(self.leitura_sup_bobina_86eh, CONDIC_INDISPONIBILIZAR))

        self.leitura_disj_125vcc_fechados = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_DISJUNTORES_125VCC_FECHADOS"], bit=31, invertido=True, descricao=f"UG{self.id}_DISJUNTORES_125VCC_FECHADOS - bit 31")
        self.condicionadores.append(CondicionadorBase(self.leitura_disj_125vcc_fechados, CONDIC_INDISPONIBILIZAR))

        self.leitura_disj_24vcc_fechados = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_DISJUNTORES_24VCC_FECHADOS"], bit=0, invertido=True, descricao=f"UG{self.id}_DISJUNTORES_24VCC_FECHADOS - bit 00")
        self.condicionadores.append(CondicionadorBase(self.leitura_disj_24vcc_fechados, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_ponte_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_PONTE_FASE_A"], bit=0, descricao=f"UG{self.id}_FALHA_TEMP_PONTE_FASE_A - bit 00")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_ponte_fase_a, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_ponte_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_PONTE_FASE_B"], bit=1, descricao=f"UG{self.id}_FALHA_TEMP_PONTE_FASE_B - bit 01")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_ponte_fase_b, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_ponte_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_PONTE_FASE_C"], bit=2, descricao=f"UG{self.id}_FALHA_TEMP_PONTE_FASE_C - bit 02")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_ponte_fase_c, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_trafo_excita = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_TRAFO_EXCITACAO"], bit=4, descricao=f"UG{self.id}_FALHA_TEMP_TRAFO_EXCITACAO - bit 04")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_trafo_excita, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_mancal_guia = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_MANCAL_GUIA"], bit=5, descricao=f"UG{self.id}_FALHA_TEMP_MANCAL_GUIA - bit 05")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_mancal_guia, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_oleo_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_OLEO_UHRV"], bit=6, descricao=f"UG{self.id}_FALHA_TEMP_OLEO_UHRV - bit 06")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_oleo_uhrv, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_oleo_uhlm = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_OLEO_UHLM"], bit=7, descricao=f"UG{self.id}_FALHA_TEMP_OLEO_UHLM - bit 07")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_oleo_uhlm, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_mancal_casq_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_CASQ_MANCAL_COMBINADO"], bit=8, descricao=f"UG{self.id}_FALHA_TEMP_CASQ_MANCAL_COMBINADO - bit 08")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_mancal_casq_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_mancal_con_esc_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO"], bit=9, descricao=f"UG{self.id}_FALHA_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO - bit 09")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_mancal_con_esc_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_mancal_pat_1_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_1_PATINS_MANCAL_COMBINADO"], bit=10, descricao=f"UG{self.id}_FALHA_TEMP_1_PATINS_MANCAL_COMBINADO - bit 10")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_mancal_pat_1_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_mancal_pat_2_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_2_PATINS_MANCAL_COMBINADO"], bit=11, descricao=f"UG{self.id}_FALHA_TEMP_2_PATINS_MANCAL_COMBINADO - bit 11")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_mancal_pat_2_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_mancal_guia_interno_1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_1_MANCAL_GUIA_INTERNO"], bit=12, descricao=f"UG{self.id}_FALHA_TEMP_1_MANCAL_GUIA_INTERNO - bit 12")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_mancal_guia_interno_1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_mancal_guia_interno_2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_2_MANCAL_GUIA_INTERNO"], bit=13, descricao=f"UG{self.id}_FALHA_TEMP_2_MANCAL_GUIA_INTERNO - bit 13")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_mancal_guia_interno_2, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_gerador_nucleo_esta = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_GERADOR_NUCLEO_ESTATORICO"], bit=14, descricao=f"UG{self.id}_FALHA_TEMP_GERADOR_NUCLEO_ESTATORICO - bit 14")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_gerador_nucleo_esta, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_gerador_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_GERADOR_FASE_A"], bit=15, descricao=f"UG{self.id}_FALHA_TEMP_GERADOR_FASE_A - bit 15")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_gerador_fase_a, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_gerador_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_GERADOR_FASE_B"], bit=16, descricao=f"UG{self.id}_FALHA_TEMP_GERADOR_FASE_B - bit 16")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_gerador_fase_b, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_temp_gerador_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_TEMP_GERADOR_FASE_C"], bit=17, descricao=f"UG{self.id}_FALHA_TEMP_GERADOR_FASE_C - bit 17")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_temp_gerador_fase_c, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_pressao_entrada_turb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_PRESSAO_ENTRADA_TURBINA"], bit=20, descricao=f"UG{self.id}_FALHA_PRESSAO_ENTRADA_TURBINA - bit 20")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_pressao_entrada_turb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_vibra_eixo_x_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_VIBRACAO_EIXO_X_MANCAL_COMBINADO"], bit=24, descricao=f"UG{self.id}_FALHA_VIBRACAO_EIXO_X_MANCAL_COMBINADO - bit 24")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_vibra_eixo_x_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_vibra_eixo_y_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO"], bit=25, descricao=f"UG{self.id}_FALHA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO - bit 25")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_vibra_eixo_y_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_vibra_eixo_z_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO"], bit=26, descricao=f"UG{self.id}_FALHA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO - bit 26")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_vibra_eixo_z_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_vibra_detec_horizontal = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_VIBRACAO_DETECCAO_HORIZONTAL"], bit=28, descricao=f"UG{self.id}_FALHA_VIBRACAO_DETECCAO_HORIZONTAL - bit 28")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_vibra_detec_horizontal, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_vibra_detec_vertical = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_FALHA_VIBRACAO_DETECACAO_VERTICAL"], bit=29, descricao=f"UG{self.id}_FALHA_VIBRACAO_DETECACAO_VERTICAL - bit 29")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_vibra_detec_vertical, CONDIC_INDISPONIBILIZAR))

        self.leitura_bloqueio_86M_atuado = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_BLOQUEIO_86M_ATUADO"], bit=31, descricao=f"UG{self.id}_BLOQUEIO_86M_ATUADO - bit 31")
        self.condicionadores.append(CondicionadorBase(self.leitura_bloqueio_86M_atuado, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_vibra_detec_horizontal = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_VIBRACAO_DETECCAO_HORIZONTAL"], bit=21, descricao=f"UG{self.id}_TRIP_VIBRACAO_DETECCAO_HORIZONTAL - bit 21")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_vibra_detec_horizontal, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_vibra_detec_vertical = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_VIBRACAO_DETECACAO_VERTICAL"], bit=22, descricao=f"UG{self.id}_TRIP_VIBRACAO_DETECACAO_VERTICAL - bit 22")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_vibra_detec_vertical, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_vibra_eixo_x_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_VIBRACAO_EIXO_X_MANCAL_COMBINADO"], bit=23, descricao=f"UG{self.id}_TRIP_VIBRACAO_EIXO_X_MANCAL_COMBINADO - bit 23")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_vibra_eixo_x_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_vibra_eixo_y_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_VIBRACAO_EIXO_Y_MANCAL_COMBINADO"], bit=24, descricao=f"UG{self.id}_TRIP_VIBRACAO_EIXO_Y_MANCAL_COMBINADO - bit 24")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_vibra_eixo_y_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_vibra_eixo_z_mancal_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_VIBRACAO_EIXO_Z_MANCAL_COMBINADO"], bit=25, descricao=f"UG{self.id}_TRIP_VIBRACAO_EIXO_Z_MANCAL_COMBINADO - bit 25")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_vibra_eixo_z_mancal_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_ponte_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_PONTE_FASE_A"], bit=16, descricao=f"UG{self.id}_TRIP_TEMP_PONTE_FASE_A - bit 16")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_ponte_fase_a, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_ponte_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_PONTE_FASE_B"], bit=17, descricao=f"UG{self.id}_TRIP_TEMP_PONTE_FASE_B - bit 17")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_ponte_fase_b, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_ponte_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_PONTE_FASE_C"], bit=18, descricao=f"UG{self.id}_TRIP_TEMP_PONTE_FASE_C - bit 18")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_ponte_fase_c, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_gerador_fase_a = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_GERADOR_FASE_A"], bit=19, descricao=f"UG{self.id}_TRIP_TEMP_GERADOR_FASE_A - bit 19")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_gerador_fase_a, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_gerador_fase_b = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_GERADOR_FASE_B"], bit=20, descricao=f"UG{self.id}_TRIP_TEMP_GERADOR_FASE_B - bit 20")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_gerador_fase_b, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_gerador_fase_c = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_GERADOR_FASE_C"], bit=21, descricao=f"UG{self.id}_TRIP_TEMP_GERADOR_FASE_C - bit 21")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_gerador_fase_c, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_gerador_nucleo_estatorico = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_GERADOR_NUCLEO_ESTATORICO"], bit=22, descricao=f"UG{self.id}_TRIP_TEMP_GERADOR_NUCLEO_ESTATORICO - bit 22")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_gerador_nucleo_estatorico, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_gerador_saida_ar = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_GERADOR_SAIDA_AR"], bit=23, descricao=f"UG{self.id}_TRIP_TEMP_GERADOR_SAIDA_AR - bit 23")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_gerador_saida_ar, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_trafo_ateramento = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_TRAFO_ATERRAMENTO"], bit=24, descricao=f"UG{self.id}_TRIP_TEMP_TRAFO_ATERRAMENTO - bit 24")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_trafo_ateramento, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_trafo_excitacao = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_TRAFO_EXCITACAO"], bit=25, descricao=f"UG{self.id}_TRIP_TEMP_TRAFO_EXCITACAO - bit 25")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_trafo_excitacao, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_pressao_acum_uhrv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_PRESSAO_ACUMULADOR_UHRV"], bit=5, descricao=f"UG{self.id}_TRIP_PRESSAO_ACUMULADOR_UHRV - bit 05")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_pressao_acum_uhrv, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_mancal_casq_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_CASQ_MANCAL_COMBINADO"], bit=18, descricao=f"UG{self.id}_TRIP_TEMP_CASQ_MANCAL_COMBINADO - bit 18")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_mancal_casq_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_mancal_contra_esc_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO"], bit=19, descricao=f"UG{self.id}_TRIP_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO - bit 19")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_mancal_contra_esc_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_mancal_patins_1_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_1_PATINS_MANCAL_COMBINADO"], bit=20, descricao=f"UG{self.id}_TRIP_TEMP_1_PATINS_MANCAL_COMBINADO - bit 20")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_mancal_patins_1_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_mancal_patins_2_comb = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_2_PATINS_MANCAL_COMBINADO"], bit=21, descricao=f"UG{self.id}_TRIP_TEMP_2_PATINS_MANCAL_COMBINADO - bit 21")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_mancal_patins_2_comb, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_mancal_guia_interno_1 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_1_MANCAL_GUIA_INTERNO"], bit=22, descricao=f"UG{self.id}_TRIP_TEMP_1_MANCAL_GUIA_INTERNO - bit 22")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_mancal_guia_interno_1, CONDIC_INDISPONIBILIZAR))

        self.leitura_trip_temp_mancal_guia_interno_2 = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_TRIP_TEMP_2_MANCAL_GUIA_INTERNO"], bit=23, descricao=f"UG{self.id}_TRIP_TEMP_2_MANCAL_GUIA_INTERNO - bit 23")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_temp_mancal_guia_interno_2, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_fechar_distrib_rv = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RV_FALHA_FECHAR_DISTRIBUIDOR"], bit=4, descricao=f"UG{self.id}_RV_FALHA_FECHAR_DISTRIBUIDOR - bit 04")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_fechar_distrib_rv, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_desbilitar_rt = LeituraModbusBit(self.clp[f"UG{self.id}"], REG_CLP["UG"][f"UG{self.id}_RT_FALHA_DESABILITAR"], bit=18, descricao=f"UG{self.id}_RT_FALHA_DESABILITAR - bit 18")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_desbilitar_rt, CONDIC_INDISPONIBILIZAR))


        # CONDICIONADORES RELÉS
        self.leitura_trip_rele_protecao1 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_TRIP_RELE_PROTECAO"], bit=5, descricao=f"RELE_UG{self.id}_TRIP_RELE_PROTECAO")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_rele_protecao1, CONDIC_NORMALIZAR))

        self.leitura_trip_rele_protecao2 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_TRIP_RELE_PROTECAO"], bit=6, descricao=f"RELE_UG{self.id}_TRIP_RELE_PROTECAO")
        self.condicionadores.append(CondicionadorBase(self.leitura_trip_rele_protecao2, CONDIC_NORMALIZAR))

        self.leitura_subtensao_geral = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_SUBTENSAO_GERAL"], bit=0, descricao=f"RELE_UG{self.id}_SUBTENSAO_GERAL")
        self.condicionadores.append(CondicionadorBase(self.leitura_subtensao_geral, CONDIC_NORMALIZAR))

        self.leitura_subfreq_ele1 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_SUBFREQ_ELEMENTO_1"], bit=7, descricao=f"RELE_UG{self.id}_SUBFREQ_ELEMENTO_1")
        self.condicionadores.append(CondicionadorBase(self.leitura_subfreq_ele1, CONDIC_NORMALIZAR))

        self.leitura_subfreq_ele2 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_SUBFREQ_ELEMENTO_2"], bit=6, descricao=f"RELE_UG{self.id}_SUBFREQ_ELEMENTO_2")
        self.condicionadores.append(CondicionadorBase(self.leitura_subfreq_ele2, CONDIC_NORMALIZAR))

        self.leitura_sobrefreq_ele1 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_SOBREFREQ_ELEMENTO_1"], bit=5, descricao=f"RELE_UG{self.id}_SOBREFREQ_ELEMENTO_1")
        self.condicionadores.append(CondicionadorBase(self.leitura_sobrefreq_ele1, CONDIC_NORMALIZAR))

        self.leitura_sobrefreq_ele2 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_SOBREFREQ_ELEMENTO_2"], bit=4, descricao=f"RELE_UG{self.id}_SOBREFREQ_ELEMENTO_2")
        self.condicionadores.append(CondicionadorBase(self.leitura_sobrefreq_ele2, CONDIC_NORMALIZAR))

        self.leitura_sobrecorr_instant = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_SOBRECORR_INSTANTANEA"], bit=0, descricao=f"RELE_UG{self.id}_SOBRECORR_INSTANTANEA")
        self.condicionadores.append(CondicionadorBase(self.leitura_sobrecorr_instant, CONDIC_NORMALIZAR))

        self.leitura_voltz_hertz = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_VOLTZ_HERTZ"], bit=5, descricao=f"RELE_UG{self.id}_VOLTZ_HERTZ")
        self.condicionadores.append(CondicionadorBase(self.leitura_voltz_hertz, CONDIC_NORMALIZAR))

        self.leitura_perda_campo_geral = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_PERDA_CAMPO_GERAL"], bit=11, descricao=f"RELE_UG{self.id}_PERDA_CAMPO_GERAL")
        self.condicionadores.append(CondicionadorBase(self.leitura_perda_campo_geral, CONDIC_NORMALIZAR))

        self.leitura_pot_reversa = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_POTENCIA_REVERSA"], bit=3, descricao=f"RELE_UG{self.id}_POTENCIA_REVERSA")
        self.condicionadores.append(CondicionadorBase(self.leitura_pot_reversa, CONDIC_NORMALIZAR))


        self.leitura_transf_disp_rele_linha_trafo = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_TRASFER_DISPARO_RELE_LINHA_TRAFO"], bit=11, descricao=f"RELE_UG{self.id}_TRASFER_DISPARO_RELE_LINHA_TRAFO")
        self.condicionadores.append(CondicionadorBase(self.leitura_transf_disp_rele_linha_trafo, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_partida_dj_maq = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_FALHA_PARTIDA_DJ_MAQUINA"], bit=6, descricao=f"RELE_UG{self.id}_FALHA_PARTIDA_DJ_MAQUINA")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_partida_dj_maq, CONDIC_INDISPONIBILIZAR))

        self.leitura_atua_rele_86bf = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE[f"UG"][f"UG{self.id}_ATUA_RELE_86BF"], bit=8, descricao=f"RELE_UG{self.id}_ATUA_RELE_86BF")
        self.condicionadores.append(CondicionadorBase(self.leitura_atua_rele_86bf, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_abretura_dj_maq1 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_FALHA_ABETRUA_DJ_MAQUINA"], bit=7, descricao=f"RELE_UG{self.id}_FALHA_ABETRUA_DJ_MAQUINA")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_abretura_dj_maq1, CONDIC_INDISPONIBILIZAR))

        self.leitura_falha_abretura_dj_maq2 = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_FALHA_ABERTURA_DJ_MAQUINA"], bit=8, descricao=f"RELE_UG{self.id}_FALHA_ABERTURA_DJ_MAQUINA")
        self.condicionadores.append(CondicionadorBase(self.leitura_falha_abretura_dj_maq2, CONDIC_INDISPONIBILIZAR))

        self.leitura_recibo_transf_disp = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_RECIBO_TRANSFER_DISPARO"], bit=9, descricao=f"RELE_UG{self.id}_RECIBO_TRANSFER_DISPARO")
        self.condicionadores.append(CondicionadorBase(self.leitura_recibo_transf_disp, CONDIC_INDISPONIBILIZAR))

        self.leitura_difer_com_restr = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_DIFERENCIAL_COM_RESTRICAO"], bit=14, descricao=f"RELE_UG{self.id}_DIFERENCIAL_COM_RESTRICAO")
        self.condicionadores.append(CondicionadorBase(self.leitura_difer_com_restr, CONDIC_INDISPONIBILIZAR))

        self.leitura_difer_sem_restr = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_DIFERENCIAL_SEM_RESTRICAO"], bit=15, descricao=f"RELE_UG{self.id}_DIFERENCIAL_SEM_RESTRICAO")
        self.condicionadores.append(CondicionadorBase(self.leitura_difer_sem_restr, CONDIC_INDISPONIBILIZAR))

        self.leitura_fuga_sobrecorr_geral = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_FUGA_SOBRECORR_GERAL"], bit=12, descricao=f"RELE_UG{self.id}_FUGA_SOBRECORR_GERAL")
        self.condicionadores.append(CondicionadorBase(self.leitura_fuga_sobrecorr_geral, CONDIC_INDISPONIBILIZAR))

        self.leitura_sobrecorr_instant_neutro = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_SOBRECORR_INSTANTANEA_NEUTRO"], bit=1, descricao=f"RELE_UG{self.id}_SOBRECORR_INSTANTANEA_NEUTRO")
        self.condicionadores.append(CondicionadorBase(self.leitura_sobrecorr_instant_neutro, CONDIC_INDISPONIBILIZAR))

        self.leitura_sobrecorr_restr_tensao = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_SOBRECORR_RESTRICAO_TENSAO"], bit=6, descricao=f"RELE_UG{self.id}_SOBRECORR_RESTRICAO_TENSAO")
        self.condicionadores.append(CondicionadorBase(self.leitura_sobrecorr_restr_tensao, CONDIC_INDISPONIBILIZAR))

        self.leitura_sobrecorr_temp_neutro = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_SOBRECORR_TEMPORIZADA_NEUTRO"], bit=4, descricao=f"RELE_UG{self.id}_SOBRECORR_TEMPORIZADA_NEUTRO")
        self.condicionadores.append(CondicionadorBase(self.leitura_sobrecorr_temp_neutro, CONDIC_INDISPONIBILIZAR))

        self.leitura_sobrecorr_seq_neg = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_SOBRECORR_SEQUENCIA_NEG"], bit=2, descricao=f"RELE_UG{self.id}_SOBRECORR_SEQUENCIA_NEG")
        self.condicionadores.append(CondicionadorBase(self.leitura_sobrecorr_seq_neg, CONDIC_INDISPONIBILIZAR))

        self.leitura_unidade_fora_passo = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_UNIDADE_FORA_PASSO"], bit=14, descricao=f"RELE_UG{self.id}_UNIDADE_FORA_PASSO")
        self.condicionadores.append(CondicionadorBase(self.leitura_unidade_fora_passo, CONDIC_INDISPONIBILIZAR))

        self.leitura_unidade_fora_passo = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_UNIDADE_FORA_PASSO"], bit=14, descricao=f"RELE_UG{self.id}_UNIDADE_FORA_PASSO")
        self.condicionadores.append(CondicionadorBase(self.leitura_unidade_fora_passo, CONDIC_INDISPONIBILIZAR))

        self.leitura_sobretensao_geral = LeituraModbusBit(self.rele[f"UG{self.id}"], REG_RELE["UG"][f"UG{self.id}_SOBRETENSAO_GERAL"], bit=1, descricao=f"RELE_UG{self.id}_SOBRETENSAO_GERAL")
        self.condicionadores.append(CondicionadorBase(self.leitura_sobretensao_geral, CONDIC_INDISPONIBILIZAR))