import pytz
import logging
import traceback

import src.subestacao as se
import src.tomada_agua as tda
import src.servico_auxiliar as sa

import src.dicionarios.dict as d
import src.funcoes.leitura as lei
import src.funcoes.escrita as esc
import src.maquinas_estado.ug as usm
import src.conectores.servidores as srv
import src.conectores.banco_dados as bd
import src.funcoes.condicionadores as c

from src.dicionarios.reg import *
from src.dicionarios.const import *

from time import sleep, time
from threading import Thread
from datetime import datetime


logger = logging.getLogger("logger")


class UnidadeDeGeracao:
    def __init__(self, id: "int", cfg: "dict"=None):

        if id <= 0:
            logger.error(f"[UG{self.id}] A Unidade não pode ser instanciada com o ID <= \"0\" ou vazio.")
            raise ValueError
        else:
            self.__id = id

        self.cfg = cfg

        self.__tensao = lei.LeituraModbus(
            srv.Servidores.clp[f"UG{self.id}"],
            REG_RELE[f"UG{self.id}"]["VAB"],
            descricao=f"[UG{self.id}] Tensão Unidade"
        )
        self.__potencia = lei.LeituraModbus(
            srv.Servidores.rele[f"UG{self.id}"],
            REG_RELE[f"UG{self.id}"]["P"],
            descricao=f"[UG{self.id}] Potência Ativa"
        )
        self.__potencia_reativa = lei.LeituraModbus(
            srv.Servidores.rele[f"UG{self.id}"],
            REG_RELE[f"UG{self.id}"]["Q"],
            descricao=f"[UG{self.id}] Potência Reativa"
        )
        self.__potencia_aparente = lei.LeituraModbus(
            srv.Servidores.rele[f"UG{self.id}"],
            REG_RELE[f"UG{self.id}"]["S"],
            descricao=f"[UG{self.id}] Potência Aparente"
        )
        self.__etapa_atual = lei.LeituraModbus(
            srv.Servidores.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["STT_PASSO_ATUAL"],
            descricao=f"[UG{self.id}] Etapa Atual"
        )
        self.__etapa_alvo = lei.LeituraModbus(
            srv.Servidores.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["SST_PASSO_SELECIONADO"],
            descricao=f"[UG{self.id}] Etapa Alvo"
        )

        self.__tempo_entre_tentativas: "int" = 0
        self.__limite_tentativas_de_normalizacao: "int" = 3

        self.__condicionadores_atenuadores: "list[str, c.CondicionadorBase]" = []

        self._etapa_alvo: "int" = 0
        self._etapa_atual: "int" = 0
        self._ultima_etapa_alvo: "int" = 0
        self._ultima_etapa_atual: "int" = 0

        self._setpoint: "int" = 0
        self._prioridade: "int" = 0
        self._tentativas_de_normalizacao: "int" = 0

        self._setpoint_minimo: "float" = 200
        self._setpoint_maximo: "float" = 500

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
        self.condicionadores_ativos: "list[c.CondicionadorBase]" = []
        self._condicionadores_essenciais: "list[c.CondicionadorBase]" = []
        self._condicionadores_atenuadores: "list[c.CondicionadorBase]" = []

        self.desabilitar_manutencao()
        self.iniciar_ultimo_estado()
        self.carregar_leituras()


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
        try:
            self._ultima_etapa_atual = self.__etapa_atual.valor
            return self._ultima_etapa_atual

        except Exception:
            logger.error(f"[UG{self.id}] Erro na leitura de \"Etapa Atual\". Mantendo última etapa.")
            return self._ultima_etapa_atual

    @property
    def etapa_alvo(self) -> "int":
        try:
            self._ultima_etapa_alvo = self.__etapa_alvo.valor
            return self._ultima_etapa_alvo

        except Exception:
            logger.error(f"[UG{self.id}] Erro na leitura de \"Etapa Alvo\". Mantendo última etapa.")
            return self._ultima_etapa_alvo

    @property
    def etapa(self) -> "int":
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
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[c.CondicionadorBase]") -> None:
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[c.CondicionadorBase]":
        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[c.CondicionadorBase]") -> None:
        self._condicionadores_essenciais = var

    @property
    def condicionadores_atenuadores(self) -> "list[c.CondicionadorBase]":
        return self._condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: "list[c.CondicionadorBase]") -> None:
        self._condicionadores_atenuadores = var


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
        estado = bd.BancoDados.get_ultimo_estado_ug(self.id)[0]

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
        srv.Servidores.clp["MOA"].write_single_register(REG_MOA[f"OUT_ETAPA_UG{self.id}"], self.etapa)
        srv.Servidores.clp["MOA"].write_single_register(REG_MOA[f"OUT_STATE_UG{self.id}"], self.codigo_state)


    def desabilitar_manutencao(self) -> "bool":
        try:
            res = esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_CONTROLE_POTENCIA_MANUAL"], valor=1)
            res = esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_RV_MANUTENCAO"], valor=0)
            res = esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_RV_AUTOMATICO"], valor=1)
            res = esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_UHLM_MODO_AUTOMATICO"], valor=1)
            res = esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_UHRV_MODO_MANUTENCAO"], valor=0)
            res = esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_UHRV_MODO_AUTOMATICO"], valor=1)
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível desabilitar o modo de manutenção da Unidade.")
            logger.debug(traceback.format_exc())
            return False


    def resetar_emergencia(self) -> "None":
        try:
            logger.info(f"[UG{self.id}] Enviando comando:                   \"RESET EMERGÊNCIA\"")

            esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_REARME_FALHAS"], valor=1)

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

            elif not self.etapa == UG_SINCRONIZADA:
                self.tentativas_norm_etapas = 0
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARTIDA\"")

                esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_REARME_FALHAS"], valor=1)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível partir a Unidade.")
            logger.debug(traceback.format_exc())


    def parar(self) -> "bool":
        try:
            if not self.etapa == UG_PARADA:
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARADA\"")
                self.enviar_setpoint(0)
                res = esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_PARADA_TOTAL"], valor=1)
                return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível parar a Unidade.")
            logger.debug(traceback.format_exc())
            return False


    def controlar_potencia_reativa(self) -> "None":
        if self.__tensao.valor > TENSAO_UG_MAXIMA:
            tensao = self.__tensao.valor

            # v = tensao
            pot_reativa = ((0.426 * 500) / ((1.05 - 1) * 380)) * (tensao - 380) # ((lim_definido * pot_máx)/((v_lim - v_base) * tensao_nominal)) * (leitura_v - v_base)

            if pot_reativa > (0.426 * self.potencia):
                pot_reativa = (0.426 * self.potencia)
                srv.Servidores.rt[f"UG{self.id}"].write_single_register(REG_RTV[f"UG{self.id}"]["SETPOINT_POTENCIA_REATIVA_PU"], -pot_reativa)


    def enviar_setpoint(self, setpoint_kw: "int") -> "bool":
        try:
            sleep(2)
            if not self.desabilitar_manutencao():
                logger.info(f"[UG{self.id}] Não foi possível enviar comando de \"Desabilitar Manutenção\"")
            else:
                if self.cfg[f"pot_maxima_ug{self.id}"] <= setpoint_kw:
                    setpoint_kw = self.cfg[f'pot_maxima_ug{self.id}']

                self.setpoint = int(setpoint_kw)
                setpoint_porcento = (setpoint_kw / POT_MAX_UGS) * 10000
                logger.debug(f"[UG{self.id}]          Enviando setpoint:         {setpoint_kw} kW ({(setpoint_kw / self.cfg[f'pot_maxima_ug{self.id}']) * 100:0.1f} %)")

                if self.setpoint > 1:
                    res = srv.Servidores.rv[f"UG{self.id}"].write_single_register(REG_RTV[f"UG{self.id}"]["RV_SETPOINT_POTENCIA_ATIVA_PU"], int(setpoint_porcento))
                    return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o Setpoint para Unidade.")
            logger.debug(traceback.format_exc())
            return False


    def acionar_trip_logico(self) -> "bool":
        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP LÓGICO\"")
            res = esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_COMANDO_PARADA_DE_EMERGENCIA"], valor=1)
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel acionar o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())
            return False


    def remover_trip_logico(self) -> "bool":
        try:
            logger.debug(f"[UG{self.id}]          Removendo comando:         \"TRIP LÓGICO\"")
            res = esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_REARME_FALHAS"], valor=1)
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())
            return False


    def acionar_trip_eletrico(self) -> "bool":
        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP ELÉTRICO\"")
            res = None # srv.Servidores.clp["MOA"].write_single_coil(REG_MOA[f"OUT_BLOCK_UG{self.id}"], [1])
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())
            return False


    def remover_trip_eletrico(self) -> "bool":
        try:
            se.Subestacao.fechar_dj_linha()

            logger.debug(f"[UG{self.id}]          Removendo comando:         \"TRIP ELÉTRICO\"")
            res = None # srv.Servidores.clp["MOA"].write_single_coil(REG_MOA[f"OUT_BLOCK_UG{self.id}"], [0])
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())
            return False


    def reconhece_reset_alarmes(self) -> "bool":
        try:
            logger.debug("")
            logger.info(f"[UG{self.id}]          Enviando comando:          \"RECONHECE E RESET\"")

            for x in range(3):
                logger.debug("")
                logger.debug(f"[UG{self.id}]          Passo: {x+1}/3")
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
                sleep(1)
                # srv.Servidores.clp["MOA"].write_single_coil(REG_MOA["PAINEL_LIDO"], [0])
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
                # Thread(target=lambda: self.verificar_sincronismo()).start()

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
        # esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_COMANDO_PARADA_DE_EMERGENCIA"], valor=1)
        self.temporizar_partida = False
        sleep(1)
        # esc.EscritaModBusBit.escrever_bit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CMD_REARME_FALHAS"], valor=1)


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

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.debug(f"[UG{self.id}] Foram detectados condicionadores ativos na Unidade!")
            else:
                logger.debug(f"[UG{self.id}] Ainda há condicionadores ativos na Unidade!")

            for condic in condics_ativos:
                if condic in self.condicionadores_ativos or condic.teste:
                    logger.debug(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\".{ 'Obs.: \"TESTE\"' if condic.teste else None}")
                    continue
                else:
                    if condic.gravidade == CONDIC_INDISPONIBILIZAR:
                        logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                        flag = CONDIC_INDISPONIBILIZAR

                    elif condic.gravidade == CONDIC_AGUARDAR:
                        logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                        flag = CONDIC_AGUARDAR if flag != CONDIC_INDISPONIBILIZAR else flag

                    elif condic.gravidade == CONDIC_NORMALIZAR:
                        logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                        flag = CONDIC_NORMALIZAR if flag not in (CONDIC_INDISPONIBILIZAR, CONDIC_AGUARDAR) else flag

                    self.condicionadores_ativos.append(condic)
                    bd.BancoDados.update_alarmes([
                        self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                        condic.gravidade,
                        condic.descricao,
                    ])
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
            self.c_tmp_fase_r.valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{self.id}"])
            self.c_tmp_fase_s.valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{self.id}"])
            self.c_tmp_fase_t.valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{self.id}"])
            self.c_tmp_nucleo_gerador_1.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_1_ug{self.id}"])
            self.c_tmp_nucleo_gerador_2.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_2_ug{self.id}"])
            self.c_tmp_nucleo_gerador_3.valor_base = float(parametros[f"alerta_temperatura_nucleo_gerador_3_ug{self.id}"])
            self.c_tmp_mancal_casq_rad.valor_base = float(parametros[f"alerta_temperatura_mancal_casq_rad_ug{self.id}"])
            self.c_tmp_mancal_casq_comb.valor_base = float(parametros[f"alerta_temperatura_mancal_casq_comb_ug{self.id}"])
            self.c_tmp_mancal_escora_comb.valor_base = float(parametros[f"alerta_temperatura_mancal_escora_comb_ug{self.id}"])

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

        return


    def verificar_leituras(self) -> "None":
        """
        Função para consulta de acionamentos da Unidade e avisos através do mecanismo
        de acionamento temporizado.
        """

        # WHATSAPP
        if self.l_teste_whats.valor:
            logger.warning(f"[UG{self.id}] Leitura Teste Mensageiro WhatsApp ativada.")

        # WHATSAPP + VOIP
        if self.l_teste_voip.valor and not d.voip[f"UG{self.id}_CD_CMD_UHRV_MODO_MANUTENCAO"][0]:
            logger.warning(f"[UG{self.id}] Leitura Teste Mensageiro Voip ativada.")
            d.voip[f"UG{self.id}_CD_CMD_UHRV_MODO_MANUTENCAO"][0] = True
        elif not self.l_teste_voip.valor and d.voip[f"UG{self.id}_CD_CMD_UHRV_MODO_MANUTENCAO"][0]:
            d.voip[f"UG{self.id}_CD_CMD_UHRV_MODO_MANUTENCAO"][0] = False


    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Unidade.
        """

        # Fase R
        self.l_tmp_fase_r = lei.LeituraModbus(
            srv.Servidores.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMPERATURA_GERADOR_FASE_A"],
            escala=0.001,
            op=4
        )
        self.c_tmp_fase_r = c.CondicionadorExponencial(self.l_tmp_fase_r)
        self.condicionadores_essenciais.append(self.c_tmp_fase_r)
        self.condicionadores_atenuadores.append(self.c_tmp_fase_r)

        # Fase S
        self.l_tmp_fase_s = lei.LeituraModbus(
            srv.Servidores.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMPERATURA_GERADOR_FASE_B"],
            escala=0.001,
            op=4
        )
        self.c_tmp_fase_s = c.CondicionadorExponencial(self.l_tmp_fase_s)
        self.condicionadores_essenciais.append(self.c_tmp_fase_s)
        self.condicionadores_atenuadores.append(self.c_tmp_fase_s)

        # Fase T
        self.l_tmp_fase_t = lei.LeituraModbus(
            srv.Servidores.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMPERATURA_GERADOR_FASE_C"],
            escala=0.001,
            op=4
        )
        self.c_tmp_fase_t = c.CondicionadorExponencial(self.l_tmp_fase_t)
        self.condicionadores_essenciais.append(self.c_tmp_fase_t)
        self.condicionadores_atenuadores.append(self.c_tmp_fase_t)

        # Nucleo Gerador 1
        self.l_tmp_nucleo_gerador_1 = lei.LeituraModbus(
            srv.Servidores.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMPERATURA_GERADOR_NUCLEO_1"],
            escala=0.001,
            op=4
        )
        self.c_tmp_nucleo_gerador_1 = c.CondicionadorExponencial(self.l_tmp_nucleo_gerador_1)
        self.condicionadores_essenciais.append(self.c_tmp_nucleo_gerador_1)
        self.condicionadores_atenuadores.append(self.c_tmp_nucleo_gerador_1)

        # Nucleo Gerador 2
        self.l_tmp_nucleo_gerador_2 = lei.LeituraModbus(
            srv.Servidores.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMPERATURA_GERADOR_NUCLEO_2"],
            escala=0.001,
            op=4
        )
        self.c_tmp_nucleo_gerador_2 = c.CondicionadorExponencial(self.l_tmp_nucleo_gerador_2)
        self.condicionadores_essenciais.append(self.c_tmp_nucleo_gerador_2)
        self.condicionadores_atenuadores.append(self.c_tmp_nucleo_gerador_2)

        # Nucleo Gerador 3
        self.l_tmp_nucleo_gerador_3 = lei.LeituraModbus(
            srv.Servidores.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMPERATURA_GERADOR_NUCLEO_3"],
            escala=0.001,
            op=4
        )
        self.c_tmp_nucleo_gerador_3 = c.CondicionadorExponencial(self.l_tmp_nucleo_gerador_3)
        self.condicionadores_essenciais.append(self.c_tmp_nucleo_gerador_3)
        self.condicionadores_atenuadores.append(self.c_tmp_nucleo_gerador_3)

        # Mancal Casquilho Radial
        self.l_tmp_mancal_casq_rad = lei.LeituraModbus(
            srv.Servidores.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMPERATURA_MANCAL_GUIA_CASQUILHO"],
            escala=0.001,
            op=4
        )
        self.c_tmp_mancal_casq_rad = c.CondicionadorExponencial(self.l_tmp_mancal_casq_rad)
        self.condicionadores_essenciais.append(self.c_tmp_mancal_casq_rad)
        self.condicionadores_atenuadores.append(self.c_tmp_mancal_casq_rad)

        # Mancal Casquilho Combinado
        self.l_tmp_mancal_casq_comb = lei.LeituraModbus(
            srv.Servidores.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMPERATURA_MANCAL_COMBINADO_CASQUILHO"],
            escala=0.001,
            op=4
        )
        self.c_tmp_mancal_casq_comb = c.CondicionadorExponencial(self.l_tmp_mancal_casq_comb)
        self.condicionadores_essenciais.append(self.c_tmp_mancal_casq_comb)
        self.condicionadores_atenuadores.append(self.c_tmp_mancal_casq_comb)

        # Mancal Escora Combinado
        self.l_tmp_mancal_escora_comb = lei.LeituraModbus(
            srv.Servidores.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["TEMPERATURA_MANCAL_COMBINADO_ESCORA"],
            escala=0.001,
            op=4
        )
        self.c_tmp_mancal_escora_comb = c.CondicionadorExponencial(self.l_tmp_mancal_escora_comb)
        self.condicionadores_essenciais.append(self.c_tmp_mancal_escora_comb)
        self.condicionadores_atenuadores.append(self.c_tmp_mancal_escora_comb)


        ## CONDICINOADORES ESSENCIAIS
        self.l_teste_ce_normalizar = lei.LeituraModbusBit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CONDIC_E_NORMALIZAR"], descricao=f"[UG{self.id}] Condicionador Essencial Teste Normalizar")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_teste_ce_normalizar, CONDIC_NORMALIZAR))

        ## CONDICIONADORES
        self.l_teste_c_normalizar = lei.LeituraModbusBit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CONDIC_NORMALIZAR"], descricao=f"[UG{self.id}] Condicionador Teste Normalizar")
        self.condicionadores.append(c.CondicionadorBase(self.l_teste_c_normalizar, CONDIC_NORMALIZAR))

        self.l_teste_c_indisponibilizar = lei.LeituraModbusBit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["CONDIC_INDISPONIBILIZAR"], descricao=f"[UG{self.id}] Condicionador Teste Indisponibilizar")
        self.condicionadores.append(c.CondicionadorBase(self.l_teste_c_indisponibilizar, CONDIC_INDISPONIBILIZAR))

        ## WHATSAPP + VOIP
        self.l_teste_voip = lei.LeituraModbusBit(srv.Servidores.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["L_VOIP"], descricao=f"[UG{self.id}] UHRV Comando Modo Manutenção")

        ## WHATSAPP
        self.l_teste_whats = lei.LeituraModbusBit(srv.Servidores.rv[f"UG{self.id}"], REG_RTV[f"UG{self.id}"]["L_WHATS"], descricao=f"[UG{self.id}] RV Potência Nula")