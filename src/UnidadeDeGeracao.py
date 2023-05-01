"""
Unidade de geração.

Esse módulo corresponde a implementação das unidades de geração e
da máquina de estado que rege a mesma.
"""
__version__ = "0.1"
__author__ = "Lucas Lavratti"

import pytz
import logging
import traceback

import src.mensageiro.dict as vd

from threading import Thread
from time import sleep, time
from datetime import datetime
from abc import abstractmethod
from pyModbusTCP.client import ModbusClient

from src.codes import *
from src.Leituras import *
from src.Condicionadores import *
from src.abstracao_usina import *
from src.maquinas_estado.ug import *
from src.database_connector import Database
from src.field_connector import FieldConnector

logger = logging.getLogger("__main__")


class UnidadeDeGeracao:
    def __init__(self, id: int = None, cfg: dict = None, clp: "dict[str, ModbusClient]" = None, db: Database = None, con: FieldConnector = None):

        if not cfg:
            raise ValueError
        else:
            self.cfg = cfg

        if not clp:
            logger.error(f"[UG{self.id}] Erro ao carregar conexões com CLPs Modbus")
            raise ValueError
        else:
            self.clp = clp

        if None in (db, con):
            logger.error(f"[UG{self.id}] Erro ao carregar parametros de conexão com banco e campo na classe. Reinciando intanciação interna.")
            self.db = Database()
            self.con = FieldConnector(cfg, clp)
        else:
            self.db = db
            self.cfg = cfg
            self.con = con

        # Variavéis internas (não são lidas nem escritas diretamente)
        self.__id = id

        self.__codigo_state = 0
        self.__prioridade = 0
        self.__etapa_atual = 0
        self.__last_EtapaAtual = 0

        self.__tempo_entre_tentativas = 0
        self.__limite_tentativas_de_normalizacao = 3

        self.__setpoint = 0
        self.__setpoint_minimo = 0
        self.__setpoint_maximo = 0
        self.__tentativas_de_normalizacao = 0
        
        self.pot_alvo_anterior = -1

        self.release_timer = False
        self.limpeza_grade = False
        self.enviar_trip_eletrico = False
        self.aux_tempo_sincronizada = None
        self.deve_ler_condicionadores = False

        self.__condicionadores = []
        self.__condicionadores_essenciais = []
        self.__condicionadores_atenuadores = []

        self.setpoint_minimo = self.cfg["pot_minima"]
        self.setpoint_maximo = self.cfg[f"pot_maxima_ug{self.id}"]

        self.ts_auxiliar = self.get_time()

        self.__next_state = StateDisponivel(self)

        self.codigo_state = self.__codigo_state

        vd.voip_dict = vd.voip_dict

        self.ajuste_inicial_cx_esp = -1

        self.potencia_ativa_kW = LeituraModbus(
            "Potência Usina",
            self.clp["SA"],
            REG_SA_RA_PM_810_Potencia_Ativa,
            1,
            op=4
        )

        # Leituras de operação das UGS
        self.leituras_ug: dict[str, LeituraBase] = {}

        self.leitura_potencia = LeituraModbus(
            f"ug{self.id}_Gerador_PotenciaAtivaMedia",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_RA_PM_710_Potencia_Ativa"],
            op=4,
        )
        self.leitura_setpoint = LeituraModbus(
            f"UG{self.id}_Setpoint",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_SA_SPPotAtiva"],
            op=4
        )
        self.leituras_ug[f"leitura_horimetro_hora"] = LeituraModbus(
            f"UG{self.id}_Horimetro",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_RA_Horimetro_Gerador"],
            op=4,
        )
        self.leituras_ug[f"leitura_horimetro_frac"] = LeituraModbus(
            f"ug{self.id}_Horimetro_min",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_RA_Horimetro_Gerador_min"],
            op=4,
            escala=1/60
        )
        self.leituras_ug[f"leitura_horimetro"] = LeituraSoma(
            f"ug{self.id} horímetro",
            self.leituras_ug[f"leitura_horimetro_hora"],
            self.leituras_ug[f"leitura_horimetro_frac"]
        )
        C1 = LeituraModbusCoil(
            descr=f"UG{self.id}_Sincronizada",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=UG[f"REG_UG{self.id}_ED_DisjGeradorFechado"],
        )
        C2 = LeituraModbusCoil(
            descr=f"UG{self.id}_Parando",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=UG[f"REG_UG{self.id}_RD_ParandoEmAuto"],
        )
        C3 = LeituraModbusCoil(
            descr=f"UG{self.id}_Parada",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=UG[f"REG_UG{self.id}_ED_RV_MaquinaParada"],
        )
        C4 = LeituraModbusCoil(
            descr=f"UG{self.id}_Sincronizando",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=UG[f"REG_UG{self.id}_RD_PartindoEmAuto"],
        )
        self.leituras_ug[f"leitura_Operacao_EtapaAtual"] = LeituraComposta(
            f"ug{self.id}_Operacao_EtapaAtual",
            leitura1=C1,
            leitura2=C2,
            leitura3=C3,
            leitura4=C4,
        )

        # Leituras para envio de torpedo voip
        self.leitura_voip: dict[str, LeituraBase] = {}

        self.leitura_voip["leitura_ED_FreioPastilhaGasta"] = LeituraModbusCoil(
            "ED_FreioPastilhaGasta",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_FreioPastilhaGasta"]
        )
        self.leitura_voip["leitura_ED_FiltroPresSujo75Troc"] = LeituraModbusCoil(
            "ED_FiltroPresSujo75Troc",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_FiltroPresSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_FiltroRetSujo75Troc"] = LeituraModbusCoil(
            "ED_FiltroRetSujo75Troc",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_FiltroRetSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_UHLMFilt1PresSujo75Troc"] = LeituraModbusCoil(
            "ED_UHLMFilt1PresSujo75Troc",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_UHLM_Filt1PresSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_UHLMFilt2PresSujo75Troc"] = LeituraModbusCoil(
            "ED_UHLMFilt2PresSujo75Troc",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_UHLM_Filt2PresSujo75Troc"]
        )
        self.leitura_voip["leitura_ED_FiltroPressaoBbaMecSj75"] = LeituraModbusCoil(
            "ED_FiltroPressaoBbaMecSj75",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_FiltroPressaoBbaMecSj75"]
        )
        self.leitura_voip["leitura_ED_TripPartRes"] = LeituraModbusCoil(
            "ED_TripPartRes",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_TripPartRes"]
        )
        self.leitura_voip["leitura_ED_FreioCmdRemoto"] = LeituraModbusCoil(
            "ED_FreioCmdRemoto",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_FreioCmdRemoto"]
        )
        self.leitura_voip[f"leitura_ED_QCAUG{self.id}_Remoto"] = LeituraModbusCoil(
            f"ED_QCAUG{self.id}_Remoto",
            self.clp[f"UG{self.id}"],
            UG[f"REG_UG{self.id}_ED_QCAUG{self.id}_Remoto"]
        )

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
            response = self.leituras_ug[f"leitura_Operacao_EtapaAtual"].valor
            if response == 1:
                return UNIDADE_SINCRONIZADA
            elif 2 <= response <= 3:
                return UNIDADE_PARANDO
            elif 4 <= response <= 7:
                return UNIDADE_PARADA
            elif 8 <= response <= 15:
                return UNIDADE_SINCRONIZANDO
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
    def lista_ugs(self) -> "list[UnidadeDeGeracao]":
        return self._lista_ugs

    @lista_ugs.setter
    def lista_ugs(self, var: "list[UnidadeDeGeracao]") -> None:
        self._lista_ugs = var


    @staticmethod
    def get_time() -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def modbus_update_state_register(self) -> None:
        self.clp["MOA"].write_single_register(self.cfg[f"REG_MOA_OUT_STATE_UG{self.id}"], self.codigo_state)
        self.clp["MOA"].write_single_register(self.cfg[f"REG_MOA_OUT_ETAPA_UG{self.id}"], self.etapa_atual)

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
            if not self.clp[f"UG{self.id}"].read_discrete_inputs(UG[f"REG_UG{self.id}_COND_PART"], 1)[0]:
                logger.debug(f"[UG{self.id}] Máquina sem condição de partida. Irá partir quando as condições forem reestabelecidas.")
                return True

            elif self.clp["SA"].read_coils(REG_SA_ED_SA_QCAP_Disj52A1Fechado)[0] != 0:
                logger.info(f"[UG{self.id}] O Disjuntor 52A1 está aberto. Para partir a máquina, o mesmo deverá ser fechado.")
                return True

            elif not self.etapa_atual == UNIDADE_SINCRONIZADA:
                logger.info(f"[UG{self.id}] Enviando comando de partida.")
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetGeral"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetRele700G"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetReleBloq86H"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetReleBloq86M"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetReleRT"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetRV"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_IniciaPartida"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_Cala_Sirene"], 1)

            else:
                logger.debug(f"[UG{self.id}] A unidade já está sincronizada.")
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_Cala_Sirene"], 1)
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o comando de partida.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def parar(self) -> bool:
        try:
            if not self.etapa_atual == UNIDADE_PARADA:
                logger.info(f"[UG{self.id}] Enviando comando de parada.")
                response = False
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_AbortaPartida"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_AbortaSincronismo"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_IniciaParada"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_Cala_Sirene"], 1)
                self.enviar_setpoint(self.setpoint)
            else:
                logger.debug(f"[UG{self.id}] A unidade já está parada.")
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_Cala_Sirene"], 1)
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
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetGeral"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_RV_RefRemHabilita"], 1)
                response = self.clp[f"UG{self.id}"].write_single_register(UG[f"REG_UG{self.id}_SA_SPPotAtiva"], self.setpoint)
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o setpoint.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def acionar_trip_eletrico(self) -> bool:
        try:
            self.enviar_trip_eletrico = True
            logger.debug(f"[UG{self.id}] Acionando sinal de TRIP -> Elétrico.")

            self.clp["MOA"].write_single_coil(self.cfg[f"REG_MOA_OUT_BLOCK_UG{self.id}"], [1])
            return True

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível acionar o TRIP -> Elétrico.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def remover_trip_eletrico(self) -> bool:
        try:
            self.enviar_trip_eletrico = False
            logger.debug(f"[UG{self.id}] Removendo sinal de TRIP -> Elétrico.")

            self.clp["MOA"].write_single_coil(self.cfg["REG_PAINEL_LIDO"], [0])
            self.clp["MOA"].write_single_coil(self.cfg[f"REG_MOA_OUT_BLOCK_UG{self.id}"], [0])
            self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_Cala_Sirene"], [1])

            if self.clp["SA"].read_coils(REG_SA_CD_Liga_DJ1)[0] == 0:
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
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_EmergenciaViaSuper"], [1])
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível acionar o TRIP -> Lógico.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def remover_trip_logico(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Removendo sinal de TRIP -> Lógico.")
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetGeral"], 1)
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetReleBloq86H"], 1)
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetReleBloq86M"], 1)
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetRele700G"], 1)
            response = self.clp["SA"].write_single_coil(REG_SA_CD_ResetRele59N, 1)
            response = self.clp["SA"].write_single_coil(REG_SA_CD_ResetRele787, 1)
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_ED_ReleBloqA86HAtuado"], 0)
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_ED_ReleBloqA86MAtuado"], 0)
            response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_RD_700G_Trip"], 0)
            return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível remover o TRIP -> Lógico.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

    def reconhece_reset_alarmes(self) -> bool:
        try:
            logger.debug(f"[UG{self.id}] Enviando comando de reconhece alarmes e reset.")
            self.clp["MOA"].write_single_coil(self.cfg["REG_PAINEL_LIDO"], [0])

            for _ in range(3):
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
                sleep(1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_ResetGeral"], 1)
                response = self.clp[f"UG{self.id}"].write_single_coil(UG[f"REG_UG{self.id}_CD_Cala_Sirene"], 1)
                sleep(1)
                return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o comando de reconhese alarmes e reset.")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return False

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

    def leituras_temporizadas(self) -> None:
        if self.leitura_voip["leitura_ED_FreioPastilhaGasta"].valor != 0 and not vd.voip_dict[f"FREIO_PASTILHA_GASTA_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor de Freio da UG retornou que a Pastilha está gasta, favor considerar troca.")
            vd.voip_dict[f"FREIO_PASTILHA_GASTA_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_FreioPastilhaGasta"].valor == 0 and vd.voip_dict[f"FREIO_PASTILHA_GASTA_UG{self.id}"]:
            vd.voip_dict[f"FREIO_PASTILHA_GASTA_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_FiltroPresSujo75Troc"].valor != 0 and not vd.voip_dict[f"FILTRO_PRES_SUJO_75_TROC_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor do Filtro de Pressão UHRV retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"FILTRO_PRES_SUJO_75_TROC_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_FiltroPresSujo75Troc"].valor == 0 and vd.voip_dict[f"FILTRO_PRES_SUJO_75_TROC_UG{self.id}"]:
            vd.voip_dict[f"FILTRO_PRES_SUJO_75_TROC_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_FiltroRetSujo75Troc"].valor != 0 and not vd.voip_dict[f"FILTRO_RET_SUJO_75_TROC_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor do Filtro de Retorno UHRV retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"FILTRO_RET_SUJO_75_TROC_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_FiltroRetSujo75Troc"].valor == 0 and vd.voip_dict[f"FILTRO_RET_SUJO_75_TROC_UG{self.id}"]:
            vd.voip_dict[f"FILTRO_RET_SUJO_75_TROC_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_UHLMFilt1PresSujo75Troc"].valor != 0 and not vd.voip_dict[f"UHLM_FILTR_1_PRES_SUJO_75_TROC_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor do Filtro 1 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"UHLM_FILTR_1_PRES_SUJO_75_TROC_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_UHLMFilt1PresSujo75Troc"].valor == 0 and vd.voip_dict[f"UHLM_FILTR_1_PRES_SUJO_75_TROC_UG{self.id}"]:
            vd.voip_dict[f"UHLM_FILTR_1_PRES_SUJO_75_TROC_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_UHLMFilt2PresSujo75Troc"].valor != 0 and not vd.voip_dict[f"UHLM_FILTR_2_PRES_SUJO_75_TROC_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor do Filtro 2 de Pressão UHLM retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"UHLM_FILTR_2_PRES_SUJO_75_TROC_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_UHLMFilt2PresSujo75Troc"].valor == 0 and vd.voip_dict[f"UHLM_FILTR_2_PRES_SUJO_75_TROC_UG{self.id}"]:
            vd.voip_dict[f"UHLM_FILTR_2_PRES_SUJO_75_TROC_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_FiltroPressaoBbaMecSj75"].valor != 0 and not vd.voip_dict[f"FILTRO_PRESSAO_BBA_MEC_SJ_75_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor do Filtro de Pressão da Bomba Mecânica retornou que o filtro está 75% sujo, favor considerar troca.")
            vd.voip_dict[f"FILTRO_PRESSAO_BBA_MEC_SJ_75_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_FiltroPressaoBbaMecSj75"].valor == 0 and vd.voip_dict[f"FILTRO_PRESSAO_BBA_MEC_SJ_75_UG{self.id}"]:
            vd.voip_dict[f"FILTRO_PRESSAO_BBA_MEC_SJ_75_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_TripPartRes"].valor != 0 and not vd.voip_dict[f"TRIP_PART_RES_UG{self.id}"]:
            logger.warning(f"[UG{self.id}] O sensor TripPartRes retornou valor 1.")
            vd.voip_dict[f"TRIP_PART_RES_UG{self.id}"] = True
        elif self.leitura_voip["leitura_ED_TripPartRes"].valor == 0 and vd.voip_dict[f"TRIP_PART_RES_UG{self.id}"]:
            vd.voip_dict[f"TRIP_PART_RES_UG{self.id}"] = False

        if self.leitura_voip["leitura_ED_FreioCmdRemoto"].valor != 1:
            logger.debug(f"[UG{self.id}] O freio da UG saiu do modo remoto, favor analisar a situação.")

        if self.leitura_voip[f"leitura_ED_QCAUG{self.id}_Remoto"].valor != 1:
            logger.debug(f"[UG{self.id}] O compressor da UG saiu do modo remoto, favor analisar a situação.")