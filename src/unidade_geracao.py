import pytz
import logging
import traceback

import src.mensageiro.dict as vd

from time import sleep
from datetime import datetime
from pyModbusTCP.client import ModbusClient

from src.usina import *
from src.dicionarios.const import *
from src.funcoes.leitura import *
from src.condicionadores import *
from src.maquinas_estado.ug import *

from src.banco_dados import Database
from src.conector import ConectorCampo

logger = logging.getLogger("__main__")


class UnidadeGeracao:
    def __init__(self, id: int = None, cfg: dict = None, clp: "dict[str, ModbusClient]" = None, db: Database = None, con: ConectorCampo = None):

        if not id or id < 1:
            logger.error(f"[UG{self.id}] O id não pode ser Nulo ou menor que 1")
            raise ValueError
        else:
            self.__id = id

        if not clp:
            logger.error(f"[UG{self.id}] Erro ao carregar conexões com CLPs Modbus")
            raise ValueError
        else:
            self.clp = clp

        self.db = db
        self.con = con
        self.cfg = cfg


        self.__prioridade = 0
        self.__codigo_state = 0
        self.__last_EtapaAtual = 0

        self.__tempo_entre_tentativas = 0
        self.__limite_tentativas_de_normalizacao = 3

        self.__setpoint = 0
        self.__setpoint_minimo = 0
        self.__setpoint_maximo = 0
        self.__tentativas_de_normalizacao = 0

        self.__condicionadores = []
        self.__condicionadores_essenciais = []
        self.__condicionadores_atenuadores = []

        self.tempo_normalizar = 0
        self.pot_alvo_anterior = -1
        self.ajuste_inicial_cx_esp = -1

        self.release = False
        self.parar_timer = False
        self.limpeza_grade = False
        self.borda_partindo = False
        self.norma_agendada = False
        self.timer_partindo = False
        self.enviar_trip_eletrico = False
        self.aux_tempo_sincronizada = None
        self.deve_ler_condicionadores = False

        self.setpoint_minimo = self.cfg["pot_minima"]
        self.setpoint_maximo = self.cfg[f"pot_maxima_ug{self.id}"]

        self.ts_auxiliar = self.get_time()

        self.leituras_iniciais()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def manual(self) -> bool:
        return isinstance(self.__next_state, StateManual)

    @property
    def disponivel(self) -> bool:
        return isinstance(self.__next_state, StateDisponivel)

    @property
    def etapa_atual(self) -> int:
        try:
            response = self.leitura_etapa_atual.valor
            if response == 1:
                return UG_SINCRONIZADA
            elif 2 <= response <= 3:
                return UG_PARANDO
            elif 4 <= response <= 7:
                return UG_PARADA
            elif 8 <= response <= 15:
                return UG_SINCRONIZANDO
            else:
                return self.__last_EtapaAtual

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar a leitura de Etapa Atual.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return self.__last_EtapaAtual

    @property
    def tempo_entre_tentativas(self) -> int:
        return self.__tempo_entre_tentativas

    @property
    def limite_tentativas_de_normalizacao(self) -> int:
        return self.__limite_tentativas_de_normalizacao

    @property
    def prioridade(self) -> int:
        return self.__prioridade

    @prioridade.setter
    def prioridade(self, var) -> None:
        self.__prioridade = var

    @property
    def codigo_state(self) -> int:
        return self.__codigo_state

    @codigo_state.setter
    def codigo_state(self, var) -> None:
        self.__codigo_state = var

    @property
    def setpoint(self) -> int:
        return self.__setpoint

    @setpoint.setter
    def setpoint(self, var: int):
        if var < self.setpoint_minimo:
            self.__setpoint = 0
        elif var > self.setpoint_maximo:
            self.__setpoint = self.setpoint_maximo
        else:
            self.__setpoint = int(var)
        logger.debug(f"[UG{self.id}] SP<-{var}")

    @property
    def setpoint_minimo(self) -> int:
        return self.__setpoint_minimo

    @setpoint_minimo.setter
    def setpoint_minimo(self, var: int):
        self.__setpoint_minimo = var

    @property
    def setpoint_maximo(self) -> int:
        return self.__setpoint_maximo

    @setpoint_maximo.setter
    def setpoint_maximo(self, var: int):
        self.__setpoint_maximo = var

    @property
    def tentativas_de_normalizacao(self) -> int:
        return self.__tentativas_de_normalizacao

    @tentativas_de_normalizacao.setter
    def tentativas_de_normalizacao(self, var: int):
        self.__tentativas_de_normalizacao = var

    @property
    def condicionadores(self) -> "list[CondicionadorBase]":
        return self.__condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[CondicionadorBase]") -> None:
        self.__condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        return self.__condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]") -> None:
        self.__condicionadores_essenciais = var

    @property
    def condicionadores_atenuadores(self) -> "list[CondicionadorBase]":
        return self.__condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: "list[CondicionadorBase]") -> None:
        self.__condicionadores_atenuadores = var

    @property
    def lista_ugs(self) -> "list[UnidadeGeracao]":
        return self._lista_ugs

    @lista_ugs.setter
    def lista_ugs(self, var: "list[UnidadeGeracao]") -> None:
        self._lista_ugs = var


    @staticmethod
    def get_time() -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def modbus_update_state_register(self) -> None:
        self.clp["MOA"].write_single_register(REG[f"MOA_OUT_STATE_UG{self.id}"], self.codigo_state)
        self.clp["MOA"].write_single_register(REG[f"MOA_OUT_ETAPA_UG{self.id}"], self.etapa_atual)

    def forcar_estado_disponivel(self) -> None:
        try:
            self.reconhece_reset_alarmes()
            sleep(1)
            self.__next_state = StateDisponivel(self)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível forçar o estado \"Disponível\".")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def forcar_estado_indisponivel(self) -> None:
        try:
            self.__next_state = StateIndisponivel(self)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível forçar o estado \"Indisponível\".")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def forcar_estado_manual(self) -> None:
        try:
            self.__next_state = StateManual(self)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível forçar o estado \"Manual\".")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def forcar_estado_restrito(self) -> None:
        try:
            self.__next_state = StateRestrito(self)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível forçar o estado \"Restrito\".")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def iniciar_ultimo_estado(self) -> None:
        estado = self.db.get_ultimo_estado_ug(self.id)

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
                logger.error(f"[UG{self.id}] Não foi possível ler o último estado da Unidade. Entrando em modo Manual.")
                self.__next_state = StateManual(self)

    def step(self) -> None:
        try:
            logger.debug("")
            logger.debug(f"[UG{self.id}] Step. (Tentativas de normalização: {self.tentativas_de_normalizacao}/{self.limite_tentativas_de_normalizacao})")
            self.__next_state = self.__next_state.step()
            self.modbus_update_state_register()

        except Exception:
            logger.error(f"[UG{self.id}] Erro na execução da Máquina de estados da UG.")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def partir(self) -> bool:
        try:
            if not self.clp[f"UG{self.id}"].read_discrete_inputs(REG[f"UG{self.id}_ED_CondicaoPartida"], 1)[0]:
                logger.debug(f"[UG{self.id}] Máquina sem condição de partida. Irá partir quando as condições forem reestabelecidas.")
                return True

            elif self.clp["SA"].read_coils(REG["SA_ED_QCAP_Disj52A1Fechado"])[0] != 0:
                logger.info(f"[UG{self.id}] O Disjuntor 52A1 está aberto. Para partir a máquina, o mesmo deverá ser fechado.")
                return True

            elif not self.etapa_atual == UG_SINCRONIZADA:
                logger.info(f"[UG{self.id}] Enviando comando de partida.")
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetGeral"], [1])
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetRele700G"], [1])
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleBloq86H"], [1])
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleBloq86M"], [1])
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleRT"], [1])
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetRV"], [1])
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_IniciaPartida"], [1])
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])

            else:
                logger.debug(f"[UG{self.id}] A unidade já está sincronizada.")
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o comando de partida.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def parar(self) -> bool:
        try:
            if not self.etapa_atual == UG_PARADA:
                logger.info(f"[UG{self.id}] Enviando comando de parada.")
                response = False
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_AbortaPartida"], [1])
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_AbortaSincronismo"], [1])
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_IniciaParada"], [1])
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])
                self.enviar_setpoint(self.setpoint)
            else:
                logger.debug(f"[UG{self.id}] A unidade já está parada.")
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o comando de parada.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def enviar_setpoint(self, setpoint_kw: int) -> bool:
        try:
            response = False
            if self.limpeza_grade:
                self.setpoint_minimo = self.cfg["pot_limpeza_grade"]
            else:
                self.setpoint_minimo = self.cfg["pot_minima"]
            self.setpoint_maximo = self.cfg[f"pot_maxima_ug{self.id}"]

            logger.debug(f"[UG{self.id}] Enviando setpoint {int(self.setpoint)} kW.")

            if self.setpoint > 1:
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetGeral"], [1])
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_RV_RefRemHabilita"], [1])
                response = self.clp[f"UG{self.id}"].write_single_register(REG[f"UG{self.id}_RA_ReferenciaCarga"], self.setpoint)
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o setpoint.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def bloquear_ug(self) -> None:
        self.parar_timer = True

        if self.etapa_atual == UG_PARADA:
            self.acionar_trip_eletrico()
            self.acionar_trip_logico()
        elif not self.borda_parar and self.parar():
            self.borda_parar = True
        else:
            logger.debug(f"[UG{self.id}] Unidade parando.")

    def normalizar_ug(self) -> bool:
        if (self.tentativas_de_normalizacao > self.limite_tentativas_de_normalizacao):
            logger.warning(f"[UG{self.id}] Indisponibilizando UG por tentativas de normalização.")
            return False

        elif self.etapa_atual == UG_PARANDO or self.etapa_atual == UG_SINCRONIZANDO:
            logger.debug(f"[UG{self.id}] Esperando para normalizar")
            return True

        elif (self.ts_auxiliar - self.get_time()).seconds > self.tempo_entre_tentativas:
            self.tentativas_de_normalizacao += 1
            self.ts_auxiliar = self.get_time()
            logger.info(f"[UG{self.id}] Normalizando UG (Tentativa {self.tentativas_de_normalizacao}/{self.limite_tentativas_de_normalizacao}).")
            self.reconhece_reset_alarmes()
            return True

    def acionar_trip_eletrico(self) -> bool:
        try:
            self.enviar_trip_eletrico = True
            logger.debug(f"[UG{self.id}] Acionando sinal de TRIP -> Elétrico.")

            self.clp["MOA"].write_single_coil(REG[f"MOA_OUT_BLOCK_UG{self.id}"], [1])
            return True

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível acionar o TRIP -> Elétrico.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def remover_trip_eletrico(self) -> bool:
        try:
            self.enviar_trip_eletrico = False
            logger.debug(f"[UG{self.id}] Removendo sinal de TRIP -> Elétrico.")

            self.clp["MOA"].write_single_coil(REG["PAINEL_LIDO"], [0])
            self.clp["MOA"].write_single_coil(REG[f"MOA_OUT_BLOCK_UG{self.id}"], [0])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])

            if self.clp["SA"].read_coils(REG["SA_CD_Liga_DJ1"])[0] == 0:
                logger.debug(f"[UG{self.id}] Comando recebido -> Fechar Dj52L")
                self.con.fechaDj52L()
            return True

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível remover o TRIP -> Elétrico.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def acionar_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Acionando sinal de TRIP -> Lógico.")
            response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_EmergenciaViaSuper"], [1])
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível acionar o TRIP -> Lógico.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def remover_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Removendo sinal de TRIP -> Lógico.")
            response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetGeral"], [1])
            response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleBloq86H"], [1])
            response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleBloq86M"], [1])
            response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetRele700G"], [1])
            response = self.clp["SA"].write_single_coil(REG["SA_CD_ResetRele59N"], [1])
            response = self.clp["SA"].write_single_coil(REG["SA_CD_ResetRele787"], [1])
            response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_ED_ReleBloqA86HAtuado"], [0])
            response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_ED_ReleBloqA86MAtuado"], [0])
            response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_RD_700G_Trip"], [0])
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível remover o TRIP -> Lógico.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def reconhece_reset_alarmes(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Enviando comando de reconhece alarmes e reset.")
            self.clp["MOA"].write_single_coil(REG["PAINEL_LIDO"], [0])

            for _ in range(3):
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
                sleep(1)
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetGeral"], [1])
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])
                sleep(1)
                return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o comando de reconhese alarmes e reset.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def controle_etapas(self) -> None:
        if self.etapa_atual == UG_PARANDO:
            if self.setpoint >= self.setpoint_minimo:
                self.enviar_setpoint(self.setpoint)

        elif self.etapa_atual == UG_SINCRONIZANDO:
            if not self.borda_partindo:
                Thread(target=lambda: self.verificar_partida()).start()
                self.borda_partindo = True

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        elif self.etapa_atual == UG_PARADA:
            if self.setpoint >= self.setpoint_minimo:
                self.partir()
                self.enviar_setpoint(self.setpoint)

        elif self.etapa_atual == UG_SINCRONIZADA:
            self.borda_partindo = False
            if not self.aux_tempo_sincronizada:
                self.aux_tempo_sincronizada = self.get_time()

            elif (self.get_time() - self.aux_tempo_sincronizada).seconds >= 300:
                self.tentativas_de_normalizacao = 0

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        if self.etapa_atual not in UG_LST_ETAPAS:
            self.inconsistente = True

        if not self.etapa_atual == UG_SINCRONIZADA:
            self.aux_tempo_sincronizada = None

    def ajuste_ganho_cx_espiral(self) -> None:
        atenuacao = 0
        for condic in self.condicionadores_atenuadores:
            atenuacao = max(atenuacao, condic.valor)
            logger.debug(f"[UG{self.id}] Atenuador \"{condic.descr}\" -> Atenuação: {atenuacao} / Leitura: {condic.leitura.valor}")

        ganho = 1 - atenuacao
        aux = self.setpoint
        if (self.setpoint > self.setpoint_minimo) and self.setpoint * ganho > self.setpoint_minimo:
            self.setpoint = self.setpoint * ganho

        elif (self.setpoint * ganho < self.setpoint_minimo) and (self.setpoint > self.setpoint_minimo):
            self.setpoint =  self.setpoint_minimo

        logger.debug(f"[UG{self.id}] SP {aux} * GANHO {ganho} = {self.setpoint}")

    def ajuste_inicial_cx(self):
        try:
            self.cx_controle_p = (self.leitura_caixa_espiral.valor - self.cfg["press_cx_alvo"]) * self.cfg["cx_kp"]
            self.cx_ajuste_ie = sum(ug.leitura_potencia for ug in self.lista_ugs) / self.cfg["pot_maxima_alvo"]
            self.cx_controle_i = self.cx_ajuste_ie - self.cx_controle_p

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar o ajuste incial do PID para pressão de caixa espiral.")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def controle_cx_espiral(self):
        if self.pot_alvo_anterior == -1:
            self.pot_alvo_anterior = pot_alvo

        if self.ajuste_inicial_cx_esp == -1:
            self.ajuste_inicial_cx()
            self.ajuste_inicial_cx_esp = 0

        try:
            self.erro_press_cx = 0
            self.erro_press_cx = self.leitura_caixa_espiral.valor - self.cfg["press_cx_alvo"]

            logger.debug(f"[UG{self.id}] Pressão Alvo: {self.cfg['press_cx_alvo']:0.3f}, Recente: {self.leitura_caixa_espiral.valor:0.3f}")

            self.cx_controle_p = self.cfg["cx_kp"] * self.erro_press_cx
            self.cx_controle_i = max(min((self.cfg["cx_ki"] * self.erro_press_cx) + self.cx_controle_i, 1), 0)
            saida_pi = self.cx_controle_p + self.cx_controle_i

            logger.debug(f"[UG{self.id}] PI: {saida_pi:0.3f} <-- P:{self.cx_controle_p:0.3f} + I:{self.cx_controle_i:0.3f}; ERRO={self.erro_press_cx}")

            self.cx_controle_ie = max(min(saida_pi + self.cx_ajuste_ie * self.cfg["cx_kie"], 1), 0)
            pot_alvo = max(min(round(self.cfg[f"pot_maxima_ug{self.id}"] * self.cx_controle_ie, 5), self.cfg[f"pot_maxima_ug{self.id}"],),self.cfg["pot_minima"],)

            logger.debug(f"[UG{self.id}] Pot alvo: {pot_alvo:0.3f}")

            pot_medidor = self.potencia_ativa_kW.valor

            logger.debug(f"Potência alvo = {pot_alvo}")
            logger.debug(f"Potência no medidor = {pot_medidor}")

            pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])

            pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

            if pot_medidor > self.cfg["pot_maxima_alvo"] * 0.97:
                pot_alvo = self.pot_alvo_anterior * (1 - 0.5 * ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))

            self.pot_alvo_anterior = pot_alvo
            self.enviar_setpoint(pot_alvo) if self.leitura_caixa_espiral.valor >= 15.5 else self.enviar_setpoint(0)

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro no método de Controle por Caixa Espiral da Unidade.")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def verificar_partida(self) -> None:
        timer = time() + 600
        logger.debug(f"[UG{self.id}] Iniciando o timer de verificação de partida")
        while time() < timer:
            if self.etapa_atual == UG_SINCRONIZADA or self.timer_partindo:
                logger.debug(f"[UG{self.id}] Condição ativada! Saindo do timer de verificação de partida...")
                self.timer_partindo = False
                self.release = True
                return

        logger.debug(f"[UG{self.id}] A Unidade estourou o timer de verificação de partida, adicionando condição para normalizar")
        self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_EmergenciaViaSuper"], [1])
        self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_EmergenciaViaSuper"], [0])
        self.borda_partindo = False
        self.release = True

    def atualizar_limites_operacao(self, db):
        self.prioridade = int(db[f"ug{self.id}_prioridade"])
        self.condicionador_caixa_espiral_ug.valor_base = float(db[f"alerta_caixa_espiral_ug{self.id}"])
        self.condicionador_caixa_espiral_ug.valor_limite = float(db[f"limite_caixa_espiral_ug{self.id}"])


    def leituras_iniciais(self):
        # Letitura de potência total da Usina
        self.potencia_ativa_kW = LeituraModbus(
            "Potência Usina",
            self.clp["SA"],
            REG["SA_EA_PM_810_Potencia_Ativa"],
            1,
            op=4
        )

        # Leituras de operação das UGS
        self.leitura_potencia = LeituraModbus(
            f"UG{self.id}_Potência",
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_RA_PM_710_Potencia_Ativa"],
            op=4,
        )
        self.leitura_setpoint = LeituraModbus(
            f"UG{self.id}_Setpoint",
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_SA_SPPotAtiva"],
            op=4
        )
        self.leitura_horimetro_hora = LeituraModbus(
            f"UG{self.id}_Horímetro_hora",
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_RA_Horimetro_Gerador"],
            op=4,
        )
        self.leitura_horimetro_min = LeituraModbus(
            f"UG{self.id}_Horímetro_min",
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_RA_Horimetro_Gerador_min"],
            op=4,
            escala=1/60
        )
        self.leitura_horimetro = LeituraSoma(
            f"UG{self.id}_Horímetro",
            self.leitura_horimetro_hora,
            self.leitura_horimetro_min
        )
        C1 = LeituraModbusCoil(
            descr=f"UG{self.id}_Sincronizada",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=REG[f"UG{self.id}_ED_DisjGeradorFechado"],
        )
        C2 = LeituraModbusCoil(
            descr=f"UG{self.id}_Parando",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=REG[f"UG{self.id}_RD_ParandoEmAuto"],
        )
        C3 = LeituraModbusCoil(
            descr=f"UG{self.id}_Parada",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=REG[f"UG{self.id}_ED_RV_MaquinaParada"],
        )
        C4 = LeituraModbusCoil(
            descr=f"UG{self.id}_Sincronizando",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=REG[f"UG{self.id}_RD_PartindoEmAuto"],
        )
        self.leitura_etapa_atual = LeituraComposta(
            f"ug{self.id}_Operacao_EtapaAtual",
            leitura1=C1,
            leitura2=C2,
            leitura3=C3,
            leitura4=C4,
        )

        # Leituras para envio de torpedo voip
        

        # CX Espiral
        self.leitura_caixa_espiral = LeituraModbus("Caixa espiral", self.clp[f"UG{self.id}"], REG[f"UG{self.id}_EA_PressK1CaixaExpiral_MaisCasas"], escala=0.01, op=4)
        self.condicionador_caixa_espiral_ug = CondicionadorExponencialReverso(self.leitura_caixa_espiral.descr, CONDIC_INDISPONIBILIZAR, self.leitura_caixa_espiral, 16.5, 15.5)
        self.condicionadores_atenuadores.append(self.condicionador_caixa_espiral_ug)