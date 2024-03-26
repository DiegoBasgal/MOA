import pytz
import logging
import traceback

import src.subestacao as se
import src.tomada_agua as tda
import src.servico_auxiliar as sa

import src.dicionarios.dict as d
import src.maquinas_estado.ug as usm
import src.conectores.servidores as srv
import src.conectores.banco_dados as bd
import src.funcoes.leitura as lei
import src.funcoes.escrita as esc
import src.funcoes.condicionadores as c

from src.dicionarios.reg import *
from src.dicionarios.const import *

from time import sleep, time
from threading import Thread
from datetime import datetime


logger = logging.getLogger("logger")


class UnidadeDeGeracao:
    def __init__(self, id: "int", cfg: "dict"=None, bd: "bd.BancoDados"=None):

        # VERIFICAÇÃO DE ARGUMENTOS
        if id <= 0:
            logger.error(f"[UG{self.id}] A Unidade não pode ser instanciada com o ID <= \"0\" ou vazio.")
            raise ValueError
        else:
            self.__id = id

        # ATRIBUIÇÃO DE OBJETOS DAS UNIDADES
        self.bd = bd
        self.cfg = cfg
        self.rv = srv.Servidores.rv
        self.rt = srv.Servidores.rt
        self.clp = srv.Servidores.clp
        self.rele = srv.Servidores.rele

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS
        self.__tensao = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_RELE[f"UG{self.id}"]["VAB"],
            descricao=f"[UG{self.id}] Tensão Unidade"
        )
        self.__potencia = lei.LeituraModbus(
            self.rele[f"UG{self.id}"],
            REG_RELE[f"UG{self.id}"]["P"],
            descricao=f"[UG{self.id}] Potência Ativa"
        )
        self.__potencia_reativa = lei.LeituraModbus(
            self.rele[f"UG{self.id}"],
            REG_RELE[f"UG{self.id}"]["Q"],
            descricao=f"[UG{self.id}] Potência Reativa"
        )
        self.__potencia_aparente = lei.LeituraModbus(
            self.rele[f"UG{self.id}"],
            REG_RELE[f"UG{self.id}"]["S"],
            descricao=f"[UG{self.id}] Potência Aparente"
        )
        self.__etapa_atual = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["STT_PASSO_ATUAL"],
            descricao=f"[UG{self.id}] Etapa Atual"
        )
        self.__etapa_alvo = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["SST_PASSO_SELECIONADO"],
            descricao=f"[UG{self.id}] Etapa Alvo"
        )

        self.__tempo_entre_tentativas: "int" = 0
        self.__limite_tentativas_de_normalizacao: "int" = 3

        self.__condicionadores_atenuadores: "list[str, c.CondicionadorBase]" = []

        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS
        self._etapa_alvo: "int" = 0
        self._etapa_atual: "int" = 0
        self._ultima_etapa_alvo: "int" = 0
        self._ultima_etapa_atual: "int" = 0

        self._setpoint: "int" = 0
        self._prioridade: "int" = 0
        self._tentativas_de_normalizacao: "int" = 0

        self._setpoint_minimo: "float" = self.cfg["pot_minima"]
        self._setpoint_maximo: "float" = self.cfg[f"pot_maxima_ug{self.id}"]


        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS
        self.atenuacao: "int" = 0
        self.tempo_normalizar: "int" = 0
        self.tentativas_norm_etapas: "int" = 0

        self.ug_parando: "bool" = False
        self.borda_parar: "bool" = False
        self.manter_unidade: "bool" = False
        self.ug_sincronizando: "bool" = False
        self.temporizar_partida: "bool" = False
        self.normalizacao_agendada: "bool" = False

        self.aux_tempo_sincronizada: "datetime" = 0
        self.ts_auxiliar: "datetime" = self.get_time()

        self._condicionadores: "list[c.CondicionadorBase]" = []
        self._condicionadores_essenciais: "list[c.CondicionadorBase]" = []
        self._condicionadores_atenuadores: "list[c.CondicionadorBase]" = []

        # EXECUÇÃO FINAL DA INICIALIZAÇÃO
        self.desabilitar_manutencao()
        self.iniciar_ultimo_estado()
        self.carregar_leituras()


    # Property -> VARIÁVEIS PRIVADAS
    @property
    def id(self) -> "int":
        return self.__id

    @property
    def potencia(self) -> "float":
        return self.__potencia.valor

    @property
    def potencia_aparente(self) -> "float":
        return self.__potencia_aparente.valor

    @property
    def manual(self) -> "bool":
        return isinstance(self.__next_state, usm.StateManual)

    @property
    def restrito(self) -> "bool":
        return isinstance(self.__next_state, usm.StateRestrito)

    @property
    def disponivel(self) -> "bool":
        return isinstance(self.__next_state, usm.StateDisponivel)

    @property
    def indisponivel(self) -> "bool":
        return isinstance(self.__next_state, usm.StateIndisponivel)

    @property
    def tempo_entre_tentativas(self) -> "int":
        return self.__tempo_entre_tentativas

    @property
    def limite_tentativas_de_normalizacao(self) -> "int":
        return self.__limite_tentativas_de_normalizacao

    @property
    def etapa_atual(self) -> "int":
        # PROPRIEDADE -> Retorna o valor da leitura de etapa atual

        try:
            self._ultima_etapa_atual = self.__etapa_atual.valor
            return self._ultima_etapa_atual

        except Exception:
            logger.error(f"[UG{self.id}] Erro na leitura de \"Etapa Atual\". Mantendo última etapa.")
            return self._ultima_etapa_atual

    @property
    def etapa_alvo(self) -> "int":
        # PROPRIEDADE -> Retorna o valor da leitura de etapa alvo

        try:
            self._ultima_etapa_alvo = self.__etapa_alvo.valor
            return self._ultima_etapa_alvo

        except Exception:
            logger.error(f"[UG{self.id}] Erro na leitura de \"Etapa Alvo\". Mantendo última etapa.")
            return self._ultima_etapa_alvo

    @property
    def etapa(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de etapa tratado

        if self.etapa_atual == UG_PARADA and self.etapa_alvo == UG_PARADA:
            self._ultima_etapa_alvo = self.etapa_alvo
            return UG_PARADA

        elif self.etapa_atual == UG_SINCRONIZADA and self.etapa_alvo == UG_SINCRONIZADA:
            self._ultima_etapa_alvo = self.etapa_alvo
            return UG_SINCRONIZADA

        elif UG_PARADA < self.etapa_atual <= UG_SINCRONIZADA and self.etapa_alvo == UG_PARADA:

            if self._ultima_etapa_alvo != self.etapa_alvo:
                if self._ultima_etapa_alvo < self.etapa_alvo:
                    self._ultima_etapa_alvo = self.etapa_alvo
                    return UG_SINCRONIZANDO

                elif self._ultima_etapa_alvo > self.etapa_alvo:
                    self._ultima_etapa_alvo = self.etapa_alvo
                    return UG_PARANDO

            else:
                self._ultima_etapa_alvo = self.etapa_alvo
                return UG_PARANDO

        elif UG_PARADA <= self.etapa_atual < UG_SINCRONIZADA and self.etapa_alvo == UG_SINCRONIZADA:
            if self._ultima_etapa_alvo != self.etapa_alvo:
                if self._ultima_etapa_alvo > self.etapa_alvo:
                    self._ultima_etapa_alvo = self.etapa_alvo
                    return UG_PARANDO

                elif self._ultima_etapa_alvo < self.etapa_alvo:
                    self._ultima_etapa_alvo = self.etapa_alvo
                    return UG_SINCRONIZANDO

            else:
                self._ultima_etapa_alvo = self.etapa_alvo
                return UG_SINCRONIZANDO



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
        if var < self.cfg['pot_minima']:
            self._setpoint = self.cfg['pot_minima'] if self.manter_unidade else 0

        elif var > self.cfg[f'pot_maxima_ug{self.id}']:
            self._setpoint = self.cfg[f'pot_maxima_ug{self.id}']

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
            raise ValueError(f"[UG{self.id}] Valor deve ser um inteiro positivo")

    @property
    def condicionadores(self) -> "list[c.CondicionadorBase]":
        # PROPRIEDADE -> Retrona a lista de condicionadores da Unidade.

        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[c.CondicionadorBase]") -> None:
        # SETTER -> Atrubui a nova lista de condicionadores da Unidade.

        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[c.CondicionadorBase]":
        # PROPRIEDADE -> Retrona a lista de condicionadores essenciais da Unidade.

        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[c.CondicionadorBase]") -> None:
        # SETTER -> Atrubui a nova lista de condicionadores essenciais da Unidade.

        self._condicionadores_essenciais = var

    @property
    def condicionadores_atenuadores(self) -> "list[c.CondicionadorBase]":
        # PROPRIEDADE -> Retorna a lista de atenuadores da Unidade.

        return self._condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: "list[c.CondicionadorBase]") -> None:
        # SETTER -> Atribui a nova lista de atenuadores da Unidade.

        self._condicionadores_atenuadores = var


    # FUNÇÕES
    @staticmethod
    def get_time() -> "datetime":
        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    def forcar_estado_manual(self) -> "None":
        self.__next_state = usm.StateManual(self)


    def forcar_estado_restrito(self) -> "None":
        self.__next_state = usm.StateRestrito(self)


    def forcar_estado_indisponivel(self) -> "None":
        self.__next_state = usm.StateIndisponivel(self)


    def forcar_estado_disponivel(self) -> "None":
        self.reconhece_reset_alarmes()
        self.__next_state = usm.StateDisponivel(self)


    def iniciar_ultimo_estado(self) -> "None":
        estado = self.bd.get_ultimo_estado_ug(self.id)[0]

        if estado == None:
            self.__next_state = usm.StateDisponivel(self)
        else:
            if estado == UG_SM_MANUAL:
                self.__next_state = usm.StateManual(self)
            elif estado == UG_SM_DISPONIVEL:
                self.__next_state = usm.StateDisponivel(self)
            elif estado == UG_SM_RESTRITA:
                if self.etapa == UG_SINCRONIZADA:
                    self.__next_state = usm.StateDisponivel(self)
                else:
                    self.__next_state = usm.StateRestrito(self)
            elif estado == UG_SM_INDISPONIVEL:
                if self.etapa == UG_SINCRONIZADA:
                    self.__next_state = usm.StateDisponivel(self)
                else:
                    self.__next_state = usm.StateIndisponivel(self)
            else:
                logger.debug("")
                logger.error(f"[UG{self.id}] Não foi possível ler o último estado da Unidade")
                logger.info(f"[UG{self.id}] Acionando estado \"Manual\".")
                self.__next_state = usm.StateManual(self)


    def atualizar_modbus_moa(self) -> "None":
        return
        self.clp["MOA"].write_single_register(REG_MOA[f"OUT_ETAPA_UG{self.id}"], self.etapa)
        self.clp["MOA"].write_single_register(REG_MOA[f"OUT_STATE_UG{self.id}"], self.codigo_state)


    def desabilitar_manutencao(self) -> "bool":
        try:
            res = esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_CONTROLE_POT_MANUAL"], valor=1)

            # res = esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_RV_MANUTENCAO"], valor=0)
            # res = esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_RV_AUTOMATICO"], valor=1)
            # res = esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_UHLM_MODO_AUTOMATICO"], valor=1)
            # res = esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_UHRV_MODO_MANUTENCAO"], valor=0) -> Está mandando comando de parada para a máquina | TODO Verificar com a Automatic
            # res = esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_UHRV_MODO_AUTOMATICO"], valor=1) -> Está mandando comando de parada para a máquina | TODO Verificar com a Automatic
            return True # res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível desabilitar o modo de manutenção da Unidade.")
            logger.debug(traceback.format_exc())
            return False


    def resetar_emergencia(self) -> "None":
        try:
            logger.info(f"[UG{self.id}] Enviando comando:                   \"RESET EMERGÊNCIA\"")

            # esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_REARME_FALHAS"], valor=1)

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(traceback.format_exc())


    def espera_normalizar(self, delay: "int"):
        while not self.parar_timer:
            sleep(max(0, time() + delay - time()))
            self.parar_timer = True
            return


    def normalizar_unidade(self) -> "bool":
        if self.etapa == UG_PARADA:
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
        self.temporizar_partida = False

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
            logger.debug(f"[UG{self.id}]          Etapa:                     \"{UG_STR_DCT_ETAPAS[self.etapa]}\" (Atual: {self.etapa_atual} | Alvo: {self.etapa_alvo})")

            if self.disponivel:
                logger.debug(f"[UG{self.id}]          Leituras de Potência:")
                logger.debug(f"[UG{self.id}]          - \"Ativa\":                 {self.potencia:0.0f} kW")
                logger.debug(f"[UG{self.id}]          - \"Reativa\":               {self.__potencia_reativa.valor - 65535 if 65300 < self.__potencia_reativa.valor <= 65535 else self.__potencia_reativa.valor:0.1f} kVAr")
                logger.debug(f"[UG{self.id}]          - \"Aparente\":              {self.potencia_aparente:0.1f} kVA")

            self.__next_state = self.__next_state.step()
            self.atualizar_modbus_moa()

        except Exception:
            logger.error(f"[UG{self.id}] Erro na execução da máquina de estados da Unidade -> \"step\".")
            logger.debug(traceback.format_exc())


    def partir(self) -> "None":
        try:
            if not se.Subestacao.status_dj_linha.valor:
                logger.info(f"[UG{self.id}] Não foi possível partir a Unidade. Disjuntor de Linha está aberto.")
                return

            elif not sa.ServicoAuxiliar.status_dj_tsa.valor:
                logger.info(f"[UG{self.id}] Não foi possível partir a Unidade. Disjuntor do Serviço Auxiliar está aberto.")
                return

            elif sa.ServicoAuxiliar.l_disj_gmg_fechado.valor:
                logger.info(f"[UG{self.id}] Não foi possível partir a Unidade. Disjuntor do Grupo Motor Gerador está fechado.")
                return

            elif not self.etapa == UG_SINCRONIZADA:
                self.tentativas_norm_etapas = 0
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARTIDA\"")

                esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_REARME_FALHAS"], valor=1)
                # esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_SINCRONISMO"], valor=1)
                self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["CMD_SINCRONISMO"][0], int(128))

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível partir a Unidade.")
            logger.debug(traceback.format_exc())


    def parar(self) -> "bool":
        try:
            if not self.etapa == UG_PARADA:
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARADA\"")
                self.enviar_setpoint(0)
                res = esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_PARADA_TOTAL"], valor=1)
                return True # res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível parar a Unidade.")
            logger.debug(traceback.format_exc())
            return False


    def controlar_potencia_reativa(self) -> None:
        if self.__tensao.valor > TENSAO_UG_MAXIMA:
            tensao = self.__tensao.valor

            # v = tensao
            pot_reativa = ((0.426 * 500) / ((1.05 - 1) * 380)) * (tensao - 380) # ((lim_definido * pot_máx)/((v_lim - v_base) * tensao_nominal)) * (leitura_v - v_base)

            if pot_reativa > (0.426 * self.potencia):
                pot_reativa = (0.426 * self.potencia)
                self.rt[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["SETPOINT_POT_REATIVA_PU"], -pot_reativa)


    def enviar_setpoint(self, setpoint_kw: int) -> "bool":
        try:
            sleep(2)
            if not self.desabilitar_manutencao():
                logger.info(f"[UG{self.id}] Não foi possível enviar comando de \"Desabilitar Manutenção\"")
            else:
                self.setpoint = int(setpoint_kw)
                setpoint_porcento = (setpoint_kw / self.cfg[f"pot_maxima_ug{self.id}"]) * 10000
                logger.debug(f"[UG{self.id}]          Enviando setpoint:         {setpoint_kw} kW ({(setpoint_kw / self.cfg[f'pot_maxima_ug{self.id}']) * 100:0.1f} %)")

                if self.setpoint > 1:
                    res = self.rv[f"UG{self.id}"].write_single_register(REG_RTV[f"UG{self.id}"]["SETPOINT_POT_ATIVA_PU"], int(setpoint_porcento))
                    # res = self.rv[f"UG{self.id}"].write_single_register(REG_RTV[f"UG{self.id}"]["SETPOINT_POT_ATIVA_PU"], int(setpoint_kw)) # SIMULADOR
                    return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o Setpoint para Unidade.")
            logger.debug(traceback.format_exc())
            return False


    def acionar_trip_logico(self) -> "bool":
        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP LÓGICO\"")
            res = esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_PARADA_EMERG"], valor=1)
            return True # res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel acionar o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())
            return False


    def remover_trip_logico(self) -> "bool":
        try:
            logger.debug(f"[UG{self.id}]          Removendo comando:         \"TRIP LÓGICO\"")
            res = esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_REARME_FALHAS"], valor=1)
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())
            return False


    def acionar_trip_eletrico(self) -> "bool":
        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP ELÉTRICO\"")
            res = None # self.clp["MOA"].write_single_coil(REG_MOA[f"OUT_BLOCK_UG{self.id}"], [1])
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())
            return False


    def remover_trip_eletrico(self) -> "bool":
        try:
            if not se.Subestacao.status_dj_linha.valor:
                logger.debug(f"[UG{self.id}]          Enviando comando:          \"FECHAR DISJUNTOR LINHA\".")
                esc.EscritaModBusBit.escrever_bit(self.clp["SA"], REG_SASE["CMD_DJ_LINHA_FECHA"], valor=1)

            logger.debug(f"[UG{self.id}]          Removendo comando:         \"TRIP ELÉTRICO\"")
            res = None # self.clp["MOA"].write_single_coil(REG_MOA[f"OUT_BLOCK_UG{self.id}"], [0])
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())
            return False


    def reconhece_reset_alarmes(self) -> "bool":
        try:
            logger.debug("")
            logger.info(f"[UG{self.id}]          Enviando comando:          \"RECONHECE E RESET\"")

            passo = 0
            for x in range(3):
                passo += 1
                logger.debug("")
                logger.debug(f"[UG{self.id}]          Passo: {passo}/3")
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


    def atenuar_carga(self) -> "None":
        """
        Função para atenuação de carga através de leitura de Pressão na Entrada da Turbina.

        Calcula o ganho e verifica os limites máximo e mínimo para deteminar se
        deve atenuar ou não.
        """

        flags = 0
        atenuacao = 0
        logger.debug(f"[UG{self.id}]          Verificando Atenuadores...") if self.etapa == UG_SINCRONIZADA else None

        for condic in self.condicionadores_atenuadores:
            atenuacao = max(atenuacao, condic.valor)
            if atenuacao > 0:
                flags += 1
                logger.debug(f"[UG{self.id}]          - \"{condic.descricao}\":")
                logger.debug(f"[UG{self.id}]                                     Leitura: {condic.leitura:3.2f} | Atenuação: {atenuacao:0.4f}")

                if flags == 1:
                    self.atenuacao = atenuacao
                elif atenuacao > self.atenuacao:
                    self.atenuacao = atenuacao
                atenuacao = 0

        if flags == 0 and self.etapa == UG_SINCRONIZADA:
            logger.debug(f"[UG{self.id}]          Não há necessidade de Atenuação.")

        ganho = 1 - self.atenuacao
        aux = self.setpoint
        self.atenuacao = 0
        if (self.setpoint > self.setpoint_minimo) and self.setpoint * ganho > self.setpoint_minimo:
            setpoint_atenuado = self.setpoint - 0.5 * (self.setpoint -  (self.setpoint * ganho))
            self.setpoint = min(max(setpoint_atenuado, self.setpoint_minimo), self.setpoint_maximo)

        elif self.setpoint > self.setpoint_minimo and (self.setpoint * ganho) < self.setpoint_minimo:
            self.setpoint = self.setpoint_minimo

        if self.etapa == UG_SINCRONIZADA and ganho < 1:
            logger.debug(f"[UG{self.id}]                                     SP {aux} * GANHO {ganho:0.4f} = {self.setpoint} kW")



    def controle_etapas(self) -> "None":
        # PARANDO
        if self.etapa == UG_PARANDO:
            if self.setpoint >= self.setpoint_minimo:
                self.enviar_setpoint(self.setpoint)

        # SINCRONIZANDO
        elif self.etapa == UG_SINCRONIZANDO:
            if not self.temporizar_partida:
                self.temporizar_partida = True
                Thread(target=lambda: self.verificar_sincronismo()).start()

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        # PARADA
        elif self.etapa == UG_PARADA:
            if self.setpoint >= self.setpoint_minimo:
                self.partir()
                self.enviar_setpoint(self.setpoint)

        # SINCRONIZADA
        elif self.etapa == UG_SINCRONIZADA:
            self.temporizar_partida = True
            if not self.aux_tempo_sincronizada:
                self.aux_tempo_sincronizada = self.get_time()

            elif (self.get_time() - self.aux_tempo_sincronizada).seconds >= 300:
                self.tentativas_de_normalizacao = 0

            self.parar() if self.setpoint == 0 else self.enviar_setpoint(self.setpoint)

        # CONTROLE TEMPO SINCRONIZADAS
        if not self.etapa == UG_SINCRONIZADA:
            self.aux_tempo_sincronizada = None


    def verificar_sincronismo(self) -> "None":
        """
        Função de verificação de partida da Unidade.

        Caso a unidade seja totalmente sincronizada, o timer é encerrado e avisado,
        senão, é enviado o comando de parada de emergência para a Unidade.
        """

        delay = time() + 600

        logger.debug(f"[UG{self.id}]          Verificação MOA:           \"Temporização de Sincronismo\"")
        while time() < delay:
            if not self.temporizar_partida:
                return

        logger.warning(f"[UG{self.id}]          Verificação MOA:          \"Acionar emergência por timeout de Sincronismo\"")
        esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_PARADA_EMERG"], valor=1)
        self.temporizar_partida = False
        sleep(1)
        esc.EscritaModBusBit.escrever_bit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_REARME_FALHAS"], valor=1)


    def verificar_condicionadores(self) -> "int":
        """
        Função para a verificação de acionamento de condicionadores e determinação
        de gravidade.

        Itera sobre a lista de condicionadores da Unidade e verifica se algum está
        ativo. Caso esteja, verifica o nível de gravidade e retorna o valor para
        a determinação do passo seguinte.
        Caso não haja nenhum condicionador ativo, apenas retorna o valor de ignorar.
        """

        flag = CONDIC_IGNORAR

        autor_a = 0
        autor_n = 0
        autor_i = 0

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.debug(f"[UG{self.id}] Foram detectados condicionadores ativos na Unidade!")
            else:
                logger.debug(f"[UG{self.id}] Ainda há condicionadores ativos na Unidade!")

            for condic in condics_ativos:
                if condic.teste:
                    logger.debug(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\", Obs.: \"TESTE\"")
                    continue

                elif condic in self.condicionadores_ativos:
                    logger.debug(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    flag = condic.gravidade
                    continue

                elif condic.gravidade == CONDIC_INDISPONIBILIZAR:
                    logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_INDISPONIBILIZAR
                    self.bd.update_alarmes([
                        self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor_i == 0 else ""
                    ])
                    autor_i += 1
                    sleep(1)

                elif condic.gravidade == CONDIC_AGUARDAR:
                    logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_AGUARDAR
                    self.bd.update_alarmes([
                        self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor_i == 0 and autor_a == 0 else ""
                    ])
                    autor_a += 1
                    sleep(1)

                elif condic.gravidade == CONDIC_NORMALIZAR:
                    logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    flag = CONDIC_NORMALIZAR
                    self.bd.update_alarmes([
                        self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor_i == 0 and autor_a == 0 and autor_n == 0 else ""
                    ])
                    autor_n += 1
                    sleep(1)

            logger.debug("")
            return flag

        else:
            self.condicionadores_ativos = []
            return flag


    def atualizar_limites_condicionadores(self, parametros: "dict") -> "None":
        """
        Função para extração de valores do Banco de Dados da Interface WEB e atribuição
        de novos limites de operação de condicionadores.
        """
        try:
            self.c_diferencial_grade.valor_base = float(parametros[f"alerta_perda_grade"])
            self.c_tmp_fase_r.valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{self.id}"])
            self.c_tmp_fase_s.valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{self.id}"])
            self.c_tmp_fase_t.valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{self.id}"])
            self.c_tmp_nucleo_gerador_1.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_1_ug{self.id}"])
            self.c_tmp_nucleo_gerador_2.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_2_ug{self.id}"])
            self.c_tmp_nucleo_gerador_3.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_3_ug{self.id}"])
            self.c_tmp_mancal_casq_rad.valor_base = float(parametros[f"alerta_temperatura_mancal_casq_rad_ug{self.id}"])
            self.c_tmp_mancal_casq_comb.valor_base = float(parametros[f"alerta_temperatura_mancal_casq_comb_ug{self.id}"])
            self.c_tmp_mancal_escora_comb.valor_base = float(parametros[f"alerta_temperatura_mancal_escora_comb_ug{self.id}"])

            self.c_diferencial_grade.valor_limite = float(parametros[f"limite_perda_grade"])
            self.c_tmp_fase_s.valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{self.id}"])
            self.c_tmp_fase_r.valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{self.id}"])
            self.c_tmp_fase_t.valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{self.id}"])
            self.c_tmp_nucleo_gerador_1.valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_1_ug{self.id}"])
            self.c_tmp_nucleo_gerador_2.valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_2_ug{self.id}"])
            self.c_tmp_nucleo_gerador_3.valor_limite = float(parametros[f"limite_temperatura_nucleo_gerador_3_ug{self.id}"])
            self.c_tmp_mancal_casq_rad.valor_limite = float(parametros[f"limite_temperatura_mancal_casq_rad_ug{self.id}"])
            self.c_tmp_mancal_casq_comb.valor_limite = float(parametros[f"limite_temperatura_mancal_casq_comb_ug{self.id}"])
            self.c_tmp_mancal_escora_comb.valor_limite = float(parametros[f"limite_temperatura_mancal_escora_comb_ug{self.id}"])

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores.")
            logger.debug(f"{traceback.format_exc()}")


    def controlar_limites_operacao(self) -> "None":
        """
        Função para verificação de limites de operação da Unidade.

        Verifica os valores base e limite da Unidade, pré-determinados na interface
        WEB, e avisa o operador caso algum valor ultrapasse o estipulado.
        """
        return

        if self.l_tmp_fase_r.valor >= self.c_tmp_fase_r.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase R da UG passou do valor base! ({self.c_tmp_fase_r.valor_base} C) | Leitura: {self.l_tmp_fase_r.valor} C")

        if self.l_tmp_fase_r.valor >= 0.9*(self.c_tmp_fase_r.valor_limite - self.c_tmp_fase_r.valor_base) + self.c_tmp_fase_r.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase R da UG está muito próxima do limite! ({self.c_tmp_fase_r.valor_limite} C) | Leitura: {self.l_tmp_fase_r.valor} C")


        if self.l_tmp_fase_s.valor >= self.c_tmp_fase_s.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase S da UG passou do valor base! ({self.c_tmp_fase_s.valor_base} C) | Leitura: {self.l_tmp_fase_s.valor} C")

        if self.l_tmp_fase_s.valor >= 0.9*(self.c_tmp_fase_s.valor_limite - self.c_tmp_fase_s.valor_base) + self.c_tmp_fase_s.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase S da UG está muito próxima do limite! ({self.c_tmp_fase_s.valor_limite} C) | Leitura: {self.l_tmp_fase_s.valor} C")


        if self.l_tmp_fase_t.valor >= self.c_tmp_fase_t.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase T da UG passou do valor base! ({self.c_tmp_fase_t.valor_base} C) | Leitura: {self.l_tmp_fase_t.valor} C")

        if self.l_tmp_fase_t.valor >= 0.9*(self.c_tmp_fase_t.valor_limite - self.c_tmp_fase_t.valor_base) + self.c_tmp_fase_t.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase T da UG está muito próxima do limite! ({self.c_tmp_fase_t.valor_limite} C) | Leitura: {self.l_tmp_fase_t.valor} C")


        if self.l_tmp_nucleo_gerador_1.valor >= self.c_tmp_nucleo_gerador_1.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Núcleo Gerador 1 da UG passou do valor base! ({self.c_tmp_nucleo_gerador_1.valor_base} C) | Leitura: {self.c_tmp_nucleo_gerador_1.valor} C")

        if self.l_tmp_nucleo_gerador_1.valor >= 0.9*(self.c_tmp_nucleo_gerador_1.valor_limite - self.c_tmp_nucleo_gerador_1.valor_base) + self.c_tmp_nucleo_gerador_1.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Núcleo Gerador 1 da UG está muito próxima do limite! ({self.c_tmp_nucleo_gerador_1.valor_limite} C) | Leitura: {self.c_tmp_nucleo_gerador_1.valor} C")


        if self.l_tmp_nucleo_gerador_2.valor >= self.c_tmp_nucleo_gerador_2.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Núcleo Gerador 2 da UG passou do valor base! ({self.c_tmp_nucleo_gerador_2.valor_base} C) | Leitura: {self.c_tmp_nucleo_gerador_2.valor} C")

        if self.l_tmp_nucleo_gerador_2.valor >= 0.9*(self.c_tmp_nucleo_gerador_2.valor_limite - self.c_tmp_nucleo_gerador_2.valor_base) + self.c_tmp_nucleo_gerador_2.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Núcleo Gerador 2 da UG está muito próxima do limite! ({self.c_tmp_nucleo_gerador_2.valor_limite} C) | Leitura: {self.c_tmp_nucleo_gerador_2.valor} C")


        if self.l_tmp_nucleo_gerador_3.valor >= self.c_tmp_nucleo_gerador_3.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Núcleo Gerador 3 da UG passou do valor base! ({self.c_tmp_nucleo_gerador_3.valor_base} C) | Leitura: {self.c_tmp_nucleo_gerador_3.valor} C")

        if self.l_tmp_nucleo_gerador_3.valor >= 0.9*(self.c_tmp_nucleo_gerador_3.valor_limite - self.c_tmp_nucleo_gerador_3.valor_base) + self.c_tmp_nucleo_gerador_3.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Núcleo Gerador 3 da UG está muito próxima do limite! ({self.c_tmp_nucleo_gerador_3.valor_limite} C) | Leitura: {self.c_tmp_nucleo_gerador_3.valor} C")


        if self.l_tmp_mancal_casq_rad.valor >= self.c_tmp_mancal_casq_rad.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Casquilho Radial da UG passou do valor base! ({self.c_tmp_mancal_casq_rad.valor_base} C) | Leitura: {self.c_tmp_mancal_casq_rad.valor} C")

        if self.l_tmp_mancal_casq_rad.valor >= 0.9*(self.c_tmp_mancal_casq_rad.valor_limite - self.c_tmp_mancal_casq_rad.valor_base) + self.c_tmp_mancal_casq_rad.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Casquilho Radial da UG está muito próxima do limite! ({self.c_tmp_mancal_casq_rad.valor_limite} C) | Leitura: {self.c_tmp_mancal_casq_rad.valor} C")


        if self.l_tmp_mancal_casq_comb.valor >= self.c_tmp_mancal_casq_comb.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Casquilho Combinado da UG passou do valor base! ({self.c_tmp_mancal_casq_comb.valor_base} C) | Leitura: {self.c_tmp_mancal_casq_comb.valor} C")

        if self.l_tmp_mancal_casq_comb.valor >= 0.9*(self.c_tmp_mancal_casq_comb.valor_limite - self.c_tmp_mancal_casq_comb.valor_base) + self.c_tmp_mancal_casq_comb.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Casquilho Combinado da UG está muito próxima do limite! ({self.c_tmp_mancal_casq_comb.valor_limite} C) | Leitura: {self.c_tmp_mancal_casq_comb.valor} C")


        if self.l_tmp_mancal_escora_comb.valor >= self.c_tmp_mancal_escora_comb.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Escora Combinado da UG passou do valor base! ({self.c_tmp_mancal_escora_comb.valor_base} C) | Leitura: {self.c_tmp_mancal_escora_comb.valor} C")

        if self.l_tmp_mancal_escora_comb.valor >= 0.9*(self.c_tmp_mancal_escora_comb.valor_limite - self.c_tmp_mancal_escora_comb.valor_base) + self.c_tmp_mancal_escora_comb.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Escora Combinado da UG está muito próxima do limite! ({self.c_tmp_mancal_escora_comb.valor_limite} C) | Leitura: {self.c_tmp_mancal_escora_comb.valor} C")


    def verificar_leituras(self) -> "None":
        """
        Função para consulta de acionamentos da Unidade e avisos através do mecanismo
        de acionamento temporizado.
        """
        return

        # WHATSAPP
        if self.l_rt_selec_modo_controle_isol.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o comando no RT de seleção de modo de controle isolado, favor verificar.")

        if self.l_alarme_rele.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma leitura de alarme do relé, favor verificar.")

        if self.l_rv_alarme.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma leitura de alarme do RV, favor verificar.")

        if self.l_rv_pot_nula.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma leitura de potência nula no RV, favor verificar.")

        if self.l_rt_alarme.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma leitura de alarme no RT, favor verificar.")

        if self.l_dispo_prot_surto.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma leitura do dispositivo de proteção de surto, favor verificar.")

        if self.l_uhrv_bomba_defeito.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um defeito na bomba da UHRV, favor verificar.")

        if self.l_uhlm_bomba_defeito.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um defeito na bomba da UHLM, favor verificar.")

        if self.l_resis_aquec_gerad_defeito.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um defeito com a resistência do aquecedor do Gerador, favor verificar.")

        if self.l_tristores_temp_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura de Tristores está alta, favor verificar.")

        if self.l_crowbar_temp_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Crowbar está alta, favor verificar.")

        if self.l_trafo_exci_temp_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Transformador de Excitação está alta, favor verificar.")

        if self.l_uhrv_oleo_temp_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Óleo da UHRV está alta, favor verificar.")

        if self.l_gerad_fase_a_temp_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura de Fase A do Gerador está alta, favor verificar.")

        if self.l_gerad_fase_b_temp_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura de Fase B do Gerador está alta, favor verificar.")

        if self.l_gerad_fase_c_temp_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura de Fase C do Gerador está alta, favor verificar.")

        if self.l_gerad_nucleo_1_temp_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Núcleo 1 do Gerador está alta, favor verificar.")

        if self.l_gerad_nucleo_2_temp_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Núcleo 2 do Gerador está alta, favor verificar.")

        if self.l_gerad_nucleo_3_temp_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Núcleo 3 do Gerador está alta, favor verificar.")

        if self.l_mancal_guia_casq_temp_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Mancal Guia Casquilho está alta, favor verificar.")

        if self.l_mancal_comb_casq_temp_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Mancal Combinado Casquilho está alta, favor verificar.")

        if self.l_mancal_comb_esc_temp_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Mancal Combinado Escora está alta, favor verificar.")

        if self.l_falha_leit_nv_jusante.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura do Nível Jusante, favor verificar.")

        if self.l_sinal_nv_jusante_muito_alto.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o Nível Jusante está muito alto, favor verificar.")

        if self.l_sinal_nv_jusante_alto.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o Nível Jusante está alto, favor verificar.")

        if self.l_uhrv_pressao_oleo_baixa.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a pressão do óleo da UHRV está baixa, favor verificar.")

        if self.l_sinal_nv_jusante_baixo.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o Nível Jusante está baixo, favor verificar.")

        if self.l_uhrv_pressao_oleo_muito_baixa.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a pressão do óleo da UHRV está muito baixa, favor verificar.")

        if self.l_sinal_nv_jusante_muito_baixo.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o Nível Jusante está muito baixo, favor verificar.")

        if self.l_alarme_contro_dif_grade.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma leitura de alarme do controle de diferencial de grade, favor verificar.")

        if self.l_resis_aquec_gerad_indisp.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a resistência do aquecedor do gerador está indisponível, favor verificar.")

        if self.l_uhlm_unidade_manut.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a UHLM entrou em modo de manutenção, favor verificar.")

        if self.l_rv_modo_manut.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o RV entrou em modo de manutenção, favor verificar.")

        if self.l_rv_girando_gir_indev.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o Rv está girando com giro indevido, favor verificar.")

        if self.l_rt_alar_1_sobretensao.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 de sobretensão do RT, favor verificar.")

        if self.l_rt_alar_1_subtensao.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 de subtensão do RT, favor verificar.")

        if self.l_rt_alar_1_sobrefrequencia.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 de sobrefrequência do RT, favor verificar.")

        if self.l_rt_alar_1_subfrequencia.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 de subfrequência do RT, favor verificar.")

        if self.l_rt_alar_1_lim_sup_pot_reativa.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 limite superior de potência reativa do RT, favor verificar.")

        if self.l_rt_alar_1_lim_inf_pot_reativa.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 limite inferior de potência reativa do RT, favor verificar.")

        if self.l_rt_alar_1_lim_sup_fator_pot.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 limite superior de fator de potência do RT, favor verificar.")

        if self.l_rt_alar_1_lim_inf_fator_pot.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 limite inferior de fator de potência do RT, favor verificar.")

        if self.l_rt_alar_1_variacao_tensao.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 variação de tensao do RT, favor verificar.")

        if self.l_rt_alar_1_pot_ativa_reversa.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 potência ativa reversa do RT, favor verificar.")

        if self.l_rt_alar_1_sobrecorr_term.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 sobrecorrente terminal do RT, favor verificar.")

        if self.l_rt_alar_1_lim_sup_corr_excitacao.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 limite superior corrente de excitação do RT, favor verificar.")

        if self.l_rt_alar_1_lim_inf_corr_exci.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 limite inferior corrente de excitação do RT, favor verificar.")

        if self.l_rt_alar_1_temp_muito_alta_rotor.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 temperatura muito alta do rotor do RT, favor verificar.")

        if self.l_rt_alar_1_pres_tens_term_aus_corr_exci.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 presença de tensão terminal e ausência de corrente de excitação no RT, favor verificar.")

        if self.l_rt_alar_1_pres_corr_exci_aus_tens_term.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 1 presença de corrente de excitação e ausenência de tensão terminal no RT, favor verificar.")

        if self.l_rt_alar_2_falha_contro_corr_exci.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 2 falha de controle de corrente de excitação do RT, favor verificar.")

        if self.l_rt_alar_2_falha_contro_tens_term.valor:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do alarme 2 falha de controle de tensão terminal do RT, favor verificar.")

        if self.l_uhrv_oleo_nv_muito_baixo.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o óleo da UHRV está com o nível muito baixo, favor verificar.")

        if self.l_uhrv_filtro_oleo_sujo.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o filtro de óleo da UHRV está sujo, favor verificar.")

        if self.l_urhv_press_crit.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a pressão da UHRV está em nível crítico, favor verificar.")

        if self.l_uhrv_oleo_nv_muito_alto.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o óleo da UHRV está com o nível muito alto, favor verificar.")

        if self.l_uhlm_oleo_nv_muito_baixo.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o óleo da UHLM está com o nível muito baixo, favor verificar.")

        if self.l_uhlm_press_linha_lubrifi.valor:
            logger.warning(f"[UG{self.id}] Foi identificado a falta de pressão de lubrificação de linha da UHLM, favor verificar.")

        if self.l_uhlm_fluxo_troc_calor.valor:
            logger.warning(f"[UG{self.id}] Foi identificado a falta de fluxo do trocador de calor da UHLM, favor verificar.")

        if self.l_qbag_escova_polo_pos_desgas.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a escova do polo positivo QBAG está desgastada, favor verificar.")

        if self.l_qbag_escova_polo_neg_desgas.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a escova do polo negativo QBAG está desgastada, favor verificar.")

        if self.l_tristor_temp_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura de Tristores está muito alta, favor verificar.")

        if self.l_crowbar_temp_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Crowbar está muito alta, favor verificar.")

        if self.l_trafo_exci_temp_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Transformado de excitação está muito alta, favor verificar.")

        if self.l_uhrv_temp_oleo_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do óleo da UHRV está muito alta, favor verificar.")

        if self.l_gera_fase_a_temp_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura de Fase A do Gerador está muito alta, favor verificar.")

        if self.l_gera_fase_b_temp_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura de Fase B do Gerador está muito alta, favor verificar.")

        if self.l_gera_fase_c_temp_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura de Fase C do Gerador está muito alta, favor verificar.")

        if self.l_gera_nucleo_1_temp_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Núcleo 1 do Gerador está muito alta, favor verificar.")

        if self.l_gera_nucleo_2_temp_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Núcleo 2 do Gerador está muito alta, favor verificar.")

        if self.l_gera_nucleo_3_temp_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Núcleo 3 do Gerador está muito alta, favor verificar.")

        if self.l_mancal_guia_casq_temp_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Mancal Guia Casquilho está muito alta, favor verificar.")

        if self.l_mancal_comb_casq_temp_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Mancal Combinado Casquilho está muito alta, favor verificar.")

        if self.l_mancal_comb_esc_temp_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a temperatura do Mancal Combinado Escora está muito alta, favor verificar.")

        if self.l_uhrv_press_oleo_falha_leitura.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de pressão do óleo da UHRV, favor verificar.")

        if self.l_uhrv_press_oleo_muito_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a pressão do óleo da UHRV está muito alta, favor verificar.")

        if self.l_uhrv_press_oleo_alta.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que a pressão do óleo da UHRV está alta, favor verificar.")

        if self.l_contro_trip_dif_grade.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um acionamento de Trip do Controle de Diferencial de Grade, favor verificar.")

        if self.l_resis_aquec_gera_falha_deslig.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha no desligamento da resistência do aquecedor do gerador, favor verificar.")

        if self.l_uhlm_bomba_1_falha_ligar.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha ao ligar a Bomba 1 da UHLM, favor verificar.")

        if self.l_uhlm_bomba_1_falha_deslig.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha no desligamento da Bomba 1 da UHLM, favor verificar.")

        if self.l_ulhm_falha_pressos.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha no pressostato da UHLM, favor verificar.")

        if self.l_rv_falha_partir.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha ao partir o RV, favor verificar.")

        if self.l_rv_falha_desab.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha ao desabilitar o RV, favor verificar.")

        if self.l_rv_falha_parar_maqu.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha ao parar a máquina pelo RV, favor verificar.")

        if self.l_rt_falha_partir.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha ao partir a máquina pelo RT, favor verificar.")

        if self.l_rt_falha_desab.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha ao desabilitar o RT, favor verificar.")

        if self.l_valv_borb_falha_fechar.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha no fechamento da válvula borboleta, favor verificar.")

        if self.l_valv_borb_dicrep_senso.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma discrepância no sensor da válvula borboleta, favor verificar.")

        if self.l_vavl_bypass_discrep_senso.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma discrepância no sensor da válvula bypass, favor verificar.")


        # WHATSAPP + VOIP
        if self.l_val_bypass_falha_abrir.valor and not d.voip[f"UG{self.id}_ED_BYPASS_FALHA_ABRIR"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha ao abrir a Válvula Bypass, favor verificar.")
            d.voip[f"UG{self.id}_ED_BYPASS_FALHA_ABRIR"][0] = True
        elif not self.l_val_bypass_falha_abrir.valor and d.voip[f"UG{self.id}_ED_BYPASS_FALHA_ABRIR"][0]:
            d.voip[f"UG{self.id}_ED_BYPASS_FALHA_ABRIR"][0] = False

        if self.l_val_bypass_falha_fechar.valor and not d.voip[f"UG{self.id}_ED_BYPASS_FALHA_FECHAR"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha ao fechar a Válvula Bypass, favor verificar.")
            d.voip[f"UG{self.id}_ED_BYPASS_FALHA_FECHAR"][0] = True
        elif not self.l_val_bypass_falha_fechar.valor and d.voip[f"UG{self.id}_ED_BYPASS_FALHA_FECHAR"][0]:
            d.voip[f"UG{self.id}_ED_BYPASS_FALHA_FECHAR"][0] = False

        if self.l_falha_fechar_distrib.valor and not d.voip[f"UG{self.id}_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha ao fechar o Distribuidor, favor verificar.")
            d.voip[f"UG{self.id}_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR"][0] = True
        elif not self.l_falha_fechar_distrib.valor and d.voip[f"UG{self.id}_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR"][0]:
            d.voip[f"UG{self.id}_ED_RV_FALHA_AO_FECHAR_DISTRIBUIDOR"][0] = False

        if self.l_cmd_uhrv_modo_manuten.valor and not d.voip[f"UG{self.id}_CD_CMD_UHRV_MODO_MANUTENCAO"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do comando do modo de manutenção da UHRV, favor verificar.")
            d.voip[f"UG{self.id}_CD_CMD_UHRV_MODO_MANUTENCAO"][0] = True
        elif not self.l_cmd_uhrv_modo_manuten.valor and d.voip[f"UG{self.id}_CD_CMD_UHRV_MODO_MANUTENCAO"][0]:
            d.voip[f"UG{self.id}_CD_CMD_UHRV_MODO_MANUTENCAO"][0] = False

        if self.l_cmd_uhlm_modo_manuten.valor and not d.voip[f"UG{self.id}_CD_CMD_UHLM_MODO_MANUTENCAO"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado o acionamento do comando do modo de manutenção da UHLM, favor verificar.")
            d.voip[f"UG{self.id}_CD_CMD_UHLM_MODO_MANUTENCAO"][0] = True
        elif not self.l_cmd_uhlm_modo_manuten.valor and d.voip[f"UG{self.id}_CD_CMD_UHLM_MODO_MANUTENCAO"][0]:
            d.voip[f"UG{self.id}_CD_CMD_UHLM_MODO_MANUTENCAO"][0] = False

        if self.l_falha_leit_temp_tristores.valor and not d.voip[f"UG{self.id}_EA_TRISTORES_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de temperatura de Tristores, favor verificar.")
            d.voip[f"UG{self.id}_EA_TRISTORES_TEMP_FALHA_LEITURA"][0] = True
        elif not self.l_falha_leit_temp_tristores.valor and d.voip[f"UG{self.id}_EA_TRISTORES_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.id}_EA_TRISTORES_TEMP_FALHA_LEITURA"][0] = False

        if self.l_falha_leit_temp_crowbar.valor and not d.voip[f"UG{self.id}_EA_CROWBAR_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de temperatura do Crowbar, favor verificar.")
            d.voip[f"UG{self.id}_EA_CROWBAR_TEMP_FALHA_LEITURA"][0] = True
        elif not self.l_falha_leit_temp_crowbar.valor and d.voip[f"UG{self.id}_EA_CROWBAR_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.id}_EA_CROWBAR_TEMP_FALHA_LEITURA"][0] = False

        if self.l_falha_leit_temp_trafo_exci.valor and not d.voip[f"UG{self.id}_EA_TRAFO_EXCITACAO_FALHA_LEITURA"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de temperatura do Transformador de Excitação, favor verificar.")
            d.voip[f"UG{self.id}_EA_TRAFO_EXCITACAO_FALHA_LEITURA"][0] = True
        elif not self.l_falha_leit_temp_trafo_exci.valor and d.voip[f"UG{self.id}_EA_TRAFO_EXCITACAO_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.id}_EA_TRAFO_EXCITACAO_FALHA_LEITURA"][0] = False

        if self.l_falha_leit_temp_uhrv_temp_oleo.valor and not d.voip[f"UG{self.id}_EA_UHRV_TEMP_OLEO_FALHA_LEITURA"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de temperatura do Óleo da UHRV, favor verificar.")
            d.voip[f"UG{self.id}_EA_UHRV_TEMP_OLEO_FALHA_LEITURA"][0] = True
        elif not self.l_falha_leit_temp_uhrv_temp_oleo.valor and d.voip[f"UG{self.id}_EA_UHRV_TEMP_OLEO_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.id}_EA_UHRV_TEMP_OLEO_FALHA_LEITURA"][0] = False

        if self.l_falha_leit_temp_gerad_fase_a.valor and not d.voip[f"UG{self.id}_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de temperatura de Fase A do gerador, favor verificar.")
            d.voip[f"UG{self.id}_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA"][0] = True
        elif not self.l_falha_leit_temp_gerad_fase_a.valor and d.voip[f"UG{self.id}_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.id}_EA_GERADOR_FASE_A_TEMP_FALHA_LEITURA"][0] = False

        if self.l_falha_leit_temp_gerad_fase_b.valor and not d.voip[f"UG{self.id}_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de temperatura de Fase B do gerador, favor verificar.")
            d.voip[f"UG{self.id}_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA"][0] = True
        elif not self.l_falha_leit_temp_gerad_fase_b.valor and d.voip[f"UG{self.id}_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.id}_EA_GERADOR_FASE_B_TEMP_FALHA_LEITURA"][0] = False

        if self.l_falha_leit_temp_gerad_fase_c.valor and not d.voip[f"UG{self.id}_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de temperatura de Fase C do gerador, favor verificar.")
            d.voip[f"UG{self.id}_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA"][0] = True
        elif not self.l_falha_leit_temp_gerad_fase_c.valor and d.voip[f"UG{self.id}_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.id}_EA_GERADOR_FASE_C_TEMP_FALHA_LEITURA"][0] = False

        if self.l_falha_leit_temp_gerad_nucleo_1.valor and not d.voip[f"UG{self.id}_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de temperatura do Núcleo 1 do Gerador, favor verificar.")
            d.voip[f"UG{self.id}_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA"][0] = True
        elif not self.l_falha_leit_temp_gerad_nucleo_1.valor and d.voip[f"UG{self.id}_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.id}_EA_GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA"][0] = False

        if self.l_falha_leit_temp_gerad_nucleo_2.valor and not d.voip[f"UG{self.id}_EA_GERADOR_NUCLEO_2_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de temperatura do Núcleo 2 do Gerador, favor verificar.")
            d.voip[f"UG{self.id}_EA_GERADOR_NUCLEO_2_FALHA_LEITURA"][0] = True
        elif not self.l_falha_leit_temp_gerad_nucleo_2.valor and d.voip[f"UG{self.id}_EA_GERADOR_NUCLEO_2_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.id}_EA_GERADOR_NUCLEO_2_FALHA_LEITURA"][0] = False

        if self.l_falha_leit_temp_gerad_nucleo_3.valor and not d.voip[f"UG{self.id}_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de temperatura do Núcleo 3 do Gerador, favor verificar.")
            d.voip[f"UG{self.id}_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA"][0] = True
        elif not self.l_falha_leit_temp_gerad_nucleo_3.valor and d.voip[f"UG{self.id}_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.id}_EA_GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA"][0] = False

        if self.l_falha_leit_temp_mancal_guia_casq.valor and not d.voip[f"UG{self.id}_EA_MANCAL_GUIA_CASQUILHO_FALHA_LEITURA"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de temperatura do Mancal Guia Casquilho, favor verificar.")
            d.voip[f"UG{self.id}_EA_MANCAL_GUIA_CASQUILHO_FALHA_LEITURA"][0] = True
        elif not self.l_falha_leit_temp_mancal_guia_casq.valor and d.voip[f"UG{self.id}_EA_MANCAL_GUIA_CASQUILHO_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.id}_EA_MANCAL_GUIA_CASQUILHO_FALHA_LEITURA"][0] = False

        if self.l_falha_leit_temp_mancal_comb_casq.valor and not d.voip[f"UG{self.id}_EA_MANCAL_COMBINADO_CASQUILHO_FALHA_LEITURA"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de temperatura do Mancal Combinado Casquilho, favor verificar.")
            d.voip[f"UG{self.id}_EA_MANCAL_COMBINADO_CASQUILHO_FALHA_LEITURA"][0] = True
        elif not self.l_falha_leit_temp_mancal_comb_casq.valor and d.voip[f"UG{self.id}_EA_MANCAL_COMBINADO_CASQUILHO_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.id}_EA_MANCAL_COMBINADO_CASQUILHO_FALHA_LEITURA"][0] = False

        if self.l_falha_leit_temp_mancal_comb_esc.valor and not d.voip[f"UG{self.id}_EA_MANCAL_COMBINADO_ESCORA_FALHA_LEITURA"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha na leitura de temperatura do Mancal Combinado Escora, favor verificar.")
            d.voip[f"UG{self.id}_EA_MANCAL_COMBINADO_ESCORA_FALHA_LEITURA"][0] = True
        elif not self.l_falha_leit_temp_mancal_comb_esc.valor and d.voip[f"UG{self.id}_EA_MANCAL_COMBINADO_ESCORA_FALHA_LEITURA"][0]:
            d.voip[f"UG{self.id}_EA_MANCAL_COMBINADO_ESCORA_FALHA_LEITURA"][0] = False

        if self.l_resis_quec_gerador_falha_ligar.valor and not d.voip[f"UG{self.id}_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado uma falha ao ligar a resistência do aquecedor do gerador, favor verificar.")
            d.voip[f"UG{self.id}_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR"][0] = True
        elif not self.l_resis_quec_gerador_falha_ligar.valor and d.voip[f"UG{self.id}_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR"][0]:
            d.voip[f"UG{self.id}_ED_RESISTENCIA_AQUEC_GERADOR_FALHA_LIGAR"][0] = False


    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Unidade.
        """

        self.l_diferencial_grade = lei.LeituraSubtracao([tda.TomadaAgua.nv_montante, tda.TomadaAgua.nv_jusante], descricao="[TDA] Diferencial de Grade")
        self.c_diferencial_grade = c.CondicionadorExponencial(self.l_diferencial_grade, CONDIC_INDISPONIBILIZAR, valor_base=0.35, valor_limite=0.4, ordem=1)
        self.condicionadores_atenuadores.append(self.c_diferencial_grade)

        # Fase R
        self.l_tmp_fase_r = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMP_GERADOR_FASE_A"],
            escala=0.001,
            op=4
        )
        self.c_tmp_fase_r = c.CondicionadorExponencial(self.l_tmp_fase_r)
        self.condicionadores_essenciais.append(self.c_tmp_fase_r)
        self.condicionadores_atenuadores.append(self.c_tmp_fase_r)

        # Fase S
        self.l_tmp_fase_s = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMP_GERADOR_FASE_B"],
            escala=0.001,
            op=4
        )
        self.c_tmp_fase_s = c.CondicionadorExponencial(self.l_tmp_fase_s)
        self.condicionadores_essenciais.append(self.c_tmp_fase_s)
        self.condicionadores_atenuadores.append(self.c_tmp_fase_s)

        # Fase T
        self.l_tmp_fase_t = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMP_GERADOR_FASE_C"],
            escala=0.001,
            op=4
        )
        self.c_tmp_fase_t = c.CondicionadorExponencial(self.l_tmp_fase_t)
        self.condicionadores_essenciais.append(self.c_tmp_fase_t)
        self.condicionadores_atenuadores.append(self.c_tmp_fase_t)

        # Nucleo Gerador 1
        self.l_tmp_nucleo_gerador_1 = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMP_GERADOR_NUCLEO_1"],
            escala=0.001,
            op=4
        )
        self.c_tmp_nucleo_gerador_1 = c.CondicionadorExponencial(self.l_tmp_nucleo_gerador_1)
        self.condicionadores_essenciais.append(self.c_tmp_nucleo_gerador_1)
        self.condicionadores_atenuadores.append(self.c_tmp_nucleo_gerador_1)

        # Nucleo Gerador 2
        self.l_tmp_nucleo_gerador_2 = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMP_GERADOR_NUCLEO_2"],
            escala=0.001,
            op=4
        )
        self.c_tmp_nucleo_gerador_2 = c.CondicionadorExponencial(self.l_tmp_nucleo_gerador_2)
        self.condicionadores_essenciais.append(self.c_tmp_nucleo_gerador_2)
        self.condicionadores_atenuadores.append(self.c_tmp_nucleo_gerador_2)

        # Nucleo Gerador 3
        self.l_tmp_nucleo_gerador_3 = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMP_GERADOR_NUCLEO_3"],
            escala=0.001,
            op=4
        )
        self.c_tmp_nucleo_gerador_3 = c.CondicionadorExponencial(self.l_tmp_nucleo_gerador_3)
        self.condicionadores_essenciais.append(self.c_tmp_nucleo_gerador_3)
        self.condicionadores_atenuadores.append(self.c_tmp_nucleo_gerador_3)

        # Mancal Casquilho Radial
        self.l_tmp_mancal_casq_rad = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMP_MANCAL_GUIA_CASQUILHO"],
            escala=0.001,
            op=4
        )
        self.c_tmp_mancal_casq_rad = c.CondicionadorExponencial(self.l_tmp_mancal_casq_rad)
        self.condicionadores_essenciais.append(self.c_tmp_mancal_casq_rad)
        self.condicionadores_atenuadores.append(self.c_tmp_mancal_casq_rad)

        # Mancal Casquilho Combinado
        self.l_tmp_mancal_casq_comb = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMP_MANCAL_COMBINADO_CASQUILHO"],
            escala=0.001,
            op=4
        )
        self.c_tmp_mancal_casq_comb = c.CondicionadorExponencial(self.l_tmp_mancal_casq_comb)
        self.condicionadores_essenciais.append(self.c_tmp_mancal_casq_comb)
        self.condicionadores_atenuadores.append(self.c_tmp_mancal_casq_comb)

        # Mancal Escora Combinado
        self.l_tmp_mancal_escora_comb = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMP_MANCAL_COMBINADO_ESCORA"],
            escala=0.001,
            op=4
        )
        self.c_tmp_mancal_escora_comb = c.CondicionadorExponencial(self.l_tmp_mancal_escora_comb)
        self.condicionadores_essenciais.append(self.c_tmp_mancal_escora_comb)
        self.condicionadores_atenuadores.append(self.c_tmp_mancal_escora_comb)

        return
        ## CONDICINOADORES ESSENCIAIS
        self.l_rele_bloq_86eh = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RELE_BLOQ_86EH"], descricao=f"[UG{self.id}] Relé Bloqueio 86EH")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_bloq_86eh, CONDIC_NORMALIZAR))

        self.l_bloq_86e = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["BLOQ_86E_ATUADO"], descricao=f"[UG{self.id}] Bloqueio 86E")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_bloq_86e, CONDIC_NORMALIZAR))

        self.l_bloq_86h = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["BLOQ_86H_ATUADO"], descricao=f"[UG{self.id}] Bloqueio 86H")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_bloq_86h, CONDIC_NORMALIZAR))

        self.l_status_bloq_86m = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["BLOQ_86M_ATUADO"], descricao=f"[UG{self.id}] Status Bloqueio 86M")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_status_bloq_86m, CONDIC_NORMALIZAR))

        self.l_rt_falha_2_bloq_externo = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_BLOQ_EXTERNO"], descricao=f"[UG{self.id}] RT Falha 2 Bloqueio Externo")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rt_falha_2_bloq_externo, CONDIC_NORMALIZAR))

        self.l_rele_trip_prot_gerad = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RELE_PROT_GERADOR_TRIP"], descricao=f"[UG{self.id}] Relé Trip Proteção Gerador")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rele_trip_prot_gerad, CONDIC_NORMALIZAR))

        self.l_rv_trip = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_TRIP"], descricao=f"[UG{self.id}] RV Trip")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rv_trip, CONDIC_NORMALIZAR))

        self.l_rt_trip = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_TRIP"], descricao=f"[UG{self.id}] RT Trip")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_rt_trip, CONDIC_NORMALIZAR))


        ## CONDICIONADORES NORMALIZAR
        self.l_val_bypass_falha_abrir = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["BYPASS_FALHA_ABRIR"], descricao=f"[UG{self.id}] Válvula Bypass Falha Abrir")
        self.condicionadores.append(c.CondicionadorBase(self.l_val_bypass_falha_abrir, CONDIC_NORMALIZAR))

        self.l_val_bypass_falha_fechar = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["BYPASS_FALHA_FECHAR"], descricao=f"[UG{self.id}] Válvula Bypass Falha Fechar")
        self.condicionadores.append(c.CondicionadorBase(self.l_val_bypass_falha_fechar, CONDIC_NORMALIZAR))

        self.l_rv_alarme_sobrefrequncia = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_ALARME_SOBREFREQUENCIA"], descricao=f"[UG{self.id}] RV Alarme Sobrefrequência")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_alarme_sobrefrequncia, CONDIC_NORMALIZAR))

        self.l_rv_alarme_subfrequencia = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_ALARME_SUBFREQUENCIA"], descricao=f"[UG{self.id}] RV Alarme Subfrequência")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_alarme_subfrequencia, CONDIC_NORMALIZAR))

        # TODO -> Verificar
        self.l_botao_bloq_86eh = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["BT_BLOQ_86EH"], descricao=f"[UG{self.id}] Botão Bloqueio 86EH")
        self.condicionadores.append(c.CondicionadorBase(self.l_botao_bloq_86eh, CONDIC_NORMALIZAR))


        # ## CONDICIONADORES INDISPONIBILIZAR
        # ENTRADAS DIGITAIS
        self.l_falha_fechar_distrib = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_FECHAR_DISTRIBUIDOR"], descricao=f"[UG{self.id}] Falha Fechamento Distribuidor")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_fechar_distrib, CONDIC_INDISPONIBILIZAR))

        self.l_contro_trip_dif_grade = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CTRL_TRIP_DIFERENCIAL_DE_GRADE"], descricao=f"[UG{self.id}] Contorle Trip Diferencial Grade")
        self.condicionadores.append(c.CondicionadorBase(self.l_contro_trip_dif_grade, CONDIC_INDISPONIBILIZAR))

        self.l_resis_aquec_gera_falha_deslig = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RESIS_AQUEC_GERA_FALHA_DESLIGAR"], descricao=f"[UG{self.id}] Resistência Aquecedor Gerador Falha Desligar")
        self.condicionadores.append(c.CondicionadorBase(self.l_resis_aquec_gera_falha_deslig, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_partir = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_PARTIR"], descricao=f"[UG{self.id}] RV Falha Partir")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_partir, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_desab = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_DESABILITAR"], descricao=f"[UG{self.id}] RV Falha Desabilitar")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_desab, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_parar_maqu = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_PARAR_MAQUINA"], descricao=f"[UG{self.id}] RV Falha Parar Máquina")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_parar_maqu, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_partir = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_PARTIR"], descricao=f"[UG{self.id}] RT Falha Partir")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_partir, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_desab = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_DESABILITAR"], descricao=f"[UG{self.id}] RT Falha Desabilitar")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_desab, CONDIC_INDISPONIBILIZAR))

        self.l_valv_borb_falha_fechar = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["BORB_FALHA_FECHAR"], descricao=f"[UG{self.id}] Válvula Borboleta Falha Fechar")
        self.condicionadores.append(c.CondicionadorBase(self.l_valv_borb_falha_fechar, CONDIC_INDISPONIBILIZAR))

        self.l_valv_borb_dicrep_senso = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["BORB_DISCRE_SENSES"], descricao=f"[UG{self.id}] Válvula Borboleta Discrepância Sensores")
        self.condicionadores.append(c.CondicionadorBase(self.l_valv_borb_dicrep_senso, CONDIC_INDISPONIBILIZAR))

        self.l_vavl_bypass_discrep_senso = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["BYPASS_DISCRE_SENSES"], descricao=f"[UG{self.id}] Válvula Bypass Discrepância Sensores")
        self.condicionadores.append(c.CondicionadorBase(self.l_vavl_bypass_discrep_senso, CONDIC_INDISPONIBILIZAR))

        # UG_STT_ENTRADAS_DIGITAIS
        self.l_uhrv_oleo_nv_muito_baixo = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_OLEO_NV_MUITO_BAIXO"], descricao=f"[UG{self.id}] UHRV Óleo Nível Muito Baixo")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhrv_oleo_nv_muito_baixo, CONDIC_INDISPONIBILIZAR))

        self.l_uhrv_filtro_oleo_sujo = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_FILTRO_OLEO_SUJO"], descricao=f"[UG{self.id}] UHRV Filtro Óleo Sujo")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhrv_filtro_oleo_sujo, CONDIC_INDISPONIBILIZAR))

        self.l_urhv_press_crit = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_PRESSAO_CRITICA"], descricao=f"[UG{self.id}] UHRV Pressão Crítica")
        self.condicionadores.append(c.CondicionadorBase(self.l_urhv_press_crit, CONDIC_INDISPONIBILIZAR))

        self.l_uhrv_oleo_nv_muito_alto = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_OLEO_NV_MUITO_ALTO"], descricao=f"[UG{self.id}] UHRV Óleo Nível Muito Alto")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhrv_oleo_nv_muito_alto, CONDIC_INDISPONIBILIZAR))

        self.l_uhlm_oleo_nv_muito_baixo = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_OLEO_NV_MUITO_BAIXO"], descricao=f"[UG{self.id}] UHLM Óleo Nível Muito Baixo")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhlm_oleo_nv_muito_baixo, CONDIC_INDISPONIBILIZAR))

        # TODO -> Verificar
        self.l_uhlm_press_linha_lubrifi = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_PRESSAO_LINHA_LUBRIF"], descricao=f"[UG{self.id}] UHLM Pressão Linha Lubrificação")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhlm_press_linha_lubrifi, CONDIC_NORMALIZAR))

        # TODO n-> Verificar
        self.l_uhlm_fluxo_troc_calor = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_FLUXO_TROCADOR_CALOR"], descricao=f"[UG{self.id}] UHLM Fluxo Trocador Calor")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhlm_fluxo_troc_calor, CONDIC_NORMALIZAR))

        # TODO -> Verificar
        self.l_qbag_escova_polo_pos_desgas = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["QBAG_ESCOVA_POLO_POS_DESGASTADA"], descricao=f"[UG{self.id}] QBAG Escova Polo Positivo Desgastada")
        self.condicionadores.append(c.CondicionadorBase(self.l_qbag_escova_polo_pos_desgas, CONDIC_INDISPONIBILIZAR))

        self.l_qbag_escova_polo_neg_desgas = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["QBAG_ESCOVA_POLO_NEG_DESGASTADA"], descricao=f"[UG{self.id}] QBAG Escova Polo Negativo Desgastada")
        self.condicionadores.append(c.CondicionadorBase(self.l_qbag_escova_polo_neg_desgas, CONDIC_INDISPONIBILIZAR))

        self.l_rele_prot_gerad_50bf = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RELE_PROT_GERADOR_50BF"], descricao=f"[UG{self.id}] Relé Proteção Gerador 50BF")
        self.condicionadores.append(c.CondicionadorBase(self.l_rele_prot_gerad_50bf, CONDIC_INDISPONIBILIZAR))

        self.l_disj_tps_protecao = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["DJ_TPS_PROTECAO"], descricao=f"[UG{self.id}] Disjuntor TPS Proteção")
        self.condicionadores.append(c.CondicionadorBase(self.l_disj_tps_protecao, CONDIC_INDISPONIBILIZAR))

        # TODO -> Verificar
        self.l_uhrv_pressao_freio = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_PRESSAO_FREIO"], descricao=f"[UG{self.id}] UHRV Pressão Freio")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhrv_pressao_freio, CONDIC_NORMALIZAR))

        self.l_rv_falha_hab = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_HABILITAR"], descricao=f"[UG{self.id}] RV Falha Habilitar")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_hab, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_hab = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_HABILITAR"], descricao=f"[UG{self.id}] RT Falha Habilitar")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_hab, CONDIC_INDISPONIBILIZAR))

        # UHRV
        # TODO -> Verificar
        self.l_uhrv_bomba_1_indisp = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_BOMBA_1_INDISPONV"], descricao=f"[UG{self.id}] UHRV Bomba 1 Indisponível") # TODO -> Verificar invertido
        self.condicionadores.append(c.CondicionadorBase(self.l_uhrv_bomba_1_indisp, CONDIC_INDISPONIBILIZAR))

        self.l_uhrv_bomba_1_falha_ligar = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_BOMBA_1_FALHA_LIGAR"], descricao=f"[UG{self.id}] UHRV Falha Ligar")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhrv_bomba_1_falha_ligar, CONDIC_INDISPONIBILIZAR))

        self.l_uhrv_filtro_oleo_sujo = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_FILTRO_OLEO_SUJO"], descricao=f"[UG{self.id}] UHRV Filtro Óleo Sujo")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhrv_filtro_oleo_sujo, CONDIC_INDISPONIBILIZAR))

        # UHLM
        self.l_uhlm_bomba_1_falha_ligar = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_BOMBA_1_FALHA_LIGAR"], descricao=f"[UG{self.id}] UHLM Bomba 1 Falha Ligar")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhlm_bomba_1_falha_ligar, CONDIC_INDISPONIBILIZAR))

        self.l_uhlm_bomba_1_falha_deslig = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_BOMBA_1_FALHA_DESLIGAR"], descricao=f"[UG{self.id}] UHLM Bomba 1 Falha Desligar")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhlm_bomba_1_falha_deslig, CONDIC_INDISPONIBILIZAR))

        self.l_ulhm_falha_pressos = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_FALHA_PRESSOSTATO"], descricao=f"[UG{self.id}] UHLM Falha Pressostato")
        self.condicionadores.append(c.CondicionadorBase(self.l_ulhm_falha_pressos, CONDIC_INDISPONIBILIZAR))

        self.l_uhlm_bomba_1_indisp = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_BOMBA_1_INDISPONV"], descricao=f"[UG{self.id}] UHLM Bomba 1 Indisponível")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhlm_bomba_1_indisp, CONDIC_INDISPONIBILIZAR))

        self.l_uhlm_bomba_1_falha_pressurizar = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_BOMBA_1_FALHA_PRESSURIZAR"], descricao=f"[UG{self.id}] UHLM Bomba 1 Falha Pressurizar")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhlm_bomba_1_falha_pressurizar, CONDIC_INDISPONIBILIZAR))

        self.l_ulhm_filtro_sujo = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_FILTRO_OLEO_SUJO"], descricao=f"[UG{self.id}] UHLM Filtro Sujo")
        self.condicionadores.append(c.CondicionadorBase(self.l_ulhm_filtro_sujo, CONDIC_INDISPONIBILIZAR))

        # RV
        self.l_rv_girando_gir_indev = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_GIRANDO_SEM_REG_GIRO_INDEVIDO"], descricao=f"[UG{self.id}] Falha RV Girando Sem Registro de Giro Indevido")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_girando_gir_indev, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_1_sobrefreq_inst = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_SOBREFREQUENCIA_INSTAN"], descricao=f"[UG{self.id}] RV Falha 1 Sobrefrequência Instantânea")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_1_sobrefreq_inst, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_1_sobrefreq_tempor = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_SOBREFREQUENCIA_TEMPO"], descricao=f"[UG{self.id}] RV Falha 1 Sobrefrequência Temporizada")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_1_sobrefreq_tempor, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_1_subfreq_tempor = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_SUBFREQUENCIA_TEMPO"], descricao=f"[UG{self.id}] RV Falha 1 Subfrequência Temporizada")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_1_subfreq_tempor, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_1_leit_pos_distrib = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_LEITURA_POS_DISTRI"], descricao=f"[UG{self.id}] RV Falha 1 Leitura Posição Distribuidor")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_1_leit_pos_distrib, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_1_leit_pot_ativa = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_LEITURA_POT_ATIVA"], descricao=f"[UG{self.id}] RV Falha 1 Leitura Potência Ativa")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_1_leit_pot_ativa, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_1_leit_refer_pot = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_LEITURA_REF_POT"], descricao=f"[UG{self.id}] RV Falha 1 Leitura Referência Potência")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_1_leit_refer_pot, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_1_nv_montante_muito_baixo = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_NV_MONTANTE_MUITO_BAIXO"], descricao=f"[UG{self.id}] RV Falha 1 Nível Montante Muito Baixo")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_1_nv_montante_muito_baixo, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_1_control_pos_distribu = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_CTRL_POS_DISTRI"], descricao=f"[UG{self.id}] RV Falha 1 Controle Posição Distribuidor")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_1_control_pos_distribu, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_1_ruido_med_veloc_princi = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_RUIDO_MED_VELO_PRINC"], descricao=f"[UG{self.id}] RV Falha 1 Ruído Medição Velocidade Principal")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_1_ruido_med_veloc_princi, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_1_ruido_med_veloc_retag = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_RUIDO_MED_VELO_RETAG"], descricao=f"[UG{self.id}] RV Falha 1 Ruído Medição Velocidade Retaguarda")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_1_ruido_med_veloc_retag, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_2_perda_med_veloc_retag = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_RUIDO_MED_VELO_RETAG"], descricao=f"[UG{self.id}] RV Falha 2 Perda Medição Velocidade Retaguarda")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_2_perda_med_veloc_retag, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_2_tempo_excess_partida = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_TEMPO_EXCESSIVO_PARTIDA"], descricao=f"[UG{self.id}] RV Falha 2 Tempo Excessivo Partida")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_2_tempo_excess_partida, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_2_tempo_excess_parada = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_TEMPO_EXCESSIVO_PARADA"], descricao=f"[UG{self.id}] RV Falha 2 Tempo Excessivo Parada")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_2_tempo_excess_parada, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_2_dif_med_velo_princ_retag = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_DIF_MED_VELO_PRINC_RETAG"], descricao=f"[UG{self.id}] RV Falha 2 Diferença Medição Velocidade Principal Retaguarda")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_2_dif_med_velo_princ_retag, CONDIC_INDISPONIBILIZAR))

        self.l_rv_falha_1_perda_med_velo_princ = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_FALHA_PERDA_MED_VELO_PRINC"], descricao=f"[UG{self.id}] RV Falha 1 Perda Medição Velocidade Principal")
        self.condicionadores.append(c.CondicionadorBase(self.l_rv_falha_1_perda_med_velo_princ, CONDIC_INDISPONIBILIZAR))

        # RT
        self.l_rt_crowbar_inativo = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_CROWBAR_INATIVO"], descricao=f"[UG{self.id}] RT Crowbar Inativo")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_crowbar_inativo, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_sobretensao = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_SOBRETENSAO"], descricao=f"[UG{self.id}] RT Alarmes 1 Sobretensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_sobretensao, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_subtensao = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_SUBTENSAO"], descricao=f"[UG{self.id}] RT Alarmes 1 Subtensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_subtensao, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_sobrefrequencia = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_SOBREFREQUENCIA"], descricao=f"[UG{self.id}] RT Alarmes 1 Sobrefrequência")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_sobrefrequencia, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_subfrequencia = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_SUBFREQUENCIA"], descricao=f"[UG{self.id}] RT Alarmes 1 Subfrequência")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_subfrequencia, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_lim_sup_pot_reativa = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_LIM_SUP_POT_REATIVA"], descricao=f"[UG{self.id}] RT Alarmes 1 Limite Superior Potência Reativa")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_lim_sup_pot_reativa, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_lim_inf_pot_reativa = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_LIM_INF_POT_REATIVA"], descricao=f"[UG{self.id}] RT Alarmes 1 Limite Inferior Potência Reativa")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_lim_inf_pot_reativa, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_lim_sup_fator_pot = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_LIM_SUP_FATOR_DE_POT"], descricao=f"[UG{self.id}] RT Alarmes 1 Limite Superior Fator Potência")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_lim_sup_fator_pot, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_lim_inf_fator_pot = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_LIM_INF_FATOR_DE_POT"], descricao=f"[UG{self.id}] RT Alarmes 1 Limite Inferior Fator Potência")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_lim_inf_fator_pot, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_variacao_tensao = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_VARIACAO_TENSAO"], descricao=f"[UG{self.id}] RT Alarmes 1 Variação de Tensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_variacao_tensao, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_pot_ativa_reversa = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_POT_ATIVA_REVERSA"], descricao=f"[UG{self.id}] RT Alarmes 1 Potência Ativa Reversa")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_pot_ativa_reversa, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_sobrecorr_term = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_SOBRECORRENTE_TERMINAL"], descricao=f"[UG{self.id}] RT Alarmes 1 Sobrecorrente Terminal")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_sobrecorr_term, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_lim_sup_corr_excitacao = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_LIM_SUP_CORRENTE_EXCITACAO"], descricao=f"[UG{self.id}] RT Alarmes 1 Limite Superior Corrente Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_lim_sup_corr_excitacao, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_lim_inf_corr_exci = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_LIM_INF_CORRENTE_EXCITACAO"], descricao=f"[UG{self.id}] RT Alarmes 1 Limite Inferior Corrente Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_lim_inf_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_temp_muito_alta_rotor = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_TEMP_MUITO_ALTA_ROTOR"], descricao=f"[UG{self.id}] RT Alarmes 1 Temperatura Muito Alta Rotor")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_temp_muito_alta_rotor, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_pres_tens_term_aus_corr_exci = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["_RT_ALARMES_1_PRES_TENS_TERM_AUSEN_CORR_EXCI"], descricao=f"[UG{self.id}] RT Alarmes 1 Presença Tensão Terminal Ausente Corrente Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_pres_tens_term_aus_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_1_pres_corr_exci_aus_tens_term = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_PRES_TENSAO_TERMINAL_AUSENCIA_CORRENTE_EXCITACAO"], descricao=f"[UG{self.id}] RT Alarmes 1 Presença Corrente Excitação Ausente Tensão Terminal")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_1_pres_corr_exci_aus_tens_term, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_2_falha_contro_corr_exci = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_FALHA_CONTROLE_CORRENTE_EXCITACAO"], descricao=f"[UG{self.id}] RT Alarmes 2 Falha Controle Corrente Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_2_falha_contro_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_2_falha_contro_tens_term = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_FALHA_CONTROLE_TENSAO_TERMINAL"], descricao=f"[UG{self.id}] RT Alarmes 2 Falha Controle Tensão Terminal")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_2_falha_contro_tens_term, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_2_crowbar_atuado_regul_hab = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_CROWBAR_ATUADO_REGULADOR_HABILITADO"], descricao=f"[UG{self.id}] RT Alarme 2 Crowbar Atuado Regulador Habilitado")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_2_crowbar_atuado_regul_hab, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_2_falha_hab_drive_excit = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_FALHA_HAB_DRIVE_EXCITACAO"], descricao=f"[UG{self.id}] RT Alarme 2 Falha Habilitar Drive Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_2_falha_hab_drive_excit, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_2_falha_fechar_contator_campo = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_FALHA_FECHAR_CONTATOR_CAMPO"], descricao=f"[UG{self.id}] RT Alarme 2 Falha Fechar Contator Campo")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_2_falha_fechar_contator_campo, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_2_falha_corr_exci_pre_exci_ativa = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_FALHA_CORRENTE_EXCITACAO_PRE_EXCITACAO_ATIVA"], descricao=f"[UG{self.id}] RT Alarme 2 Falha Corrente Excitação Pré Excitação Ativa")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_2_falha_corr_exci_pre_exci_ativa, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_2_perda_med_pot_reat = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_PERDA_MED_POT_REATIVA"], descricao=f"[UG{self.id}] RT Alarme 2 Perda Medição Potência Reativa")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_2_perda_med_pot_reat, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_2_perda_med_tens_term = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_PERDA_MED_TENSAO_TERMINAL"], descricao=f"[UG{self.id}] RT Alarme 2 Perda Medição Tensão Terminal")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_2_perda_med_tens_term, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_2_perda_med_corr_exci = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_PERDA_MED_CORRENTE_EXCITACAO"], descricao=f"[UG{self.id}] RT Alarme 2 Perda Medição Corrente Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_2_perda_med_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_ruido_intrumen_reat = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_RUIDO_INSTRU_REATIVO"], descricao=f"[UG{self.id}] RT Alarme 2 Ruído Leitura Intrumentador Reativo")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_ruido_intrumen_reat, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_ruido_intrumen_tensao = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_RUIDO_INSTRU_TENSAO"], descricao=f"[UG{self.id}] RT Alarme 2 Ruído Leitura Intrumentador Tensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_ruido_intrumen_tensao, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_ruido_intrumen_exci_princ = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_RUIDO_INSTRU_EXCITACAO_PRINC"], descricao=f"[UG{self.id}] RT Alarme 2 Ruído Leitura Intrumentador Excitação Principal")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_ruido_intrumen_exci_princ, CONDIC_INDISPONIBILIZAR))

        self.l_rt_alar_ruido_intrumen_exci_retag = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_ALARME_RUIDO_INSTRU_EXCITACAO_RETAG"], descricao=f"[UG{self.id}] RT Alarme 2 Ruído Leitura Intrumentador Excitação Retaguarda")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_alar_ruido_intrumen_exci_retag, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_sobretensao = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_SOBRETENSAO"], descricao=f"[UG{self.id}] RT Falha 1 Sobretensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_sobretensao, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_subtensao = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_SUBTENSAO"], descricao=f"[UG{self.id}] RT Falha 1 Subtensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_subtensao, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_sobrefreq = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_SOBREFREQUENCIA"], descricao=f"[UG{self.id}] RT Falha 1 Sobrefrequência")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_sobrefreq, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_subfreq = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_SUBFREQUENCIA"], descricao=f"[UG{self.id}] RT Falha 1 Subfrequência")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_subfreq, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_lim_sup_pot_reat = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_LIM_SUP_POT_REATIVA"], descricao=f"[UG{self.id}] RT Falha 1 Limite Superior Potência Reativa")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_lim_sup_pot_reat, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_lim_inf_pot_reat = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_LIM_INF_POT_REATIVA"], descricao=f"[UG{self.id}] RT Falha 1 Limite Inferior Potência Reativa")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_lim_inf_pot_reat, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_lim_sup_fator_pot = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_LIM_SUP_FATOR_POT"], descricao=f"[UG{self.id}] RT Falha 1 Limite Superior Fator Potência")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_lim_sup_fator_pot, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_lim_inf_fator_pot = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_LIM_INF_FATOR_POT"], descricao=f"[UG{self.id}] RT Falha 1 Limite Inferior Fator Potência")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_lim_inf_fator_pot, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_sobretensao_inst = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_SOBRETENSAO_INSTAN"], descricao=f"[UG{self.id}] RT Falha 1 Sobretensão Instantânea")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_sobretensao_inst, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_variacao_tensao = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_VARIACAO_TENSAO"], descricao=f"[UG{self.id}] RT Falha 1 Variação Tensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_variacao_tensao, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_pot_ativ_reversa = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_POT_ATIVA_REVERSA"], descricao=f"[UG{self.id}] RT Falha 1 Potência Ativa Reversa")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_pot_ativ_reversa, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_sobrecorr_term = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_SOBRECORRENTE_TERM"], descricao=f"[UG{self.id}] RT Falha 1 Sobrecorrente Terminal")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_sobrecorr_term, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_lim_sup_corr_exci = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_LIM_SUP_CORRENTE_EXCITACAO"], descricao=f"[UG{self.id}] RT Falha 1 Limite Superior Corrente Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_lim_sup_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_lim_inf_corr_exci = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_LIM_INF_CORRENTE_EXCITACAO"], descricao=f"[UG{self.id}] RT Falha 1 Limite Inferior Corrente Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_lim_inf_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_lim_sup_tensao_exci = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_LIM_SUP_TENSAO_EXCITACAO"], descricao=f"[UG{self.id}] RT Falha 1 Limite Superior Tensão Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_lim_sup_tensao_exci, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_1_lim_inf_tensao_exci = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_LIM_INF_TENSAO_EXCITACAO"], descricao=f"[UG{self.id}] RT Falha 1 Limite Inferior Tensão Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_1_lim_inf_tensao_exci, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_2_temp_muito_alta_rotor = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_TEMP_MUITO_ALTA_ROTOR"], descricao=f"[UG{self.id}] RT Falha 2 Temperatura Muito Alta Rotor")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_2_temp_muito_alta_rotor, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_2_pres_tens_term_aus_corr_exci = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_PRESENCA_TENSAO_TERMINAL_AUSENCIA_CORRENTE_EXCITACAO"], descricao=f"[UG{self.id}] RT Falha 2 Presença Tensão Terminal Ausente Corrente Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_2_pres_tens_term_aus_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_2_pres_corr_exci_aus_tens_term = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_PRESENCA_CORRENTE_EXCITACAO_AUSENCIA_TENSAO_TERM"], descricao=f"[UG{self.id}] RT Falha 2 Presença Corrente Excitação Ausente Tensão Terminal")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_2_pres_corr_exci_aus_tens_term, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_2_control_corr_exci = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_CTRL_CORRENTE_EXCITACAO"], descricao=f"[UG{self.id}] RT Falha 2 Controle Corrente Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_2_control_corr_exci, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_2_tensao_term = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_CTRL_TENSAO_TERMINAL"], descricao=f"[UG{self.id}] RT Falha 2 Tensão Terminal")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_2_tensao_term, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_2_crowbar_atuado_regu_hab = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_CROWBAR_ATUADO_REGULADOR_HAB"], descricao=f"[UG{self.id}] RT Falha 2 Crowbar Atuado Regulador Habilitado")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_2_crowbar_atuado_regu_hab, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_2_hab_drive_exci = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_HAB_DRIVE_EXCITACAO_LOGICA_DISPARO"], descricao=f"[UG{self.id}] RT Falha 2 Habilitar Drive Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_2_hab_drive_exci, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_2_fechar_contator_campo = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_FECHAR_CONTATOR_CAMPO"], descricao=f"[UG{self.id}] RT Falha 2 Fechar Contator Campo")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_2_fechar_contator_campo, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_2_corr_exci_pre_exci_ativa = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_CORRENTE_EXCITACAO_PRE_EXCITACAO_ATIVA"], descricao=f"[UG{self.id}] RT Falha 2 Corrente Excitação Pré Excitada Ativa")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_2_corr_exci_pre_exci_ativa, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_2_excess_pre_exci = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_TEMPO_EXCESSIVO_PRE_EXCITACAO"], descricao=f"[UG{self.id}] RT Falha 2 Excessivo Pré Excitação")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_2_excess_pre_exci, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_2_excess_parada = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_TEMPO_EXCESSIVO_PARADA"], descricao=f"[UG{self.id}] RT Falha 2 Excessivo Parada")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_2_excess_parada, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_3_perda_med_pot_reativa = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_TEMPO_EXCESSIVO_PARTIDA"], descricao=f"[UG{self.id}] RT Falha 3 Perda Medição Potência Reativa")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_3_perda_med_pot_reativa, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_3_perda_med_tensao_term = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_PERDA_MED_TENSAO_TERMINAL"], descricao=f"[UG{self.id}] RT Falha 3 Perda Medição Tensão Terminal")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_3_perda_med_tensao_term, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_3_perda_med_corr_exci_princ = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_PERDA_MED_CORRENTE_EXCITACAO_PRINC"], descricao=f"[UG{self.id}] RT Falha 3 Perda Medição Corrente Excitação Principal")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_3_perda_med_corr_exci_princ, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_3_perda_med_corr_exci_retag = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_PERDA_MED_CORRENTE_EXCITACAO_RETAG"], descricao=f"[UG{self.id}] RT Falha 3 Perda Medição Corrente Excitação Retaguarda")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_3_perda_med_corr_exci_retag, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_3_ruido_leit_instrum_reativo = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_RUIDO_INSTRU_REATIVO"], descricao=f"[UG{self.id}] RT Falha 3 Ruído Leitura Instrumentador Reativo")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_3_ruido_leit_instrum_reativo, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_3_ruido_leit_instrum_tensao = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_RUIDO_INSTRU_TENSAO"], descricao=f"[UG{self.id}] RT Falha 3 Ruído Leitura Instrumentador Tensão")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_3_ruido_leit_instrum_tensao, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_3_ruido_leit_instrum_principal = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_RUIDO_INSTRU_EXCITACAO_PRINC"], descricao=f"[UG{self.id}] RT Falha 3 Ruído Leitura Instrumentador Principal")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_3_ruido_leit_instrum_principal, CONDIC_INDISPONIBILIZAR))

        self.l_rt_falha_3_ruido_leit_instrum_retag = lei.LeituraModbusBit(self.rt[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RT_FALHA_RUIDO_INSTRU_EXCITACAO_RETAG"], descricao=f"[UG{self.id}] RT Falha 3 Ruído Leitura Instrumentador Retaguarda")
        self.condicionadores.append(c.CondicionadorBase(self.l_rt_falha_3_ruido_leit_instrum_retag, CONDIC_INDISPONIBILIZAR))


        # ENTRADAS ANALÓGICAS
        self.l_tristor_temp_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TIRISTORES_TEMP_MUITO_ALTA"], descricao=f"[UG{self.id}] Tristores Temperatura Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_tristor_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_crowbar_temp_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CROWBAR_TEMP_MUITO_ALTA"], descricao=f"[UG{self.id}] Crowbar Temperatura Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_crowbar_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_trafo_exci_temp_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRAFO_EXCITACAO_TEMP_MUITO_ALTA"], descricao=f"[UG{self.id}] Transformador Excitação Temperatura Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_trafo_exci_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_uhrv_temp_oleo_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_TEMP_OLEO_MUITO_ALTA"], descricao=f"[UG{self.id}] UHRV Óleo Temperatura Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhrv_temp_oleo_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_gera_fase_a_temp_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_FASE_A_TEMP_MUITO_ALTA"], descricao=f"[UG{self.id}] Gerador Fase A Temperatura Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_gera_fase_a_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_gera_fase_b_temp_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_FASE_B_TEMP_MUITO_ALTA"], descricao=f"[UG{self.id}] Gerador Fase B Temperatura Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_gera_fase_b_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_gera_fase_c_temp_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_FASE_C_TEMP_MUITO_ALTA"], descricao=f"[UG{self.id}] Gerador Fase C Temperatura Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_gera_fase_c_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_gera_nucleo_1_temp_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_NUCLEO_1_TEMP_MUITO_ALTA"], descricao=f"[UG{self.id}] Gerador Núcleo 1 Temperatura Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_gera_nucleo_1_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_gera_nucleo_2_temp_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_NUCLEO_2_TEMP_MUITO_ALTA"], descricao=f"[UG{self.id}] Gerador Núcleo 2 Temperatura Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_gera_nucleo_2_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_gera_nucleo_3_temp_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_NUCLEO_3_TEMP_MUITO_ALTA"], descricao=f"[UG{self.id}] Gerador Núcleo 3 Temperatura Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_gera_nucleo_3_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_mancal_guia_casq_temp_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["MANCAL_GUIA_CASQUILHO_TEMP_MUITO_ALTA"], descricao=f"[UG{self.id}] Mancal Guia Casquilho Temperatura Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_mancal_guia_casq_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_mancal_comb_casq_temp_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["MANCAL_COMBINADO_CASQUILHO_TEMP_MUITO_ALTA"], descricao=f"[UG{self.id}] Mancal Combinado Casquilho Temperatura Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_mancal_comb_casq_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_mancal_comb_esc_temp_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["MANCAL_COMBINADO_ESCORA_TEMP_MUITO_ALTA"], descricao=f"[UG{self.id}] Mancal Combinado Escora Temperatura Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_mancal_comb_esc_temp_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_uhrv_press_oleo_falha_leitura = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_PRESSAO_OLEO_FALHA_LEITURA"], descricao=f"[UG{self.id}] UHRV Pressão Óleo Falha Leitura")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhrv_press_oleo_falha_leitura, CONDIC_INDISPONIBILIZAR))

        self.l_uhrv_press_oleo_muito_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_PRESSAO_OLEO_MUITO_ALTA"], descricao=f"[UG{self.id}] UHRV Pressão Óleo Muito Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhrv_press_oleo_muito_alta, CONDIC_INDISPONIBILIZAR))

        self.l_uhrv_press_oleo_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_PRESSAO_OLEO_ALTA"], descricao=f"[UG{self.id}] UHRV Pressão Óleo Alta")
        self.condicionadores.append(c.CondicionadorBase(self.l_uhrv_press_oleo_alta, CONDIC_INDISPONIBILIZAR))


        # ## WHATSAPP + VOIP
        self.l_cmd_uhrv_modo_manuten = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_UHRV_MODO_MANUTENCAO"], descricao=f"[UG{self.id}] UHRV Comando Modo Manutenção")
        self.l_cmd_uhlm_modo_manuten = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_UHLM_MODO_MANUTENCAO"], descricao=f"[UG{self.id}] UHLM Comando Modo Manutenção")
        self.l_resis_quec_gerador_falha_ligar = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RESIS_AQUEC_GERA_FALHA_LIGAR"], descricao=f"[UG{self.id}] ")

        self.l_falha_leit_temp_tristores = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TIRISTORES_TEMP_FALHA_LEITURA"], descricao=f"[UG{self.id}] Tristores Temperatura Falha Leitura")
        self.l_falha_leit_temp_crowbar = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CROWBAR_TEMP_FALHA_LEITURA"], descricao=f"[UG{self.id}] Crowbar Temperatura Falha Leitura")
        self.l_falha_leit_temp_trafo_exci = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRAFO_EXCITACAO_TEMP_FALHA_LEITURA"], descricao=f"[UG{self.id}] Transformador Excitação Temperatura Falha Leitura")
        self.l_falha_leit_temp_uhrv_temp_oleo = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_TEMP_OLEO_FALHA_LEITURA"], descricao=f"[UG{self.id}] UHRV Temperatura Óleo Falha Leitura")
        self.l_falha_leit_temp_gerad_fase_a = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_FASE_A_TEMP_FALHA_LEITURA"], descricao=f"[UG{self.id}] Gerador Fase A Temperatura Falha Leitura")
        self.l_falha_leit_temp_gerad_fase_b = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_FASE_B_TEMP_FALHA_LEITURA"], descricao=f"[UG{self.id}] Gerador Fase B Temperatura Falha Leitura")
        self.l_falha_leit_temp_gerad_fase_c = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_FASE_C_TEMP_FALHA_LEITURA"], descricao=f"[UG{self.id}] Gerador Fase C Temperatura Falha Leitura")
        self.l_falha_leit_temp_gerad_nucleo_1 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_NUCLEO_1_TEMP_FALHA_LEITURA"], descricao=f"[UG{self.id}] Gerador Núcleo 1 Temperatura Falha Leitura")
        self.l_falha_leit_temp_gerad_nucleo_2 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_NUCLEO_2_TEMP_FALHA_LEITURA"], descricao=f"[UG{self.id}] Gerador Núcleo 2 Temperatura Falha Leitura")
        self.l_falha_leit_temp_gerad_nucleo_3 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_NUCLEO_3_TEMP_FALHA_LEITURA"], descricao=f"[UG{self.id}] Gerador Núcleo 3 Temperatura Falha Leitura")
        self.l_falha_leit_temp_mancal_guia_casq = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["MANCAL_GUIA_CASQUILHO_TEMP_FALHA_LEITURA"], descricao=f"[UG{self.id}] Mancal Guia Casquilho temperatura Falha Leitura")
        self.l_falha_leit_temp_mancal_comb_esc = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["MANCAL_COMBINADO_CASQUILHO_TEMP_FALHA_LEITURA"], descricao=f"[UG{self.id}] Mancal Combinado Escora Temperatura Falha Leitura")
        self.l_falha_leit_temp_mancal_comb_casq = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["MANCAL_COMBINADO_ESCORA_TEMP_FALHA_LEITURA"], descricao=f"[UG{self.id}] Mancal Combinado Casquilho Temperatura Falha Leitura")

        # ## WHATSAPP
        self.l_rv_pot_nula = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_RELE_POT_NULA"], descricao=f"[UG{self.id}] RV Potência Nula")
        self.l_uhrv_bomba_defeito = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_BOMBA_DEFEITO"], descricao=f"[UG{self.id}] UHRV Bomba Defeito") # TODO -> Verificar invertido
        self.l_uhlm_bomba_defeito = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_BOMBA_DEFEITO"], descricao=f"[UG{self.id}] UHLM Bomba Defeito")
        self.l_dispo_prot_surto = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["DPS"], descricao=f"[UG{self.id}] Dispositivo Proteção Surto")
        self.l_rt_selec_modo_controle_isol = lei.LeituraModbusBit(self.rv[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_SELEC_MODO_CTRL_ISOLADO"], descricao=f"[UG{self.id}] RT Selecionado Modo Controle Isolado")
        self.l_resis_aquec_gerad_defeito = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RESIS_AQUEC_GERA_DEFEITO"], descricao=f"[UG{self.id}] Resistência Aquecimento Gerador Defeito")

        self.l_crowbar_temp_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CROWBAR_TEMP_ALTA"], descricao=f"[UG{self.id}] Temperatura Alta")
        self.l_tristores_temp_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TIRISTORES_TEMP_ALTA"], descricao=f"[UG{self.id}] Temperatura Alta")
        self.l_uhrv_oleo_temp_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_TEMP_OLEO_ALTA"], descricao=f"[UG{self.id}] Temperatura Alta")
        self.l_trafo_exci_temp_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TRAFO_EXCITACAO_TEMP_ALTA"], descricao=f"[UG{self.id}] Temperatura Alta")
        self.l_gerad_fase_a_temp_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_FASE_A_TEMP_ALTA"], descricao=f"[UG{self.id}] Gerador Fase A Temperatura Alta")
        self.l_gerad_fase_b_temp_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_FASE_B_TEMP_ALTA"], descricao=f"[UG{self.id}] Gerador Fase B Temperatura Alta")
        self.l_gerad_fase_c_temp_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_FASE_C_TEMP_ALTA"], descricao=f"[UG{self.id}] Gerador Fase C Temperatura Alta")
        self.l_gerad_nucleo_1_temp_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_NUCLEO_1_TEMP_ALTA"], descricao=f"[UG{self.id}] Gerador Núcleo 1 Temperatura Alta")
        self.l_gerad_nucleo_2_temp_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_NUCLEO_2_TEMP_ALTA"], descricao=f"[UG{self.id}] Gerador Núcleo 2 Temperatura Alta")
        self.l_gerad_nucleo_3_temp_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["GERADOR_NUCLEO_3_TEMP_ALTA"], descricao=f"[UG{self.id}] Gerador Núcleo 3 Temperatura Alta")
        self.l_mancal_guia_casq_temp_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["MANCAL_GUIA_CASQUILHO_TEMP_ALTA"], descricao=f"[UG{self.id}] Mancal Guia Casquilho Temperatura Alta")
        self.l_mancal_comb_esc_temp_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["MANCAL_COMBINADO_CASQUILHO_TEMP_ALTA"], descricao=f"[UG{self.id}] Mancal Combinado Escora Temperatura Alta")
        self.l_mancal_comb_casq_temp_alta = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["MANCAL_COMBINADO_ESCORA_TEMP_ALTA"], descricao=f"[UG{self.id}] Mancal Combinado Casquilho Temperatura Alta")

        self.l_rv_modo_manut = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RV_MODO_MANUTENCAO"], descricao=f"[UG{self.id}] RV Modo Manutenção")
        self.l_uhlm_unidade_manut = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_UNIDADE_MANUTENCAO"], descricao=f"[UG{self.id}] UHLM Unidade Manutenção")
        self.l_sinal_nv_jusante_alto = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["NV_JUSANTE_ALTO"], descricao=f"[UG{self.id}] Nível Jusante Sinal Alto")
        self.l_uhrv_pressao_oleo_baixa = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_PRESSAO_OLEO_BAIXA"], descricao=f"[UG{self.id}] UHRV Pressão Óleo Baixa")
        self.l_sinal_nv_jusante_baixo = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["NV_JUSANTE_BAIXO"], descricao=f"[UG{self.id}] Nível Jusante Sinal Baixo")
        self.l_falha_leit_nv_jusante = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["NV_JUSANTE_FALHA_LEITURA"], descricao=f"[UG{self.id}] Nível Jusante Falha Leitura")
        self.l_sinal_nv_jusante_muito_alto = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["NV_JUSANTE_MUITO_ALTO"], descricao=f"[UG{self.id}] Nível Jusante Sinal Muito Alto")
        self.l_uhrv_pressao_oleo_muito_baixa = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHRV_PRESSAO_OLEO_MUITO_BAIXA"], descricao=f"[UG{self.id}] UHRV Pressão Óleo Muito Baixa")
        self.l_alarme_contro_dif_grade = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CTRL_ALARME_DIFERENCIAL_GRADE"], descricao=f"[UG{self.id}] Alarme Controle Diferencial Grade")
        self.l_sinal_nv_jusante_muito_baixo = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["NV_JUSANTE_MUITO_BAIXO"], descricao=f"[UG{self.id}] Nível Jusante Sinal Muito Baixo")
        self.l_resis_aquec_gerad_indisp = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["RESIS_AQUEC_GERA_INDISPONIVEL"], descricao=f"[UG{self.id}] Resistência Aquecimento Gerador Indisponível"),
