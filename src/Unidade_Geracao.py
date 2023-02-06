__version__ = "0.2"
__authors__ = "Lucas Lavratti, Diego Basgal"

import pytz
import logging
import traceback
import VAR_REG

from Usina import *
from Escrita import *
from Leituras import *
from time import sleep, time
from threading import Thread
from datetime import datetime
from abc import abstractmethod
from src.Condicionadores import *

# Class Stubs
class UnidadeDeGeracao:
    ...

class State:
    ...

class StateDisponivel(State):
    ...

class StateIndisponivel(State):
    ...

class StateManual(State):
    ...

class StateRestrito(State):
    ...

class UnidadeDeGeracao:
    def __init__(self, id: int, cfg=None, leituras_usina=None):

        if not cfg or not leituras_usina:
            raise ValueError
        else:
            self.cfg = cfg
            self.leituras_usina = leituras_usina

        REG_MB = VAR_REG.REG_MB
        REG_OPC = VAR_REG.REG_OPC

        self._id = id

        self._setpoint = 0
        self._prioridade = 0
        self._etapa_atual = 0
        self._setpoint_minimo = 0
        self._setpoint_maximo = 0
        self._tempo_entre_tentativas = 0
        self._tentativas_de_normalizacao = 0
        self._limite_tentativas_de_normalizacao = 3

        self._condicionadores = []
        self._condicionadores_essenciais = []
        self._condicionadores_atenuadores = []

        self._next_state = StateDisponivel(self)

        self.modo_autonomo = 1
        self.last_EtapaAtual = 0
        self.last_EtapaAlvo = -1

        self.timer_sinc = False
        self.timer_press = False
        self.limpeza_grade = False
        self.avisou_emerg_voip = False
        self.enviar_trip_eletrico = False
        self.aux_tempo_sincronizada = None
        self.deve_ler_condicionadores = False

        self.codigo_state = self._codigo_state

        self.setpoint_minimo = self.cfg["pot_minima"]
        self.setpoint_maximo = self.cfg["pot_maxima_ug{}".format(self.id)]

        self.db = Database()

        self.con = FieldConnector(self.cfg)

        self.client = Client(self.cfg["client"])
        
        self.logger = logging.getLogger("__main__")

        self.ts_auxiliar = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

        self.clp = ModbusClient(host=self.cfg["UG{}_slave_ip".format(self.id)], port=self.cfg["UG{}_slave_porta".format(self.id)], timeout=0.5,unit_id=1, auto_open=True, auto_close=True,)

        self.leitura_potencia = LeituraOPC(self.client,REG_OPC["UG"]["UG{}_UG_P".format(self.id)])

        self.leitura_horimetro_hora = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_UG_HORIMETRO".format(self.id)])

        self.leitura_operacao_etapa_atual = LeituraModbus(self.clp, REG_MB["UG"]["UG{}_RV_ESTADO_OPERACAO".format(self.id)])

        self.leitura_potencia_outra_ug = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_UG_P".format(2 if self.id == 1 else 1)])

        self.leitura_setpoint_outra_ug = LeituraModbus(self.clp, REG_MB["UG"]["UG{}_RV_SETPOINT_POTENCIA_ATIVA_PU".format(2 if self.id == 1 else 1)])

        self.condic_ativos_sim_ug = LeituraOPC(self.client, REG_OPC["UG"]["REG_UG{}_RetrornosAnalogicos_AUX_Condicionadores".format(self.id)])
    
        self.pt_controle_p = (self.leitura_pressao_turbina.valor - self.cfg["press_turbina_alvo"]) * self.cfg["pt_kp"]
        self.pt_ajuste_ie = (self.leitura_potencia.valor + self.leitura_potencia_outra_ug.valor) / self.cfg["pot_maxima_alvo"]
        self.pt_controle_i = self.pt_ajuste_ie - self.pt_controle_p

        self.leitura_condicionadores()

    @property
    def disponivel(self) -> bool:
        return isinstance(self._next_state, StateDisponivel)
    
    @property
    def manual(self) -> bool:
        return isinstance(self._next_state, StateManual)

    @property
    def id(self) -> int:
        return self._id

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
        self.logger.debug("[UG{}] SP<-{}".format(self.id, var))

    @property
    def prioridade(self) -> int:
        return self._prioridade
    
    @prioridade.setter
    def prioridade(self, var) -> None:
        self._prioridade = var

    @property
    def etapa_atual(self) -> int:
        self.logger.debug("[UG{}] Etapa atual = Etapa atual <- {}".format(self.id, self._etapa_atual))
        return self._etapa_atual
    
    @etapa_atual.setter
    def etapa_atual(self, var: int):
        self._etapa_atual = var

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
    def condicionadores(self) -> list([CondicionadorBase]):
        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: list([CondicionadorBase])):
        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> list([CondicionadorBase]):
        return self._condicionadores_essenciais
    
    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: list([CondicionadorBase])):
        self._condicionadores_essenciais = var

    @property
    def condicionadores_atenuadores(self) -> list([CondicionadorBase]):
        return self._condicionadores_atenuadores
    
    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: list([CondicionadorBase])):
        self._condicionadores_atenuadores = var

    @property
    def tempo_entre_tentativas(self) -> int:
        return self._tempo_entre_tentativas

    @property
    def tentativas_de_normalizacao(self) -> int:
        return self._tentativas_de_normalizacao
    
    @tentativas_de_normalizacao.setter
    def tentativas_de_normalizacao(self, var: int):
        var += Usina.tentativas_normalizacao
        if 0 <= var and var == int(var) and self._tentativas_de_normalizacao <= self._limite_tentativas_de_normalizacao:
            self._tentativas_de_normalizacao = int(var)
        elif self._tentativas_de_normalizacao == self._limite_tentativas_de_normalizacao:
            logger.debug("Última tentativa de normalização...")
        else:
            raise ValueError("Valor deve se um inteiro positivo")

    @property
    def limite_tentativas_de_normalizacao(self) -> int:
        return self._limite_tentativas_de_normalizacao

    @codigo_state.setter
    def codigo_state(self, var) -> int:
        self._codigo_state = var

    @property
    def etapa_atual(self) -> int:
        try:
            response = self.leitura_operacao_etapa_atual.valor
            if response > 0:
                self.last_EtapaAtual = response
                return response
            else:
                return self.last_EtapaAtual
        except Exception as e:
            raise (e)

    @property
    def etapa_comporta(self) -> int:
        try:
            aberta = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_ABERTA".format(self.id)], 17).valor
            fechada = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_FECHADA".format(self.id)], 18).valor
            cracking = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_CRACKING".format(self.id)], 25).valor
            remoto = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_REMOTO".format(self.id)], 22).valor
            
            if fechada:
                return COMPORTA_FECHADA
            elif aberta:
                return COMPORTA_ABERTA
            elif cracking:
                return COMPORTA_CRACKING
            elif remoto:
                return COMPORTA_REMOTO
            else:
                self.logger.debug("[UG{}] Comporta em etapa inconsistente".format(self.id))
                return False
        except Exception as e:
            raise(e)
    
    @property
    def permissao_comporta(self) -> bool:
        try:
            response = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_PERMISSIVOS_OK".format(self.id)], 31, True).valor
        except Exception as e:
            raise(e)
        else:
            return response
    
    @property
    def bloqueio_comporta(self) -> bool:
        try:
            response = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_BLOQUEIO_ATUADO".format(self.id)], 31, True).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def status_comporta(self) -> int:
        try:
            response = LeituraOPC(self.client, REG_OPC["TDA"]["CP{}_COMPORTA_OPERANDO".format(self.id)]).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def status_outra_comporta(self) -> int:
        try:
            response = LeituraOPC(self.client, REG_OPC["TDA"]["CP{}_COMPORTA_OPERANDO".format(2 if self.id == 1 else 1)]).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def status_limpa_grades(self) -> int:
        try:
            response = LeituraOPC(self.client, REG_OPC["TDA"]["LG_OPERACAO_MANUAL"]).valor
        except Exception as e:
            raise (e)
        else:
            return response

    @property
    def status_valvula_borboleta(self) -> int:
        try:
            response = LeituraOPC(self.client, REG_OPC["TDA"]["VB_FECHANDO"]).valor
        except Exception as e:
            raise(e)
        else:
            return response

    @property
    def status_unidade_hidraulica(self) -> bool:
        try:
            response = LeituraOPCBit(self.client, REG_OPC["TDA"]["UH_UNIDADE_HIDRAULICA_DISPONIVEL"], 1).valor
        except Exception as e:
            raise(e)
        else:
            return response

    def step(self) -> None:
        try:
            self.logger.debug("[UG{}] Step.".format(self.id))
            self.interstep()
            self._next_state = self._next_state.step()
            DataBank.set_words(REG_MB["MOA"]["OUT_STATE_UG{}".format(self.id)][self.codigo_state])
            DataBank.set_words(REG_MB["MOA"]["OUT_ETAPA_UG{}".format(self.id)][self.etapa_atual])

        except Exception as e:
            self.logger.error("[UG{}] Erro na execução da sm. Traceback: {}".format(self.id, traceback.format_exc()))
            raise e

    def interstep(self) -> None:
        if (not self.avisou_emerg_voip) and (self.condicionador_pressao_turbina_ug.valor > 0.1):
            self.avisou_emerg_voip = True
            
        elif self.condicionador_pressao_turbina_ug.valor < 0.05:
            self.avisou_emerg_voip = False

    def carregar_parametros(self, parametros: dict):
        for key, val in parametros.items():
            while not key[0:1] == "__":
                key = "_" + key[:]
            setattr(self, key, val)
            self.logger.debug("[UG{}] Variavél carregada: {} = {}.".format(self.id, key, val))

    def partir(self) -> bool:
        try:
            if self.etapa_atual == UNIDADE_PARADA:
                self.logger.info("[UG{}] Enviando comando de partida.".format(self.id))
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_RESET_FALHAS_PASSOS".format(self.id)], 0, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_REARME_BLOQUEIO_86M".format(self.id)], 1, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_REARME_BLOQUEIO_86E".format(self.id)], 2, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_REARME_BLOQUEIO_86H".format(self.id)], 3, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_UHRV_REARME_FALHAS".format(self.id)], 0, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_UHLM_REARME_FALHAS".format(self.id)], 16, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_PARTIDA_CMD_SINCRONISMO".format(self.id)], 10, 1)
                self.enviar_setpoint(self.setpoint)
            else:
                self.logger.debug("[UG{}] A unidade já está sincronizada.".format(self.id))
        except Exception as e:
            raise(e)
        else:
            return response

    def parar(self) -> bool:
        try:
            if self.etapa_atual == (UNIDADE_SINCRONIZADA or UNIDADE_SINCRONIZANDO):
                self.logger.info("[UG{}] Enviando comando de parada.".format(self.id))
                response = False
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_PARADA_CMD_DESABILITA_UHLM".format(self.id)], 15, 1)
                self.enviar_setpoint(0)
            else:
                self.logger.debug("[UG{}] A unidade já está parada.".format(self.id))
            
        except Exception as e:
            self.logger.exception(e)
            return False
        else:
            return response
        
    def enviar_setpoint(self, setpoint_kw: int) -> bool:
        try:
            self.setpoint_minimo = self.cfg["pot_minima"]
            self.setpoint_maximo = self.cfg["pot_maxima_ug{}".format(self.id)]

            self.setpoint = int(setpoint_kw)
            self.logger.debug("[UG{}] Enviando setpoint {} kW.".format(self.id, int(self.setpoint)))
            response = False
            if self.setpoint > 1:
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_RESET_FALHAS_PASSOS".format(self.id)], 0, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_REARME_BLOQUEIO_86M".format(self.id)], 1, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_REARME_BLOQUEIO_86E".format(self.id)], 2, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_REARME_BLOQUEIO_86H".format(self.id)], 3, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_UHRV_REARME_FALHAS".format(self.id)], 0, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_UHLM_REARME_FALHAS".format(self.id)], 16, 1)
                response = self.clp.write_single_register(REG_MB["UG"]["UG{}_RV_SETPOINT_POTENCIA_ATIVA_PU".format(self.id)], self.setpoint)
        except Exception as e:
            raise(e)
        else:
            return response

    def rearme_falhas_comporta(self) -> bool:
        try:
            response = EscritaOPCBit(self.client, REG_OPC["TDA"]["CP{}_CMD_REARME_FALHAS".format(self.id)], 0, 1)
        except Exception as e:
            raise(e)
        else:
            return response

    def verificar_precondicoes_comporta(self) -> bool:
        self.rearme_falhas_comporta()
        try:
            if self.status_unidade_hidraulica and not self.permissao_comporta and not self.bloqueio_comporta:
                if self.status_outra_comporta == (2 or 4 or 32) or self.status_valvula_borboleta != 0 or self.status_limpa_grades != 0:
                    self.logger.debug("[UG{0}] Não há condições para operar a comporta {0}".format(self.id))
                    if self.status_outra_comporta != 0:
                        self.logger.debug("[UG{}] A comporta {} está repondo".format(self.id, 2 if self.id == 1 else 1)) if self.status_outra_comporta == 2 else None
                        self.logger.debug("[UG{}] A comporta {} está abrindo".format(self.id, 2 if self.id == 1 else 1)) if self.status_outra_comporta == 4 else None
                        self.logger.debug("[UG{}] A comporta {} está em cracking".format(self.id, 2 if self.id == 1 else 1)) if self.status_outra_comporta == 32 else None
                        return False
                    elif self.status_limpa_grades != 0:
                        self.logger.debug("[UG{}] O limpa grades está em operação".format(self.id))
                        return False
                    elif self.status_valvula_borboleta != 0:
                        self.logger.debug("[UG{}] A válvula borboleta está em operação".format(self.id))
                        return False
                    else:
                        self.logger.debug("[UG{}] Favor aguardar normalização".format(self.id))
                        return False
            elif not self.status_unidade_hidraulica:
                self.logger.debug("[UG{}] A Unidade Hidráulica ainda não está disponível".format(self.id))
                return False
            elif self.bloqueio_comporta:
                self.logger.debug("[UG{0}] A comporta {0} ainda possui bloqueios ativados".format(self.id))
                return False
            elif self.permissao_comporta:
                self.logger.debug("[UG{0}] A permissão da comporta {0} ainda não foi concedida".format(self.id))
                return False
        except Exception as e:
            raise(e)
        else:
            return True

    def abrir_comporta(self) -> bool:
        try:
            if self.etapa_comporta == COMPORTA_ABERTA:
                self.logger.debug("[UG{0}] A comporta {0} já está aberta".format(self.id))
                return True
            elif self.verificar_precondicoes_comporta():
                press_equalizada = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_PRESSAO_EQUALIZADA".format(self.id)], 4)
                aguardando_cmd_abert = LeituraOPCBit(self.client, REG_OPC["TDA"]["CP{}_AGUARDANDO_COMANDO_ABERTURA".format(self.id)], 3)
                if press_equalizada.valor and aguardando_cmd_abert.valor:
                    self.logger.debug("[UG{0}] Enviando comando de abertura para a comporta {0}".format(self.id))
                    response = EscritaOPCBit(self.client, REG_OPC["TDA"]["CP{}_CMD_ABERTURA_TOTAL".format(self.id)], 1, 1)
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise(e)
        else:
            return response
    
    def fechar_comporta(self) -> bool:
        try:
            if self.etapa_comporta == COMPORTA_FECHADA:
                self.logger.debug("[UG{0}] A comporta {0} já está fechada".format(self.id))
                return True
            else:
                response = EscritaOPCBit(self.client, REG_OPC["TDA"]["CP{}_CMD_FECHAMENTO".format(self.id)], 3, 1)
        except Exception as e:
            raise(e)
        else:
            return response

    def cracking_comporta(self) -> bool:
        try:
            if self.etapa_comporta == COMPORTA_CRACKING:
                self.logger.debug("[UG{0}] A comporta {} já está em cracking".format(self.id))
                return True
            elif self.verificar_precondicoes_comporta():
                self.logger.debug("[UG{0}] Enviando comando de cracking para a comporta {0}".format(self.id))
                response = EscritaOPCBit(self.client, REG_OPC["TDA"]["CP{}_CMD_ABERTURA_CRACKING".format(self.id)], 1, 1)
            else:
                return False
        except Exception as e:
            raise(e)
        else:
            return response

    def reconhece_reset_alarmes(self) -> bool:
        try:
            self.logger.info("[UG{}] Enviando comando de reconhece e reset alarmes. (Aproximadamente 10s)".format(self.id))
            for _ in range(3):
                DataBank.set_words(REG_MB["MOA"]["PAINEL_LIDO"], [0])
                self.remover_trip_eletrico()
                DataBank.set_words(REG_MB["MOA"]["PAINEL_LIDO"], [0])
                sleep(1)
                self.remover_trip_logico()
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_RESET_FALHAS_PASSOS".format(self.id)], 0, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_REARME_BLOQUEIO_86M".format(self.id)], 1, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_REARME_BLOQUEIO_86E".format(self.id)], 2, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_REARME_BLOQUEIO_86H".format(self.id)], 3, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_UHRV_REARME_FALHAS".format(self.id)], 0, 1)
                response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_UHLM_REARME_FALHAS".format(self.id)], 16, 1)
                DataBank.set_words(REG_MB["MOA"]["PAINEL_LIDO"], [0])
                sleep(1)
        except Exception as e:
            raise(e)
        else:
            return response

    def acionar_trip_logico(self) -> bool:
        try:
            self.logger.debug("[UG{}] Acionando sinal de TRIP.".format(self.id))
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_PARADA_EMERGENCIA".format(self.id)], 4, 1)
        except Exception as e:
            raise(e)
        else:
            return response

    def remover_trip_logico(self) -> bool:
        try:
            self.logger.debug("[UG{}] Removendo sinal de TRIP.".format(self.id))
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_RESET_FALHAS_PASSOS".format(self.id)], 0, 1)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_REARME_BLOQUEIO_86M".format(self.id)], 1, 1)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_REARME_BLOQUEIO_86E".format(self.id)], 2, 1)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_REARME_BLOQUEIO_86H".format(self.id)], 3, 1)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_UHRV_REARME_FALHAS".format(self.id)], 0, 1)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_CMD_UHLM_REARME_FALHAS".format(self.id)], 16, 1)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_BLOQUEIO_86H_ATUADO".format(self.id)], 31, 0)
            response = EscritaOPCBit(self.client, REG_OPC["UG"]["UG{}_RELE_700G_TRIP_ATUADO".format(self.id)], 31, 0)
        except Exception as e:
            raise(e)
        else:
            return response

    def acionar_trip_eletrico(self) -> bool:
        try:
            self.enviar_trip_eletrico = True
            self.logger.debug("[UG{}] Acionando sinal elétrico de TRIP.".format(self.id))
            DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG{}".format(self.id)],[1],)
        except Exception as e:
            raise(e)
        else:
            return True

    def remover_trip_eletrico(self) -> bool:
        try:
            self.enviar_trip_eletrico = False
            self.logger.debug("[UG{}] Removendo sinal elétrico de TRIP.".format(self.id))
            DataBank.set_words(REG_MB["MOA"]["OUT_BLOCK_UG{}".format(self.id)],[0],)
            DataBank.set_words(REG_MB["MOA"]["PAINEL_LIDO"],[0],)

            if not LeituraOPCBit(self.client, REG_OPC["SE"]["CMD_SE_FECHA_52L"], 4, True):
                self.logger.debug("Comando recebido da UG{} - Fechando Dj52L".format(self.id))
                self.con.fechaDj52L()
        except Exception as e:
            self.logger.debug("Exception! Traceback: {}".format(traceback.format_exc()))
            return False
        else:
            return True

    def forcar_estado_manual(self) -> bool:
        try:
            self._next_state = StateManual(self)
        except Exception:
            self.logger.error("[UG{}] Não foi possivel forcar_estado_manual. {}".format(self.id, traceback.print_stack))
            return False
        else:
            return True

    def forcar_estado_restrito(self) -> bool:
        try:
            self._next_state = StateRestrito(self)
        except Exception:
            self.logger.error("[UG{}] Não foi possivel forcar_estado_restrito. {}".format(self.id, traceback.print_stack))
            return False
        else:
            return True

    def forcar_estado_disponivel(self) -> bool:
        try:
            self.reconhece_reset_alarmes()
            sleep(1)
            self._next_state = StateDisponivel(self)
        except Exception:
            self.logger.error("[UG{}] Não foi possivel forcar_estado_disponivel. {}".format(self.id, traceback.print_stack))
            return False
        else:
            return True
        
    def forcar_estado_indisponivel(self) -> bool:
        try:
            self._next_state = StateIndisponivel(self)
        except Exception:
            self.logger.error("[UG{}] Não foi possivel forcar_estado_indisponivel. {}".format(self.id, traceback.print_stack))
            return False
        else:
            return True

    def verificar_partindo(self) -> bool:
        timer = time() + 600
        try:
            self.logger.debug("[UG{}] Iniciando o timer de verificação de partida".format(self.id))
            while time() < timer:
                if self.etapa_atual == UNIDADE_SINCRONIZADA:
                    self.logger.debug("[UG{}] Unidade sincronizada. Saindo do timer de verificação de partida".format(self.id))
                    self.timer_sinc = True
                    return True
            self.logger.debug("[UG{}] A Unidade estourou o timer de verificação de partida, adicionando condição para normalizar".format(self.id))
            EscritaOPCBit(Client(CFG["client"]), REG_OPC["UG"]["UG{}_CMD_PARADA_EMERGENCIA".format(self.id)], 4, 1)
            self.timer_sinc = True
        except Exception as e:
            raise (e)
        return False

    def verificar_pressao(self) -> bool:
        timer = time() + 120
        try:
            self.logger.info("[UG{}] Iniciando o timer para equilização da pressão da UH".format(self.id))
            while time() < timer:
                if LeituraOPCBit(Client(CFG["client"]), REG_OPC["TDA"]["CP{}_PRESSAO_EQUALIZADA".format(self.id)], 4).valor:
                    self.logger.debug("[UG{}] Pressão equalizada, saindo do timer".format(self.id))
                    self.timer_press = True
                    return True
            self.logger.warning("[UG{}] Estourou o timer de equalização de pressão da unidade hidráulica".format(self.id))
            self.forcar_estado_indisponivel()
            self.timer_press = True
        except Exception as e:
            raise(e)
        return False

    def controle_press_turbina(self):
        # Calcula PI
        self.erro_press_turbina = 0
        self.erro_press_turbina = self.leitura_pressao_turbina.valor - self.cfg["press_turbina_alvo"]

        self.logger.debug("[UG{}] Pressão Alvo: {:0.3f}, Recente: {:0.3f}".format(self.id, self.cfg["press_turbina_alvo"], self.leitura_pressao_turbina.valor))

        self.pt_controle_p = self.cfg["pt_kp"] * self.erro_press_turbina
        self.pt_controle_i = max(min((self.cfg["pt_ki"] * self.erro_press_turbina) + self.pt_controle_i, 1), 0)
        saida_pi = self.pt_controle_p + self.pt_controle_i
        
        self.logger.debug("[UG{}] PI: {:0.3f} <-- P:{:0.3f} + I:{:0.3f}; ERRO={}".format(self.id, saida_pi, self.pt_controle_p, self.pt_controle_i, self.erro_press_turbina))

        # Calcula o integrador de estabilidade e limita
        self.pt_controle_ie = max(min(saida_pi + self.pt_ajuste_ie * self.cfg["pt_kie"], 1), 0)

        # Arredondamento e limitação
        pot_alvo = max(min(round(self.cfg["pot_maxima_ug{}".format(self.id)] * self.pt_controle_ie, 5), self.cfg["pot_maxima_ug{}".format(self.id)],),self.cfg["pot_minima"],)

        self.logger.debug("[UG{}] Pot alvo: {:0.3f}".format(self.id, pot_alvo))
        
        ts = datetime.now(pytz.timezone("Brazil/East")).timestamp()
        try:
            self.db.insert_debug(
                ts,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
                0,
                0,
                0,
                0,
                self.setpoint,
                self.leitura_potencia.valor,
                self.leitura_setpoint_outra_ug.valor,
                self.leitura_potencia_outra_ug.valor,
                0,
                0,
                1,
                self.cfg["pt_kp"],
                self.cfg["pt_ki"],
                self.cfg["pt_kie"],
                self.pt_controle_ie,
            )
        except Exception as e:
            logger.exception(e)

        if self.leitura_pressao_turbina.valor >= 15.5:
            self.enviar_setpoint(pot_alvo)
        else:
            self.enviar_setpoint(0)

    def leitura_condicionadores(self):
        # Temperaturas
        # R
        self.leitura_temperatura_fase_R = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_TEMP_GERADOR_FASE_A".format(self.id)])
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_R
        self.condicionador_temperatura_fase_r_ug = CondicionadorExponencial("UG{}_TEMP_GERADOR_FASE_A".format(self.id), DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_r_ug)

        # S
        self.leitura_temperatura_fase_S = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_TEMP_GERADOR_FASE_B".format(self.id)])
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_S
        self.condicionador_temperatura_fase_s_ug = CondicionadorExponencial("UG{}_TEMP_GERADOR_FASE_B".format(self.id), DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_s_ug)
        
        # T
        self.leitura_temperatura_fase_T = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_TEMP_GERADOR_FASE_C".format(self.id)])
        base, limite = 100, 200
        x = self.leitura_temperatura_fase_T
        self.condicionador_temperatura_fase_t_ug = CondicionadorExponencial("UG{}_TEMP_GERADOR_FASE_C".format(self.id), DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_fase_t_ug)
        
        # Nucleo Gerador 1
        self.leitura_temperatura_nucleo_gerador_1 = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_TEMP_GERADOR_NUCLEO".format(self.id)])
        base, limite = 100, 200
        x = self.leitura_temperatura_nucleo_gerador_1
        self.condicionador_temperatura_nucleo_gerador_1_ug = CondicionadorExponencial("UG{}_TEMP_GERADOR_NUCLEO".format(self.id), DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_nucleo_gerador_1_ug)

        # Mancal Guia
        self.leitura_temperatura_mancal_guia = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_TEMP_MANCAL_GUIA_GERADOR".format(self.id)])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_guia
        self.condicionador_temperatura_mancal_guia_ug = CondicionadorExponencial("UG{}_TEMP_MANCAL_GUIA_GERADOR".format(self.id), DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_ug)

        # Mancal Guia Interno 1
        self.leitura_temperatura_mancal_guia_interno_1 = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_TEMP_1_MANCAL_GUIA_INTERNO".format(self.id)])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_guia_interno_1
        self.condicionador_temperatura_mancal_guia_interno_1_ug = CondicionadorExponencial("UG{}_TEMP_1_MANCAL_GUIA_INTERNO".format(self.id), DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_interno_1_ug)
        
        # Mancal Guia Interno 2
        self.leitura_temperatura_mancal_guia_interno_2 = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_TEMP_2_MANCAL_GUIA_INTERNO".format(self.id)])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_guia_interno_2
        self.condicionador_temperatura_mancal_guia_interno_2_ug = CondicionadorExponencial("UG{}_TEMP_2_MANCAL_GUIA_INTERNO".format(self.id), DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_guia_interno_2_ug)
        
        # Patins Mancal Combinado 1
        self.leitura_temperatura_patins_mancal_comb_1 = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_TEMP_1_PATINS_MANCAL_COMBINADO".format(self.id)])
        base, limite = 100, 200
        x = self.leitura_temperatura_patins_mancal_comb_1
        self.condicionador_temperatura_patins_mancal_comb_1_ug = CondicionadorExponencial("UG{}_TEMP_1_PATINS_MANCAL_COMBINADO".format(self.id), DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_patins_mancal_comb_1_ug)
        
        # Patins Mancal Combinado 2
        self.leitura_temperatura_patins_mancal_comb_2 = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_TEMP_2_PATINS_MANCAL_COMBINADO".format(self.id)])
        base, limite = 100, 200
        x = self.leitura_temperatura_patins_mancal_comb_2
        self.condicionador_temperatura_patins_mancal_comb_2_ug = CondicionadorExponencial("UG{}_TEMP_2_PATINS_MANCAL_COMBINADO".format(self.id), DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_patins_mancal_comb_2_ug)
        
        # Mancal Casquilho Combinado
        self.leitura_temperatura_mancal_casq_comb = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_TEMP_CASQ_MANCAL_COMBINADO".format(self.id)])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_casq_comb
        self.condicionador_temperatura_mancal_casq_comb_ug = CondicionadorExponencial("UG{}_TEMP_CASQ_MANCAL_COMBINADO".format(self.id), DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_casq_comb_ug)

        # Mancal Contra Escora Combinado
        self.leitura_temperatura_mancal_contra_esc_comb = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO".format(self.id)])
        base, limite = 100, 200
        x = self.leitura_temperatura_mancal_contra_esc_comb
        self.condicionador_temperatura_mancal_contra_esc_comb_ug = CondicionadorExponencial("UG{}_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO".format(self.id), DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_essenciais.append(self.condicionador_temperatura_mancal_contra_esc_comb_ug)
        
        # Pressão Entrada Turbina
        self.leitura_pressao_turbina = LeituraOPC(self.client, REG_OPC["UG"]["UG{}_PRESSAO_ENTRADA_TURBINA".format(self.id)], escala=0.1)
        base = 16.1
        limite = 15.5
        x = self.leitura_pressao_turbina
        self.condicionador_pressao_turbina_ug = CondicionadorExponencialReverso("UG{}_PRESSAO_ENTRADA_TURBINA".format(self.id), DEVE_INDISPONIBILIZAR, x, base, limite)
        self.condicionadores_atenuadores.append(self.condicionador_pressao_turbina_ug)


        # Essenciais
        self.leitura_saidas_digitiais_rv_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_SAIDAS_DIGITAIS".format(self.id)], 0, True)
        x = self.leitura_alarme_1_rt_b0
        self.condicionadores_essenciais.append(CondicionadorBase("UG{}_RV_SAIDAS_DIGITAIS - bit 00".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_2_rv_b3 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_2".format(self.id)], 3)
        x = self.leitura_falha_2_rv_b3
        self.condicionadores_essenciais.append(CondicionadorBase("UG{}_RV_FALHA_2 - bit 03".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_saidas_digitais_rt_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_SAIDAS_DIGITAIS".format(self.id)], 0, True)
        x = self.leitura_saidas_digitais_rt_b0
        self.condicionadores_essenciais.aapend(CondicionadorBase("UG{}_RT_SAIDAS_DIGITAIS - bit 00".format(self.id), DEVE_NORMALIZAR, x))
    
        self.leitura_trip_rele700G_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RELE_700G_TRIP_ATUADO".format(self.id)], 31)
        x = self.leitura_trip_rele700G_atuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG{}_RELE_700G_TRIP_ATUADO - bit 31".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_rele_bloq_86EH_desatuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RELE_BLOQUEIO_86EH_DESATUADO".format(self.id)], 28, True)
        x = self.leitura_rele_bloq_86EH_desatuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG{}_RELE_BLOQUEIO_86EH_DESATUADO - bit 28".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_trip_rele_rv_naoatuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RV_RELE_TRIP_NAO_ATUADO".format(self.id)], 14, True)
        x = self.leitura_trip_rele_rv_naoatuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG{}_RV_RELE_TRIP_NAO_ATUADO - bit 14".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_trip_rele_rt_naoatuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RT_RELE_TRIP_NAO_ATUADO".format(self.id)], 23, True)
        x = self.leitura_trip_rele_rt_naoatuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG{}_RT_RELE_TRIP_NAO_ATUADO - bit 23".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_bt_emerg_naoatuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_BT_EMERGENCIA_NAO_ATUADO".format(self.id)], 11, True)
        x = self.leitura_bt_emerg_naoatuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG{}_BT_EMERGENCIA_NAO_ATUADO - bit 11".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_clp_geral_sem_bloq_exter = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_CLP_GERAL_SEM_BLOQUEIO_EXTERNO".format(self.id)], 1, True)
        x = self.leitura_clp_geral_sem_bloq_exter
        self.condicionadores_essenciais.append(CondicionadorBase("UG{}_CLP_GERAL_SEM_BLOQUEIO_EXTERNO - bit 1".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_bloq_86M_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_BLOQUEIO_86M_ATUADO".format(self.id)], 31)
        x = self.leitura_bloq_86M_atuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG{}_BLOQUEIO_86M_ATUADO - bit 31".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_bloq_86E_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_BLOQUEIO_86E_ATUADO".format(self.id)], 31)
        x = self.leitura_bloq_86E_atuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG{}_BLOQUEIO_86E_ATUADO - bit 31".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_bloq_86H_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_BLOQUEIO_86H_ATUADO".format(self.id)], 31)
        x = self.leitura_bloq_86H_atuado
        self.condicionadores_essenciais.append(CondicionadorBase("UG{}_BLOQUEIO_86H_ATUADO - bit 31".format(self.id), DEVE_NORMALIZAR, x))


        # Gerais
        self.leitura_falha_1_rv_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 0)
        x = self.leitura_falha_1_rv_b0
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_1 - bit 00".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b1 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 1)
        x = self.leitura_falha_1_rv_b1
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_1 - bit 01".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b2 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 2)
        x = self.leitura_falha_1_rv_b2
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_1 - bit 02".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b3 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 3)
        x = self.leitura_falha_1_rv_b3
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_1 - bit 03".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b4 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 4)
        x = self.leitura_falha_1_rv_b4
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_1 - bit 04".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b5 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 5)
        x = self.leitura_falha_1_rv_b5
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_1 - bit 05".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b10 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 10)
        x = self.leitura_falha_1_rv_b10
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_1 - bit 10".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b11 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 11)
        x = self.leitura_falha_1_rv_b11
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_1 - bit 11".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b12 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 12)
        x = self.leitura_falha_1_rv_b12
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_1 - bit 12".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rv_b13 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 13)
        x = self.leitura_falha_1_rv_b13
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_1 - bit 13".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_alarme_1_rt_b8 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_ALARMES_1".format(self.id)], 8)
        x = self.leitura_alarme_1_rt_b8
        self.condicionadores.append(CondicionadorBase("UG{}_RT_ALARMES_1 - bit 08".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_1_rt_b1 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 1)
        x = self.leitura_falha_1_rt_b1
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 01".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_falha_1_rt_b2 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 2)
        x = self.leitura_falha_1_rt_b2
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 02".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_falha_1_rt_b3 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 3)
        x = self.leitura_falha_1_rt_b3
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 03".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b2 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_2".format(self.id)], 2)
        x = self.leitura_falha_2_rt_b2
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_2 - bit 02".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b5 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_2".format(self.id)], 5)
        x = self.leitura_falha_2_rt_b5
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_2 - bit 05".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b6 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_2".format(self.id)], 6)
        x = self.leitura_falha_2_rt_b6
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_2 - bit 06".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b7 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_2".format(self.id)], 7)
        x = self.leitura_falha_2_rt_b7
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_2 - bit 07".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b10 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_2".format(self.id)], 10)
        x = self.leitura_falha_2_rt_b10
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_2 - bit 10".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b11 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_2".format(self.id)], 11)
        x = self.leitura_falha_2_rt_b11
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_2 - bit 11".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_falha_2_rt_b12 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_2".format(self.id)], 12)
        x = self.leitura_falha_2_rt_b12
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_2 - bit 12".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_falha_bomba_1_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_UHRV_BOMBA_1_FALHA".format(self.id)], 0)
        x = self.leitura_falha_bomba_1_uhrv
        self.condicionadores.append(CondicionadorBase("UG{}_UHRV_BOMBA_1_FALHA - bit 00".format(self.id), DEVE_NORMALIZAR, x))
        
        self.leitura_falha_bomba_2_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_UHRV_BOMBA_2_FALHA".format(self.id)], 2)
        x = self.leitura_falha_bomba_2_uhrv
        self.condicionadores.append(CondicionadorBase("UG{}_UHRV_BOMBA_2_FALHA - bit 02".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_bomba_1_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_UHLM_BOMBA_1_FALHA".format(self.id)], 4)
        x = self.leitura_falha_bomba_1_uhlm
        self.condicionadores.append(CondicionadorBase("UG{}_UHLM_BOMBA_1_FALHA - bit 04".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_bomba_2_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_UHLM_BOMBA_2_FALHA".format(self.id)], 6)
        x = self.leitura_falha_bomba_2_uhlm
        self.condicionadores.append(CondicionadorBase("UG{}_UHLM_BOMBA_2_FALHA - bit 06".format(self.id), DEVE_NORMALIZAR, x))
       
        self.leitura_alarme_rele_rv_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RV_RELE_ALARME_ATUADO".format(self.id)], 15)
        x = self.leitura_alarme_rele_rv_atuado
        self.condicionadores.append(CondicionadorBase("UG{}_RV_RELE_ALARME_ATUADO - bit 15".format(self.id), DEVE_NORMALIZAR, 15))

        self.leitura_sistema_agua_clp_geral_ok = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_CLP_GERAL_SISTEMA_AGUA_OK".format(self.id)], 2, True)
        x = self.leitura_sistema_agua_clp_geral_ok
        self.condicionadores.append(CondicionadorBase("UG{}_CLP_GERAL_SISTEMA_AGUA_OK - bit 02".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_clp_geral_com_tens_barra_essenc = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_CLP_GERAL_COM_TENSAO_BARRA_ESSENCIAIS".format(self.id)], 3, True)
        x = self.leitura_clp_geral_com_tens_barra_essenc
        self.condicionadores.append(CondicionadorBase("UG{}_CLP_GERAL_COM_TENSAO_BARRA_ESSENCIAIS - bit 03".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_disparo_mecanico_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_DISPARO_MECANICO_ATUADO".format(self.id)], 9)
        x = self.leitura_disparo_mecanico_atuado
        self.condicionadores.append(CondicionadorBase("UG{}_DISPARO_MECANICO_ATUADO - bit 09".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_disparo_mecanico_desatuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_DISPARO_MECANICO_DESATUADO".format(self.id)], 8, True)
        x = self.leitura_disparo_mecanico_desatuado
        self.condicionadores.append(CondicionadorBase("UG{}_DISPARO_MECANICO_DESATUADO - bit 08".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_habilitar_sistema_agua = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_HABILITAR_SISTEMA_AGUA".format(self.id)], 11)
        x = self.leitura_falha_habilitar_sistema_agua
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_HABILITAR_SISTEMA_AGUA - bit 11".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_trip_temp_oleo_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_OLEO_UHLM".format(self.id)], 4)
        x = self.leitura_trip_temp_oleo_uhlm
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_OLEO_UHLM - bit 04".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_trip_temp_oleo_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_OLEO_UHRV".format(self.id)], 5)
        x = self.leitura_trip_temp_oleo_uhrv
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_OLEO_UHRV - bit 05".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_parada_bloq_abertura_disj = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_PARADA_BLOQUEIO_ABERTURA_DISJUNTOR".format(self.id)], 11)
        x = self.leitura_parada_bloq_abertura_disj
        self.condicionadores.append(CondicionadorBase("UG{}_PARADA_BLOQUEIO_ABERTURA_DISJUNTOR - bit 11".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_parada_bloq_descarga_pot = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_PARADA_BLOQUEIO_DESCARGA_POTENCIA".format(self.id)], 10)
        x = self.leitura_parada_bloq_descarga_pot
        self.condicionadores.append(CondicionadorBase("UG{}_PARADA_BLOQUEIO_DESCARGA_POTENCIA - bit 10".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_pressao_linha_b1_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_UHLM_FALHA_PRESSAO_LINHA_B1".format(self.id)], 9)
        x = self.leitura_falha_pressao_linha_b1_uhlm
        self.condicionadores.append(CondicionadorBase("UG{}_UHLM_FALHA_PRESSAO_LINHA_B1 - bit 09".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_pressao_linha_b2_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_UHLM_FALHA_PRESSAO_LINHA_B2".format(self.id)], 10)
        x = self.leitura_falha_pressao_linha_b2_uhlm
        self.condicionadores.append(CondicionadorBase("UG{}_UHLM_FALHA_PRESSAO_LINHA_B2 - bit 10".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_pressostato_linha_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_UHLM_FALHA_PRESSOSTATO_LINHA".format(self.id)], 11)
        x = self.leitura_falha_pressostato_linha_uhlm
        self.condicionadores.append(CondicionadorBase("UG{}_UHLM_FALHA_PRESSOSTATO_LINHA - bit 11".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_habilitar_rv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RV_FALHA_HABILITAR_RV".format(self.id)], 0)
        x = self.leitura_falha_habilitar_rv
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_HABILITAR_RV - bit 00".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_partir_rv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RV_FALHA_PARTIR_RV".format(self.id)], 1)
        x = self.leitura_falha_partir_rv
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_PARTIR_RV - bit 01".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_desabilitar_rv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RV_FALHA_DESABILITAR_RV".format(self.id)], 2)
        x = self.leitura_falha_desabilitar_rv
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_DESABILITAR_RV - bit 02".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_habilitar_rt = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RT_FALHA_HABILITAR".format(self.id)], 16)
        x = self.leitura_falha_habilitar_rt
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHA_HABILITAR - bit 16".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_falha_partir_rt = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RT_FALHA_PARTIR".format(self.id)], 17)
        x = self.leitura_falha_partir_rt
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHA_PARTIR - bit 17".format(self.id), DEVE_NORMALIZAR, x))

        self.leitura_alarme_1_rt_b0 = LeituraModbusBit(self.clp, REG_OPC["UG"]["UG{}_RT_ALARMES_1".format(self.id)], 0)
        x = self.leitura_alarme_1_rt_b0
        self.condicionadores.append(CondicionadorBase("UG{}_RT_ALARMES_1 - bit 00".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_alarme_1_rt_b4 = LeituraModbusBit(self.clp, REG_OPC["UG"]["UG{}_RT_ALARMES_1".format(self.id)], 4)
        x = self.leitura_alarme_1_rt_b4
        self.condicionadores.append(CondicionadorBase("UG{}_RT_ALARMES_1 - bit 04".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_alarme_1_rt_b5 = LeituraModbusBit(self.clp, REG_OPC["UG"]["UG{}_RT_ALARMES_1".format(self.id)], 5)
        x = self.leitura_alarme_1_rt_b5
        self.condicionadores.append(CondicionadorBase("UG{}_RT_ALARMES_1 - bit 05".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_1_rt_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 0)
        x = self.leitura_falha_1_rt_b0
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 00".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b4 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 4)
        x = self.leitura_falha_1_rt_b4
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 04".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b5 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 5)
        x = self.leitura_falha_1_rt_b5
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 05".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b6 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 6)
        x = self.leitura_falha_1_rt_b6
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 06".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b7 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 7)
        x = self.leitura_falha_1_rt_b7
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 07".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b8 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 8)
        x = self.leitura_falha_1_rt_b8
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 08".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b9 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 9)
        x = self.leitura_falha_1_rt_b9
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 09".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b10 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 10)
        x = self.leitura_falha_1_rt_b10
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 10".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b11 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 11)
        x = self.leitura_falha_1_rt_b11
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 11".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b12 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 12)
        x = self.leitura_falha_1_rt_b12
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 12".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b13 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 13)
        x = self.leitura_falha_1_rt_b13
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 13".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b14 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 14)
        x = self.leitura_falha_1_rt_b14
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 14".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_1_rt_b15 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_1".format(self.id)], 15)
        x = self.leitura_falha_1_rt_b15
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHAS_1 - bit 15".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rt_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHAS_2".format(self.id)], 0)
        x = self.leitura_falha_2_rt_b0
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHAS_2 - bit 00".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rt_b1 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHAS_2".format(self.id)], 1)
        x = self.leitura_falha_2_rt_b1
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHAS_2 - bit 01".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rt_b3 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHAS_2".format(self.id)], 3)
        x = self.leitura_falha_2_rt_b3
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHAS_2 - bit 03".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rt_b4 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHAS_2".format(self.id)], 4)
        x = self.leitura_falha_2_rt_b4
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHAS_2 - bit 04".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rt_b8 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHAS_2".format(self.id)], 8)
        x = self.leitura_falha_2_rt_b8
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHAS_2 - bit 08".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rt_b9 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHAS_2".format(self.id)], 9)
        x = self.leitura_falha_2_rt_b9
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHAS_2 - bit 09".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rv_b1 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_2".format(self.id)], 1)
        x = self.leitura_falha_2_rv_b1
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_2 - bit 01".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_2_rv_b2 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_2".format(self.id)], 2)
        x = self.leitura_falha_2_rv_b2
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_2 - bit 02".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_rele_700G_bf_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RELE_700G_BF_ATUADO".format(self.id)], 0)
        x = self.leitura_rele_700G_bf_atuado
        self.condicionadores.append(CondicionadorBase("UG{}_RELE_700G_BF_ATUADO - bit 00".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_sup_tensao_125vcc = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_SUPERVISAO_TENSAO_125VCC".format(self.id)], 29, True)
        x = self.leitura_sup_tensao_125vcc
        self.condicionadores.append(CondicionadorBase("UG{}_SUPERVISAO_TENSAO_125VCC - bit 29".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_sup_tensao_24vcc = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_SUPERVISAO_TENSAO_24VCC".format(self.id)], 30, True)
        x = self.leitura_sup_tensao_24vcc
        self.condicionadores.append(CondicionadorBase("UG{}_SUPERVISAO_TENSAO_24VCC - bit 30".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_sup_bobina_52g = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_SUPERVISAO_BOBINA_52G".format(self.id)], 12, True)
        x = self.leitura_sup_bobina_52g
        self.condicionadores.append(CondicionadorBase("UG{}_SUPERVISAO_BOBINA_52G - bit 12".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_sup_bobina_86eh = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_SUPERVISAO_BOBINA_86EH".format(self.id)], 13, True)
        x = self.leitura_sup_bobina_86eh
        self.condicionadores.append(CondicionadorBase("UG{}_SUPERVISAO_BOBINA_86EH - bit 13".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_disj_125vcc_fechados = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_DISJUNTORES_125VCC_FECHADOS".format(self.id)], 31, True)
        x = self.leitura_disj_125vcc_fechados
        self.condicionadores.append(CondicionadorBase("UG{}_DISJUNTORES_125VCC_FECHADOS - bit 31".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_disj_24vcc_fechados = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_DISJUNTORES_24VCC_FECHADOS".format(self.id)], 0, True)
        x = self.leitura_disj_24vcc_fechados
        self.condicionadores.append(CondicionadorBase("UG{}_DISJUNTORES_24VCC_FECHADOS - bit 00".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_ponte_fase_a = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_PONTE_FASE_A".format(self.id)], 0)
        x = self.leitura_falha_temp_ponte_fase_a
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_PONTE_FASE_A - bit 00".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_ponte_fase_b = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_PONTE_FASE_B".format(self.id)], 1)
        x = self.leitura_falha_temp_ponte_fase_b
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_PONTE_FASE_B - bit 01".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_ponte_fase_c = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_PONTE_FASE_C".format(self.id)], 2)
        x = self.leitura_falha_temp_ponte_fase_c
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_PONTE_FASE_C - bit 02".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_trafo_excita = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_TRAFO_EXCITACAO".format(self.id)], 4)
        x = self.leitura_falha_temp_trafo_excita
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_TRAFO_EXCITACAO - bit 04".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_guia = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_MANCAL_GUIA".format(self.id)], 5)
        x = self.leitura_falha_temp_mancal_guia
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_MANCAL_GUIA - bit 05".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_oleo_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_OLEO_UHRV".format(self.id)], 6)
        x = self.leitura_falha_temp_oleo_uhrv
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_OLEO_UHRV - bit 06".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_oleo_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_OLEO_UHLM".format(self.id)], 7)
        x = self.leitura_falha_temp_oleo_uhlm
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_OLEO_UHLM - bit 07".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_casq_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_CASQ_MANCAL_COMBINADO".format(self.id)], 8)
        x = self.leitura_falha_temp_mancal_casq_comb
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_CASQ_MANCAL_COMBINADO - bit 08".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_con_esc_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO".format(self.id)], 9)
        x = self.leitura_falha_temp_mancal_con_esc_comb
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO - bit 09".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_pat_1_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_1_PATINS_MANCAL_COMBINADO".format(self.id)], 10)
        x = self.leitura_falha_temp_mancal_pat_1_comb
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_1_PATINS_MANCAL_COMBINADO - bit 10".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_pat_2_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_2_PATINS_MANCAL_COMBINADO".format(self.id)], 11)
        x = self.leitura_falha_temp_mancal_pat_2_comb
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_2_PATINS_MANCAL_COMBINADO - bit 11".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_mancal_guia_interno_1 = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_1_MANCAL_GUIA_INTERNO".format(self.id)], 12)
        x = self.leitura_falha_temp_mancal_guia_interno_1
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_1_MANCAL_GUIA_INTERNO - bit 12".format(self.id), DEVE_INDISPONIBILIZAR, x))
        
        self.leitura_falha_temp_mancal_guia_interno_2 = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_2_MANCAL_GUIA_INTERNO".format(self.id)], 13)
        x = self.leitura_falha_temp_mancal_guia_interno_2
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_2_MANCAL_GUIA_INTERNO - bit 13".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_gerador_nucleo_esta = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_GERADOR_NUCLEO_ESTATORICO".format(self.id)], 14)
        x = self.leitura_falha_temp_gerador_nucleo_esta
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_GERADOR_NUCLEO_ESTATORICO - bit 14".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_gerador_fase_a = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_GERADOR_FASE_A".format(self.id)], 15)
        x = self.leitura_falha_temp_gerador_fase_a
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_GERADOR_FASE_A - bit 15".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_gerador_fase_b = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_GERADOR_FASE_B".format(self.id)], 16)
        x = self.leitura_falha_temp_gerador_fase_b
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_GERADOR_FASE_B - bit 16".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_temp_gerador_fase_c = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_TEMP_GERADOR_FASE_C".format(self.id)], 17)
        x = self.leitura_falha_temp_gerador_fase_c
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_TEMP_GERADOR_FASE_C - bit 17".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_pressao_entrada_turb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_PRESSAO_ENTRADA_TURBINA".format(self.id)], 20)
        x = self.leitura_falha_pressao_entrada_turb
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_PRESSAO_ENTRADA_TURBINA - bit 20".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_eixo_x_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_VIBRACAO_EIXO_X_MANCAL_COMBINADO".format(self.id)], 24)
        x = self.leitura_falha_vibra_eixo_x_mancal_comb
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_VIBRACAO_EIXO_X_MANCAL_COMBINADO - bit 24".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_eixo_y_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO".format(self.id)], 25)
        x = self.leitura_falha_vibra_eixo_y_mancal_comb
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_VIBRACAO_EIXO_Y_MANCAL_COMBINADO - bit 25".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_eixo_z_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO".format(self.id)], 26)
        x = self.leitura_falha_vibra_eixo_z_mancal_comb
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_VIBRACAO_EIXO_Z_MANCAL_COMBINADO - bit 26".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_detec_horizontal = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_VIBRACAO_DETECCAO_HORIZONTAL".format(self.id)], 28)
        x = self.leitura_falha_vibra_detec_horizontal
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_VIBRACAO_DETECCAO_HORIZONTAL - bit 28".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_vibra_detec_vertical = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_FALHA_VIBRACAO_DETECACAO_VERTICAL".format(self.id)], 29)
        x = self.leitura_falha_vibra_detec_vertical
        self.condicionadores.append(CondicionadorBase("UG{}_FALHA_VIBRACAO_DETECACAO_VERTICAL - bit 29".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_bloqueio_86M_atuado = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_BLOQUEIO_86M_ATUADO".format(self.id)], 31)
        x = self.leitura_bloqueio_86M_atuado
        self.condicionadores.append(CondicionadorBase("UG{}_BLOQUEIO_86M_ATUADO - bit 31".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_detec_horizontal = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_VIBRACAO_DETECCAO_HORIZONTAL".format(self.id)], 21)
        x = self.leitura_trip_vibra_detec_horizontal
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_VIBRACAO_DETECCAO_HORIZONTAL - bit 21".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_detec_vertical = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_VIBRACAO_DETECACAO_VERTICAL".format(self.id)], 22)
        x = self.leitura_trip_vibra_detec_vertical
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_VIBRACAO_DETECACAO_VERTICAL - bit 22".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_eixo_x_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_VIBRACAO_EIXO_X_MANCAL_COMBINADO".format(self.id)], 23)
        x = self.leitura_trip_vibra_eixo_x_mancal_comb
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_VIBRACAO_EIXO_X_MANCAL_COMBINADO - bit 23".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_eixo_y_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_VIBRACAO_EIXO_Y_MANCAL_COMBINADO".format(self.id)], 24)
        x = self.leitura_trip_vibra_eixo_y_mancal_comb
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_VIBRACAO_EIXO_Y_MANCAL_COMBINADO - bit 24".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_vibra_eixo_z_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_VIBRACAO_EIXO_Z_MANCAL_COMBINADO".format(self.id)], 25)
        x = self.leitura_trip_vibra_eixo_z_mancal_comb
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_VIBRACAO_EIXO_Z_MANCAL_COMBINADO - bit 25".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_ponte_fase_a = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_PONTE_FASE_A".format(self.id)], 16)
        x = self.leitura_trip_temp_ponte_fase_a
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_PONTE_FASE_A - bit 16".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_ponte_fase_b = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_PONTE_FASE_B".format(self.id)], 17)
        x = self.leitura_trip_temp_ponte_fase_b
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_PONTE_FASE_B - bit 17".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_ponte_fase_c = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_PONTE_FASE_C".format(self.id)], 18)
        x = self.leitura_trip_temp_ponte_fase_c
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_PONTE_FASE_C - bit 18".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_fase_a = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_GERADOR_FASE_A".format(self.id)], 19)
        x = self.leitura_trip_temp_gerador_fase_a
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_GERADOR_FASE_A - bit 19".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_fase_b = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_GERADOR_FASE_B".format(self.id)], 20)
        x = self.leitura_trip_temp_gerador_fase_b
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_GERADOR_FASE_B - bit 20".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_fase_c = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_GERADOR_FASE_C".format(self.id)], 21)
        x = self.leitura_trip_temp_gerador_fase_c
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_GERADOR_FASE_C - bit 21".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_nucleo_estatorico = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_GERADOR_NUCLEO_ESTATORICO".format(self.id)], 22)
        x = self.leitura_trip_temp_gerador_nucleo_estatorico
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_GERADOR_NUCLEO_ESTATORICO - bit 22".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_gerador_saida_ar = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_GERADOR_SAIDA_AR".format(self.id)], 23)
        x = self.leitura_trip_temp_gerador_saida_ar
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_GERADOR_SAIDA_AR - bit 23".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_trafo_ateramento = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_TRAFO_ATERRAMENTO".format(self.id)], 24)
        x = self.leitura_trip_temp_trafo_ateramento
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_TRAFO_ATERRAMENTO - bit 24".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_trafo_excitacao = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_TRAFO_EXCITACAO".format(self.id)], 25)
        x = self.leitura_trip_temp_trafo_excitacao
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_TRAFO_EXCITACAO - bit 25".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_pressao_acum_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_PRESSAO_ACUMULADOR_UHRV".format(self.id)], 5)
        x = self.leitura_trip_pressao_acum_uhrv
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_PRESSAO_ACUMULADOR_UHRV - bit 05".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_casq_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_CASQ_MANCAL_COMBINADO".format(self.id)], 18)
        x = self.leitura_trip_temp_mancal_casq_comb
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_CASQ_MANCAL_COMBINADO - bit 18".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_contra_esc_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO".format(self.id)], 19)
        x = self.leitura_trip_temp_mancal_contra_esc_comb
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO - bit 19".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_patins_1_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_1_PATINS_MANCAL_COMBINADO".format(self.id)], 20)
        x = self.leitura_trip_temp_mancal_patins_1_comb
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_1_PATINS_MANCAL_COMBINADO - bit 20".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_patins_2_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_2_PATINS_MANCAL_COMBINADO".format(self.id)], 21)
        x = self.leitura_trip_temp_mancal_patins_2_comb
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_2_PATINS_MANCAL_COMBINADO - bit 21".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_guia_interno_1 = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_1_MANCAL_GUIA_INTERNO".format(self.id)], 22)
        x = self.leitura_trip_temp_mancal_guia_interno_1
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_1_MANCAL_GUIA_INTERNO - bit 22".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_trip_temp_mancal_guia_interno_2 = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_TRIP_TEMP_2_MANCAL_GUIA_INTERNO".format(self.id)], 23)
        x = self.leitura_trip_temp_mancal_guia_interno_2
        self.condicionadores.append(CondicionadorBase("UG{}_TRIP_TEMP_2_MANCAL_GUIA_INTERNO - bit 23".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_fechar_distrib_rv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RV_FALHA_FECHAR_DISTRIBUIDOR".format(self.id)], 4)
        x = self.leitura_falha_fechar_distrib_rv
        self.condicionadores.append(CondicionadorBase("UG{}_RV_FALHA_FECHAR_DISTRIBUIDOR - bit 04".format(self.id), DEVE_INDISPONIBILIZAR, x))

        self.leitura_falha_desbilitar_rt = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RT_FALHA_DESABILITAR".format(self.id)], 18)
        x = self.leitura_falha_desbilitar_rt
        self.condicionadores.append(CondicionadorBase("UG{}_RT_FALHA_DESABILITAR - bit 18".format(self.id), DEVE_INDISPONIBILIZAR, x))

        return True

    def controle_limites_operacao(self):
        if self.leitura_temperatura_fase_R.valor >= self.condicionador_temperatura_fase_r_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura de Fase R da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_r_ug.valor_base, self.leitura_temperatura_fase_R.valor))
        if self.leitura_temperatura_fase_R.valor >= 0.9*(self.condicionador_temperatura_fase_r_ug.valor_limite - self.condicionador_temperatura_fase_r_ug.valor_base) + self.condicionador_temperatura_fase_r_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura de Fase R da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_r_ug.valor_limite, self.leitura_temperatura_fase_R.valor))
        
        if self.leitura_temperatura_fase_S.valor >= self.condicionador_temperatura_fase_s_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura de Fase S da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_s_ug.valor_base, self.leitura_temperatura_fase_S.valor))
        if self.leitura_temperatura_fase_S.valor >= 0.9*(self.condicionador_temperatura_fase_s_ug.valor_limite - self.condicionador_temperatura_fase_s_ug.valor_base) + self.condicionador_temperatura_fase_s_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura de Fase S da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_s_ug.valor_limite, self.leitura_temperatura_fase_S.valor))

        if self.leitura_temperatura_fase_T.valor >= self.condicionador_temperatura_fase_t_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura de Fase T da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_t_ug.valor_base, self.leitura_temperatura_fase_T.valor))
        if self.leitura_temperatura_fase_T.valor >= 0.9*(self.condicionador_temperatura_fase_t_ug.valor_limite - self.condicionador_temperatura_fase_t_ug.valor_base) + self.condicionador_temperatura_fase_t_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura de Fase T da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_fase_t_ug.valor_limite, self.leitura_temperatura_fase_T.valor))

        if self.leitura_temperatura_nucleo_gerador_1.valor >= self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Núcleo Gerador 1 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base, self.leitura_temperatura_nucleo_gerador_1.valor))
        if self.leitura_temperatura_nucleo_gerador_1.valor >= 0.9*(self.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite - self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base) + self.condicionador_temperatura_nucleo_gerador_1_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Núcleo Gerador 1 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_nucleo_gerador_1_ug.valor_limite, self.leitura_temperatura_nucleo_gerador_1.valor))
        
        if self.leitura_temperatura_mancal_guia.valor >= self.condicionador_temperatura_mancal_guia_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Guia da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_ug.valor_base, self.leitura_temperatura_mancal_guia.valor))
        if self.leitura_temperatura_mancal_guia.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_ug.valor_limite - self.condicionador_temperatura_mancal_guia_ug.valor_base) + self.condicionador_temperatura_mancal_guia_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Guia da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_ug.valor_limite, self.leitura_temperatura_mancal_guia.valor))
        
        if self.leitura_temperatura_mancal_guia_interno_1.valor >= self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Guia Interno 1 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base, self.leitura_temperatura_mancal_guia_interno_1.valor))
        if self.leitura_temperatura_mancal_guia_interno_1.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_limite - self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base) + self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Guia Interno 1 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_interno_1_ug.valor_limite, self.leitura_temperatura_mancal_guia_interno_1.valor))
        
        if self.leitura_temperatura_mancal_guia_interno_2.valor >= self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Guia Interno 2 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base, self.leitura_temperatura_mancal_guia_interno_2.valor))
        if self.leitura_temperatura_mancal_guia_interno_2.valor >= 0.9*(self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_limite - self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base) + self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Guia Interno 2 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_guia_interno_2_ug.valor_limite, self.leitura_temperatura_mancal_guia_interno_2.valor))

        if self.leitura_temperatura_patins_mancal_comb_1.valor >= self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura dos Patins do Mancal Combinado 1 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base, self.leitura_temperatura_patins_mancal_comb_1.valor))
        if self.leitura_temperatura_patins_mancal_comb_1.valor >= 0.9*(self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_limite - self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base) + self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura dos Patins do Mancal Combinado 1 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_patins_mancal_comb_1_ug.valor_limite, self.leitura_temperatura_patins_mancal_comb_1.valor))
        
        if self.leitura_temperatura_patins_mancal_comb_2.valor >= self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura dos Patins do Mancal Combinado 2 da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base, self.leitura_temperatura_patins_mancal_comb_2.valor))
        if self.leitura_temperatura_patins_mancal_comb_2.valor >= 0.9*(self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_limite - self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base) + self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura dos Patins do Mancal Combinado 2 da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_patins_mancal_comb_2_ug.valor_limite, self.leitura_temperatura_patins_mancal_comb_2.valor))

        if self.leitura_temperatura_mancal_casq_comb.valor >= self.condicionador_temperatura_mancal_casq_comb_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Casquilho Combinado da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_casq_comb_ug.valor_base, self.leitura_temperatura_mancal_casq_comb.valor))
        if self.leitura_temperatura_mancal_casq_comb.valor >= 0.9*(self.condicionador_temperatura_mancal_casq_comb_ug.valor_limite - self.condicionador_temperatura_mancal_casq_comb_ug.valor_base) + self.condicionador_temperatura_mancal_casq_comb_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Casquilho Combinado da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_casq_comb_ug.valor_limite, self.leitura_temperatura_mancal_casq_comb.valor))

        if self.leitura_temperatura_mancal_contra_esc_comb.valor >= self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base:
            self.logger.warning("[UG{}] A temperatura do Mancal Contra Escora Combinado da UG passou do valor base! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base, self.leitura_temperatura_mancal_contra_esc_comb.valor))
        if self.leitura_temperatura_mancal_contra_esc_comb.valor >= 0.9*(self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_limite - self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base) + self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_base:
            self.logger.critical("[UG{}] A temperatura do Mancal Contra Escora Combinado da UG está muito próxima do limite! ({}C) | Leitura: {}C".format(self.id, self.condicionador_temperatura_mancal_contra_esc_comb_ug.valor_limite, self.leitura_temperatura_mancal_contra_esc_comb.valor))

        if self.leitura_pressao_turbina.valor <= self.condicionador_pressao_turbina_ug.valor_base and self.leitura_pressao_turbina.valor != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            self.logger.warning("[UG{}] A pressão na entrada da turbina da UG passou do valor base! ({:03.2f} KGf/m2) | Leitura: {:03.2f}".format(self.id, self.condicionador_pressao_turbina_ug.valor_base, self.leitura_pressao_turbina.valor))
        if self.leitura_pressao_turbina.valor <= self.condicionador_pressao_turbina_ug.valor_limite+0.9*(self.condicionador_pressao_turbina_ug.valor_base - self.condicionador_pressao_turbina_ug.valor_limite) and self.leitura_pressao_turbina.valor != 0 and self.etapa_atual == UNIDADE_SINCRONIZADA:
            self.logger.critical("[UG{}] A pressão na entrada da turbina da UG está muito próxima do limite! ({:03.2f} KGf/m2) | Leitura: {:03.2f} KGf/m2".format(self.id, self.condicionador_pressao_turbina_ug.valor_limite, self.leitura_pressao_turbina.valor))

    def leituras_por_hora(self):
        # Telegram
        self.leitura_saidas_digitais_rv_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_SAIDAS_DIGITAIS".format(self.id)], 0)
        if self.leitura_saidas_digitais_rv_b0:
            self.logger.warning("[UG{}] O alarme do Regulador de Velocidade da UG foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_saidas_digitais_rt_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_SAIDAS_DIGITAIS".format(self.id)], 0)
        if self.leitura_saidas_digitais_rt_b0:
            self.logger.warning("[UG{}] O alarme do Regulador de Tensão da UG foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_falha_3_rt_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_3".format(self.id)], 0)
        if self.leitura_falha_3_rt_b0:
            self.logger.warning("[UG{}] Houve uma falha na leitura de potência reativa pelo Regulador de Tensão da UG. Favor Verificar.".format(self.id))
        
        self.leitura_falha_3_rt_b1 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_3".format(self.id)], 1)
        if self.leitura_falha_3_rt_b1:
            self.logger.warning("[UG{}] Houve uma falha na leitura da tensão terminal pelo Regulador de Tensão da UG. Favor Verificar.".format(self.id))
        
        self.leitura_falha_3_rt_b2 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_3".format(self.id)], 2)
        if self.leitura_falha_3_rt_b2:
            self.logger.warning("[UG{}] Houve uma falha na leitura principal da corrente de excitação pelo Regulador de Tensão da UG. Favor Verificar.".format(self.id))
        
        self.leitura_falha_3_rt_b3 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_3".format(self.id)], 3)
        if self.leitura_falha_3_rt_b3:
            self.logger.warning("[UG{}] Houve uma falha na leitura retaguarda da corrente de excitação pelo Regulador de Tensão da UG. Favor Verificar.".format(self.id))
        
        self.leitura_falha_3_rt_b4 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_3".format(self.id)], 4)
        if self.leitura_falha_3_rt_b4:
            self.logger.warning("[UG{}] Foi identificado ruído na instrumentação de reativo do Regulador de Tensão da UG. Favor Verificar.".format(self.id))
        
        self.leitura_falha_3_rt_b5 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_3".format(self.id)], 5)
        if self.leitura_falha_3_rt_b5:
            self.logger.warning("[UG{}] Foi identificado ruído na instrumentação de tensão do Regulador de Tensão da UG. Favor Verificar.".format(self.id))
        
        self.leitura_falha_3_rt_b6 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_3".format(self.id)], 6)
        if self.leitura_falha_3_rt_b6:
            self.logger.warning("[UG{}] Foi identificado ruído na instrumentação de excitação principal do Regulador de Tensão da UG. Favor Verificar.".format(self.id))
        
        self.leitura_falha_3_rt_b7 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RT_FALHAS_3".format(self.id)], 7)
        if self.leitura_falha_3_rt_b7:
            self.logger.warning("[UG{}] Foi identificado ruído na instrumentação de excitação retaguarda do Regulador de Tensão da UG. Favor Verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b4 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 4)
        if self.leitura_falha_1_rv_b4:
            self.logger.warning("[UG{}] Houve uma falha de leitura de posição do distribuidor pelo Regulador de Velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b5 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 5)
        if self.leitura_falha_1_rv_b5:
            self.logger.warning("[UG{}] Houve uma falha de leitura de posição do rotor pelo Regulador de Velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b6 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 6)
        if self.leitura_falha_1_rv_b6:
            self.logger.warning("[UG{}] Houve uma falha de leitura de potência ativa pelo Regulador de Velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b7 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 7)
        if self.leitura_falha_1_rv_b7:
            self.logger.warning("[UG{}] Houve uma falha de leitura de referência de potência pelo Regulador de Velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b8 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 8)
        if self.leitura_falha_1_rv_b8:
            self.logger.warning("[UG{}] Houve uma falha de leitura de nível montante pelo Regulador de Velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b13 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 13)
        if self.leitura_falha_1_rv_b13:
            self.logger.warning("[UG{}] Foi identificado ruído na medição principal de velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b14 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 14)
        if self.leitura_falha_1_rv_b14:
            self.logger.warning("[UG{}] Foi identificado ruído na medição retaguarda de velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_1_rv_b15 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 15)
        if self.leitura_falha_1_rv_b15:
            self.logger.warning("[UG{}] Foi identificada perda na medição principal de velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_2_rv_b0 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 0)
        if self.leitura_falha_2_rv_b0:
            self.logger.warning("[UG{}] Foi identificada perda na medição retaguarda de velocidade da UG. Favor verificar.".format(self.id))
        
        self.leitura_falha_2_rv_b4 = LeituraModbusBit(self.clp, REG_MB["UG"]["UG{}_RV_FALHA_1".format(self.id)], 4)
        if self.leitura_falha_2_rv_b4:
            self.logger.warning("[UG{}] Foi identificada diferença entre medidor principal e retaguarda da UG. Favor verificar.".format(self.id))
        
        self.leitura_unidade_manutencao_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_UHRV_UNIDADE_EM_MANUTENCAO".format(self.id)], 0)
        if self.leitura_unidade_manutencao_uhrv:
            self.logger.warning("[UG{}] UHRV da UG entrou em modo de manutenção".format(self.id))
        
        self.leitura_unidade_manutencao_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_UHLM_UNIDADE_EM_MANUTENCAO".format(self.id)], 4)
        if self.leitura_unidade_manutencao_uhlm:
            self.logger.warning("[UG{}] UHLM da UG entrou em modo de manutenção".format(self.id))

        self.leitura_filtro_limpo_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_UHRV_FILTRO_LIMPO".format(self.id)], 24, True)
        if not self.leitura_filtro_limpo_uhrv:
            self.logger.warning("[UG{}] O filtro da UHRV da UG está sujo. Favor realizar limpeza/troca.".format(self.id))

        self.leitura_filtro_limpo_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_UHLM_FILTRO_LIMPO".format(self.id)], 21, True)
        if not self.leitura_filtro_limpo_uhrv:
            self.logger.warning("[UG{}] O filtro da UHLM da UG está sujo. Favor realizar limpeza/troca.".format(self.id))

        self.leitura_porta_interna_fechada_cpg = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_CPG_UG_PORTA_INTERNA_FECHADA".format(self.id)], 12, True)
        if not self.leitura_porta_interna_fechada_cpg:
            self.logger.warning("[UG{}] A porta interna do CPG da UG está aberta. Favor fechar.".format(self.id))

        self.leitura_porta_traseira_fechada_cpg = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_CPG_UG_PORTA_TRASEIRA_FECHADA".format(self.id)], 13, True)
        if not self.leitura_porta_traseira_fechada_cpg:
            self.logger.warning("[UG{}] A porta traseira do CPG da UG está aberta. Favor fechar.".format(self.id))

        self.leitura_resistencia_sem_falha = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_RESISTENCIA_SEM_FALHA".format(self.id)], 28, True)
        if not self.leitura_resistencia_sem_falha:
            self.logger.warning("[UG{}] Houve uma falha na resistência da UG. Favor verificar.".format(self.id))

        self.leitura_escovas_gastas_polo_positivo = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ESCOVAS_GASTAS_POLO_POSITIVO".format(self.id)], 5)
        if self.leitura_escovas_gastas_polo_positivo:
            self.logger.warning("[UG{}] Foi identificado que as escovas do polo positivo da UG estão gastas. Favor verificar.".format(self.id))
        
        self.leitura_escovas_gastas_polo_negativo = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ESCOVAS_GASTAS_POLO_NEGATIVO".format(self.id)], 6)
        if self.leitura_escovas_gastas_polo_negativo:
            self.logger.warning("[UG{}] Foi identificado que as escovas do polo negativo da UG estão gastas. Favor verificar.".format(self.id))

        self.leitura_alarme_temp_ponte_fase_a = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_PONTE_FASE_A".format(self.id)], 0)
        if self.leitura_alarme_temp_ponte_fase_a:
            self.logger.warning("[UG{}] O alarme de temperatura da pote fase A foi acionado. Favor verificar.".format(self.id))

        self.leitura_alarme_temp_ponte_fase_b = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_PONTE_FASE_B".format(self.id)], 1)
        if self.leitura_alarme_temp_ponte_fase_b:
            self.logger.warning("[UG{}] O alarme de temperatura da pote fase B foi acionado. Favor verificar.".format(self.id))

        self.leitura_alarme_temp_ponte_fase_c = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_PONTE_FASE_C".format(self.id)], 2)
        if self.leitura_alarme_temp_ponte_fase_c:
            self.logger.warning("[UG{}] O alarme de temperatura da pote fase C foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_trafo_excitacao = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_TRAFO_EXCITACAO".format(self.id)], 4)
        if self.leitura_alarme_temp_trafo_excitacao:
            self.logger.warning("[UG{}] O alarme de temperatura do transformador excitação foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_mancal_guia = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_MANCAL_GUIA".format(self.id)], 5)
        if self.leitura_alarme_temp_mancal_guia:
            self.logger.warning("[UG{}] O alarme de temperatura do mancal guia foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_oleo_uhrv = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_OLEO_UHRV".format(self.id)], 6)
        if self.leitura_alarme_temp_oleo_uhrv:
            self.logger.warning("[UG{}] O alarme de temperatura de óleo da UHRV foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_oleo_uhlm = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_OLEO_UHLM".format(self.id)], 7)
        if self.leitura_alarme_temp_oleo_uhlm:
            self.logger.warning("[UG{}] O alarme de temperatura de óleo da UHLM foi acionado. Favor verificar.".format(self.id))

        self.leitura_alarme_temp_mancal_casq_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_CASQ_MANCAL_COMBINADO".format(self.id)], 8)
        if self.leitura_alarme_temp_mancal_casq_comb:
            self.logger.warning("[UG{}] O alarme de temperatura do mancal casquilho combinado foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_mancal_con_esc_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_CONTRA_ESCORA_MANCAL_COMBINADO".format(self.id)], 9)
        if self.leitura_alarme_temp_mancal_con_esc_comb:
            self.logger.warning("[UG{}] O alarme de temperatura do mancal contra escora combinado foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_patins_1_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_1_PATINS_MANCAL_COMBINADO".format(self.id)], 10)
        if self.leitura_alarme_temp_patins_1_mancal_comb:
            self.logger.warning("[UG{}] O alarme de temperatura do patins 1 mancal combinado foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_patins_2_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_2_PATINS_MANCAL_COMBINADO".format(self.id)], 11)
        if self.leitura_alarme_temp_patins_2_mancal_comb:
            self.logger.warning("[UG{}] O alarme de temperatura do patins 2 mancal combinado foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_mancal_guia_interno_1 = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_1_MANCAL_GUIA_INTERNO".format(self.id)], 12)
        if self.leitura_alarme_temp_mancal_guia_interno_1:
            self.logger.warning("[UG{}] O alarme de temperatura do mancal guia interno 1 foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_temp_mancal_guia_interno_2 = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_2_MANCAL_GUIA_INTERNO".format(self.id)], 13)
        if self.leitura_alarme_temp_mancal_guia_interno_2:
            self.logger.warning("[UG{}] O alarme de temperatura do mancal guia interno 2 foi acionado. Favor verificar.".format(self.id))

        self.leitura_alarme_temp_nucleo_estatorico_gerador = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_GERADOR_NUCLEO_ESTATORICO".format(self.id)], 14)
        if self.leitura_alarme_temp_nucleo_estatorico_gerador:
            self.logger.warning("[UG{}] O alarme de temperatura do núcleo estatórico do gerador foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_temp_fase_a_gerador = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_GERADOR_FASE_A".format(self.id)], 15)
        if self.leitura_temp_fase_a_gerador:
            self.logger.warning("[UG{}] O alarme de temperatura de fase A do gerador foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_temp_fase_b_gerador = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_GERADOR_FASE_B".format(self.id)], 16)
        if self.leitura_temp_fase_b_gerador:
            self.logger.warning("[UG{}] O alarme de temperatura de fase B do gerador foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_temp_fase_c_gerador = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_TEMP_GERADOR_FASE_C".format(self.id)], 17)
        if self.leitura_temp_fase_c_gerador:
            self.logger.warning("[UG{}] O alarme de temperatura de fase C do gerador foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_vibra_eixo_x_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_VIBRACAO_EIXO_X_MANCAL_COMBINADO".format(self.id)], 24)
        if self.leitura_alarme_vibra_eixo_x_mancal_comb:
            self.logger.warning("[UG{}] O alarme de vibração do eixo X do mancal combinado foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_vibra_eixo_y_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_VIBRACAO_EIXO_Y_MANCAL_COMBINADO".format(self.id)], 25)
        if self.leitura_alarme_vibra_eixo_y_mancal_comb:
            self.logger.warning("[UG{}] O alarme de vibração do eixo Y do mancal combinado foi acionado. Favor verificar.".format(self.id))
        
        self.leitura_alarme_vibra_eixo_z_mancal_comb = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_VIBRACAO_EIXO_Z_MANCAL_COMBINADO".format(self.id)], 26)
        if self.leitura_alarme_vibra_eixo_z_mancal_comb:
            self.logger.warning("[UG{}] O alarme de vibração do eixo Z do mancal combinado foi acionado. Favor verificar.".format(self.id))

        self.leitura_alarme_vibra_detec_horizontal = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_VIBRACAO_DETECCAO_HORIZONTAL".format(self.id)], 28)
        if self.leitura_alarme_vibra_detec_horizontal:
            self.logger.warning("[UG{}] O alarme de vibração detecção horizontal foi acionado. Favor verificar.".format(self.id))

        self.leitura_alarme_vibra_detec_vertical = LeituraOPCBit(self.client, REG_OPC["UG"]["UG{}_ALM_VIBRACAO_DETECCAO_VERTICAL".format(self.id)], 29)
        if self.leitura_alarme_vibra_detec_vertical:
            self.logger.warning("[UG{}] O alarme de vibração detecção vertical foi acionado. Favor verificar.".format(self.id))

class State:
    def __init__(self, parent_ug: UnidadeDeGeracao):
        self.parent_ug = parent_ug
        self.logger = logging.getLogger("__main__")

    @abstractmethod
    def step(self) -> State:
        pass

class StateManual(State):
    def __init__(self, parent_ug: UnidadeDeGeracao):
        super().__init__(parent_ug)
        self.parent_ug.codigo_state = MOA_UNIDADE_MANUAL
        self.logger.info("[UG{}] Entrando no estado manual. Para retornar a operação autônoma da UG é necessário intervenção manual via interface web.".format(self.parent_ug.id))

    def step(self) -> State:
        self.parent_ug.setpoint = self.parent_ug.leitura_potencia.valor
        return self

class StateIndisponivel(State):
    def __init__(self, parent_ug: UnidadeDeGeracao):
        super().__init__(parent_ug)
        self.selo = False
        self.parent_ug._next_state = self
        self.parent_ug.codigo_state = MOA_UNIDADE_INDISPONIVEL
        self.logger.warning("[UG{}] Entrando no estado indisponível. Para retornar a operação autônoma da UG é necessário intervenção manual via interface web.".format(self.parent_ug.id))

    def step(self) -> State:
        self.logger.debug("[UG{}] Etapa atual -> {}".format(self.parent_ug.id, self.parent_ug.etapa_atual))
        if self.parent_ug.etapa_atual == UNIDADE_PARADA or self.selo:
            self.selo = True
            self.parent_ug.fechar_comporta()
            if self.parent_ug.etapa_comporta == COMPORTA_FECHADA:
                self.parent_ug.acionar_trip_logico()
                self.parent_ug.acionar_trip_eletrico()
            else:
                self.logger.debug("[UG{0}] A comporta {0} deve estar completamente fechada para acionar o bloqueio da UG".format(self.parent_ug.id))
        else:
            self.parent_ug.parar()
        return self

class StateRestrito(State):
    def __init__(self, parent_ug: UnidadeDeGeracao):
        super().__init__(parent_ug)
        self.parent_ug.codigo_state = MOA_UNIDADE_RESTRITA
        self.logger.info("[UG{}] Entrando no estado restrito.".format(self.parent_ug.id))

    def step(self) -> State:
        deve_indisponibilizar = False
        condicionadores_ativos = []

        for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.parent_ug.deve_ler_condicionadores = True

        if self.parent_ug.deve_ler_condicionadores:
            for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    deve_indisponibilizar = True

            for condicionador in self.parent_ug.condicionadores:
                if condicionador.ativo and condicionador.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador)
                    deve_indisponibilizar = True
            self.parent_ug.deve_ler_condicionadores = False

        if deve_indisponibilizar:
            self.logger.warning("[UG{}] UG em modo disponível detectou condicionadores ativos, indisponibilizando UG.\nCondicionadores ativos:\n{}".format(self.parent_ug.id, [d.descr for d in condicionadores_ativos]))
            return StateIndisponivel(self.parent_ug)

        elif self.parent_ug.etapa_atual == UNIDADE_PARADA or self.selo:
            self.selo = True
            self.parent_ug.fechar_comporta()
            if self.parent_ug.etapa_comporta == COMPORTA_FECHADA:
                self.parent_ug.acionar_trip_logico()
                self.parent_ug.acionar_trip_eletrico()
            else:
                self.logger.debug("[UG{0}] A comporta {0} deve estar completamente fechada para acionar o bloqueio da UG".format(self.parent_ug.id))
        else:
            self.parent_ug.parar()
        return self

class StateDisponivel(State):
    def __init__(self, parent_ug: UnidadeDeGeracao):
        super().__init__(parent_ug)
        self.release_sinc = True
        self.release_press = True
        self.parent_ug.codigo_state = MOA_UNIDADE_DISPONIVEL
        self.logger.info("[UG{}] Entrando no estado disponível.".format(self.parent_ug.id))

    def step(self) -> State:
        self.logger.debug("[UG{}] (tentativas_de_normalizacao atual: {})".format(self.parent_ug.id, self.parent_ug.tentativas_de_normalizacao))
        deve_normalizar = False
        deve_indisponibilizar = False
        condicionadores_ativos = []
        self.parent_ug.controle_limites_operacao()

        for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
            if condicionador_essencial.ativo:
                self.parent_ug.deve_ler_condicionadores = True

        if self.parent_ug.deve_ler_condicionadores:
            for condicionador_essencial in self.parent_ug.condicionadores_essenciais:
                if condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    deve_indisponibilizar = True
                elif condicionador_essencial.ativo and condicionador_essencial.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condicionador_essencial)
                    deve_normalizar = True

            for condicionador in self.parent_ug.condicionadores:
                if condicionador.ativo and condicionador.gravidade == DEVE_INDISPONIBILIZAR:
                    condicionadores_ativos.append(condicionador)
                    deve_indisponibilizar = True
                elif condicionador.ativo and condicionador.gravidade == DEVE_NORMALIZAR:
                    condicionadores_ativos.append(condicionador)
                    deve_normalizar = True
            self.parent_ug.deve_ler_condicionadores = False

        if deve_indisponibilizar or deve_normalizar:
            self.logger.info("[UG{}] UG em modo disponível detectou condicionadores ativos.\nCondicionadores ativos:".format(self.parent_ug.id))
            for d in condicionadores_ativos:
                self.logger.warning("Desc: {}; Ativo: {}; Valor: {}; Gravidade: {}".format(d.descr, d.ativo, d.valor, d.gravidade))

        if deve_indisponibilizar:
            self.logger.warning("[UG{}] Indisponibilizando UG.".format(self.parent_ug.id))
            return StateIndisponivel(self.parent_ug)

        if deve_normalizar:
            if (self.parent_ug.tentativas_de_normalizacao > self.parent_ug.limite_tentativas_de_normalizacao):
                self.logger.warning("[UG{}] A UG estourou as tentativas de normalização, indisponibilizando UG. \n Condicionadores ativos:\n{}".format(self.parent_ug.id,[d.descr for d in condicionadores_ativos],))
                return StateIndisponivel(self.parent_ug)

            elif (self.parent_ug.ts_auxiliar - datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)).seconds > self.parent_ug.tempo_entre_tentativas:
                self.parent_ug.tentativas_de_normalizacao += 1
                self.parent_ug.ts_auxiliar = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)
                self.logger.info("[UG{}] Normalizando UG (tentativa {}/{}).".format(self.parent_ug.id,self.parent_ug.tentativas_de_normalizacao,self.parent_ug.limite_tentativas_de_normalizacao,))
                self.parent_ug.reconhece_reset_alarmes()
                return self

            else:
                return self

        else:
            self.logger.debug("[UG{}] Etapa atual: {}".format(self.parent_ug.id, self.parent_ug.etapa_atual))
            atenuacao = 0
            self.logger.debug(f"[UG{self.parent_ug.id}] Lendo condicionadores_atenuadores")
            for condicionador in self.parent_ug.condicionadores_atenuadores:
                atenuacao = max(atenuacao, condicionador.valor)
                self.logger.debug(f"[UG{self.parent_ug.id}] Atenuador \"{condicionador.descr}\" -> leitura: {condicionador.leitura.valor}-> atenucao: {atenuacao}")

            ganho = 1 - atenuacao
            aux = self.parent_ug.setpoint
            if (self.parent_ug.setpoint > self.parent_ug.setpoint_minimo) and self.parent_ug.setpoint * ganho > self.parent_ug.setpoint_minimo:
                self.parent_ug.setpoint = self.parent_ug.setpoint * ganho

            elif self.parent_ug.limpeza_grade:
                self.parent_ug.setpoint_minimo = self.parent_ug.cfg["pot_limpeza_grade"]
                self.parent_ug.setpoint = self.parent_ug.setpoint_minimo

            elif (self.parent_ug.setpoint * ganho < self.parent_ug.setpoint_minimo) and (self.parent_ug.setpoint > self.parent_ug.setpoint_minimo):
                self.parent_ug.setpoint =  self.parent_ug.setpoint_minimo

            self.logger.debug("[UG{}] SP {} * GAIN {} = {}".format(self.parent_ug.id, aux, ganho, self.parent_ug.setpoint,))

            if self.parent_ug.etapa_atual == UNIDADE_PARANDO:
                self.logger.debug("[UG{}] Unidade parando".format(self.parent_ug.id))
                if self.parent_ug.leitura_potencia < 300:
                    self.parent_ug.fechar_comporta()

                elif self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:
                    if self.parent_ug.etapa_comporta == COMPORTA_FECHADA:
                        self.parent_ug.cracking_comporta()

                    elif self.parent_ug.etapa_comporta == COMPORTA_CRACKING:
                        if not self.parent_ug.timer_press and self.release_press:
                            Thread(target=lambda: self.parent_ug.verificar_pressao()).start()
                            self.release_press = False
                        elif self.parent_ug.timer_press and not self.release_press:
                            self.parent_ug.timer_press = False
                            self.release_press = True
                            self.parent_ug.abrir_comporta()

                    elif self.parent_ug.etapa_comporta == COMPORTA_ABERTA:
                        self.parent_ug.partir()
                        self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)
                        if not self.parent_ug.timer_sinc and self.release_sinc:
                            Thread(target=lambda: self.parent_ug.verificar_partindo()).start()
                            self.release_sinc = False
                        elif self.parent_ug.timer_sinc and not self.release_sinc:
                            self.parent_ug.timer_sinc = False
                            self.timer_sinc = True
                    
                    elif self.parent_ug.etapa_comporta == COMPORTA_REMOTO:
                        self.logger.debug("[UG{0}] Comporta {0} em modo manual".format(self.parent_ug.id))
                        pass
                    
                    else:
                        self.logger.debug("[UG{0}] Comporta {0} entre etapas/etapa inconsistente".format(self.parent_ug.id))

            elif self.parent_ug.etapa_atual == UNIDADE_SINCRONIZANDO:
                self.logger.debug("[UG{}] Unidade sincronizando".format(self.parent_ug.id))
                if self.parent_ug.setpoint == 0:
                    self.logger.warning("[UG{}] A UG estava sincronizando com SP zerado, parando a UG.".format(self.parent_ug.id))
                    self.parent_ug.parar()

            elif self.parent_ug.etapa_atual == UNIDADE_PARADA:
                self.logger.debug("[UG{}] Unidade parada".format(self.parent_ug.id))
                if self.parent_ug.setpoint >= self.parent_ug.setpoint_minimo:

                    if self.parent_ug.etapa_comporta == COMPORTA_FECHADA:
                        self.parent_ug.cracking_comporta()

                    elif self.parent_ug.etapa_comporta == COMPORTA_CRACKING:
                        if not self.parent_ug.timer_press and self.release_press:
                            Thread(target=lambda: self.parent_ug.verificar_pressao()).start()
                            self.release_press = False
                        elif self.parent_ug.timer_press and not self.release_press:
                            self.parent_ug.timer_press = False
                            self.release_press = True
                            self.parent_ug.abrir_comporta()

                    elif self.parent_ug.etapa_comporta == COMPORTA_ABERTA:
                        self.parent_ug.partir()
                        self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)
                        if not self.parent_ug.timer_sinc and self.release_sinc:
                            Thread(target=lambda: self.parent_ug.verificar_partindo()).start()
                            self.release_sinc = False
                        elif self.parent_ug.timer_sinc and not self.release_sinc:
                            self.parent_ug.timer_sinc = False
                            self.timer_sinc = True
                    
                    elif self.parent_ug.etapa_comporta == COMPORTA_REMOTO:
                        self.logger.debug("[UG{0}] Comporta {0} em modo manual".format(self.parent_ug.id))
                        pass
                    
                    else:
                        self.logger.debug("[UG{0}] Comporta {0} entre etapas/etapa inconsistente".format(self.parent_ug.id))

            elif self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                self.logger.debug("[UG{}] Unidade sincronizada".format(self.parent_ug.id))
                if not self.parent_ug.aux_tempo_sincronizada:
                    self.parent_ug.aux_tempo_sincronizada = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

                elif (datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None) - self.parent_ug.aux_tempo_sincronizada).seconds >= 300:
                    self.parent_ug.tentativas_de_normalizacao = 0

                if self.parent_ug.setpoint == 0:
                    self.parent_ug.parar()
                else:
                    self.parent_ug.enviar_setpoint(self.parent_ug.setpoint)

            elif self.parent_ug.etapa_atual not in UNIDADE_LISTA_DE_ETAPAS:
                self.logger.warning("[UG{}] UG em etapa inconsistente. (etapa_atual:{})".format(self.parent_ug.id,self.parent_ug.etapa_atual,))

            if not self.parent_ug.etapa_atual == UNIDADE_SINCRONIZADA:
                self.parent_ug.aux_tempo_sincronizada = None

            return self
