__version__ = "0.2"
__authors__ = "Lucas Lavratti", " Henrique Pfeifer"
__credits__ = ["Diego Basgal", ...]
__description__ = "Este módulo corresponde a implementação da operação da Usina."

import os
import sys
import json
import pytz
import logging
import traceback

import dicionarios.dict as dct

from time import sleep, time
from datetime import  datetime, timedelta

from condicionador import *
from dicionarios.reg import *
from dicionarios.const import *

from comporta import Comporta
from mensageiro.voip import Voip
from banco_dados import BancoDados
from unidade_geracao import UnidadeGeracao
from condicionador import CondicionadorBase

from funcoes.leitura import *

from bay import Bay as BAY
from subestacao import Subestacao as SE
from tomada_agua import TomadaAgua as TDA
from conector import ClientesUsina as cli
from servico_auxiliar import ServicoAuxiliar as SA
from funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("__main__")

class Usina:
    def __init__(self, cfg: "dict" = None):

        # VERIFICAÇÃO DE ARGUMENTOS

        if None in (cfg):
            raise ValueError("[USN] Não foi possível carregar os arquivos de configuração (\"cfg.json\").")
        else:
            self.cfg = cfg

        self.clp = cli.clp
        self.rele = cli.rele


        # INCIALIZAÇÃO DE OBJETOS DA USINA

        self.ug1: "UnidadeGeracao" = UnidadeGeracao(self, 1)
        self.ug2: "UnidadeGeracao" = UnidadeGeracao(self, 2)

        self.ugs: "list[UnidadeGeracao]" = [self.ug1, self.ug2]

        self.cp: "dict[str, Comporta]" = {}
        self.cp["CP1"] = Comporta(1)
        self.cp["CP2"] = Comporta(2)


        # ATRIBUIÇÃO DE VARIÀVEIS
        # PRIVADAS
        self.__split1: "bool" = False
        self.__split2: "bool" = False

        # PROTEGIDAS
        self._pid_inicial: "int" = -1
        self._tentativas_normalizar: "int" = 0

        self._pot_alvo_anterior: "float" = -1

        self._modo_autonomo: "bool" = False

        # PÚBLICAS
        self.estado_moa: "int" = 0

        self.pot_disp: "int" = 0
        self.ug_operando: "int" = 0

        self.modo_de_escolha_das_ugs: "int" = 0

        self.aguardando_reservatorio: "int" = 0

        self.controle_p: "float" = 0
        self.controle_i: "float" = 0
        self.controle_d: "float" = 0

        self.bd_emergencia: "bool" = False
        self.clp_emergencia: "bool" = False
        self.borda_emergencia: "bool" = False
        self.normalizar_forcado: "bool" = False


        # FINALIZAÇÃO DO __INIT__

        self.ler_valores()
        self.normalizar_inicializacao()
        self.normalizar_usina()
        self.escrever_valores()


    # PROPRIEDADES/GETTERS

    @property
    def modo_autonomo(self) -> "bool":
        return self._modo_autonomo

    @modo_autonomo.setter
    def modo_autonomo(self, var: "bool") -> "None":
        self._modo_autonomo = var
        BancoDados.update_modo_moa(var)

    @property
    def tentativas_normalizar(self) -> "int":
        return self._tentativas_normalizar

    @tentativas_normalizar.setter
    def tentativas_normalizar(self, var: "int") -> "None":
        self._tentativas_normalizar = var


    # FUNÇÕES DE CONTROLE E NORMALIZAÇÃO DA OPERAÇÃO

    @staticmethod
    def get_time() -> "datetime":
        """
        Função para obter data e hora atual.
        """

        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

    def resetar_emergencia(self) -> "None":
        """
        Função para reset geral da Usina. Envia o comando de reset para todos os
        CLPs.
        """

        logger.info("[USN] Acionando reset de emergência.")
        logger.debug("[USN] Bay resetado.") if BAY.resetar_emergencia() else logger.info("[USN] Reset de emergência do Bay falhou.")
        logger.debug("[USN] Subestação resetada.") if SE.resetar_emergencia() else logger.info("[USN] Reset de emergência da subestação falhou.")
        logger.debug("[USN] Tomada da Água resetada.") if TDA.resetar_emergencia else logger.info("[USN] Reset de emergência da Tomada da Água falhou.")
        logger.debug("[USN] Serviço Auxiliar resetado.") if SA.resetar_emergencia() else logger.info("[USN] Reset de emergência do serviço auxiliar falhou.")

    def acionar_emergencia(self) -> "bool":
        """
        Função para acionamento de emergência geral da Usina.

        Envia o comando de parada de emergência para as Unidades.
        """

        self.db_emergencia = True
        self.clp_emergencia = True

        try:
            [EMB.escrever_bit(self.clp[f"UG{ug.id}"], REG_CLP["UG"][f"UG{ug.id}_CMD_PARADA_EMERGENCIA"], bit=4, valor=1) for ug in self.ugs]
            sleep(5)
            [EMB.escrever_bit(self.clp[f"UG{ug.id}"], REG_CLP["UG"][f"UG{ug.id}_CMD_PARADA_EMERGENCIA"], bit=4, valor=0) for ug in self.ugs]

        except Exception:
            logger.error(f"[USN] Houve um erro ao executar o comando de Emergência.")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")
            return False

    def normalizar_inicializacao(self) -> "None":
        """
        Funçao para ajustar variáveis de cálculos de controle de operação, na inicialização
        da Classe da Usina.
        """

        for ug in self.ugs:
            if ug.etapa_atual == UG_SINCRONIZADA:
                self.ug_operando += 1

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False

        self.controle_ie = self.ajustar_ie_padrao()

        self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["MOA_OUT_BLOCK_UG1"], [0])
        self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["MOA_OUT_BLOCK_UG2"], [0])
        self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["MOA_OUT_BLOCK_UG3"], [0])

    def normalizar_usina(self) -> "int":
        """
        Função para normalização de ocorrências da Usina.

        Verifica primeiramente a tensão da linha.
        Caso a tenão esteja dentro dos limites, passa a verificar se a
        normalização foi executada à pouco tempo, se foi, avisa o operador,
        senão, passa a chamar as funções de reset geral.
        """

        logger.debug("[USN] Normalizando...")
        logger.debug(f"[USN] Última tentativa de normalização:   {self.ultima_tentativa_norm.strftime('%d-%m-%Y %H:%M:%S')}")
        logger.debug(f"[USN] Tensão na linha:                    RS -> \"{SE.tensao_rs.valor:2.1f} kV\" | ST -> \"{SE.tensao_st.valor:2.1f} kV\" | TR -> \"{SE.tensao_tr.valor:2.1f} kV\"")

        if not BAY.fechar_dj_bay():
            return NORM_USN_DJBAY_ABERTO

        if not SE.dj_se.valor:
            logger.info("[USN] Enviando comando de fechamento do Disjuntor 52L")
            if not SE.fechar_dj_linha():
                logger.warning("[USN] Não foi possível realizar o fechameto do Disjuntor 52L")
                return NORM_USN_DJL_ABERTO

        if not SE.verificar_tensao():
            return NORM_USN_FALTA_TENSAO

        elif ((self.get_time() - self.ultima_tentativa_norm).seconds >= 60 * self.tentativas_normalizar) or self.normalizar_forcado:
            self.ultima_tentativa_norm = self.get_time()
            self.tentativas_normalizar += 1
            self.bd_emergencia = False
            self.clp_emergencia = False
            SA.resetar_emergencia()
            SE.resetar_emergencia()
            BAY.resetar_emergencia()
            TDA.resetar_emergencia()
            BancoDados.update_remove_emergencia()
            return NORM_USN_EXECUTADA

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minuto atrás.")
            return NORM_USN_JA_EXECUTADA

    def verificar_leituras_periodicas(self) -> "None":
        """
        Função de temporizador com leituras para alertas de manutenção.

        Chama os métodos de leitura de objetos da Usina e Unidades de Geração.
        Caso haja alguma leitura fora do esperado, é enviado o alerta via
        WhatsApp ou Voip.
        """

        while True:
            SA.verificar_leituras()
            SE.verificar_leituras()
            TDA.verificar_leituras()
            for ug in self.ugs:
                ug.verificar_leituras()

            if True in (dct.voip[r][0] for r in dct.voip):
                Voip.acionar_chamada()
                pass
            sleep(max(0, (time() + 1800) - time()))

    def verificar_condicionadores(self) -> "int":
        flag = CONDIC_IGNORAR

        lst_sa = SA.verificar_condicionadores()
        lst_se = SE.verificar_condicionadores()
        lst_bay = BAY.verificar_condicionadores()
        lst_tda = TDA.verificar_condicionadores()

        condics = [condic for condics in [lst_sa, lst_se, lst_bay, lst_tda] for condic in condics]

        for condic in condics:
            if condic.gravidade == CONDIC_INDISPONIBILIZAR:
                return CONDIC_INDISPONIBILIZAR
            elif condic.gravidade == CONDIC_NORMALIZAR:
                flag = CONDIC_NORMALIZAR

        return flag


    # FUNÇÕES PARA CÁLCULOS E AJUSTES DE OERAÇÃO

    def ajustar_ie_padrao(self) -> "int":
        """
        Função para ajustar o valor do IE.
        """

        return (sum(ug.leitura_potencia for ug in self.ugs) / self.cfg["pot_maxima_alvo"]) / self.ug_operando

    def controlar_potencia(self) -> "None":
        """
        Função para calcular PID (Proporcional, Integral e Derivativo), para controle de potência
        das Unidades a partir da leitura de Nível Montante.
        """
        
        logger.debug(f"[TDA] NÍVEL -> Alvo:                      {self.cfg['nv_alvo']:0.3f}")
        logger.debug(f"[TDA]          Leitura:                   {TDA.nv_montante_recente:0.3f}")

        self.controle_p = self.cfg["kp"] * TDA.erro_nv

        if self._pid_inicial == -1:
            self.controle_i = max(min(self.controle_ie - self.controle_p, 0,8), 0)
            self._pid_inicial = 0
        else:
            self.controle_i = max(min((self.cfg["ki"] * TDA.erro_nv) + self.controle_i, 0.8), 0)
            self.controle_d = self.cfg["kd"] * (TDA.erro_nv - TDA.erro_nv_anterior)

        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))

        logger.debug("")
        logger.debug(f"[USN] PID   -> P + I + D:                 {saida_pid:0.3f}")
        logger.debug(f"[USN] P:                                  {self.controle_p:0.3f}")
        logger.debug(f"[USN] I:                                  {self.controle_i:0.3f}")
        logger.debug(f"[USN] D:                                  {self.controle_d:0.3f}")

        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)

        logger.debug(f"[USN] IE:                                 {self.controle_ie:0.3f}")
        logger.debug(f"[USN] ERRO:                               {TDA.erro_nv}")
        logger.debug("")

        if TDA.nv_montante_recente >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if TDA.nv_montante_recente <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"]), self.cfg["pot_minima"])

        logger.debug(f"[USN] Potência alvo:                      {pot_alvo:0.3f}")

        pot_alvo = self.ajustar_potencia(pot_alvo)

    def ajustar_potencia(self, pot_alvo: "float") -> "float":
        if self._pot_alvo_anterior == -1:
            self._pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs:
                ug.setpoint = 0
            return 0

        pot_medidor = self.potencia_medidor

        logger.debug(f"[USN] Potência no medidor:                {self.potencia_ativa:0.3f}")

        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])
        pot_medidor = max(pot_aux, min(self.potencia_medidor, self.cfg["pot_maxima_usina"]))

        try:
            if pot_medidor > self.cfg["pot_maxima_alvo"]:
                pot_alvo = self.pot_alvo_anterior * (1 - ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))
        except TypeError as te:
            logger.error(f"[USN] A comunicação com os MFs falharam. Exception: \"{repr(te)}\"")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

        self.pot_alvo_anterior = pot_alvo

        logger.debug(f"[USN] Pot alvo pós ajuste: {pot_alvo:0.3f}")
        self.distribuir_potencia(pot_alvo)
        return pot_alvo

    def distribuir_potencia(self, pot_alvo) -> None:
        ugs = self.controle_ugs_disponiveis()
        if ugs is None:
            logger.warning("[USN] Sem UGs disponíveis para realizar a distribuição de potência.")
            return

        logger.debug(f"[USN] UG{[ug.id for ug in ugs]}")

        self.pot_disp = [sum(self.cfg[f"pot_maxima_ug{ug.id}"]) for ug in self.ugs if ug.disponivel]
        ajuste_manual = min(max(0, [sum(ug.leitura_potencia) for ug in self.ugs if ug.manual]))

        logger.debug(f"[USN] Distribuindo: {pot_alvo - ajuste_manual:0.3f}")
        sp = (pot_alvo - ajuste_manual) / self.cfg["pot_maxima_usina"]

        self.__split1 = True if sp > (0) else self.__split1
        self.__split2 = (True if sp > (0.5 + self.cfg["margem_pot_critica"]) else self.__split2)

        self.__split2 = False if sp < (0.5) else self.__split2
        self.__split1 = False if sp < (self.cfg["pot_minima"] / self.cfg["pot_maxima_usina"]) else self.__split1

        logger.debug(f"[USN] SP<-{sp}")
        if len(ugs) == 2:
            if self.__split2:
                logger.debug("[USN] Split 2")
                ugs[0].setpoint = sp * self.cfg[f"pot_maxima_ug{ugs[0].id}"]
                ugs[1].setpoint = sp * self.cfg[f"pot_maxima_ug{ugs[1].id}"]

            elif self.__split1:
                logger.debug("[USN] Split 1")
                ugs[0].setpoint = (sp * 2 / 1) * self.cfg[f"pot_maxima_ug{ugs[0].id}"]
                ugs[1].setpoint = 0

        elif len(ugs) == 1:
            logger.debug("[USN] Split 1B")
            ugs[0].setpoint = (sp * 2 / 1) * self.cfg[f"pot_maxima_ug{ugs[0].id}"] if self.__split1 or self.__split2 else ...

        else:
            for ug in ugs:
                ug.setpoint = 0

    def controle_ugs_disponiveis(self) -> "list[UnidadeGeracao]":
        ls = []
        [ls.append(ug) for ug in self.ugs if ug.disponivel and not ug.etapa_atual == UG_PARANDO]
        logger.debug("")

        if self.modo_de_escolha_das_ugs == MODO_ESCOLHA_MANUAL:
            logger.debug("[USN] UGs disponíveis em ordem (prioridade):")
            return sorted(ls, key=lambda y: (-1 * y.leitura_potencia, -1 * y.setpoint, y.prioridade))
        else:
            logger.debug("[USN] UGs disponíveis em ordem (horas-máquina):")
            return sorted(ls, key=lambda y: (y.leitura_horimetro, -1 * y.leitura_potencia, -1 * y.setpoint))


    # FUNÇÕES DE CONTROLE DE DADOS

    def ler_valores(self) -> "None":
        """
        Função para leitura e atualização de parâmetros de operação através de
        Banco de Dados da Interface WEB.
        """

        cli.ping_clients()
        TDA.atualizar_montante()

        parametros = BancoDados.get_parametros_usina()

        self.atualizar_valores_cfg(parametros)
        self.atualizar_valores_banco(parametros)

        for ug in self.ugs:
            ug.atualizar_limites(parametros)

        self.heartbeat()

    def atualizar_valores_banco(self, parametros) -> None:
        """
        Função para atualização de valores de Banco de Dados.
        """

        try:
            if int(parametros["emergencia_acionada"]) == 1:
                self.bd_emergencia = True
                logger.debug("[USN] Emergência acionada!")
            else:
                self.bd_emergencia = False

            if int(parametros["modo_autonomo"]) == 1:
                self.modo_autonomo = True
                logger.debug(f"[USN] Modo autônomo:                      \"{'Ativado'}\"")
            else:
                self.modo_autonomo = False
                logger.debug(f"[USN] Modo autônomo:                      \"{'Desativado'}\"")

            if not self.modo_de_escolha_das_ugs == int(parametros["modo_de_escolha_das_ugs"]):
                self.modo_de_escolha_das_ugs = int(parametros["modo_de_escolha_das_ugs"])
                logger.info(f"[USN] Modo de prioridade das UGs:         \"{UG_STR_DCT_PRIORIDADE[self.modo_de_escolha_das_ugs]}\"")

        except Exception:
            logger.error(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados.")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

    def atualizar_valores_cfg(self, parametros) -> "None":
        """
        Função para atualização de valores de operação do arquivo cfg.json.
        """

        try:
            self.cfg["kp"] = float(parametros["kp"])
            self.cfg["ki"] = float(parametros["ki"])
            self.cfg["kd"] = float(parametros["kd"])
            self.cfg["kie"] = float(parametros["kie"])

            self.cfg["nv_alvo"] = float(parametros["nv_alvo"])
            self.cfg["nv_minimo"] = float(parametros["nv_minimo"])
            self.cfg["nv_maximo"] = float(parametros["nv_maximo"])

            self.cfg["pot_maxima_alvo"] = float(parametros["pot_nominal"])
            self.cfg["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])
            self.cfg["pot_maxima_usina"] = float(parametros["pot_nominal_ug"]) * 2
            self.cfg["margem_pot_critica"] = float(parametros["margem_pot_critica"])

            with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'w') as file:
                json.dump(self.cfg, file)

        except Exception:
            logger.error(f"[USN] Houve um erro ao atualizar o arquivo de configuração \"cfg.json\".")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

    def escrever_valores(self) -> "None":
        """
        Função para escrita de valores de operação nos Bancos do módulo do Django
        e Debug.
        """

        try:
            BancoDados.update_valores_usina(
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"), # timestamp
                1 if self.aguardando_reservatorio else 0,  # aguardando_reservatorio
                True,  # DEPRECATED clp_online
                TDA.nv_montante.valor, # nv_montante
                1 if self.ug1.disponivel else 0,  # ug1_disp
                self.ug1.leitura_potencia,  # ug1_pot
                self.ug1.setpoint,  # ug1_setpot
                self.ug1.etapa_atual,  # ug1_sinc
                self.ug1.leitura_horimetro,  # ug1_tempo
                1 if self.ug2.disponivel else 0,  # ug2_disp
                self.ug2.leitura_potencia,  # ug2_pot
                self.ug2.setpoint,  # ug2_setpot
                self.ug2.etapa_atual,  # ug2_sinc
                self.ug2.leitura_horimetro,  # ug2_tempo
            )

        except Exception:
            logger.error(f"[USN] Houve um erro ao atualizar os valores de controle de operação no Banco de Dados.")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

        try:
            BancoDados.update_debug(
                self.time(),
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.ug1.setpoint,
                self.ug1.leitura_potencia,
                self.ug2.setpoint,
                self.ug2.leitura_potencia,
                TDA.nv_montante_recente,
                TDA.erro_nv,
                1 if self.modo_autonomo else 0,
            )

        except Exception:
            logger.error(f"[USN] Houve um erro ao atualizar valores DEBUG do controle de potência no Banco de Dados.")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")

    def heartbeat(self) -> "None":
        """
        Função para controle do CLP - MOA.

        Esta função tem como objetivo enviar comandos de controle/bloqueio para
        os CLPs da Usina e também, ativação/desativação do MOA através de chaves
        seletoras no painel do Sistema Auxiliar.
        """

        try:
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["PAINEL_LIDO"], [1])
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["MOA_OUT_MODE"], [1 if self.modo_autonomo else 0])
            self.clp["MOA"].write_single_register(REG_CLP["MOA"]["MOA_OUT_STATUS"], self.estado_moa)

            if self.modo_autonomo:
                self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_EMERG"], [1 if self.clp_emergencia else 0])
                self.clp["MOA"].write_multiple_registers(REG_CLP["MOA"]["OUT_SETPOINT"], [int(sum(ug.setpoint for ug in self.ugs))])
                self.clp["MOA"].write_multiple_registers(REG_CLP["MOA"]["OUT_TARGET_LEVEL"], [int((self.cfg["nv_alvo"] - 800) * 1000)])

                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_HABILITA_AUTO"])[0] == 1:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_HABILITA_AUTO"], [1])
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = True

                elif self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_DESABILITA_AUTO"])[0] == 1:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_HABILITA_AUTO"], [0])
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_DESABILITA_AUTO"], [1])
                    self.modo_autonomo = False

                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_EMERG"])[0] == 1 and not self.borda_emergencia:
                    for ug in self.ugs:
                        ug.verificar_condicionadores()

                elif self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_EMERG"])[0] == 0 and self.borda_emergencia:
                    self.borda_emergencia = False

                for ug in self.ugs:
                    if self.clp["MOA"].read_coils(REG_CLP["MOA"][f"IN_EMERG_UG{ug.id}"])[0] == 1:
                        ug.verificar_condicionadores()

                    if self.clp["MOA"].read_coils(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"])[0] == 1:
                        self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"], [1])

                    elif self.clp["MOA"].read_coils(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"])[0] == 0:
                        self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"], [0])

            elif not self.modo_autonomo:
                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_HABILITA_AUTO"])[0] == 1:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_HABILITA_AUTO"], [1])
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_DESABILITA_AUTO"], [0])
                    self.modo_autonomo = True

                self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_EMERG"], [0])
                self.clp["MOA"].write_single_register(REG_CLP["MOA"]["OUT_SETPOINT"], [0])
                self.clp["MOA"].write_single_register(REG_CLP["MOA"]["OUT_TARGET_LEVEL"], [0])
                [self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"], [0]) for ug in self.ugs]

        except Exception:
            logger.error(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA.")
            logger.debug(f"[USN] Traceback: {traceback.format_exc()}")
