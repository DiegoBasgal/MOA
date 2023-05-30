import pytz
import logging
import traceback

import src.dicionarios.dict as d

from time import sleep, time
from threading import Thread
from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *

import src.ocorrencias as oco_ug
from src.condicionadores import *
from src.funcoes.leitura import *
from src.maquinas_estado.ug import *

from src.banco_dados import BancoDados
from src.funcoes.escrita import EscritaModBusBit as EMB


logger = logging.getLogger("__main__")

class UnidadeDeGeracao:
    def __init__(self, id: int, cfg=None, clp: "dict[str, ModbusClient]"=None, db: BancoDados=None):
        # VERIFICAÇÃO DE ARGUMENTOS
        if id <= 0:
            logger.error(f"[UG{self.id}] A Unidade não pode ser instanciada com o ID <= \"0\" ou vazio.")
            raise ValueError
        else:
            self.__id = id

        self.db = db
        self.cfg = cfg
        self.clp = clp
        self.oco = oco_ug.OcorrenciasUg(self.id, self.clp)

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS
        self.__etapa_atual: int = 0
        self.__ultima_etapa_atual: int = 0
        self.__tempo_entre_tentativas: int = 0
        self.__limite_tentativas_de_normalizacao: int = 3

        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS
        self._setpoint: int = 0
        self._prioridade: int = 0
        self._tentativas_de_normalizacao: int = 0

        self._setpoint_minimo: float = self.cfg["pot_minima"]
        self._setpoint_maximo: float = self.cfg[f"pot_maxima_ug{self.id}"]

        self._lista_ugs: "list[UnidadeDeGeracao]" = []

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS
        self.tempo_normalizar: int = 0

        self.parar_timer: bool = False
        self.borda_parar: bool = False
        self.acionar_voip: bool = False
        self.limpeza_grade: bool = False
        self.release_timer: bool = False
        self.borda_partindo: bool = False
        self.avisou_emerg_voip: bool = False
        self.normalizacao_agendada: bool = False

        self.aux_tempo_sincronizada: datetime = 0
        self.ts_auxiliar: datetime = self.get_time()

        self._leitura_potencia = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_RELE["UG"][f"RELE_UG{self.id}_P"],
            op=3,
            descr=f"[UG{self.id}] Potência Ativa"
        )
        self._leitura_potencia_reativa = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_RELE["UG"][f"RELE_UG{self.id}_Q"],
            op=3,
            descr=f"[UG{self.id}] Potência Reativa"
        )
        self._leitura_potencia_aparente = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_RELE["UG"][f"RELE_UG{self.id}_S"],
            op=3,
            descr=f"[UG{self.id}] Potência Aparente"
        )
        self._leitura_etapa_atual = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}_ED_STT_PASSO_ATUAL"],
            op=3,
            descr=f"[UG{self.id}] Etapa Atual"
        )

    # Property -> VARIÁVEIS PRIVADAS
    @property
    def id(self) -> int:
        return self.__id

    @property
    def manual(self) -> bool:
        return isinstance(self.__next_state, StateManual)

    @property
    def restrito(self) -> bool:
        return isinstance(self.__next_state, StateRestrito)

    @property
    def disponivel(self) -> bool:
        return isinstance(self.__next_state, StateDisponivel)

    @property
    def indisponivel(self) -> bool:
        return isinstance(self.__next_state, StateIndisponivel)

    @property
    def tempo_entre_tentativas(self) -> int:
        return self.__tempo_entre_tentativas

    @property
    def limite_tentativas_de_normalizacao(self) -> int:
        return self.__limite_tentativas_de_normalizacao

    @property
    def leitura_potencia(self) -> float:
        return self._leitura_potencia.valor

    @property
    def etapa_atual(self) -> int:
        try:
            leitura = self._leitura_etapa_atual.valor

            if leitura == 0:
                self.__etapa_atual = UG_PARADA
                self.__ultima_etapa_atual = self.__etapa_atual

            elif 0 < leitura < 10:
                self.__etapa_atual = UG_SINCRONIZANDO
                self.__ultima_etapa_atual = self.__etapa_atual

            elif 10 < leitura < 28:
                self.__etapa_atual = UG_PARANDO
                self.__ultima_etapa_atual = self.__etapa_atual

            elif leitura == 10:
                self.__etapa_atual = UG_SINCRONIZADA
                self.__ultima_etapa_atual = self.__etapa_atual
            
            else:
                logger.info(f"[UG{self.id}] Unidade em etapa inconsistente ({self.__etapa_atual}). Mantendo valor anterior -> \"{UG_STR_DCT_ETAPAS[self.__ultima_etapa_atual]}\"")
                return self.__ultima_etapa_atual

            return self.__etapa_atual

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar a leitura da etapa atual. Mantendo etapa anterior")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return self.__ultima_etapa_atual

    # Property/Setter -> VARIÁVEIS PROTEGIDAS
    @property
    def codigo_state(self) -> int:
        return self._codigo_state

    @codigo_state.setter
    def codigo_state(self, var) -> int:
        self._codigo_state = var

    @property
    def prioridade(self) -> int:
        return self._prioridade

    @prioridade.setter
    def prioridade(self, var) -> None:
        self._prioridade = var

    @property
    def setpoint(self) -> int:
        return self._setpoint

    @setpoint.setter
    def setpoint(self, var: int):
        if var < self.setpoint_minimo:
            self._setpoint = 0
        elif var > self.setpoint_maximo:
            self._setpoint = self.setpoint_maximo
        else:
            self._setpoint = int(var)
        logger.debug(f"[UG{self.id}] SP<-{var}")

    @property
    def setpoint_minimo(self) -> int:
        return self._setpoint_minimo

    @setpoint_minimo.setter
    def setpoint_minimo(self, var: int):
        self._setpoint_minimo = var

    @property
    def setpoint_maximo(self) -> int:
        return self._setpoint_maximo

    @setpoint_maximo.setter
    def setpoint_maximo(self, var: int):
        self._setpoint_maximo = var

    @property
    def tentativas_de_normalizacao(self) -> int:
        return self._tentativas_de_normalizacao

    @tentativas_de_normalizacao.setter
    def tentativas_de_normalizacao(self, var: int):
        if 0 <= var and var == int(var):
            self._tentativas_de_normalizacao = int(var)
        else:
            raise ValueError(f"[UG{self.id}] Valor deve se um inteiro positivo")

    @property
    def lista_ugs(self) -> "list[UnidadeDeGeracao]":
        return self._lista_ugs

    @lista_ugs.setter
    def lista_ugs(self, var: "list[UnidadeDeGeracao]") -> None:
        self._lista_ugs = var

    # Funções
    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def forcar_estado_manual(self) -> None:
        self.__next_state = StateManual(self)

    def forcar_estado_restrito(self) -> None:
        self.__next_state = StateRestrito(self)

    def forcar_estado_indisponivel(self) -> None:
        self.__next_state = StateIndisponivel(self)

    def forcar_estado_disponivel(self) -> None:
        self.reconhece_reset_alarmes()
        self.__next_state = StateDisponivel(self)

    def iniciar_ultimo_estado(self) -> None:
        estado = self.db.get_ultimo_estado_ug(self.id)

        if not estado:
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
                logger.error(f"[UG{self.id}] Não foi possível ler o último estado da Unidade. Entrando em modo Manual.")
                self.__next_state = StateManual(self)

    # TODO -> Adicionar após a integração do CLP do MOA no painel do SA, que depende da intervenção da Automatic.
    def atualizar_modbus_moa(self) -> None:
        return
        self.clp["MOA"].write_single_register(REG_MOA[f"OUT_ETAPA_UG{self.id}"], self.etapa_atual)
        self.clp["MOA"].write_single_register(REG_MOA[f"OUT_STATE_UG{self.id}"], self.codigo_state)

    def desabilitar_manutencao(self) -> None:
        try:
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_RV_MANUTENCAO"], 0)
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_RV_AUTOMATICO"], 1)
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_UHRV_MODO_MANUTENCAO"], 0)
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_UHRV_MODO_AUTOMATICO"], 1)
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_UHLM_MODO_MANUTENCAO"], 0)
            EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_UHLM_MODO_AUTOMATICO"], 1)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível desabilitar o modo de manutenção das unidades de operação.")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")


    def espera_normalizar(self, delay: int):
        while not self.parar_timer:
            sleep(max(0, time() + delay - time()))
            self.parar_timer = True
            return

    def normalizar_unidade(self) -> bool:
        if self.tentativas_de_normalizacao > self.limite_tentativas_de_normalizacao:
            logger.warning(f"[UG{self.id}] A UG estourou as tentativas de normalização, indisponibilizando UG.")
            return False

        elif (self.ts_auxiliar - self.get_time()).seconds > self.tempo_entre_tentativas:
            self.tentativas_de_normalizacao += 1
            self.ts_auxiliar = self.get_time()
            logger.info(f"[UG{self.id}] Normalizando UG (Tentativa {self.tentativas_de_normalizacao}/{self.limite_tentativas_de_normalizacao})")
            self.reconhece_reset_alarmes()
            return True

    def bloquear_unidade(self) -> None:
        if self.etapa_atual == UG_PARADA:
            self.acionar_trip_logico()
            self.acionar_trip_eletrico()

        elif not self.borda_parar and self.parar():
            self.borda_parar = True

        else:
            logger.debug(f"[UG{self.id}] Unidade Parando")

    def step(self) -> None:
        try:
            logger.debug(f"[UG{self.id}] Step -> (Tentativas de normalização: {self.tentativas_de_normalizacao}/{self.limite_tentativas_de_normalizacao}).")
            self.__next_state = self.__next_state.step()
            self.atualizar_modbus_moa()

        except Exception:
            logger.error(f"[UG{self.id}] Erro na execução da máquina de estados da Unidade -> step.")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")

    def partir(self) -> bool:
        return None
        try:
            if not self.desabilitar_manutencao():
                logger.info(f"[UG{self.id}] Não foi possível enviar o comando de desativação do modo de manutenção dos equipamentos")

            elif self.clp["SA"].read_coils(REG_SA[f"SA_ED_PSA_DIJS_TSA_FECHADO"], 26)[0] == 0:
                logger.info(f"[UG{self.id}] O Disjuntor do Serviço Auxiliar está aberto.")
                return True

            elif self.clp["SA"].read_coils(REG_SA[f"SA_ED_PSA_DIJS_GMG_FECHADO"], 27)[0] == 1:
                logger.info(f"[UG{self.id}] O Disjuntor do Grupo Motor Gerador está fechado.")

            elif not self.etapa_atual == UG_SINCRONIZADA:
                logger.info(f"[UG{self.id}] Enviando comando de partida.")
                res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_REARME_FALHAS"], 1)
                res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_SINCRONISMO"], 1)
                self.enviar_setpoint(self.setpoint)

            else:
                logger.debug(f"[UG{self.id}] A UG já está sincronizada.")

            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível partir a UG.")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def parar(self) -> bool:
        return None
        try:
            if not self.etapa_atual == UG_PARADA:
                logger.info(f"[UG{self.id}] Enviando comando de parada.")
                res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_PARADA_TOTAL"], 1)
                self.enviar_setpoint(0)

            else:
                logger.debug(f"[UG{self.id}] A unidade já está parada.")

            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível parar a UG.")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def enviar_setpoint(self, setpoint_kw: int) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Enviando setpoint {int(setpoint_kw)}kW.")
            self.setpoint = int(setpoint_kw)

            if self.setpoint > 1:
                res = self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}_RV_SETPOINT_POTENCIA_ATIVA_PU"], self.setpoint)

            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o setpoint.")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def acionar_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Acionando TRIP -> Lógico.")
            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_PARADA_EMERGENCIA"], 1)
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel acionar o TRIP -> Lógico.")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def remover_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Removendo TRIP -> Lógico.")
            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_REARME_FALHAS"], 1)
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível remover o TRIP -> Lógico.")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def acionar_trip_eletrico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Acionando TRIP -> Elétrico.")
            res = None # self.clp["MOA"].write_single_coil(REG_MOA[f"OUT_BLOCK_UG{self.id}"], [1])
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível acionar o TRIP -> Elétrico.")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def remover_trip_eletrico(self) -> bool:
        try:
            if self.clp["SA"].read_coils(REG_SA["SA_CD_DISJ_LINHA_FECHA"])[0] == 0:
                logger.debug(f"[UG{self.id}] Comando recebido -> Fechando Disjuntor de Linha.")
                self.fechar_dj_linha()

            logger.debug(f"[UG{self.id}] Removendo TRIP -> Elétrico.")
            res = None # self.clp["MOA"].write_single_coil(REG_MOA[f"OUT_BLOCK_UG{self.id}"], [0])
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível remover o TRIP -> Elétrico.")
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
                # self.clp["MOA"].write_single_coil(REG_MOA["PAINEL_LIDO"], [0])
                sleep(1)

            return True

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o comando de reconhecer e resetar alarmes.")
            logger.debug(f"[UG{self.id}] Traceback: {traceback.format_exc()}")
            return False

    def controle_etapas(self) -> None:
        # PARANDO
        if self.etapa_atual == UG_PARANDO:
            if self.setpoint >= self.setpoint_minimo:
                self.enviar_setpoint(self.setpoint)

        # SINCRONIZANDO
        elif self.etapa_atual == UG_SINCRONIZANDO:
            if not self.borda_partindo:
                logger.debug(f"[UG{self.id}] Iniciando o timer de verificação de partida")
                Thread(target=lambda: self.verificar_partida()).start()
                self.borda_partindo = True

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        # PARADA
        elif self.etapa_atual == UG_PARADA:
            if self.setpoint >= self.setpoint_minimo:
                self.partir()
                self.enviar_setpoint(self.setpoint)

        # SINCRONIZADA
        elif self.etapa_atual == UG_SINCRONIZADA:
            self.borda_partindo = False

            if not self.aux_tempo_sincronizada:
                self.aux_tempo_sincronizada = self.get_time()

            elif (self.get_time() - self.aux_tempo_sincronizada).seconds >= 300:
                self.tentativas_de_normalizacao = 0

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        # CONTROLE TEMPO SINCRONIZADAS
        if not self.etapa_atual == UG_SINCRONIZADA:
            self.aux_tempo_sincronizada = None

    def verificar_partida(self) -> None:
        while time() < (time() + 600):
            if self.etapa_atual == UG_SINCRONIZADA or self.release_timer:
                logger.debug(f"[UG{self.id}] Condição de saída ativada! Verificação de partida encerrada.")
                return

        logger.debug(f"[UG{self.id}] Verificação de partida estourou o timer, acionando normalização.")
        self.borda_partindo = False
        EMB.escrever_bit(self.clp[f"UG{self.id}"], [f"UG{self.id}_CD_CMD_PARADA_EMERGENCIA"], 1)
        sleep(1)
        EMB.escrever_bit(self.clp[f"UG{self.id}"], [f"UG{self.id}_CD_CMD_REARME_FALHAS"], 1)