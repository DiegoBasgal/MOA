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

from threading import Thread
from time import sleep, time
from datetime import datetime
from abc import abstractmethod

from src.codes import *
from src.Leituras import *
from src.Condicionadores import *
from src.abstracao_usina import *
from src.maquinas_estado.ug import *
from src.database_connector import Database
from src.field_connector import FieldConnector

logger = logging.getLogger("__main__")


class UnidadeDeGeracao:
    """
    Unidade de geração.
    Esse módulo corresponde a implementação das unidades de geração.
    """

    def __init__(self, id: int = None, cfg: dict = None, db: Database = None, con: FieldConnector = None):

        if not cfg:
            raise ValueError
        else:
            self.cfg = cfg

        if None in (db, con):
            logger.error(f"[UG-SM] Erro ao carregar parametros de conexão com banco e campo na classe. Reinciando intanciação interna.")
            self.db = Database()
            self.con = FieldConnector(cfg)
        else:
            self.db = db
            self.cfg = cfg
            self.con = con

        # Variavéis internas (não são lidas nem escritas diretamente)
        self.__id = id

        self.__codigo_state = 0
        self.__prioridade = 0
        self.__etapa_atual = 0
        self.__tempo_entre_tentativas = 0
        self.__limite_tentativas_de_normalizacao = 2
        self.__setpoint = 0
        self.__setpoint_minimo = 0
        self.__setpoint_maximo = 0
        self.__tentativas_de_normalizacao = 0

        self.__next_state = StateDisponivel(self)

        self.limpeza_grade = False
        self.aux_tempo_sincronizada = None
        self.deve_ler_condicionadores = False
        
        self.__condicionadores = []
        self.__condicionadores_essenciais = []
        self.__condicionadores_atenuadores = []
        
        self.codigo_state = self.__codigo_state

        self.ts_auxiliar = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

        self.clp_moa = ModbusClient(
            host=self.cfg['MOA_slave_ip'],
            port=self.cfg['MOA_slave_porta'],
            timeout=0.5,
            unit_id=1,
            auto_open=True
        )
        self.clp_ug1 = ModbusClient(
            host=self.cfg["UG1_slave_ip"],
            port=self.cfg["UG1_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
        )
        self.clp_ug2 = ModbusClient(
            host=self.cfg["UG2_slave_ip"],
            port=self.cfg["UG2_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
        )
        self.clp_ug3 = ModbusClient(
            host=self.cfg["UG3_slave_ip"],
            port=self.cfg["UG3_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
        )
        self.clp_sa = ModbusClient(
            host=self.cfg["USN_slave_ip"],
            port=self.cfg["USN_slave_porta"],
            timeout=0.5,
            unit_id=1,
            auto_open=True,
        )

        self.potencia_ativa_kW = LeituraModbus(
            "REG_SA_RetornosAnalogicos_Medidor_potencia_kw_mp",
            self.clp_sa,
            REG_SA_RA_PM_810_Potencia_Ativa,
            1,
            op=4,
        )


    def debug_set_etapa_atual(self, var):
        self.__etapa_atual = var

    def modbus_update_state_register(self):
        raise NotImplementedError

    def carregar_parametros(self, parametros: dict):
        """
        Carrega os parametros/vars iniciais.

        Args:
            parametros (dict): Os parametros a serem carregados
        """

        for key, val in parametros.items():
            while not key[0:1] == "__":
                key = "_" + key[:]
            setattr(self, key, val)
            logger.debug(f"[UG{self.id}] Variavél carregada: {key} = {val}.")

    def interstep(self) -> None:
        raise NotImplementedError
    
    def leituras_por_hora(self) -> None:
        raise NotImplementedError
        
    def step(self) -> None:
        """
        Função que rege a máquina de estados.

        Raises:
            e: Exceptions geradas ao executar um estado
        """
        try:
            logger.debug("")
            logger.debug(f"[UG{self.id}] Step -> (Tentativas de normalização: {self.tentativas_de_normalizacao}/{self.limite_tentativas_de_normalizacao})")
            self.interstep()
            self.__next_state = self.__next_state.step()
            self.modbus_update_state_register()

        except Exception as e:
            logger.error(f"[UG{self.id}] Erro na execução da sm. Traceback: {traceback.print_stack}")
            raise e

    def forcar_estado_disponivel(self) -> bool:
        """
        Força a máquina de estados a entrar no estado disponível na proxima execução

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.reconhece_reset_alarmes()
            sleep(1)
            self.__next_state = StateDisponivel(self)
        except Exception as e:
            logger.error(f"[UG{self.id}] Não foi possivel forcar_estado_disponivel. Traceback: {traceback.print_stack}")
            return False
        else:
            return True

    def forcar_estado_indisponivel(self) -> bool:
        """
        Força a máquina de estados a entrar no estado indisponível na proxima execução

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.__next_state = StateIndisponivel(self)
        except Exception as e:
            logger.error(f"[UG{self.id}] Não foi possivel forcar_estado_indisponivel. {traceback.print_stack}")
            return False
        else:
            return True

    def forcar_estado_manual(self) -> bool:
        """
        Força a máquina de estados a entrar no estado manual na proxima execução

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.__next_state = StateManual(self)
        except Exception as e:
            logger.error(f"[UG{self.id}] Não foi possivel forcar_estado_manual. {traceback.print_stack}")
            return False
        else:
            return True

    def forcar_estado_restrito(self) -> bool:
        """
        Força a máquina de estados a entrar no estado restrito na proxima execução

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            self.__next_state = StateRestrito(self)
        except Exception as e:
            logger.error(f"[UG{self.id}] Não foi possivel forcar_estado_restrito. {traceback.print_stack}")
            return False
        else:
            return True

    @property
    def id(self) -> int:
        """
        Id da unidade de deração

        Returns:
            int: id
        """
        return self.__id

    @property
    def prioridade(self) -> int:
        """
        Prioridade da unidade de deração

        Returns:
            int: id
        """
        return self.__prioridade

    @prioridade.setter
    def prioridade(self, var) -> None:
        self.__prioridade = var

    @property
    def condicionadores_essenciais(self) -> list[CondicionadorBase]:
        """
        Lista de condicionadores (objetos) essenciais que deverão ser lidos SEMPRE

        Returns:
            list: lista de condicionadores (objetos)
        """
        return self.__condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: list[CondicionadorBase]):
        self.__condicionadores_essenciais = var

    @property
    def condicionadores(self) -> list[CondicionadorBase]:
        """
        Lista de condicionadores (objetos) que deverão ser lidaos no caso de uma chamada

        Returns:
            list: lista de condicionadores (objetos)
        """
        return self.__condicionadores

    @condicionadores.setter
    def condicionadores(self, var: list([CondicionadorBase])):
        self.__condicionadores = var

    @property
    def condicionadores_atenuadores(self) -> list([CondicionadorBase]):
        """
        Lista de condicionadores_atenuadores (objetos) relacionados com a unidade de geração

        Returns:
            list: lista de condicionadores_atenuadores (objetos)
        """
        return self.__condicionadores_atenuadores

    @condicionadores_atenuadores.setter
    def condicionadores_atenuadores(self, var: list([CondicionadorBase])):
        self.__condicionadores_atenuadores = var

    @property
    def etapa_atual(self) -> int:
        """
        Etapa atual, esta chamada deve recuperar a informação diratamente da unidade de geração por meio dos drivers de comunicação

        Verifique a lista UNIDADE_LISTA_DE_ETAPAS para as constantes retornadas por esta chamda.
        Returns:
            int: ETAPA_ATUAL
        """
        logger.debug(f"[UG{self.id}] etapa_atual = __etapa_atual <- {self.__etapa_atual}")
        return self.__etapa_atual

    @property
    def tempo_entre_tentativas(self) -> int:
        """
        Limite mínimo de tempo entre tentaivas de normalização da unidade de geração
        Este valor deve ser carregado com o restante dos parâmetros da unidade de geração utilizando a função carregar_parametros()
        Valor recomendado: 30 segundos

        Returns:
            int: tempo_entre_tentativas [s]
        """
        return self.__tempo_entre_tentativas

    @property
    def limite_tentativas_de_normalizacao(self) -> int:
        """
        Limite máximo do número de tentativas de normalização da unidade de geração
        Este valor deve ser carregado com o restante dos parâmetros da unidade de geração utilizando a função carregar_parametros()
        Valor recomendado: 3 tentativas

        Returns:
            int: limite_tentativas_de_normalizacao
        """
        return self.__limite_tentativas_de_normalizacao

    @property
    def setpoint(self) -> int:
        """
        Setpoint da unidade de geração

        Quando escrito:
            Caso o setpoint estiver abixo do limte, ele retornará 0 kW.
            Caso o setpoint estiver acima do limte, ele retornará o limite.

        Returns:
            int: setpoint [kW]
        """
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
        """
        Setpoint mínimo da unidade de geração'
        Este valor deve ser carregado com o restante dos parâmetros da unidade de geração utilizando a função carregar_parametros()

        Returns:
            int: setpoint_minimo [kW]
        """
        return self.__setpoint_minimo

    @setpoint_minimo.setter
    def setpoint_minimo(self, var: int):
        self.__setpoint_minimo = var

    @property
    def setpoint_maximo(self) -> int:
        """
        Setpoint máximo da unidade de geração
        Este valor deve ser carregado com o restante dos parâmetros da unidade de geração utilizando a função carregar_parametros()

        Returns:
            int: setpoint_maximo [kW]
        """
        return self.__setpoint_maximo

    @setpoint_maximo.setter
    def setpoint_maximo(self, var: int):
        self.__setpoint_maximo = var

    @property
    def tentativas_de_normalizacao(self) -> int:
        """
        Contador de tentativas de normalização realizadas

        Returns:
            int: tentativas_de_normalizacao ( sempre >= 0 )
        """
        return self.__tentativas_de_normalizacao

    @tentativas_de_normalizacao.setter
    def tentativas_de_normalizacao(self, var: int):
        self.__tentativas_de_normalizacao = var
    
    @property
    def manual(self) -> bool:
        return isinstance(self.__next_state, StateManual)

    @property
    def disponivel(self) -> bool:
        """
        Retrofit
        """
        return isinstance(self.__next_state, StateDisponivel)

    @property
    def codigo_state(self) -> int:
        return self.__codigo_state

    @codigo_state.setter
    def codigo_state(self, var) -> int:
        self.__codigo_state = var

    def partir(self) -> bool:
        """
        Envia o comando de parida da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            logger.info(f"[UG{self.id}] Enviando comando de partida.")
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return True

    def parar(self) -> bool:
        """
        Envia o comando de parada da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            logger.info(f"[UG{self.id}] Enviando comando de parada.")
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return True

    def reconhece_reset_alarmes(self) -> bool:
        """
        Envia o comando de reconhece e reset dos alarmes da unidade de geração para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:
            logger.debug(f"[UG{self.id}] Enviando comando de reconhecer e resetar alarmes.")
            raise NotImplementedError
        except:
            #! TODO Tratar exceptions
            return False
        else:
            return True

    def enviar_setpoint(self, setpoint_kw: int) -> bool:
        """
        Envia o setpoint desejado para o CLP via rede

        Returns:
            bool: True se sucesso, Falso caso contrário
        """
        try:

            if self.limpeza_grade:
                self.setpoint_minimo = self.cfg["pot_limpeza_grade"]
            else:
                self.setpoint_minimo = self.cfg["pot_minima"]
            self.setpoint_maximo = self.cfg[f"pot_maxima_ug{self.id}"]

            logger.debug(f"[UG{self.id}] Enviando setpoint {int(self.setpoint)} kW.")
            response = False
            if self.setpoint > 1:
                response = self.clp_ug3.write_single_coil(UG[f"REG_UG{self.id}_CD_ResetGeral"], 1)
                response = self.clp_ug3.write_single_coil(UG[f"REG_UG{self.id}_CD_RV_RefRemHabilita"], 1)
                response = self.clp_ug3.write_single_register(UG[f"REG_UG{self.id}_SA_SPPotAtiva"], self.setpoint)

        except:
            #! TODO Tratar exceptions
            return False
        else:
            return response
        s