import sys
import pytz
import logging
import threading
import traceback
import subprocess

import src.mensageiro.dict as vd

from time import sleep, time
from datetime import  datetime, timedelta
from pyModbusTCP.client import ModbusClient

from src.ocorrencias import *
from src.funcoes.leitura import  *
from src.dicionarios.reg import *
from src.dicionarios.const import *
from src.maquinas_estado.ug import *

from src.mensageiro.voip import Voip
from src.banco_dados import BancoDados
from src.conector import ClientesUsina
from src.agendamentos import Agendamentos
from src.unidade_geracao import UnidadeGeracao
from src.Condicionadores import CondicionadorBase

logger = logging.getLogger("logger")

class Usina:
    def __init__(self, cfg: dict=None):

        # VERIFICAÇÃO DE ARGUMENTOS

        if None in (cfg):
            raise ValueError("[USN] Não foi possível carregar os arquivos de configuração (\"cfg.json\").")
        else:
            self.cfg = cfg


        # INCIALIZAÇÃO DE OBJETOS DA USINA

        self.db = BancoDados("MOA-SEB")
        self.clp = ClientesUsina.clp
        self.oco = OcorrenciasUsn(self.clp, self.db)
        self.agn = Agendamentos(self.cfg, self.db, self)

        self.ug = UnidadeGeracao(1, self.cfg, self.db)

        CondicionadorBase.ug = self.ug

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__potencia_ativa_kW: "LeituraModbus" = LeituraModbus(
            "[USN] Leitura Potência Medidor",
            self.clp["SA"],
            1,
            op=4,
        )
        self.__tensao_rs: "LeituraModbus" = LeituraModbus(
            "[USN] Tensão RS",
            self.clp["SA"],
            100,
            op=4,
        )
        self.__tensao_st: "LeituraModbus" = LeituraModbus(
            "[USN] Tensão ST",
            self.clp["SA"],
            100,
            op=4,
        )
        self.__tensao_tr: "LeituraModbus" = LeituraModbus(
            "[USN] Tensão TR",
            self.clp["SA"],
            100,
            op=4,
        )


        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS

        self._nv_montante: "LeituraModbus" = LeituraModbus(
            "[USN] Nível Montante",
            self.clp["TDA"],
            1 / 10000,
            op=4,
        )

        self._pid_inicial: "int" = -1
        self._pot_alvo_anterior: "int" = -1
        self._tentativas_normalizar: "int" = 0

        self._modo_autonomo: "bool" = False


        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.estado_moa: "int" = 0
        self.status_tensao: "int" = 0

        self.pot_disp: "int" = 0

        self.erro_nv: "int" = 0
        self.erro_nv_anterior: "int" = 0
        self.nv_montante_recente: "int" = 0

        self.controle_p: "float" = 0
        self.controle_i: "float" = 0
        self.controle_d: "float" = 0
        self.pid_inicial: "float" = -1

        self.tentar_normalizar: "bool" = True

        self.TDA_Offline: "bool" = False
        self.borda_emerg: "bool" = False
        self.db_emergencia: "bool" = False
        self.clp_emergencia: "bool" = False
        self.normalizar_forcado: "bool" = False
        self.aguardando_reservatorio: "bool" = False

        self.nv_montante_recentes: "list" = []

        self.ultima_tentativa_norm: "datetime" = self.get_time()


        # FINALIZAÇÃO DO __INIT__

        logger.debug("")

        self.ug.iniciar_ultimo_estado()

        self.ler_valores()
        self.controlar_inicializacao()
        self.normalizar_usina()
        self.escrever_valores()


    # Property -> VARIÁVEIS PRIVADAS

    @property
    def potencia_ativa(self) -> int:
        # PROPRIEDADE -> Retrona a potência geral atual da Usina.

        return self.__potencia_ativa_kW.valor

    @property
    def nv_montante(self) -> float:
        # PROPRIEDADE -> Retrona a leitura de nível montante da Tomada da Água.

        return self._nv_montante.valor


    # Property/Setter -> VARIÁVEIS PROTEGIDAS

    @property
    def modo_autonomo(self) -> bool:
        # PROPRIEDADE -> Retrona o modo do MOA.

        return self._modo_autonomo

    @modo_autonomo.setter
    def modo_autonomo(self, var: bool) -> None:
        # SETTER -> Atribui o novo valor de modo do MOA e atualiza o Banco.

        self._modo_autonomo = var
        self.db.update_modo_moa(self._modo_autonomo)

    @property
    def tentativas_normalizar(self) -> int:
        # PROPRIEDADE -> Retrona o número de tentativas de normalização da Usina.

        return self._tentativas_normalizar

    @tentativas_normalizar.setter
    def tentativas_normalizar(self, var: int) -> None:
        # SETTER -> Atribui o novo valor de tentativas de normalização da Usina.

        self._tentativas_normalizar = var

    @property
    def _pot_alvo_anterior(self) -> float:
        # PROPRIEDADE -> Retrona o valor de potência alvo anterior da Usina.

        return self._potencia_alvo_anterior

    @_pot_alvo_anterior.setter
    def _pot_alvo_anterior(self, var):
        # SETTER -> Atribui o novo valor de de potência alvo anterior da Usina.

        self._potencia_alvo_anterior = var


    # FUNÇÕES

    @staticmethod
    def get_time() -> datetime:
        """
        Função para obter data e hora atual.
        """

        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    ### FUNÇÕES DE CONTROLE DE RESET E NORMALIZAÇÃO

    def acionar_emergencia(self) -> None:
        """
        Função para acionamento de emergência geral da Usina. Envia o comando de
        emergência via supervisório para todos os CLPs.
        """

        logger.warning("[USN] Acionando Emergência.")
        self.db_emergencia = True
        self.clp_emergencia = True

        try:
            sleep(5)

        except Exception:
            logger.error(f"[USN] Houve um erro ao acionar a Emergência.")
            logger.debug(traceback.format_exc())

    def resetar_emergencia(self) -> None:
        """
        Função para reset geral da Usina. Envia o comando de reset para todos os
        CLPs.
        """

        try:
            logger.debug("[USN] Reset geral")

            self.fechar_dj_linha() if not d.glb["TDA_Offline"] else logger.debug("[USN] CLP TDA Offline, não há como realizar o reset geral")

        except Exception:
            logger.error(f"[USN] Houve um erro ao realizar o Reset Geral.")
            logger.debug(traceback.format_exc())

    def normalizar_usina(self) -> bool:
        """
        Função para normalização de ocorrências da Usina.

        Verifica primeiramente a tensão da linha.
        Caso a tenão esteja dentro dos limites, passa a verificar se a
        normalização foi executada à pouco tempo, se foi, avisa o operador,
        senão, passa a chamar as funções de reset geral.
        """


        logger.debug("[USN] Normalizando...")
        logger.debug(f"[USN] Última tentativa de normalização:   {self.ultima_tentativa_norm.strftime('%d-%m-%Y %H:%M:%S')}")
        logger.debug(f"[USN] Tensão na linha:                    RS -> \"{self.__tensao_rs.valor:2.1f} kV\" | ST -> \"{self.__tensao_st.valor:2.1f} kV\" | TR -> \"{self.__tensao_tr.valor:2.1f} kV\"")

        if not self.verificar_tensao():
            return False

        elif (self.tentar_normalizar and (self.get_time() - self.ultima_tentativa_norm).seconds >= 60 * self.tentativas_normalizar) or self.normalizar_forcado:
            self.ultima_tentativa_norm = self.get_time()
            self.tentativas_normalizar += 1
            self.db_emergencia = False
            self.clp_emergencia = False
            self.resetar_emergencia()
            self.db.update_remove_emergencia()
            return True

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minuto atrás")

    def fechar_dj_linha(self) -> bool:
        """
        Função para acionamento do comando de fechamento do Disjuntor 52L (Linha).

        Primeiramente, chama a função de verificação de bloqueios de fechamento,
        caso não haja nenhuma condição, envia o comando para o CLP - SA.
        """

        try:
            if self.verificar_falha_dj_linha():
                return False
            else:
                response = self.clp["SA"].write_single_coil(REG[""], [1])
                return response

        except Exception:
            logger.error(f"[USN] Houver um erro ao fechar o Disjuntor de Linha.")
            logger.debug(traceback.format_exc())

    def verificar_falha_dj_linha(self):
        """
        Função para verificação das condições de fechamento do Disjuntor 52L (Linha).
        """

        flag = 0

        # TODO -> adicionar condições

        if flag > 0:
            logger.warning(f"[USN] Foram detectados bloqueios ao fechar o Dj52L. Número de bloqueios: \"{flag}\".")
            return True
        else:
            return False

    def verificar_tensao(self) -> bool:
        """
        Função para verificação de limites de tensão da linha de transmissão.
        """

        try:
            if (TENSAO_LINHA_BAIXA < self.__tensao_rs.valor < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.__tensao_st.valor < TENSAO_LINHA_ALTA) \
                and (TENSAO_LINHA_BAIXA < self.__tensao_tr.valor < TENSAO_LINHA_ALTA):
                return True
            else:
                logger.warning("[USN] Tensão da linha fora do limite.")
                return False

        except Exception:
            logger.error(f"[USN] Houve um erro ao realizar a verificação da tensão na linha.")
            logger.debug(traceback.format_exc())
            return False

    def aguardar_tensao(self) -> bool:
        """
        Função para normalização após a queda de tensão da linha de transmissão.

        Primeiramente, caso haja uma queda, será chamada a função com o timer de
        espera com tempo pré determinado. Caso a tensão seja reestabelecida
        dentro do limite de tempo, é chamada a funcão de normalização da Usina.
        Se o timer passar do tempo, é chamada a função de acionamento de emergência
        e acionado chamada de emergência por Voip.
        """

        if self.status_tensao == TENSAO_VERIFICAR:
            self.status_tensao = TENSAO_AGUARDO
            logger.debug("[USN] Iniciando o timer para a normalização da tensão na linha.")
            threading.Thread(target=lambda: self.acionar_temporizador_tensao(600)).start()

        elif self.status_tensao == TENSAO_REESTABELECIDA:
            logger.info("[USN] Tensão na linha reestabelecida.")
            self.status_tensao = TENSAO_VERIFICAR
            return True

        elif self.status_tensao == TENSAO_FORA:
            logger.critical("[USN] Não foi possível reestabelecer a tensão na linha. Acionando emergência")
            self.status_tensao = TENSAO_VERIFICAR
            return False

        else:
            logger.debug("[USN] A tensão na linha ainda está fora.")

    def acionar_temporizador_tensao(self, delay) -> None:
        """
        Função de temporizador para espera de normalização de tensão da linha de
        transmissão.
        """

        while time() <= time() + delay:
            if self.verificar_tensao():
                self.status_tensao = TENSAO_REESTABELECIDA
                return
            sleep(time() - (time() - 15))
        self.status_tensao = TENSAO_FORA


    ### FUNÇÕES DE CONTROLE DE OPERAÇÃO:

    def leitura_periodica(self):
        """
        Função de temporizador com leituras para alertas de manutenção.

        Chama os métodos de leitura de objetos da Usina e Unidades de Geração.
        Caso haja alguma leitura fora do esperado, é enviado o alerta via
        WhatsApp ou Voip.
        """

        try:
            logger.debug("[USN] Iniciando o timer de leitura periódica...")
            while True:
                self.ug.oco.leitura_temporizada()
                self.oco.leitura_temporizada()

                if True in (vd.voip_dict[r][0] for r in vd.voip_dict):
                    Voip.acionar_chamada()
                    pass

                sleep(max(0, (time() + 1800) - time()))

        except Exception:
            logger.error(f"[USN] Houve um erro ao executar o timer de leituras periódicas.")
            logger.debug(traceback.format_exc())

    def controlar_inicializacao(self) -> None:
        """
        Função para ajustes na inicialização do MOA. Essa função é executada apenas
        uma vez.
        """

        self.__split1 = True if self.ug.etapa_atual == UG_SINCRONIZADA else False

        self.controle_ie = self.ug.leitura_potencia / self.cfg["pot_maxima_alvo"]

        self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG1"], [0])

    def controlar_reservatorio(self) -> int:
        """
        Função para controle de níveis do reservatório.

        Primeiramente aciona a função de reset da Tomada da Água (para desabilitar
        mecanismos como controle de nível e religamento do Dj 52L). Logo em seguida,
        realiza a leitura de nível montante e determina qual condição entrar. Se
        o nível estiver acima do máximo, verifica se atingiu o Maximorum. Nesse
        caso é acionada a emergência da Usina, porém se for apenas vertimento,
        distribui a potência máxima para as Unidades.
        Caso a leitura retornar que o nível está abaixo do mínimo, verifica antes
        se atingiu o fundo do reservatório, nesse caso é acionada a emergência.
        Se o valor ainda estiver acima do nível de fundo, será distribuída a
        potência 0 para todas as Unidades e aciona a espera pelo nível.
        Caso a leitura esteja dentro dos limites normais, é chamada a função para
        calcular e distribuir a potência para as Unidades.
        """

        if self.nv_montante >= self.cfg["nv_maximo"]:
            logger.debug("[USN] Nível montante acima do máximo")

            if self.nv_montante_recente >= NIVEL_MAXIMORUM:
                logger.critical(f"[USN] Nível montante ({self.nv_montante_recente:3.2f}) atingiu o maximorum!")
                return NV_FLAG_EMERGENCIA
            else:
                self.controle_i = 0.5
                self.controle_ie = 0.5
                self.ajustar_potencia(self.cfg["pot_maxima_usina"])
                self.ug.step()

        elif self.nv_montante <= self.cfg["nv_minimo"] and not self.aguardando_reservatorio:
            logger.debug("[USN] Nível montante abaixo do mínimo")
            self.aguardando_reservatorio = True
            self.distribuir_potencia(0)

            self.ug.step()

            if self.nv_montante_recente <= NIVEL_FUNDO_RESERVATORIO:
                if not ClientesUsina.ping(d.ips["TDA_ip"]):
                    d.glb["TDA_Offline"] = True
                    return NV_FLAG_NORMAL
                else:
                    logger.critical(f"[USN] Nível montante ({self.nv_montante_recente:3.2f}) atingiu o fundo do reservatorio!")
                    return NV_FLAG_EMERGENCIA

        elif self.aguardando_reservatorio:
            if self.nv_montante >= self.cfg["nv_alvo"]:
                logger.debug("[USN] Nível montante dentro do limite de operação")
                self.aguardando_reservatorio = False

        else:
            self.controlar_potencia()

            self.ug.step()

        return NV_FLAG_NORMAL

    def controlar_potencia(self) -> None:
        logger.debug(f"[USN] NÍVEL -> Alvo:                      {self.cfg['nv_alvo']:0.3f}")
        logger.debug(f"[USN]          Leitura:                   {self.nv_montante_recente:0.3f}")

        self.controle_p = self.cfg["kp"] * self.erro_nv

        if self._pid_inicial == -1:
            self.controle_i = max(min(self.controle_ie - self.controle_p, 0.8), 0)
            self._pid_inicial = 0
        else:
            self.controle_i = max(min((self.cfg["ki"] * self.erro_nv) + self.controle_i, 0.8), 0)
            self.controle_d = self.cfg["kd"] * (self.erro_nv - self.erro_nv_anterior)

        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))

        logger.debug("")
        logger.debug(f"[USN] PID   -> P + I + D:                 {saida_pid:0.3f}")
        logger.debug(f"[USN] P:                                  {self.controle_p:0.3f}")
        logger.debug(f"[USN] I:                                  {self.controle_i:0.3f}")
        logger.debug(f"[USN] D:                                  {self.controle_d:0.3f}")

        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)
        logger.debug(f"[USN] IE:                                 {self.controle_ie:0.3f}")
        logger.debug(f"[USN] ERRO:                               {self.erro_nv}")
        logger.debug("")

        if self.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if self.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"],), self.cfg["pot_minima"],)
        logger.debug(f"[USN] Potência alvo:                      {pot_alvo:0.3f}")

        pot_alvo = self.ajustar_potencia(pot_alvo)

    def verificar_disponibilidade_unidade(self) -> UnidadeGeracao:
        ls = self.ug if self.ug.disponivel and not self.ug.etapa_atual == UG_PARANDO else None
        return ls

    def ajustar_potencia(self, pot_alvo) -> None:
        if self._pot_alvo_anterior == -1:
            self._pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            self.ug.setpoint = 0
            return 0

        pot_medidor = self.potencia_ativa

        logger.debug(f"[USN] Potência no medidor:                {self.potencia_ativa:0.3f}")

        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])

        pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

        if pot_medidor > self.cfg["pot_maxima_alvo"] * 0.97 and pot_alvo >= self.cfg["pot_maxima_alvo"]:
            pot_alvo = self._pot_alvo_anterior * (1 - 0.25 * ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))

        self._pot_alvo_anterior = pot_alvo

        logger.debug(f"[USN] Potência alvo pós ajuste:           {pot_alvo:0.3f}")
        self.distribuir_potencia(pot_alvo)

    def ajustar_ie_padrao(self) -> int:
        """
        Função para ajustar o valor do IE.
        """

        return self.ug.leitura_potencia / self.cfg["pot_maxima_alvo"]

    def distribuir_potencia(self, pot_alvo) -> None:
        ug: "UnidadeGeracao" = self.verificar_disponibilidade_unidade()

        if ug is None:
            return

        logger.debug(f"[USN] Distribuindo:                       {pot_alvo:0.3f}")

        sp = pot_alvo / self.cfg["pot_maxima_usina"]

        self.__split1 = True if sp > (0) else self.__split1
        self.__split1 = False if sp < (self.cfg["pot_minima"] / self.cfg["pot_maxima_usina"]) else self.__split1

        logger.debug(f"[USN] SP Geral:                           {sp}")

        ug.setpoint = sp * ug.setpoint_maximo
        logger.debug(f"[UG{ug.id}] SP    <-                            {int(ug.setpoint)}")


    ### FUNÇÕES DE CONTROLE DE DADOS:

    def ler_valores(self) -> None:
        """
        Função para leitura e atualização de parâmetros de operação através de
        Banco de Dados da Interface WEB.
        """

        ClientesUsina.ping_clients()
        self.atualizar_valores_montante()

        parametros = self.db.get_parametros_usina()
        self.atualizar_valores_cfg(parametros)
        self.atualizar_valores_banco(parametros)

        self.ug.oco.atualizar_limites_condicionadores(parametros)

        self.heartbeat()

    def atualizar_valores_montante(self) -> None:
        """
        Função para atualização de valores anteriores e erro de nível montante.
        """

        self.nv_montante_recente = self.nv_montante
        self.erro_nv_anterior = self.erro_nv
        self.erro_nv = self.nv_montante_recente - self.cfg["nv_alvo"]

    def atualizar_valores_banco(self, parametros) -> None:
        """
        Função para atualização de valores de Banco de Dados.
        """

        try:
            if int(parametros["emergencia_acionada"]) == 1:
                logger.debug("[USN] Emergência acionada!")
                self.db_emergencia = True
            else:
                self.db_emergencia = False

            if int(parametros["modo_autonomo"]) == 1 and not self.modo_autonomo:
                self.modo_autonomo = True
                logger.debug(f"[USN] Modo autônomo:                      \"{'Ativado'}\"")
            elif int(parametros["modo_autonomo"]) == 0 and self.modo_autonomo:
                self.modo_autonomo = False
                logger.debug(f"[USN] Modo autônomo:                      \"{'Desativado'}\"")

        except Exception:
            logger.error(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados.")
            logger.debug(traceback.format_exc())

    def atualizar_valores_cfg(self, parametros) -> None:
        """
        Função para atualização de valores de operação do arquivo cfg.json.
        """

        self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
        self.cfg["nv_minimo"] = float(parametros["nv_minimo"])
        self.cfg["nv_maximo"] = float(parametros["nv_maximo"])

        self.cfg["kp"] = float(parametros["kp"])
        self.cfg["ki"] = float(parametros["ki"])
        self.cfg["kd"] = float(parametros["kd"])
        self.cfg["kie"] = float(parametros["kie"])
        self.cfg["cx_kp"] = float(parametros["cx_kp"])
        self.cfg["cx_ki"] = float(parametros["cx_ki"])
        self.cfg["cx_kie"] = float(parametros["cx_kie"])
        self.cfg["press_cx_alvo"] = float(parametros["press_cx_alvo"])

        self.cfg["pot_maxima_alvo"] = float(parametros["pot_nominal"])
        self.cfg["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])
        self.cfg["pot_maxima_usina"] = float(parametros["pot_nominal_ug"])
        self.cfg["margem_pot_critica"] = float(parametros["margem_pot_critica"])

    def escrever_valores(self) -> None:
        """
        Função para escrita de valores de operação nos Bancos do módulo do Django
        e Debug.
        """

        try:
            v_params = [
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                1 if self.aguardando_reservatorio else 0,
                self.nv_montante if not d.glb["TDA_Offline"] else 0,
                self.ug.leitura_potencia,
                self.ug.setpoint,
                self.ug.codigo_state
            ]
            self.db.update_valores_usina(v_params)

        except Exception:
            logger.error(f"[USN] Houve um erro ao gravar os parâmetros da Usina no Banco.")
            logger.debug(traceback.format_exc())

        try:
            v_params = [
                time(),
                self.ug.codigo_state
            ]
            self.db.update_controle_estados(v_params)

        except Exception:
            logger.error(f"[USN] Houve um erro ao gravar os estados das Unidades no Banco.")
            logger.debug(traceback.format_exc())

        try:
            v_debug = [
                time(),
                1 if self.modo_autonomo else 0,
                self.nv_montante_recente,
                self.erro_nv,
                self.ug.setpoint,
                self.ug.leitura_potencia,
                self.ug.codigo_state,
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"]
            ]
            self.db.update_debug(v_debug)

        except Exception:
            logger.error(f"[USN] Houve um erro ao gravar os parâmetros debug no Banco.")
            logger.debug(traceback.format_exc())

    def heartbeat(self) -> None:
        """
        Função para controle do CLP - MOA.

        Esta função tem como objetivo enviar comandos de controle/bloqueio para
        os CLPs da Usina e também, ativação/desativação do MOA através de chaves
        seletoras no painel do Sistema Auxiliar.
        """

        try:
            self.clp["MOA"].write_single_coil(REG["PAINEL_LIDO"], [1])
            self.clp["MOA"].write_single_coil(REG["MOA_OUT_MODE"], [1 if self._modo_autonomo else 0])
            self.clp["MOA"].write_single_register(REG["MOA_OUT_STATUS"], self.estado_moa)

            self.ug.atualizar_modbus_moa()

            if self.modo_autonomo:
                self.clp["MOA"].write_single_coil(REG["MOA_OUT_EMERG"], [1 if self.clp_emergencia else 0])
                self.clp["MOA"].write_single_register(REG["MOA_OUT_TARGET_LEVEL"], int((self.cfg["nv_alvo"] - 0) * 1000))
                self.clp["MOA"].write_single_register(REG["MOA_OUT_SETPOINT"], int(self.ug.setpoint))

                if self.clp["MOA"].read_coils(REG["MOA_IN_EMERG"]) == 1 and not self.borda_emerg:
                    self.borda_emerg = True
                    self.ug.oco.verificar_condicionadores(self.ug)

                elif self.clp["MOA"].read_coils(REG["MOA_IN_EMERG"]) == 0 and self.borda_emerg:
                    self.borda_emerg = False

                if self.clp["MOA"].read_coils(REG["MOA_IN_EMERG_UG1"]) == 1:
                    self.ug.oco.verificar_condicionadores(self.ug)

                if self.clp["MOA"].read_coils(REG["MOA_IN_HABILITA_AUTO"]) == 1:
                    self.clp["MOA"].write_single_coil(REG["MOA_IN_HABILITA_AUTO"], [1])
                    self.clp["MOA"].write_single_coil(REG["MOA_IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = True

                if self.clp["MOA"].read_coils(REG["MOA_IN_DESABILITA_AUTO"]) == 1:
                    self.clp["MOA"].write_single_coil(REG["MOA_IN_HABILITA_AUTO"], [0])
                    self.clp["MOA"].write_single_coil(REG["MOA_IN_DESABILITA_AUTO"], [1])
                    self.modo_autonomo = False

                if self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG1"]) == 1:
                    self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG1"], [1])

                elif self.clp["MOA"].read_coils(REG["MOA_OUT_BLOCK_UG1"]) == 0:
                    self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG1"], [0])

            elif not self.modo_autonomo:
                if self.clp["MOA"].read_coils(REG["MOA_IN_HABILITA_AUTO"]) == 1:
                    self.clp["MOA"].write_single_coil(REG["MOA_IN_HABILITA_AUTO"], [1])
                    self.clp["MOA"].write_single_coil(REG["MOA_IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = True

                self.clp["MOA"].write_single_coil(REG["MOA_OUT_EMERG"], [0])
                self.clp["MOA"].write_single_coil(REG["MOA_OUT_BLOCK_UG1"], [0])
                self.clp["MOA"].write_single_register(REG["MOA_OUT_SETPOINT"], int(0))
                self.clp["MOA"].write_single_register(REG["MOA_OUT_TARGET_LEVEL"], int(0))

        except Exception:
            logger.error(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA.")
            logger.debug(traceback.format_exc())