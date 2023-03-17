import pytz
import logging
import traceback

import dicionarios.dict as d

from time import sleep, time
from threading import Thread
from datetime import datetime

from conector import *
from leituras import *
from condicionadores import *
from dicionarios.const import *
from dicionarios.reg import UG, MOA
from maquinas_estado.unidade_geracao import *

from clients import ClpClients

logger = logging.getLogger("__main__")

class UnidadeDeGeracao:
    def __init__(self, id: int, cfg=None, clp: ClpClients=None, con: ConectorCampo=None, db: ConectorBancoDados=None):
        # VERIFICAÇÃO DE ARGUMENTOS
        if id == 0:
            logger.exception(f"[UG{self.id}] A Unidade não pode ser instanciada com o ID -> \"0\".")
            raise ValueError
        else:
            self.__id = id

        if not cfg:
            logger.exception(f"[UG{self.id}] Não foi possível carregar o arquivo de configuração \"cfg.json\".")
            raise ValueError
        else:
            self.cfg = cfg

        if not db or not con or not clp:
            logger.warning(f"[UG{self.id}] Não foi possível carregar classes de conexão com clps | campo | banco de dados.")
            raise ConnectionError
        else:
            self.db = db
            self.con = con
            self.clp_moa = clp.clp_dict[0]
            self.clp_usn = clp.clp_dict[1]
            self.clp_ug = clp.clp_dict[f"clp_ug{self.id}"]

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS
        self.__etapa_alvo: int = 0
        self.__etapa_atual: int = 0
        self.__last_EtapaAtual: int = 0
        self.__last_EtapaAlvo: int = -1
        self.__tempo_entre_tentativas: int = 0
        self.__limite_tentativas_de_normalizacao: int = 3

        self.__next_state: object = StateDisponivel(self)

        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS
        self._setpoint: int = 0
        self._prioridade: int = 0
        self._tentativas_de_normalizacao: int = 0

        self._cx_kp: float = self.cfg["cx_kp"]
        self._cx_ki: float = self.cfg["cx_ki"]
        self._cx_kie: float = self.cfg["cx_kie"]

        self._setpoint_minimo: float = self.cfg["pot_minima"]
        self._setpoint_maximo: float = self.cfg[f"pot_maxima_ug{self.id}"]

        self._lista_ugs: list[UnidadeDeGeracao] = []

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS
        self.tempo_normalizar: int = 0

        self.cx_ajuste_ie: float = 0.1
        self.erro_press_cx: float = 0

        self.acionar_voip: bool = False
        self.limpeza_grade: bool = False
        self.release_timer: bool = False
        self.avisou_emerg_voip: bool = False
        self.normalizacao_agendada: bool = False

        self.dict: dict[str, str | bool | int | float] = d.shared_dict

        self.aux_tempo_sincronizada: datetime = 0
        self.ts_auxiliar: datetime = self.get_time()


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
        return LeituraModbus(
            f"[UG{self.id}] Potência",
            self.clp_ug,
            UG[f"UG{self.id}_RA_PM_710_Potencia_Ativa"],
            op=4,
        ).valor

    @property
    def leitura_horimetro(self) -> int:
        leitura_hora = LeituraModbus(
            UG[f"UG{self.id}_RA_Horimetro_Gerador"],
            self.clp_ug,
            op=4,
        ).valor

        leitura_min = LeituraModbus(
            UG[f"UG{self.id}_RA_Horimetro_Gerador_min"],
            self.clp_ug,
            escala=1/60,
            op=4,
        ).valor

        return LeituraSoma(
            f"[UG{self.id}] Horímetro",
            leitura_hora,
            leitura_min
        ).valor

    @property
    def leitura_caixa_espiral(self) -> float:
        return LeituraModbus(
            f"[UG{self.id}] Pressão Caixa espiral",
            self.clp_ug,
            UG[f"UG{self.id}_EA_PressK1CaixaExpiral_MaisCasas"],
            escala=0.1,
            op=4
        ).valor

    @property
    def etapa_atual(self) -> int:
        try:
            leitura = LeituraModbus(
                f"[UG{self.id}] Etapa Aux SIM",
                self.clp_ug,
                UG[f"UG{self.id}_RD_EtapaAux_Sim"],
                1,
                op=4
            ).valor

            if 0 < leitura < 255:
                self.__last_EtapaAtual = leitura
                self.__etapa_atual = leitura
                return self.__etapa_atual
            else:
                return self.__last_EtapaAtual
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível realizar a leitura da etapa atual. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    @property
    def etapa_alvo(self) -> int:
        try:
            leitura = LeituraModbus(
                f"[UG{self.id}] Etapa Alvo",
                self.clp_ug,
                UG[f"UG{self.id}_RD_EtapaAlvo_Sim"],
                1,
                op=4
            ).valor

            if 0 < leitura < 255:
                self.__last_EtapaAlvo = leitura
                self.__etapa_alvo = leitura
                return self.__etapa_alvo
            else:
                self.__last_EtapaAlvo = self.etapa_atual
                return self.__last_EtapaAlvo
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível realizar a leitura da etapa alvo. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    # Property/Setter -> VARIÁVEIS PROTEGIDAS
    @property
    def cx_kp(self) -> float:
        return self._cx_kp

    @cx_kp.setter
    def cx_kp(self, var) -> float:
        self._cx_kp = var

    @property
    def cx_ki(self) -> float:
        return self._cx_ki

    @cx_ki.setter
    def cx_ki(self, var) -> float:
        self._cx_ki = var

    @property
    def cx_kie(self) -> float:
        return self._cx_kie

    @cx_kie.setter
    def cx_kie(self, var) -> float:
        self._cx_kie = var

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
    def lista_ugs(self) -> list[UnidadeDeGeracao]:
        return self._lista_ugs

    @lista_ugs.setter
    def lista_ugs(self, var: list[UnidadeDeGeracao]) -> None:
        self._lista_ugs = var

    # Funções
    def get_time(self) -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

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
            self.clp_moa.write_single_coil(MOA[f"OUT_STATE_UG{self.id}"], [self.codigo_state])
            self.clp_moa.write_single_coil(MOA[f"OUT_ETAPA_UG{self.id}"], [self.etapa_atual])
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível escrever os valores no CLP MOA. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")

    def partir(self) -> bool:
        try:
            if self.clp_usn.read_coils(SA[f"SA_EntradasDigitais_MXI_SA_QCAP_Disj52A{self.id}Fechado"])[0] != 0:
                logger.info(f"[UG{self.id}] O Disjuntor 52A{self.id} está aberto. Favor fechá-lo para partir a UG.")
                return True

            if not self.etapa_atual == UG_SINCRONIZADA:
                logger.info(f"[UG{self.id}] Enviando comando de partida.")
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_ResetGeral"], 1)
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_ResetRele700G"], 1)
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_ResetReleBloq86H"], 1)
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_ResetReleBloq86M"], 1)
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_ResetReleRT"], 1)
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_ResetRV"], 1)
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_Cala_Sirene"], 1)
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_IniciaPartida"], 1)
                self.enviar_setpoint(self.setpoint)
            else:
                logger.debug(f"[UG{self.id}] A UG já está sincronizada.")
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_Cala_Sirene"], 1)
            return response
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível partir a UG. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def parar(self) -> bool:
        try:
            if not self.etapa_atual == UG_PARADA:
                logger.info(f"[UG{self.id}] Enviando comando de parada.")
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_AbortaPartida"], 1)
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_AbortaSincronismo"], 1)
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_Cala_Sirene"], 1)
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_IniciaParada"], 1)
                self.enviar_setpoint(0)
            else:
                logger.debug(f"[UG{self.id}] A unidade já está parada.")
                response = self.clp_ug.write_single_coil(UG["UG1_CD_Cala_Sirene"], 1)
            return response
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível partir a UG. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def enviar_setpoint(self, setpoint_kw: int) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Enviando setpoint {int(setpoint_kw)}kW.")
            self.setpoint = int(setpoint_kw)
            response = False
            if self.setpoint > 1:
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_ResetGeral"], 1)
                response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_RV_RefRemHabilita"], 1)
                response = self.clp_ug.write_single_register(UG[f"UG{self.id}_SD_SPPotAtiva"], self.setpoint)
            return response
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel enviar o setpoint. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def acionar_trips(self) -> None:
        self.acionar_trip_logico()
        self.acionar_trip_eletrico()

    def acionar_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Acionando TRIP -> Lógico.")
            response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_EmergenciaViaSuper"], 1)
            return response
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel acionar o TRIP lógico. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def remover_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Removendo TRIP -> Lógico.")
            response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_ResetGeral"], 1)
            response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_ED_ReleBloqA86HAtuado"], 0)
            response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_RD_700G_Trip"], 0)
            return response
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível remover o TRIP lógico. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def acionar_trip_eletrico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Acionando TRIP -> Elétrico.")
            response = self.clp_moa.write_single_coil(MOA[f"OUT_BLOCK_UG{self.id}"], [1])
            return response
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível acionar o TRIP elétrico. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def remover_trip_eletrico(self) -> bool:
        try:
            if self.clp_usn.read_coils(SA["SA_CD_Liga_DJ1"])[0] == 0:
                logger.debug(f"[UG{self.id}] Comando recebido -> Fechando DJ52L.")
                self.con.fechaDj52L()
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível fechar o DJ52L. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")

        try:
            logger.debug(f"[UG{self.id}] Removendo TRIP -> Elétrico.")
            response = self.clp_moa.write_single_coil(MOA[f"OUT_BLOCK_UG{self.id}"], [0])
            response = self.clp_ug.write_single_coil(UG[f"UG{self.id}_CD_Cala_Sirene"], 1)
            return response
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possível remover o TRIP elétrico. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def reconhece_reset_alarmes(self) -> bool:
        try:
            logger.info(f"[UG{self.id}] Enviando comando de reconhecer e resetar alarmes.")
            for x in range(3):
                logger.debug(f"[UG{self.id}] Tentativa: {x}/3")
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
                sleep(1)
                self.clp_moa.write_single_coil(MOA["PAINEL_LIDO"], [0])
                sleep(1)
            return True
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel enviar o comando de reconhecer e resetar alarmes. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def forcar_estado_manual(self) -> bool:
        try:
            self.__next_state = StateManual(self)
            return True
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel forçar o estado manual. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def forcar_estado_restrito(self) -> bool:
        try:
            self.__next_state = StateRestrito(self)
            return True
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel forçar o estado restrito. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def forcar_estado_indisponivel(self) -> bool:
        try:
            self.__next_state = StateIndisponivel(self)
            return True
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel forçar o estado indisponível. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def forcar_estado_disponivel(self) -> bool:
        try:
            self.reconhece_reset_alarmes()
            self.__next_state = StateDisponivel(self)
            return True
        except Exception as e:
            logger.exception(f"[UG{self.id}] Não foi possivel forçar o estado disponível. Exception: \"{repr(e)}\"")
            logger.exception(f"[UG{self.id}] Traceback: {traceback.print_stack}")
            return False

    def controle_cx_espiral(self) -> None:
        self.cx_kp = (self.leitura_caixa_espiral - self.cfg["press_cx_alvo"]) * self.cfg["cx_kp"]
        self.cx_ajuste_ie = [sum(ug.leitura_potencia) for ug in self.lista_ugs] / self.cfg["pot_maxima_alvo"]
        self.cx_ki = self.cx_ajuste_ie - self.cx_kp

        self.erro_press_cx = 0
        self.erro_press_cx = self.leitura_caixa_espiral - self.cfg["press_cx_alvo"]

        logger.debug(f"[UG{self.id}] Pressão Alvo: {self.cfg['press_cx_alvo']:0.3f}, Recente: {self.leitura_caixa_espiral:0.3f}")

        self.cx_controle_p = self.cfg["cx_kp"] * self.erro_press_cx
        self.cx_controle_i = max(min((self.cfg["cx_ki"] * self.erro_press_cx) + self.cx_controle_i, 1), 0)
        saida_pi = self.cx_controle_p + self.cx_controle_i

        logger.debug(f"[UG{self.id}] PI: {saida_pi:0.3f} <-- P: {self.cx_controle_p:0.3f} + I: {self.cx_controle_i:0.3f}; ERRO={self.erro_press_cx}")

        self.cx_controle_ie = max(min(saida_pi + self.cx_ajuste_ie * self.cfg["cx_kie"], 1), 0)

        pot_alvo = max(min(round(self.cfg[f"pot_maxima_ug{self.id}"] * self.cx_controle_ie, 5), self.cfg[f"pot_maxima_ug{self.id}"],),self.cfg["pot_minima"],)

        logger.debug(f"[UG{self.id}] Pot alvo: {pot_alvo:0.3f}")

        self.enviar_setpoint(pot_alvo) if self.leitura_caixa_espiral >= 15.5 else self.enviar_setpoint(0)