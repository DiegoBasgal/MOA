__version__ = "0.2"
__author__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal",
__description__ = "Este módulo corresponde a implementação da operação da Usina."

import os
import json
import pytz
import logging
import traceback

import src.dicionarios.dict as dct

import src.bay as bay
import src.subestacao as se
import src.tomada_agua as tda
import src.servico_auxiliar as sa

from time import sleep, time
from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *
from src.funcoes.condicionadores import *

from src.mensageiro.voip import Voip
from src.conectores.servidores import Servidores
from src.conectores.banco_dados import BancoDados
from src.funcoes.agendamentos import Agendamentos
from src.funcoes.escrita import EscritaModBusBit as EMB

from src.funcoes.leitura import *
from src.unidade_geracao import UnidadeGeracao


logger = logging.getLogger("logger")
debug_log = logging.getLogger("debug")


class Usina:
    def __init__(self, cfg: "dict"=None, serv: "Servidores"=None) -> "None":


        # VERIFICAÇÃO DE ARGUMENTOS

        if None in (cfg):
            raise ValueError("[USN] Não foi possível carregar os arquivos de configuração (\"cfg.json\").")
        else:
            self.cfg = cfg

        if not serv:
            raise ValueError("[USN] Não foi possível carregar a classe de conxeão com Servidores.")
        else:
            self.clp = serv.clp
            self.rele = serv.rele


        # INCIALIZAÇÃO DE OBJETOS DA USINA

        self.bd = BancoDados("MOA")

        self.bay = bay.Bay(serv, self.bd)
        self.se = se.Subestacao(serv, self.bd)
        self.sa = sa.ServicoAuxiliar(serv, self.bd)
        self.tda = tda.TomadaAgua(self.cfg, serv, self.bd)

        self.ug1 = UnidadeGeracao(1, self.cfg, self.bd, self.tda.cp, serv)
        self.ug2 = UnidadeGeracao(2, self.cfg, self.bd, self.tda.cp, serv)
        self.ugs: "list[UnidadeGeracao]" = [self.ug1, self.ug2]

        self.agn = Agendamentos(self.cfg, self.bd, self)


        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__split1: "bool" = False
        self.__split2: "bool" = False
        self.__pid_inicial: "int" = -1

        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS

        self._tentativas_normalizar: "int" = 0

        self._pot_alvo_anterior: "float" = -1

        self._modo_autonomo: "bool" = False

        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.estado_moa: "int" = 5

        self.pot_disp: "int" = 0
        self.ug_operando: "int" = 0

        self.modo_prioridade_ugs: "int" = 0

        self.controle_p: "float" = 0
        self.controle_i: "float" = 0
        self.controle_d: "float" = 0

        self.bd_emergencia: "bool" = False
        self.clp_emergencia: "bool" = False
        self.borda_emergencia: "bool" = False
        self.normalizar_forcado: "bool" = False

        self.ultima_tentativa_norm: "datetime" = self.get_time()


        # FINALIZAÇÃO DO __INIT__

        self.bay.carregar_leituras()
        self.se.carregar_leituras()
        self.tda.carregar_leituras()
        self.sa.carregar_leituras()

        serv.open_all()

        self.ler_valores()
        self.verificar_bay_se()
        self.ajustar_inicializacao()
        self.escrever_valores()

        self._tentativas_normalizar = 0
        self.tentativas_normalizar = 0


    # PROPRIEDADES/GETTERS

    @property
    def modo_autonomo(self) -> "bool":
        # PROPRIEDADE -> Retorna o modo do MOA.

        return self._modo_autonomo

    @modo_autonomo.setter
    def modo_autonomo(self, var: "bool") -> "None":
        # SETTER -> Atribui o novo valor do modo do MOA e atualiza no Banco de Dados.

        self._modo_autonomo = var
        self.bd.update_modo_moa(var)

    @property
    def tentativas_normalizar(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de Tentativas de Normalização.

        return self._tentativas_normalizar

    @tentativas_normalizar.setter
    def tentativas_normalizar(self, var: "int") -> "None":
        # SETTER -> Atribui o novo valor de Tentativas de Normalização.

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
        logger.debug("")
        logger.info("[USN] Acionando Comandos de RESET de Emergência:")
        logger.debug("")
        logger.debug("[USN] Bay resetado.") if self.bay.resetar_emergencia() else logger.info("[USN] Reset de emergência do Bay \"FALHOU\"!.")
        logger.debug("[USN] Subestação resetada.") if self.se.resetar_emergencia() else logger.info("[USN] Reset de emergência da subestação \"FALHOU\"!.")
        logger.debug("[USN] Tomada da Água resetada.") if self.tda.resetar_emergencia else logger.info("[USN] Reset de emergência da Tomada da Água \"FALHOU\"!.")
        logger.debug("[USN] Serviço Auxiliar resetado.") if self.sa.resetar_emergencia() else logger.info("[USN] Reset de emergência do serviço auxiliar \"FALHOU\"!.")
        logger.debug("")


    def acionar_emergencia(self) -> "bool":
        """
        Função para acionamento de emergência geral da Usina.

        Envia o comando de parada de emergência para as Unidades.
        """

        self.db_emergencia = True
        self.clp_emergencia = True

        return

        try:
            [EMB.escrever_bit(self.clp[f"UG{ug.id}"], REG_CLP[f"UG{ug.id}"][f"PARADA_CMD_EMERGENCIA"], valor=1) for ug in self.ugs]
            sleep(5)
            [EMB.escrever_bit(self.clp[f"UG{ug.id}"], REG_CLP[f"UG{ug.id}"][f"PARADA_CMD_EMERGENCIA"], valor=0) for ug in self.ugs]

        except Exception:
            logger.error(f"[USN] Houve um erro ao executar o comando de Emergência.")
            logger.debug(traceback.format_exc())
            return False


    def normalizar_usina(self) -> "bool":
        """
        Função para normalização de ocorrências da Usina.

        Verifica primeiramente a tensão da linha.
        Caso a tenão esteja dentro dos limites, passa a verificar se a
        normalização foi executada à pouco tempo, se foi, avisa o operador,
        senão, passa a chamar as funções de reset geral.
        """

        logger.debug(f"[USN] Última tentativa de normalização:   {self.ultima_tentativa_norm.strftime('%d-%m-%Y %H:%M:%S')}")

        if (self.tentativas_normalizar < 3 and (self.get_time() - self.ultima_tentativa_norm).seconds >= self.tentativas_normalizar * 2) or self.normalizar_forcado:
            self.ultima_tentativa_norm = self.get_time()
            self.tentativas_normalizar += 1
            logger.info(f"[USN] Normalizando... (Tentativa {self.tentativas_normalizar}/3)")
            self.normalizar_forcado = self.clp_emergencia = self.bd_emergencia = False
            self.resetar_emergencia()
            sleep(1)
            self.bay.fechar_dj_linha()
            sleep(1)
            self.se.fechar_dj_linha()
            self.bd.update_remove_emergencia()
            return True

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minutos atrás.")
            sleep(1)
            return False


    def verificar_bay_se(self) -> "int":
        """
        Função para verificação do Bay e Subestação.

        Apresenta a leitura de tensão VAB, VBC, VCA do Bay e Subestação.
        Caso haja uma falta de tensão na linha da subestação, aciona o temporizador
        para retomada em caso de queda de tensão. Caso a tensão esteja normal, tenta
        realizar o fechamento dos disjuntores do Bay e depois da Subestação. Caso
        haja um erro com o fechamento dos disjuntores, aciona a normalização da usina
        senão, sinaliza que está tudo correto para a máquina de estados do MOA.
        """
    
        if not self.bay.verificar_tensao_trifasica():
            logger.debug("")
            logger.debug(f"[BAY] Tensão BAY:                   VAB -> \"{self.bay.tensao_vab.valor:2.1f} V\" | VBC -> \"{self.bay.tensao_vbc.valor:2.1f} V\" | VCA -> \"{self.bay.tensao_vca.valor:2.1f} V\"")
            logger.debug(f"[SE]  Tensão Subestação:            VAB -> \"{self.se.tensao_vab.valor:2.1f} V\" | VBC -> \"{self.se.tensao_vbc.valor:2.1f} V\" | VCA -> \"{self.se.tensao_vca.valor:2.1f} V\"")
            logger.debug("")
            return DJS_FALTA_TENSAO

        elif not self.bay.fechar_dj_linha() or not self.se.fechar_dj_linha():
            self.normalizar_forcado = True
            return DJS_FALHA

        else:
            return DJS_OK


    def verificar_leituras_periodicas(self) -> "None":
        """
        Função de temporizador com leituras para alertas de manutenção.

        Chama os métodos de leitura de objetos da Usina e Unidades de Geração.
        Caso haja alguma leitura fora do esperado, é enviado o alerta via
        WhatsApp ou Voip.
        """

        while True:
            self.se.verificar_leituras()
            self.sa.verificar_leituras()
            self.tda.verificar_leituras()

            for ug in self.ugs:
                ug.verificar_leituras()

            if True in (dct.voip[r][0] for r in dct.voip):
                Voip.acionar_chamada()
                pass
            sleep(max(0, (time() + 1800) - time()))


    def verificar_condicionadores(self) -> "int":

        flag = CONDIC_IGNORAR

        lst_bay = self.bay.verificar_condicionadores()
        lst_se = self.se.verificar_condicionadores()
        lst_tda = self.tda.verificar_condicionadores()
        lst_sa = self.sa.verificar_condicionadores()

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

        return sum(ug.leitura_potencia for ug in self.ugs) / self.cfg["pot_maxima_alvo"]


    def ajustar_inicializacao(self) -> "None":
        """
        Funçao para ajustar variáveis de cálculos de controle de operação, na inicialização
        da Classe da Usina.
        """

        for ug in self.ugs:
            if ug.etapa == UG_SINCRONIZADA:
                self.ug_operando += 1

        self.__split1 = True if self.ug_operando == 1 else False
        self.__split2 = True if self.ug_operando == 2 else False

        self.controle_ie = self.ajustar_ie_padrao()

        self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_BLOCK_UG1"], 0)
        self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_BLOCK_UG2"], 0)


    def controlar_reservatorio(self) -> "int":
        """
        Função para controle de níveis do reservatório.

        Realiza a leitura de nível montante e determina qual condição entrar. Se
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

        if self.tda.nivel_montante.valor >= self.cfg["nv_maximo"]:
            logger.debug("[TDA] Nível Montante acima do Máximo.")
            logger.debug(f"[TDA]          Leitura:                   {self.tda.nivel_montante.valor:0.3f}")
            logger.debug("")

            if self.tda.nivel_montante_anterior >= NIVEL_MAXIMORUM:
                logger.critical(f"[TDA] Nivel Montante ({self.tda.nivel_montante_anterior:3.2f}) atingiu o Maximorum!")
                logger.debug("")
                return NV_EMERGENCIA
            else:
                self.controle_i = 0.5
                self.controle_ie = 0.5
                self.ajustar_potencia(self.cfg["pot_maxima_usina"])

                for ug in self.ugs:
                    ug.step()

        elif self.tda.nivel_montante.valor <= self.cfg["nv_minimo"] and not self.tda.aguardando_reservatorio:
            logger.debug("[TDA] Nível Montante abaixo do Mínimo.")
            logger.debug(f"[TDA]          Leitura:                   {self.tda.nivel_montante.valor:0.3f}")
            logger.debug("")
            self.tda.aguardando_reservatorio = True
            self.distribuir_potencia(0)

            for ug in self.ugs:
                ug.step()

            if self.tda.nivel_montante_anterior <= NIVEL_FUNDO_RESERVATORIO:
                logger.critical(f"[TDA] Nível Montante ({self.tda.nivel_montante_anterior:3.2f}) atingiu o fundo do reservatorio!")
                logger.debug("")
                return NV_EMERGENCIA

        elif self.tda.aguardando_reservatorio:
            logger.debug("[TDA] Aguardando Nível Montante...")
            logger.debug(f"[TDA]          Leitura:                   {self.tda.nivel_montante.valor:0.3f}")
            logger.debug(f"[TDA]          Nível de Religamento:      {self.cfg['nv_religamento']:0.3f}")
            logger.debug("")

            if self.tda.nivel_montante.valor >= self.cfg["nv_religamento"]:
                logger.debug("[TDA] Nível Montante dentro do limite de operação.")
                logger.debug(f"[TDA]          Leitura:                   {self.tda.nivel_montante.valor:0.3f}")
                logger.debug("")
                self.tda.aguardando_reservatorio = False

        else:
            self.controlar_potencia()

            for ug in self.ugs:
                ug.step()

        return NV_NORMAL


    def controlar_potencia(self) -> "None":
        """
        Função para calcular PID (Proporcional, Integral e Derivativo), para controle de potência
        das Unidades a partir da leitura de Nível Montante.
        """

        logger.debug(f"[TDA] NÍVEL -> Alvo:                      {self.cfg['nv_alvo']:0.3f}")
        logger.debug(f"[TDA]          Leitura:                   {self.tda.nivel_montante.valor:0.3f}")
        logger.debug(f"[TDA]          Filtro EMA:                {self.tda.nivel_montante_anterior:0.3f}")

        self.controle_p = self.cfg["kp"] * self.tda.erro_nivel

        if self.__pid_inicial == -1:
            self.controle_i = max(min(self.controle_ie - self.controle_p, 0.9), 0)
            self.__pid_inicial = 0
        else:
            self.controle_i = max(min((self.cfg["ki"] * self.tda.erro_nivel) + self.controle_i, 0.9), 0)
            self.controle_d = self.cfg["kd"] * (self.tda.erro_nivel - self.tda.erro_nivel_anterior)

        saida_pid = (self.controle_p + self.controle_i + min(max(-0.3, self.controle_d), 0.3))

        logger.debug("")
        logger.debug(f"[USN] PID   -> P + I + D:                 {saida_pid:0.3f}")
        logger.debug(f"[USN] P:                                  {self.controle_p:0.3f}")
        logger.debug(f"[USN] I:                                  {self.controle_i:0.3f}")
        logger.debug(f"[USN] D:                                  {self.controle_d:0.3f}")

        self.controle_ie = max(min(saida_pid + self.controle_ie * self.cfg["kie"], 1), 0)

        logger.debug(f"[USN] IE:                                 {self.controle_ie:0.3f}")
        logger.debug(f"[USN] ERRO:                               {self.tda.erro_nivel}")
        logger.debug("")

        if self.tda.nivel_montante_anterior >= (self.cfg["nv_maximo"] + 0.03):
            self.controle_ie = 1
            self.controle_i = 1 - self.controle_p

        if self.tda.nivel_montante_anterior <= (self.cfg["nv_minimo"] + 0.03):
            self.controle_ie = min(self.controle_ie, 0.3)
            self.controle_i = 0

        pot_alvo = max(min(round(self.cfg["pot_maxima_usina"] * self.controle_ie, 5), self.cfg["pot_maxima_usina"]), self.cfg["pot_minima"])

        pot_alvo = self.ajustar_potencia(pot_alvo)


    def ajustar_potencia(self, pot_alvo: "float") -> "float":
        """
        Função para ajustar a potência de controle após do cálculo do PID.
        """

        if self._pot_alvo_anterior == -1:
            self._pot_alvo_anterior = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs:
                ug.setpoint = 0
            return 0

        pot_medidor = self.bay.potencia_mp.valor

        logger.debug(f"[USN] Potência no medidor:                {pot_medidor:0.3f}")

        pot_aux = self.cfg["pot_maxima_alvo"] - (self.cfg["pot_maxima_usina"] - self.cfg["pot_maxima_alvo"])
        pot_medidor = max(pot_aux, min(pot_medidor, self.cfg["pot_maxima_usina"]))

        if pot_medidor > self.cfg["pot_maxima_alvo"]:
            pot_alvo = self._pot_alvo_anterior * (1 - ((pot_medidor - self.cfg["pot_maxima_alvo"]) / self.cfg["pot_maxima_alvo"]))

        self._pot_alvo_anterior = pot_alvo

        logger.debug(f"[USN] Potência alvo após ajuste:          {pot_alvo:0.3f}")

        self.distribuir_potencia(pot_alvo)


    def distribuir_potencia(self, pot_alvo) -> "None":
        """
        Função para distribuição de potência, após cálculos de controle/ajustes.

        Chama a função de controle de unidades disponíveis e determina através de janelas
        de potência para entrada ou retirada de uma Unidade.
        """

        ugs: "list[UnidadeGeracao]" = self.verificar_ugs_disponiveis()

        logger.debug("")
        logger.debug(f"[USN] Ordem das UGs (Prioridade):         {[ug.id for ug in ugs]}")
        logger.debug("")

        ajuste_manual = 0

        for ug in self.ugs:
            if ug.manual:
                ajuste_manual += ug.leitura_potencia
            else:
                self.pot_disp += ug.setpoint_maximo

        if ugs is None or not len(ugs):
            return

        logger.debug(f"[USN] Distribuindo:                       {pot_alvo - ajuste_manual:0.3f}")
        sp = (pot_alvo - ajuste_manual) / self.cfg["pot_maxima_usina"]

        self.__split1 = True if sp > (0) else self.__split1
        self.__split2 = (True if sp > (0.5 + self.cfg["margem_pot_critica"]) else self.__split2)

        self.__split2 = False if sp < (0.5) else self.__split2
        self.__split1 = False if sp < (self.cfg["pot_minima"] / self.cfg["pot_maxima_usina"]) else self.__split1

        logger.debug(f"[USN] SP Geral:                           {sp * 100:3.2f} %")

        if len(ugs) == 2:
            if self.__split2:
                logger.debug("[USN] Split:                              2")
                logger.debug("")

                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = sp * ugs[1].setpoint_maximo

                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")

            elif self.__split1:
                logger.debug("[USN] Split:                              2 -> \"1B\"")
                logger.debug("")

                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo
                ugs[1].setpoint = 0

                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")

            else:
                logger.debug("")

                ugs[0].setpoint = 0
                ugs[1].setpoint = 0

                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")
                logger.debug(f"[UG{ugs[1].id}] SP    <-                            {int(ugs[1].setpoint)}")

        elif len(ugs) == 1:
            if self.__split1 or self.__split2:
                logger.debug("[USN] Split:                              1")
                logger.debug("")

                sp = sp * 2 / 1
                ugs[0].setpoint = sp * ugs[0].setpoint_maximo

                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")

            else:
                logger.debug("")

                ugs[0].setpoint = 0

                logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")


    def verificar_ugs_disponiveis(self) -> "list[UnidadeGeracao]":
        """
        Função para verificar leituras/condições específicas e determinar a Prioridade das Unidades.
        """

        ls = [ug for ug in self.ugs if ug.disponivel and not ug.etapa == UG_PARANDO]

        if self.modo_prioridade_ugs in (UG_PRIORIDADE_1, UG_PRIORIDADE_2):
            return sorted(ls, key=lambda y: (y.prioridade, -1 * y.etapa_atual, -1 * y.leitura_potencia, -1 * y.setpoint))

        else:
            return sorted(ls, key=lambda y: (-1 * y.etapa_atual, y.leitura_horimetro, -1 * y.leitura_potencia, -1 * y.setpoint))


    # FUNÇÕES DE CONTROLE DE DADOS

    def ler_valores(self) -> "None":
        """
        Função para leitura e atualização de parâmetros de operação através de
        Banco de Dados da Interface WEB.
        """

        # Servidores.ping_clients()
        self.tda.atualizar_montante()

        parametros = self.bd.get_parametros_usina()

        self.atualizar_valores_cfg(parametros)
        self.atualizar_valores_banco(parametros)

        for ug in self.ugs:
            ug.atualizar_limites(parametros)


    def atualizar_valores_banco(self, parametros) -> "None":
        """
        Função para atualização de valores de Banco de Dados.
        """

        try:
            if int(parametros["emergencia_acionada"]) == 1 and not self.bd_emergencia:
                self.bd_emergencia = True
                logger.info(f"[USN] Emergência:                         \"{'Ativada'}\"")

            elif int(parametros["emergencia_acionada"]) == 0 and self.bd_emergencia:
                self.bd_emergencia = False
                logger.info(f"[USN] Emergência:                         \"{'Desativada'}\"")

            if int(parametros["modo_autonomo"]) == 1 and not self.modo_autonomo:
                self.modo_autonomo = True
                logger.info(f"[USN] Modo autônomo:                      \"{'Ativado'}\"")

            elif int(parametros["modo_autonomo"]) == 0 and self.modo_autonomo:
                self.modo_autonomo = False
                logger.info(f"[USN] Modo autônomo:                      \"{'Desativado'}\"")

            if self.modo_prioridade_ugs != int(parametros["modo_de_escolha_das_ugs"]):
                self.modo_prioridade_ugs = int(parametros["modo_de_escolha_das_ugs"])
                logger.info(f"[USN] Modo de prioridade das UGs:         \"{UG_STR_DCT_PRIORIDADE[self.modo_prioridade_ugs]}\"")

        except Exception:
            logger.error(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados.")
            logger.debug(traceback.format_exc())


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
            self.cfg["nv_religamento"] = float(parametros["nv_religamento"])

            self.cfg["pot_maxima_alvo"] = float(parametros["pot_nominal"])
            self.cfg["pot_maxima_ug"] = float(parametros["pot_nominal_ug"])
            self.cfg["pot_maxima_usina"] = float(parametros["pot_nominal_ug"]) * 2
            self.cfg["margem_pot_critica"] = float(parametros["margem_pot_critica"])

            with open(os.path.join(os.path.dirname("/opt/operacao-autonoma/src/dicionarios/"), 'cfg.json'), 'w') as file:
                json.dump(self.cfg, file)

        except Exception:
            logger.error(f"[USN] Houve um erro ao atualizar o arquivo de configuração \"cfg.json\".")
            logger.debug(traceback.format_exc())


    def escrever_valores(self) -> "None":
        """
        Função para escrita de valores de operação nos Bancos do módulo do Django
        e Debug.
        """
        
        try:
            self.bd.update_valores_usina([
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                1 if self.tda.aguardando_reservatorio else 0,
                self.tda.nivel_montante.valor,
                self.ug1.leitura_potencia,
                self.ug1.setpoint,
                self.ug1.codigo_state,
                self.tda.cp["CP1"].etapa,
                self.ug2.leitura_potencia,
                self.ug2.setpoint,
                self.ug2.codigo_state,
                self.tda.cp["CP2"].etapa
            ])

        except Exception:
            logger.error(f"[USN] Houve um erro ao atualizar os valores de controle de operação no Banco de Dados.")
            logger.debug(traceback.format_exc())

        try:
            sleep(3/1000) #espera 3 milisegundo para gravar no banco, dessa forma ele evita problemas de chave primária duplicada

            self.bd.update_debug([
                time(),
                1 if self.modo_autonomo else 0,
                self.tda.nivel_montante.valor,
                self.tda.erro_nivel,
                self.ug1.setpoint,
                self.ug1.leitura_potencia,
                self.ug1.codigo_state,
                self.ug2.setpoint,
                self.ug2.leitura_potencia,
                self.ug2.codigo_state,
                self.controle_p,
                self.controle_i,
                self.controle_d,
                self.controle_ie,
                self.cfg["kp"],
                self.cfg["ki"],
                self.cfg["kd"],
                self.cfg["kie"],
            ])

        except Exception:
            logger.debug(f"[USN] Houve um erro ao atualizar valores DEBUG no Banco de Dados.")
            logger.debug(traceback.format_exc())


    def heartbeat(self) -> "None":
        """
        Função para controle do CLP - MOA.

        Esta função tem como objetivo enviar comandos de controle/bloqueio para
        os CLPs da Usina e também, ativação/desativação do MOA através de chaves
        seletoras no painel do Sistema Auxiliar.
        """

        try:
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["PAINEL_LIDO"], 1)
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["MOA_OUT_MODE"], 1 if self.modo_autonomo else 0)
            self.clp["MOA"].write_single_register(REG_CLP["MOA"]["MOA_OUT_STATUS"], self.estado_moa)

            for ug in self.ugs:
                ug.atualizar_modbus_moa()

            if self.modo_autonomo:
                self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_EMERG"], 1 if self.clp_emergencia else 0)
                self.clp["MOA"].write_single_register(REG_CLP["MOA"]["OUT_TARGET_LEVEL"], int((self.cfg["nv_alvo"] - 400) * 1000))
                self.clp["MOA"].write_single_register(REG_CLP["MOA"]["OUT_SETPOINT"], int(sum(ug.setpoint for ug in self.ugs)))

                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_EMERG"])[0] and not self.borda_emergencia:
                    self.borda_emergencia = True
                    for ug in self.ugs:
                        ug.verificar_condicionadores(ug)

                elif not self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_EMERG"])[0] and self.borda_emergencia:
                    self.borda_emergencia = False

                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_EMERG_UG1"])[0] and self.ug1.etapa not in (UG_PARADA, UG_PARADA2):
                    self.ug1.verificar_condicionadores()

                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_EMERG_UG2"])[0] and self.ug2.etapa not in (UG_PARADA, UG_PARADA2):
                    self.ug2.verificar_condicionadores()

                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_HABILITA_AUTO"])[0]:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_HABILITA_AUTO"], 1)
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_DESABILITA_AUTO"], 0)
                    self.modo_autonomo = True

                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_DESABILITA_AUTO"])[0]:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_HABILITA_AUTO"], 0)
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_DESABILITA_AUTO"], 1)
                    self.modo_autonomo = False

                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["OUT_BLOCK_UG1"])[0]:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_BLOCK_UG1"], 1)

                elif not self.clp["MOA"].read_coils(REG_CLP["MOA"]["OUT_BLOCK_UG1"])[0]:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_BLOCK_UG1"], 0)

                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["OUT_BLOCK_UG2"])[0]:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_BLOCK_UG2"], 1)

                elif not self.clp["MOA"].read_coils(REG_CLP["MOA"]["OUT_BLOCK_UG2"])[0]:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_BLOCK_UG2"], 0)

            else:
                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_HABILITA_AUTO"])[0]:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_HABILITA_AUTO"], 1)
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_DESABILITA_AUTO"], 0)
                    self.modo_autonomo = True

                self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_EMERG"], 0)
                self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_BLOCK_UG1"], 0)
                self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_BLOCK_UG2"], 0)
                self.clp["MOA"].write_single_register(REG_CLP["MOA"]["OUT_SETPOINT"], int(0))
                self.clp["MOA"].write_single_register(REG_CLP["MOA"]["OUT_TARGET_LEVEL"], int(0))


        except Exception:
            logger.error(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA.")
            logger.debug(traceback.format_exc())
