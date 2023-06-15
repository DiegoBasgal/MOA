import pytz
import logging
import traceback

import src.dicionarios.dict as d

from time import sleep, time
from threading import Thread
from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *

from src.condicionadores import *
from src.funcoes.leitura import *
from src.maquinas_estado.ug import *

import src.ocorrencias as oco_ug
from src.conector import ClientesUsina
from src.banco_dados import BancoDados
from src.funcoes.escrita import EscritaModBusBit as EMB


logger = logging.getLogger("__main__")

class UnidadeDeGeracao:
    def __init__(self, id: "int", cfg=None, db: "BancoDados"=None):

        # VERIFICAÇÃO DE ARGUMENTOS

        if id <= 0:
            logger.error(f"[UG{self.id}] A Unidade não pode ser instanciada com o ID <= \"0\" ou vazio.")
            raise ValueError
        else:
            self.__id = id

        self.db = db
        self.cfg = cfg
        self.rv = ClientesUsina.rv
        self.rt = ClientesUsina.rt
        self.clp = ClientesUsina.clp
        self.rele = ClientesUsina.rele
        self.oco = oco_ug.OcorrenciasUg(self.id, self.clp)


        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        # self.__etapa_alvo: "int" = 0
        # self.__etapa_atual: "int" = 0
        # self.__ultima_etapa_alvo: "int" = 0
        # self.__ultima_etapa_atual: "int" = 0
        self.__tempo_entre_tentativas: "int" = 0
        self.__limite_tentativas_de_normalizacao: "int" = 3

        self.__leitura_dj_tsa: LeituraModbusBit = LeituraModbusBit(
            self.clp["SA"],
            REG_SA["SA_ED_PSA_DIJS_TSA_FECHADO"],
            descr=f"[UG{self.id}] Status Disjuntor Serviço Auxiliar"
        )
        self.__leitura_dj_gmg = LeituraModbusBit(
            self.clp["SA"],
            REG_SA["SA_ED_PSA_DIJS_GMG_FECHADO"],
            descr=f"[UG{self.id}] Status Disjuntor Grupo Motor Gerador"
        )
        self.__leitura_dj_linha: LeituraModbusBit = LeituraModbusBit(
            self.clp["SA"],
            REG_SA["SA_ED_PSA_SE_DISJ_LINHA_FECHADO"],
            descr=f"[UG{self.id}] Status Disjuntor Linha"
        )
        self.__leitura_status_uhrv: LeituraModbusBit = LeituraModbusBit(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}_ED_UHRV_UNIDADE_HABILITADA"],
            descr=f"[UG{self.id}] Status UHRV"
        )
        self.__leitura_dj_maquina: LeituraModbusBit = LeituraModbusBit(
            self.rele[f"UG{self.id}"],
            REG["RELE"][f"UG{self.id}_ED_PRTVA_DISJUNTOR_MAQUINA_FECHADO"],
            descr=f"[UG{self.id}] Status Disjuntor de Máquina"
        )
        self.__tensao: LeituraModbus = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_RELE["UG"][f"RELE_UG{self.id}_VAB"],
            op=3,
            descr="[USN] Tensão Unidade"
        )
        """
        self.__leitura_etapa_atual: LeituraModbus = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}_ED_STT_PASSO_ATUAL_BIT"],
            op=3,
            descr=f"[UG{self.id}] Etapa Atual"
        )
        self.__leitura_etapa_alvo: LeituraModbus = LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}_ED_STT_PASSO_SELECIONADO_BIT"],
            op=3,
            descr=f"[UG{self.id}] Etapa Alvo"
        )
        """

        self.__ultima_etapa : "int" = 0
        self.__ultima_etapa_absoluta: "int" = UG_SINCRONIZADA if self.__leitura_dj_maquina.valor == 1 else UG_PARADA


        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS

        self._setpoint: "int" = 0
        self._prioridade: "int" = 0
        self._tentativas_de_normalizacao: "int" = 0

        self._setpoint_minimo: "float" = self.cfg["pot_minima"]
        self._setpoint_maximo: "float" = self.cfg[f"pot_maxima_ug{self.id}"]

        self._lista_ugs: "list[UnidadeDeGeracao]" = []

        self._leitura_potencia = LeituraModbus(
            self.rele[f"UG{self.id}"],
            REG_RELE["UG"][f"RELE_UG{self.id}_P"],
            op=3,
            descr=f"[UG{self.id}] Potência Ativa"
        )

        # self._leitura_potencia_reativa = LeituraModbus(
        #     self.rele[f"UG{self.id}"],
        #     REG_RELE["UG"][f"RELE_UG{self.id}_Q"],
        #     op=3,
        #     descr=f"[UG{self.id}] Potência Ativa"
        # )
        self._leitura_potencia_aparente = LeituraModbus(
            self.rele[f"UG{self.id}"],
            REG_RELE["UG"][f"RELE_UG{self.id}_S"],
            op=3,
            descr=f"[UG{self.id}] Potência Ativa"
        )


        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.tempo_normalizar: "int" = 0

        self.aguardar_etapa_alvo: "int" = 0
        self.aguardar_etapa_atual: "int" = 0

        self.ug_parando: "bool" = False
        self.parar_timer: "bool" = False
        self.borda_parar: "bool" = False
        self.acionar_voip: "bool" = False
        self.limpeza_grade: "bool" = False
        self.release_timer: "bool" = False
        self.borda_partindo: "bool" = False
        self.ug_sincronizando: "bool" = False
        self.avisou_emerg_voip: "bool" = False
        self.normalizacao_agendada: "bool" = False

        self.aux_tempo_sincronizada: "datetime" = 0
        self.ts_auxiliar: "datetime" = self.get_time()

        if not self.desabilitar_manutencao():
            logger.info(f"[UG{self.id}] Não foi possível enviar comando de \"Desabilitar Manutenção\"")

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

    # @property
    # def leitura_potencia_reativa(self) -> "int | float":
    #     return self._leitura_potencia_reativa.valor

    @property
    def leitura_potencia_aparente(self) -> "int | float":
        return self._leitura_potencia_aparente.valor

    @property
    def etapa(self) -> "int":
        try:
            if self.__leitura_dj_maquina.valor:
                self.__ultima_etapa_absoluta = UG_SINCRONIZADA
                self.__ultima_etapa = UG_SINCRONIZADA
                return UG_SINCRONIZADA

            elif not self.__leitura_status_uhrv.valor:
                self.__ultima_etapa_absoluta = UG_PARADA
                self.__ultima_etapa = UG_PARADA
                return UG_PARADA

            elif self.__ultima_etapa_absoluta == UG_PARADA and self.__leitura_status_uhrv:
                self.__ultima_etapa = UG_SINCRONIZANDO
                return UG_SINCRONIZANDO

            elif self.__ultima_etapa_absoluta == UG_SINCRONIZADA and not self.__leitura_dj_maquina.valor:
                self.__ultima_etapa = UG_PARANDO
                return UG_PARANDO

            else:
                logger.debug(f"[UG{self.id}] Contorle de etapas sem condições. Mantendo etapa anterior.")
                return self.__ultima_etapa

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro no controle de Etapas da Unidade. Mantendo Etapa anterior.")
            logger.debug(traceback.format_exc())
            return self.__ultima_etapa

    """
    @property
    def etapa_atual(self) -> "int":
        try:
            if self.__leitura_etapa_atual.valor == None:
                self.__etapa_atual = self.__ultima_etapa_atual
                return self.__etapa_atual
            else:
                self.__etapa_atual = self.__leitura_etapa_atual.valor
                self.__ultima_etapa_atual = self.__etapa_atual
                return self.__etapa_atual

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar a leitura da \"Etapa Atual\". Mantendo Etapa Atual anteriror.")
            logger.debug(traceback.format_exc())
            self.__etapa_atual = self.__ultima_etapa_atual
            return self.__etapa_atual

    @property
    def etapa_alvo(self) -> "int":
        try:

            if self.__leitura_etapa_alvo.valor == None:
                self.__etapa_alvo = self.__ultima_etapa_alvo
                return self.__etapa_alvo
            else:
                self.__etapa_alvo = self.__leitura_etapa_alvo.valor
                self.__ultima_etapa_alvo = self.__etapa_alvo
                return self.__etapa_alvo

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível realizar a leitura da \"Etapa Alvo\". Mantendo etapa alvo anterior.")
            logger.debug(traceback.format_exc())
            self.__etapa_alvo = self.__ultima_etapa_alvo
            return self.__etapa_alvo
    """


    # Property/Setter -> VARIÁVEIS PROTEGIDAS

    @property
    def codigo_state(self) -> "int":
        return self._codigo_state

    @codigo_state.setter
    def codigo_state(self, var) -> "int":
        self._codigo_state = var

    @property
    def prioridade(self) -> "int":
        return self._prioridade

    @prioridade.setter
    def prioridade(self, var) -> "None":
        self._prioridade = var

    @property
    def setpoint(self) -> "int":
        return self._setpoint

    @setpoint.setter
    def setpoint(self, var: "int"):
        if var < self.setpoint_minimo:
            self._setpoint = 0
        elif var > self.setpoint_maximo:
            self._setpoint = self.setpoint_maximo
        else:
            self._setpoint = int(var)

    @property
    def setpoint_minimo(self) -> "int":
        return self._setpoint_minimo

    @setpoint_minimo.setter
    def setpoint_minimo(self, var: "int"):
        self._setpoint_minimo = var

    @property
    def setpoint_maximo(self) -> "int":
        return self._setpoint_maximo

    @setpoint_maximo.setter
    def setpoint_maximo(self, var: "int"):
        self._setpoint_maximo = var

    @property
    def tentativas_de_normalizacao(self) -> "int":
        return self._tentativas_de_normalizacao

    @tentativas_de_normalizacao.setter
    def tentativas_de_normalizacao(self, var: "int"):
        if 0 <= var and var == int(var):
            self._tentativas_de_normalizacao = int(var)
        else:
            raise ValueError(f"[UG{self.id}] Valor deve se um inteiro positivo")

    @property
    def lista_ugs(self) -> "list[UnidadeDeGeracao]":
        return self._lista_ugs

    @lista_ugs.setter
    def lista_ugs(self, var: "list[UnidadeDeGeracao]") -> "None":
        self._lista_ugs = var


    # Funções

    def get_time(self) -> datetime:
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
                logger.error(f"[UG{self.id}] Não foi possível ler o último estado da Unidade. Entrando no estado \"Manual\".")
                self.__next_state = StateManual(self)

    # TODO -> Adicionar após a integração do CLP do MOA no painel do SA, que depende da intervenção da Automatic.
    def atualizar_modbus_moa(self) -> "None":
        return
        self.clp["MOA"].write_single_register(REG_MOA[f"OUT_ETAPA_UG{self.id}"], self.etapa)
        self.clp["MOA"].write_single_register(REG_MOA[f"OUT_STATE_UG{self.id}"], self.codigo_state)

    def desabilitar_manutencao(self) -> "bool":
        try:
            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_CONTROLE_POTENCIA_MANUAL"], 1, descr=f"UG{self.id}_CD_CMD_CONTROLE_POTENCIA_MANUAL")

            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_RV_MANUTENCAO"], 0, descr=f"UG{self.id}_CD_CMD_RV_MANUTENCAO")
            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_RV_AUTOMATICO"], 1, descr=f"UG{self.id}_CD_CMD_RV_AUTOMATICO")
            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_UHLM_MODO_MANUTENCAO"], 0, descr=f"UG{self.id}_CD_CMD_UHLM_MODO_MANUTENCAO")
            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_UHLM_MODO_AUTOMATICO"], 1, descr=f"UG{self.id}_CD_CMD_UHLM_MODO_AUTOMATICO")
            # res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_UHRV_MODO_MANUTENCAO"], 0, descr=f"UG{self.id}_CD_CMD_UHRV_MODO_MANUTENCAO") -> Está mandando comando de parada para a máquina | TODO Verificar com a Automatic
            # res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_UHRV_MODO_AUTOMATICO"], 1, descr=f"UG{self.id}_CD_CMD_UHRV_MODO_AUTOMATICO") -> Está mandando comando de parada para a máquina | TODO Verificar com a Automatic
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível desabilitar o modo de manutenção da Unidade.")
            logger.debug(traceback.format_exc())
            return False

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
        if self.etapa == UG_PARADA:
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
            logger.debug(f"[UG{self.id}]          Etapa atual:               \"{UG_STR_DCT_ETAPAS[self.etapa]}\"")

            self.__next_state = self.__next_state.step()
            self.atualizar_modbus_moa()

        except Exception:
            logger.error(f"[UG{self.id}] Erro na execução da máquina de estados da Unidade -> \"step\".")
            logger.debug(traceback.format_exc())

    def partir(self) -> "None":
        try:
            if not self.__leitura_dj_linha.valor:
                logger.info(f"[UG{self.id}] Não foi possível partir a Unidade. Disjuntor de Linha está aberto.")
                return

            elif not self.__leitura_dj_tsa.valor:
                logger.info(f"[UG{self.id}] Não foi possível partir a Unidade. Disjuntor do Serviço Auxiliar está aberto.")
                return

            elif self.__leitura_dj_gmg.valor:
                logger.info(f"[UG{self.id}] Não foi possível partir a Unidade. Disjuntor do Grupo Motor Gerador está fechado.")
                return

            elif not self.etapa == UG_SINCRONIZADA:
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARTIDA\"")
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_REARME_FALHAS"], 1, descr=f"UG{self.id}_CD_CMD_REARME_FALHAS")
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG["UG"][f"UG{self.id}_CD_CMD_SINCRONISMO"], 1, descr=f"UG{self.id}_CD_CMD_SINCRONISMO")

            else:
                logger.debug(f"[UG{self.id}] A Unidade já está sincronizada")

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível partir a Unidade.")
            logger.debug(traceback.format_exc())

    def parar(self) -> "None":
        try:
            if not self.etapa == UG_PARADA:
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARADA\"")
                EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_PARADA_TOTAL"], 1, descr=f"UG{self.id}_CD_CMD_PARADA_TOTAL")
                self.enviar_setpoint(0)

            else:
                logger.debug(f"[UG{self.id}] A Unidade já está parada")

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível parar a Unidade.")
            logger.debug(traceback.format_exc())

    def controlar_potencia_reativa(self) -> None:
        if self.__tensao.valor > TENSAO_UG_MAXIMA:
            tensao = self.__tensao.valor

            # v = tensao
            pot_reativa = ((0.426 * 500) / ((1.05 - 1) * 380)) * (tensao - 380) # ((lim_definido * pot_máx)/((v_lim - v_base) * tensao_nominal)) * (leitura_v - v_base)

            if pot_reativa > (0.426 * self.leitura_potencia):
                pot_reativa = (0.426 * self.leitura_potencia)
                self.rt[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}_RT_SETPOINT_POTENCIA_REATIVA_PU"], -pot_reativa)


    def enviar_setpoint(self, setpoint_kw: int) -> "bool":
        try:
            sleep(2)
            if not self.desabilitar_manutencao():
                logger.info(f"[UG{self.id}] Não foi possível enviar comando de \"Desabilitar Manutenção\"")
            else:
                self.setpoint = int(setpoint_kw)
                setpoint_porcento = (setpoint_kw / self.cfg["pot_maxima_ug"]) * 10000
                logger.debug(f"[UG{self.id}]          Enviando setpoint:         {(setpoint_kw / self.cfg['pot_maxima_ug']) * 100} %")

                if self.setpoint > 1:
                    res = self.rv[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}_RV_SETPOINT_POTENCIA_ATIVA_PU"], int(setpoint_porcento))
                    return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o Setpoint para Unidade.")
            logger.debug(traceback.format_exc())
            return False

    def acionar_trip_logico(self) -> "bool":
        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP LÓGICO\"")
            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_PARADA_EMERGENCIA"], 1, descr=f"UG{self.id}_CD_CMD_PARADA_EMERGENCIA")
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel acionar o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())
            return False

    def remover_trip_logico(self) -> "bool":
        try:
            logger.debug(f"[UG{self.id}]          Removendo comando:          \"TRIP LÓGICO\"")
            res = EMB.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}_CD_CMD_REARME_FALHAS"], 1, descr=f"UG{self.id}_CD_CMD_REARME_FALHAS")
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())
            return False

    def acionar_trip_eletrico(self) -> "bool":
        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP ELÉTRICO\" (SEM EFEITO -> Falta Automatic instalar CLP MOA)")
            res = None # self.clp["MOA"].write_single_coil(REG_MOA[f"OUT_BLOCK_UG{self.id}"], [1])
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())
            return False

    def remover_trip_eletrico(self) -> "bool":
        try:
            if self.clp["SA"].read_coils(REG_SA["SA_CD_DISJ_LINHA_FECHA"])[0] == 0:
                logger.debug(f"[UG{self.id}]          Enviando comando:          \"FECHAR DJ LINHA\".")
                EMB.escrever_bit(self.clp["SA"], REG_SA["SA_CD_DISJ_LINHA_FECHA"], 1, descr="SA_CD_DISJ_LINHA_FECHA")

            logger.debug(f"[UG{self.id}]          Removendo comando:          \"TRIP ELÉTRICO\" (SEM EFEITO -> Falta Automatic instalar CLP MOA)")
            res = None # self.clp["MOA"].write_single_coil(REG_MOA[f"OUT_BLOCK_UG{self.id}"], [0])
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())
            return False

    def reconhece_reset_alarmes(self) -> "bool":
        try:
            logger.info(f"[UG{self.id}]           Enviando comando:           \"RECONHECE E RESET\"")

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
            logger.debug(traceback.format_exc())
            return False

    def controle_etapas(self) -> "None":
        # PARANDO
        if self.etapa == UG_PARANDO:
            if self.setpoint >= self.setpoint_minimo:
                self.enviar_setpoint(self.setpoint)

        # SINCRONIZANDO
        elif self.etapa == UG_SINCRONIZANDO:
            if not self.borda_partindo:
                Thread(target=lambda: self.verificar_partida()).start()
                self.borda_partindo = True

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        # PARADA
        elif self.etapa == UG_PARADA:
            if self.setpoint >= self.setpoint_minimo:
                self.partir()
                self.enviar_setpoint(self.setpoint)

        # SINCRONIZADA
        elif self.etapa == UG_SINCRONIZADA:
            self.borda_partindo = False

            if not self.aux_tempo_sincronizada:
                self.aux_tempo_sincronizada = self.get_time()

            elif (self.get_time() - self.aux_tempo_sincronizada).seconds >= 300:
                self.tentativas_de_normalizacao = 0

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        # CONTROLE TEMPO SINCRONIZADAS
        if not self.etapa == UG_SINCRONIZADA:
            self.aux_tempo_sincronizada = None

    def verificar_partida(self) -> "None":
        return
        logger.debug(f"[UG{self.id}]          Comando MOA:                \"Iniciar timer de verificação de partida\"")
        while time() < (time() + 600):
            if self.etapa == UG_SINCRONIZADA or self.release_timer:
                logger.debug(f"[UG{self.id}]          Comando MOA:                \"Encerrar timer de verificação de partida por condição verdadeira\"")
                return

        logger.debug(f"[UG{self.id}]          Comando MOA:                \"Encerrar timer de verificação de partida por timeout\"")
        self.borda_partindo = False
        EMB.escrever_bit(self.clp[f"UG{self.id}"], [f"UG{self.id}_CD_CMD_PARADA_EMERGENCIA"], 1, descr=f"UG{self.id}_CD_CMD_PARADA_EMERGENCIA")
        sleep(1)
        EMB.escrever_bit(self.clp[f"UG{self.id}"], [f"UG{self.id}_CD_CMD_REARME_FALHAS"], 1, descr=f"UG{self.id}_CD_CMD_REARME_FALHAS")