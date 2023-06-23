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

logger = logging.getLogger("__main__")

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
        self.oco = OcorrenciasUg(self.id, self.clp, self.db)


        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__potencia_ativa_kW = LeituraModbus(
            "[USN] Potência Usina",
            self.clp["SA"],
            REG["SA_EA_PM_810_Potencia_Ativa"],
            1,
            op=4
        )
        self.__leitura_pressao_uhrv = LeituraModbus(
            f"[UG{self.id}] Leitura Pressão UHRV",
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_RA_UHRV_Pressao"],
            escala=0.1,
            op=4
        )

        self.__leitura_horimetro_hora = LeituraModbus(
            f"[UG{self.id}] Horímetro Hora",
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_RA_Horimetro_Gerador"],
            op=4,
        )
        self.__leitura_horimetro_min = LeituraModbus(
            f"[UG{self.id}] Horímetro Min",
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_RA_Horimetro_Gerador_min"],
            op=4,
            escala=1/60
        )
        __C1 = LeituraModbusCoil(
            descr=f"UG{self.id}_Sincronizada",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=REG[f"UG{self.id}_ED_DisjGeradorFechado"],
        )
        __C2 = LeituraModbusCoil(
            descr=f"UG{self.id}_Parando",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=REG[f"UG{self.id}_RD_ParandoEmAuto"],
        )
        __C3 = LeituraModbusCoil(
            descr=f"UG{self.id}_Parada",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=REG[f"UG{self.id}_ED_RV_MaquinaParada"],
        )
        __C4 = LeituraModbusCoil(
            descr=f"UG{self.id}_Sincronizando",
            modbus_client=self.clp[f"UG{self.id}"],
            registrador=REG[f"UG{self.id}_RD_PartindoEmAuto"],
        )
        self.__leitura_etapa_atual = LeituraComposta(
            f"ug{self.id}_Operacao_EtapaAtual",
            leitura1=__C1,
            leitura2=__C2,
            leitura3=__C3,
            leitura4=__C4,
        )

        self.__tempo_entre_tentativas: "int" = 0
        self.__limite_tentativas_de_normalizacao: "int" = 2

        self.__prioridade: "int" = 0
        self.__codigo_state: "int" = 0
        self.__ultima_etapa_atual: "int" = 0

        self.__setpoint: "int" = 0
        self.__setpoint_minimo: "int" = 0
        self.__setpoint_maximo: "int" = 0
        self.__tentativas_de_normalizacao: "int" = 0

        self.__condicionadores_atenuadores: "list[CondicionadorBase]" = []


        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS

        self._leitura_potencia = LeituraModbus(
            f"UG{self.id}_Potência",
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_RA_PM_710_Potencia_Ativa"],
            op=4,
        )
        self._leitura_horimetro = LeituraSoma(
            f"UG{self.id}_Horímetro",
            self.__leitura_horimetro_hora,
            self.__leitura_horimetro_min
        )
        self._leitura_caixa_espiral = LeituraModbus(
            "Caixa espiral",
            self.clp[f"UG{self.id}"],
            REG[f"UG{self.id}_EA_PressK1CaixaExpiral_MaisCasas"],
            escala=0.01,
            op=4
        )
        self.condicionador_caixa_espiral_ug = CondicionadorExponencialReverso(
            self._leitura_caixa_espiral.descr,
            CONDIC_INDISPONIBILIZAR,
            self._leitura_caixa_espiral,
            16.5,
            15.5
        )
        self.condicionadores_atenuadores.append(self.condicionador_caixa_espiral_ug)


        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.tempo_normalizar: "int" = 0
        self.pot_alvo_anterior: "int"  = -1
        self.ajuste_inicial_cx_esp: "int"  = -1

        self.release: "bool" = False
        self.parar_timer: "bool" = False
        self.borda_parar: "bool" = False
        self.limpeza_grade: "bool" = False
        self.borda_partindo: "bool" = False
        self.timer_partindo: "bool" = False
        self.normalizacao_agendada: "bool" = False

        self.setpoint_minimo: "int" = self.cfg["pot_minima"]
        self.setpoint_maximo: "int" = self.cfg[f"pot_maxima_ug{self.id}"]

        self.aux_tempo_sincronizada: "datetime" = 0

        self.ts_auxiliar: "datetime" = self.get_time()


    # Property -> VARIÁVEIS PRIVADAS

    @property
    def id(self) -> "int":
        return self.__id

    @property
    def manual(self) -> "bool":
        return isinstance(self.__next_state, StateManual)

    @property
    def restrito(self) -> "bool":
        return isinstance(self.__next_state, StateRestrito)

    @property
    def disponivel(self) -> "bool":
        return isinstance(self.__next_state, StateDisponivel)

    @property
    def indisponivel(self) -> "bool":
        return isinstance(self.__next_state, StateIndisponivel)

    @property
    def tempo_entre_tentativas(self) -> "int":
        return self.__tempo_entre_tentativas

    @property
    def limite_tentativas_de_normalizacao(self) -> "int":
        return self.__limite_tentativas_de_normalizacao

    @property
    def leitura_potencia(self) -> "int | float":
        return self._leitura_potencia.valor

    @property
    def leitura_horimetro(self) -> "int | float":
        return self._leitura_horimetro.valor

    @property
    def tempo_entre_tentativas(self) -> int:
        return self.__tempo_entre_tentativas

    @property
    def limite_tentativas_de_normalizacao(self) -> int:
        return self.__limite_tentativas_de_normalizacao

    @property
    def etapa_atual(self) -> int:
        try:
            response = self.__leitura_etapa_atual.valor
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


    # FUNÇÕES

    @staticmethod
    def get_time() -> datetime:
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def forcar_estado_manual(self) -> "None":
        self.__next_state = StateManual(self)

    def forcar_estado_restrito(self) -> "None":
        self.__next_state = StateRestrito(self)

    def forcar_estado_indisponivel(self) -> "None":
        self.__next_state = StateIndisponivel(self)

    def forcar_estado_disponivel(self) -> "None":
        self.reconhece_reset_alarmes()
        self.__next_state = StateDisponivel(self)

    def iniciar_ultimo_estado(self) -> "None":
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
        self.clp["MOA"].write_single_register(REG[f"MOA_OUT_STATE_UG{self.id}"], self.codigo_state)
        self.clp["MOA"].write_single_register(REG[f"MOA_OUT_ETAPA_UG{self.id}"], self.etapa_atual)

    def atualizar_limites_operacao(self, db) -> "None":
        self.prioridade = int(db[f"ug{self.id}_prioridade"])
        self.condicionador_caixa_espiral_ug.valor_base = float(db[f"alerta_caixa_espiral_ug{self.id}"])
        self.condicionador_caixa_espiral_ug.valor_limite = float(db[f"limite_caixa_espiral_ug{self.id}"])

    def espera_normalizar(self, delay: "int"):
        while not self.parar_timer:
            sleep(max(0, time() + delay - time()))
            self.parar_timer = True
            return

    def normalizar_unidade(self) -> "bool":
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
        if self.etapa_atual == UG_PARADA:
            self.acionar_trip_logico()
            self.acionar_trip_eletrico()

        elif not self.borda_parar and self.parar():
            self.borda_parar = True

        else:
            logger.debug(f"[UG{self.id}] Unidade Parando")

    def step(self) -> "None":
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
        try:
            if not self.clp[f"UG{self.id}"].read_discrete_inputs(REG[f"UG{self.id}_ED_CondicaoPartida"], 1)[0]:
                logger.debug(f"[UG{self.id}] Máquina sem condição de partida. Irá partir quando as condições forem reestabelecidas.")
                return True

            elif self.clp["SA"].read_coils(REG["SA_ED_QCAP_Disj52A1Fechado"])[0] != 0:
                logger.info(f"[UG{self.id}] O Disjuntor 52A1 está aberto. Para partir a máquina, o mesmo deverá ser fechado.")
                return True

            elif not self.etapa_atual == UG_SINCRONIZADA:
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARTIDA\"")
                self.clp["SA"].write_single_coil(REG["SA_CD_ResetRele59N"], [1])
                self.clp["SA"].write_single_coil(REG["SA_CD_ResetRele787"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetGeral"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetRele700G"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleBloq86H"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleBloq86M"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_ED_ReleBloqA86HAtuado"], [0])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_ED_ReleBloqA86MAtuado"], [0])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_RD_700G_Trip"], [0])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleRT"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetRV"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_IniciaPartida"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])

            else:
                logger.debug(f"[UG{self.id}] A unidade já está sincronizada.")
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o comando de partida.")
            logger.debug(traceback.format_exc())

    def parar(self) -> "None":
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

    def enviar_setpoint(self, setpoint_kw: int) -> "bool":
        try:
            if self.limpeza_grade:
                self.setpoint_minimo = self.cfg["pot_limpeza_grade"]
            else:
                self.setpoint_minimo = self.cfg["pot_minima"]
            self.setpoint_maximo = self.cfg[f"pot_maxima_ug{self.id}"]

            logger.debug(f"[UG{self.id}]          Enviando setpoint:         {int(self.setpoint)} kW")

            if self.setpoint > 1:
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetGeral"], [1])
                response = self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_RV_RefRemHabilita"], [1])
                response = self.clp[f"UG{self.id}"].write_single_register(REG[f"UG{self.id}_RA_ReferenciaCarga"], self.setpoint)
                return response

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível enviar o setpoint.")
            logger.debug(traceback.format_exc())
            return False

    def acionar_trip_eletrico(self) -> "None":
        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP ELÉTRICO\"")
            self.clp["MOA"].write_single_coil(REG[f"MOA_OUT_BLOCK_UG{self.id}"], [1])

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel acionar o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())

    def remover_trip_eletrico(self) -> "None":
        try:
            logger.debug(f"[UG{self.id}]          Removendo comando:         \"TRIP ELÉTRICO\"")

            self.clp["MOA"].write_single_coil(REG["PAINEL_LIDO"], [0])
            self.clp["MOA"].write_single_coil(REG[f"MOA_OUT_BLOCK_UG{self.id}"], [0])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])

            if self.clp["SA"].read_coils(REG["SA_CD_Liga_DJ1"])[0] == 0:
                logger.debug(f"[UG{self.id}]          Enviando comando:          \"FECHAR DJ LINHA\".")
                self.clp["SA"].write_single_coil(REG["SA_CD_Liga_DJ1"], [1])

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())

    def acionar_trip_logico(self) -> "None":
        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP LÓGICO\"")
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_EmergenciaViaSuper"], [1])

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel acionar o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())

    def remover_trip_logico(self) -> "None":
        try:
            logger.debug(f"[UG{self.id}]          Removendo comando:         \"TRIP LÓGICO\"")
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetGeral"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleBloq86H"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleBloq86M"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetRele700G"], [1])
            self.clp["SA"].write_single_coil(REG["SA_CD_ResetRele59N"], [1])
            self.clp["SA"].write_single_coil(REG["SA_CD_ResetRele787"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_ED_ReleBloqA86HAtuado"], [0])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_ED_ReleBloqA86MAtuado"], [0])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_RD_700G_Trip"], [0])


        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())

    def reconhece_reset_alarmes(self) -> "None":
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
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetGeral"], [1])
                self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_Cala_Sirene"], [1])
                sleep(1)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o comando de reconhecer e resetar alarmes.")
            logger.debug(traceback.format_exc())

    def verificar_pressao_uhrv(self) -> "None":
        if self.__leitura_pressao_uhrv.valor <= 120:
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_ResetReleBloq86H"], [1])
            self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_ED_ReleBloqA86HAtuado"], [0])

    def controle_etapas(self) -> "None":
        # PARANDO
        if self.etapa_atual == UG_PARANDO:
            if self.setpoint >= self.setpoint_minimo:
                self.enviar_setpoint(self.setpoint)

        # SINCRONIZANDO
        elif self.etapa_atual == UG_SINCRONIZANDO:
            if not self.borda_partindo:
                Thread(target=lambda: self.verificar_partida()).start()
                self.borda_partindo = True

            self.verificar_pressao_uhrv()

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

    def verificar_partida(self) -> "None":
        logger.debug(f"[UG{self.id}]          Comando MOA:               \"Iniciar timer de verificação de partida\"")
        timer = time() + 600
        while time() < timer:
            if self.etapa_atual == UG_SINCRONIZADA or self.timer_partindo:
                logger.debug(f"[UG{self.id}]          Comando MOA:               \"Encerrar timer de verificação de partida por condição verdadeira\"")
                self.timer_partindo = False
                self.release = True
                return

        logger.debug(f"[UG{self.id}]          Comando MOA:               \"Encerrar timer de verificação de partida por timeout\"")
        self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_EmergenciaViaSuper"], [1])
        self.clp[f"UG{self.id}"].write_single_coil(REG[f"UG{self.id}_CD_EmergenciaViaSuper"], [0])
        self.borda_partindo = False
        self.release = True


    def ajuste_ganho_cx_espiral(self) -> "None":
        atenuacao = 0
        for condic in self.condicionadores_atenuadores:
            atenuacao = max(atenuacao, condic.valor)
            logger.debug(f"[UG{self.id}]          Verificando Atenuadores:")
            logger.debug(f"[UG{self.id}]          - \"{condic.descr}\":         Leitura: {condic.leitura.valor} | Atenuação: {atenuacao}")

        ganho = 1 - atenuacao
        aux = self.setpoint
        if (self.setpoint > self.setpoint_minimo) and self.setpoint * ganho > self.setpoint_minimo:
            self.setpoint = self.setpoint * ganho

        elif (self.setpoint * ganho < self.setpoint_minimo) and (self.setpoint > self.setpoint_minimo):
            self.setpoint =  self.setpoint_minimo

        logger.debug(f"[UG{self.id}]                                     SP {aux} * GANHO {ganho} = {self.setpoint} kW")

    def ajuste_inicial_cx(self) -> "None":
        try:
            self.cx_controle_p = (self._leitura_caixa_espiral.valor - self.cfg["press_cx_alvo"]) * self.cfg["cx_kp"]
            self.cx_ajuste_ie = sum(ug.leitura_potencia for ug in self.lista_ugs) / self.cfg["pot_maxima_alvo"]
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
            self.erro_press_cx = self._leitura_caixa_espiral.valor - self.cfg["press_cx_alvo"]

            logger.debug(f"[UG{self.id}] Pressão Alvo: {self.cfg['press_cx_alvo']:0.3f}, Recente: {self._leitura_caixa_espiral.valor:0.3f}")

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
            self.enviar_setpoint(pot_alvo) if self._leitura_caixa_espiral.valor >= 15.5 else self.enviar_setpoint(0)

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro no método de Controle por Caixa Espiral da Unidade.")
            logger.debug(traceback.format_exc())