__version__ = "0.2"
__author__ = "Lucas Lavratti", " Henrique Pfeifer", "Diego Basgal",
__description__ = "Este módulo corresponde a implementação da operação da Usina."

import os
import json
import pytz
import logging
import traceback

import src.dicionarios.dict as dct

import src.adufas as ad
import src.subestacao as se
import src.tomada_agua as tda
import src.unidade_geracao as ug
import src.mensageiro.voip as vp
import src.servico_auxiliar as sa
import src.funcoes.agendamentos as agn
import src.conectores.banco_dados as bd
import src.conectores.servidores as serv

from src.dicionarios.compartilhado import *

from time import sleep, time
from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class Usina:
    def __init__(self, cfg: "dict"=None) -> "None":

        # VERIFICAÇÃO DE ARGUMENTOS
        if None in (cfg):
            raise ValueError("[USN] Não foi possível carregar os arquivos de configuração (\"cfg.json\").")
        else:
            dct_usn['CFG'] = cfg

        # INCIALIZAÇÃO DE OBJETOS DA USINA
        self.clp = serv.Servidores.clp

        dct_usn['BD'] = bd.BancoDados("MOA")
        dct_usn['AGN'] = agn.Agendamentos(self)

        self.ug1 = ug.UnidadeGeracao(1)
        self.ug2 = ug.UnidadeGeracao(2)
        self.ug3 = ug.UnidadeGeracao(3)
        self.ug4 = ug.UnidadeGeracao(4)
        self.ugs: "list[ug.UnidadeGeracao]" = [self.ug1, self.ug2, self.ug3, self.ug4]

        # VARIÁVEIS PÚBLICAS
        self.ts_ultima_norm = self.get_time()

        # FINALIZAÇÃO DO __INIT__
        se.Subestacao.carregar_leituras()
        tda.TomadaAgua.carregar_leituras()
        sa.ServicoAuxiliar.carregar_leituras()

        self.ler_valores()
        self.normalizar_usina()
        self.ajustar_inicializacao()
        self.escrever_valores()


    # PROPRIEDADES/GETTERS
    @property
    def modo_autonomo(self) -> "bool":
        # PROPRIEDADE -> Retorna o modo do MOA.

        return dct_usn['_modo_autonomo']

    @modo_autonomo.setter
    def modo_autonomo(self, var: "bool") -> "None":
        # SETTER -> Atribui o novo valor do modo do MOA e atualiza no Banco de Dados.

        dct_usn['_modo_autonomo'] = var
        dct_usn['BD'].update_modo_moa(var)

    @property
    def tentativas_normalizar(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de Tentativas de Normalização.

        return dct_usn['_tentativas_normalizar']

    @tentativas_normalizar.setter
    def tentativas_normalizar(self, var: "int") -> "None":
        # SETTER -> Atribui o novo valor de Tentativas de Normalização.

        dct_usn['_tentativas_normalizar'] = var


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

        try:
            res = self.clp["SA"].write_single_register(REG_SA["CMD_RESET_ALARMES"], 1)
            res = self.clp["SA"].write_single_register(REG_SA["CMD_RECONHECE_ALARMES"], 1)
            res = self.clp["SA"].write_single_register(REG_SA["CMD_EMERGENCIA_DESLIGAR"], 1)
            return res

        except Exception:
            logger.exception(f"[USN] Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(traceback.format_exc)
            return False


    def acionar_emergencia(self) -> "bool":
        """
        Função para acionamento de emergência geral da Usina.

        Envia o comando de parada de emergência para as Unidades.
        """

        dct_usn['bd_emergencia'] = True
        dct_usn['clp_emergencia'] = True

        try:
            self.clp["SA"].write_single_register(REG_SA["CMD_EMERGENCIA_LIGAR"], 1)

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

        logger.debug(f"[USN] Última tentativa de normalização:   {self.ts_ultima_norm.strftime('%d-%m-%Y %H:%M:%S')}")
        logger.debug("")
        logger.debug(f"[SE]  Tensão Subestação:                  RS -> \"{se.Subestacao.tensao_r.valor/1000:2.1f} kV\" | ST -> \"{se.Subestacao.tensao_s.valor/1000:2.1f} kV\" | TR -> \"{se.Subestacao.tensao_t.valor/1000:2.1f} kV\"")
        logger.debug("")

        if (self.tentativas_normalizar < 3 and (self.get_time() - self.ts_ultima_norm).seconds >= 60) or dct_usn['normalizar_forcado']:
            self.ts_ultima_norm = self.get_time()
            self.tentativas_normalizar += 1
            logger.info(f"[USN] Normalizando... (Tentativa {self.tentativas_normalizar}/3)")
            dct_usn['normalizar_forcado'] = dct_usn['clp_emergencia'] = dct_usn['bd_emergencia'] = False
            self.resetar_emergencia()
            sleep(1)
            se.Subestacao.fechar_dj_linha()
            dct_usn['BD'].update_remove_emergencia()
            return True

        else:
            logger.debug("[USN] A normalização foi executada menos de 1 minutos atrás.")
            sleep(1)
            return False


    def verificar_leituras_periodicas(self) -> "None":
        """
        Função de temporizador com leituras para alertas de manutenção.

        Chama os métodos de leitura de objetos da Usina e Unidades de Geração.
        Caso haja alguma leitura fora do esperado, é enviado o alerta via
        WhatsApp ou Voip.
        """

        while True:
            # sa.ServicoAuxiliar.verificar_leituras()
            # se.Subestacao.verificar_leituras()
            # tda.TomadaAgua.verificar_leituras()

            # for ug in self.ugs:
            #     ug.verificar_leituras()

            if True in (dct.voip[r][0] for r in dct.voip):
                vp.Voip.acionar_chamada()
                pass
            sleep(max(0, (time() + 1800) - time()))


    def verificar_condicionadores(self) -> "int":
        flag = CONDIC_IGNORAR

        lst_se = se.Subestacao.verificar_condicionadores()
        lst_tda = tda.TomadaAgua.verificar_condicionadores()
        lst_sa = sa.ServicoAuxiliar.verificar_condicionadores()

        trafos_sa = sa.ServicoAuxiliar.verificar_trafos_sa()

        if trafos_sa:
            return CONDIC_INDISPONIBILIZAR

        condics = [condic for condics in [lst_sa, lst_se, lst_tda] for condic in condics]

        for condic in condics:
            if condic.gravidade == CONDIC_INDISPONIBILIZAR:
                return CONDIC_INDISPONIBILIZAR

            elif condic.gravidade == CONDIC_NORMALIZAR:
                flag = CONDIC_NORMALIZAR

        return flag


    # FUNÇÕES PARA CÁLCULOS E AJUSTES DE OERAÇÃO

    def ajustar_ie_padrao(self) -> "float":
        """
        Função para ajustar o valor do IE.
        """

        return sum(ug.leitura_potencia for ug in self.ugs) / dct_usn['CFG']["pot_alvo_usina"]


    def ajustar_inicializacao(self) -> "None":
        """
        Funçao para ajustar variáveis de cálculos de controle de operação, na inicialização
        da Classe da Usina.
        """

        for ug in self.ugs:
            if ug.etapa_atual == UG_SINCRONIZADA:
                dct_usn['ug_operando'] += 1

        dct_usn['__split1'] = True if dct_usn['ug_operando'] == 1 else False
        dct_usn['__split2'] = True if dct_usn['ug_operando'] == 2 else False
        dct_usn['__split3'] = True if dct_usn['ug_operando'] == 3 else False
        dct_usn['__split4'] = True if dct_usn['ug_operando'] == 4 else False

        dct_usn['controle_ie'] = self.ajustar_ie_padrao()

        # self.clp["MOA"].write_single_coil(REG_MOA["MOA"]["OUT_BLOCK_UG1"], 0)
        # self.clp["MOA"].write_single_coil(REG_MOA["MOA"]["OUT_BLOCK_UG2"], 0)
        # self.clp["MOA"].write_single_coil(REG_MOA["MOA"]["OUT_BLOCK_UG3"], 0)
        # self.clp["MOA"].write_single_coil(REG_MOA["MOA"]["OUT_BLOCK_UG4"], 0)


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

        if dct_tda['nivel_montante'].valor >= dct_usn['CFG']["nv_vert_max"]:
            logger.debug("[TDA] Nível montante em Vertimento.")
            logger.debug("")
            logger.debug(f"[TDA] NÍVEL -> Alvo:                      {dct_usn['CFG']['nv_alvo']:0.3f}")
            logger.debug(f"[TDA]          Leitura:                   {dct_tda['nivel_montante'].valor:0.3f}")
            logger.debug(f"[TDA]          Máximo Vertimento:         {dct_usn['CFG']['nv_vert_max']:0.3f}")
            logger.debug("")

            if dct_tda['nivel_montante_anterior'] >= NIVEL_MAXIMORUM:
                logger.critical(f"[TDA] Nivel montante ({dct_tda['nivel_montante_anterior']:3.2f}) atingiu o maximorum!")
                return NV_EMERGENCIA

            else:
                dct_usn['controle_i'] = 0.9
                dct_usn['controle_ie'] = 0.5
                self.ajustar_potencia(dct_usn['CFG']["pot_maxima_usina"])

                for ug in self.ugs: ug.step()

                ad.Adufas.controlar_comportas()

        elif dct_tda['nivel_montante'].valor <= dct_usn['CFG']["nv_minimo"] and not dct_tda['aguardando_reservatorio']:
            logger.debug("[TDA] Nível montante abaixo do mínimo.")
            logger.debug(f"[TDA]          Leitura:                   {dct_tda['nivel_montante'].valor:0.3f}")
            logger.debug("")
            dct_tda['aguardando_reservatorio'] = True
            self.distribuir_potencia(0)

            for ug in self.ugs: ug.step()

            if dct_tda['nivel_montante_anterior'] <= NIVEL_FUNDO_RESERVATORIO:
                logger.critical(f"[TDA] Nivel montante ({dct_tda['nivel_montante_anterior']:3.2f}) atingiu o fundo do reservatorio!")
                return NV_EMERGENCIA

        elif dct_tda['aguardando_reservatorio']:
            if dct_tda['nivel_montante'].valor >= dct_usn['CFG']["nv_alvo"]:
                logger.debug("[TDA] Nível montante dentro do limite de operação.")
                logger.debug(f"[TDA]          Leitura:                   {dct_tda['nivel_montante'].valor:0.3f}")
                logger.debug("")
                dct_tda['aguardando_reservatorio'] = False

        else:
            if dct_tda['nivel_montante'].valor >= dct_usn['CFG']["nv_maximo"]:
                logger.debug("[TDA] Nível montante em Vertimento.")
                logger.debug("")

            self.controlar_potencia()

            for ug in self.ugs: ug.step()

            for cp in ad.Adufas.cps:
                cp.setpoint = 0
                cp.enviar_setpoint(0)

        return NV_NORMAL


    def controlar_potencia(self) -> "None":
        """
        Função para calcular PID (Proporcional, Integral e Derivativo), para controle de potência
        das Unidades a partir da leitura de Nível Montante.
        """

        logger.debug(f"[TDA] NÍVEL -> Alvo:                      {dct_usn['CFG']['nv_alvo']:0.3f}")
        logger.debug(f"[TDA]          Leitura:                   {dct_tda['nivel_montante'].valor:0.3f}")

        dct_usn['controle_p'] = dct_usn['CFG']["kp"] * dct_tda['erro_nivel']

        if dct_usn['_pid_inicial'] == -1:
            dct_usn['controle_i'] = max(min(dct_usn['controle_ie'] - dct_usn['controle_p'], 0.9), 0)
            dct_usn['_pid_inicial'] = 0
        else:
            dct_usn['controle_i'] = max(min((dct_usn['CFG']["ki"] * dct_tda['erro_nivel']) + dct_usn['controle_i'], 0.9), 0)
            dct_usn['controle_d'] = dct_usn['CFG']["kd"] * (dct_tda['erro_nivel'] - dct_tda['erro_nivel_anterior'])

        saida_pid = (dct_usn['controle_p'] + dct_usn['controle_i'] + min(max(-0.07, dct_usn['controle_d']), 0.07))

        logger.debug("")
        logger.debug(f"[USN] PID   -> P + I + D:                 {saida_pid:0.3f}")
        logger.debug(f"[USN] P:                                  {dct_usn['controle_p']:0.3f}")
        logger.debug(f"[USN] I:                                  {dct_usn['controle_i']:0.3f}")
        logger.debug(f"[USN] D:                                  {dct_usn['controle_d']:0.3f}")

        dct_usn['controle_ie'] = max(min(saida_pid + dct_usn['controle_ie'] * dct_usn['CFG']["kie"], 1), 0)

        logger.debug(f"[USN] IE:                                 {dct_usn['controle_ie']:0.3f}")
        logger.debug(f"[USN] ERRO:                               {dct_tda['erro_nivel']}")
        logger.debug("")

        if dct_tda['nivel_montante_anterior'] >= (dct_usn['CFG']["nv_vert_max"] + 0.03):
            dct_usn['controle_ie'] = 1
            dct_usn['controle_i'] = 1 - dct_usn['controle_p']

        if dct_tda['nivel_montante_anterior'] <= (dct_usn['CFG']["nv_minimo"] + 0.03):
            dct_usn['controle_ie'] = min(dct_usn['controle_ie'], 0.3)
            dct_usn['controle_i'] = 0

        pot_alvo = max(min(round(dct_usn['CFG']["pot_maxima_usina"] * dct_usn['controle_ie'], 5), dct_usn['CFG']["pot_maxima_usina"]), dct_usn['CFG']["pot_minima_ugs"])

        pot_alvo = self.ajustar_potencia(pot_alvo)


    def ajustar_potencia(self, pot_alvo: "float") -> "float":
        """
        Função para ajustar a potência de controle após do cálculo do PID.
        """

        if dct_usn['_pot_alvo_anterior'] == -1:
            dct_usn['_pot_alvo_anterior'] = pot_alvo

        if pot_alvo < 0.1:
            for ug in self.ugs:
                ug.setpoint = 0
            return 0

        pot_medidor = se.Subestacao.medidor_usina.valor

        logger.debug(f"[USN] Potência no medidor:                {pot_medidor:0.3f}")

        pot_aux = dct_usn['CFG']["pot_alvo_usina"] - (dct_usn['CFG']["pot_maxima_usina"] - dct_usn['CFG']["pot_alvo_usina"])
        pot_medidor = max(pot_aux, min(pot_medidor, dct_usn['CFG']["pot_maxima_usina"]))

        if pot_medidor > dct_usn['CFG']["pot_alvo_usina"]:
            pot_alvo = dct_usn['_pot_alvo_anterior'] * (1 - ((pot_medidor - dct_usn['CFG']["pot_alvo_usina"]) / dct_usn['CFG']["pot_alvo_usina"]))

        dct_usn['_pot_alvo_anterior'] = pot_alvo

        logger.debug(f"[USN] Distribuindo Potência Alvo:         {pot_alvo:0.3f}")

        self.distribuir_potencia(pot_alvo)


    def distribuir_potencia(self, pot_alvo: "float") -> "None":
        """
        Função para distribuição de potência, após cálculos de controle/ajustes.

        Chama a função de controle de unidades disponíveis e determina através de janelas
        de potência para entrada ou retirada de uma Unidade.
        """

        ugs: "list[ug.UnidadeGeracao]" = self.verificar_ugs_disponiveis()

        logger.debug("")

        ajuste_manual = 0

        for ug in self.ugs:
            if ug.manual:
                ajuste_manual += ug.leitura_potencia
            else:
                dct_usn['pot_disp'] += ug.setpoint_maximo

            ug.pot_alvo_usina = pot_alvo - ajuste_manual

        if ugs is None or not len(ugs):
            return

        sp = (pot_alvo - ajuste_manual) / dct_usn['CFG']["pot_maxima_usina"]

        dct_usn['__split1'] = True if sp > (0) else dct_usn['__split1']
        dct_usn['__split2'] = True if sp > ((dct_usn['CFG']["pot_maxima_ugs"] / dct_usn['CFG']["pot_maxima_usina"]) + dct_usn['CFG']["margem_pot_critica"]) else dct_usn['__split2']
        dct_usn['__split3'] = True if sp > (2 * (dct_usn['CFG']["pot_maxima_ugs"] / dct_usn['CFG']["pot_maxima_usina"]) + dct_usn['CFG']["margem_pot_critica"]) else dct_usn['__split3']
        dct_usn['__split4'] = True if sp > (3 * (dct_usn['CFG']["pot_maxima_ugs"] / dct_usn['CFG']["pot_maxima_usina"]) + dct_usn['CFG']["margem_pot_critica"]) else dct_usn['__split4']

        dct_usn['__split4'] = False if sp < (3 * (dct_usn['CFG']["pot_maxima_ugs"] / dct_usn['CFG']["pot_maxima_usina"]) - dct_usn['CFG']["margem_pot_critica"]) else dct_usn['__split4']
        dct_usn['__split3'] = False if sp < (2 * (dct_usn['CFG']["pot_maxima_ugs"] / dct_usn['CFG']["pot_maxima_usina"]) - dct_usn['CFG']["margem_pot_critica"]) else dct_usn['__split3']
        dct_usn['__split2'] = False if sp < ((dct_usn['CFG']["pot_maxima_ugs"] / dct_usn['CFG']["pot_maxima_usina"]) - dct_usn['CFG']["margem_pot_critica"]) else dct_usn['__split2']
        dct_usn['__split1'] = False if sp < (dct_usn['CFG']["pot_minima_ugs"] / dct_usn['CFG']["pot_maxima_usina"]) else dct_usn['__split1']

        logger.debug(f"[USN] SP Geral:                           {sp}")

        if len(ugs) == 4:
            if dct_usn['__split4']:
                logger.debug("[USN] Split:                              4")

                for ug in ugs: 
                    ug.setpoint = sp * ug.setpoint_maximo

            elif dct_usn['__split3']:
                logger.debug("[USN] Split:                              4 -> \"3B\"")

                ugs[0].setpoint = (sp * (4/3)) * ugs[0].setpoint_maximo
                ugs[1].setpoint = (sp * (4/3)) * ugs[1].setpoint_maximo
                ugs[2].setpoint = (sp * (4/3)) * ugs[2].setpoint_maximo
                ugs[3].setpoint = 0

            elif dct_usn['__split2']:
                logger.debug("[USN] Split:                              4 -> \"2B\"")

                ugs[0].setpoint = (sp * (4/2)) * ugs[0].setpoint_maximo
                ugs[1].setpoint = (sp * (4/2)) * ugs[1].setpoint_maximo
                ugs[2].setpoint = 0
                ugs[3].setpoint = 0

            elif dct_usn['__split1']:
                logger.debug("[USN] Split:                              4 -> \"1B\"")

                ugs[0].setpoint = sp * 4 * ugs[0].setpoint_maximo
                ugs[1].setpoint = 0
                ugs[2].setpoint = 0
                ugs[3].setpoint = 0

            else:
                for ug in ugs: ug.setpoint = 0

            logger.debug("")
            for ug in ugs: logger.debug(f"[UG{ug.id}] SP    <-                            {int(ug.setpoint)}")

        elif len(ugs) == 3:
            if dct_usn['__split3']:
                logger.debug("[USN] Split:                              3")

                ugs[0].setpoint = (sp * (4/3)) * ugs[0].setpoint_maximo
                ugs[1].setpoint = (sp * (4/3)) * ugs[1].setpoint_maximo
                ugs[2].setpoint = (sp * (4/3)) * ugs[2].setpoint_maximo

            elif dct_usn['__split2']:
                logger.debug("[USN] Split:                              3 -> \"2B\"")

                ugs[0].setpoint = (sp * (4/2)) * ugs[0].setpoint_maximo
                ugs[1].setpoint = (sp * (4/2)) * ugs[1].setpoint_maximo
                ugs[2].setpoint = 0

            elif dct_usn['__split1']:
                logger.debug("[USN] Split:                              3 -> \"1B\"")

                ugs[0].setpoint = sp * 4 * ugs[0].setpoint_maximo
                ugs[1].setpoint = 0
                ugs[2].setpoint = 0

            else:
                for ug in ugs: ug.setpoint = 0

            logger.debug("")
            for ug in ugs: logger.debug(f"[UG{ug.id}] SP    <-                            {int(ug.setpoint)}")

        elif len(ugs) == 2:
            if dct_usn['__split2']:
                logger.debug("[USN] Split:                              2")

                ugs[0].setpoint = (sp * (4/2)) * ugs[0].setpoint_maximo
                ugs[1].setpoint = (sp * (4/2)) * ugs[0].setpoint_maximo

            elif dct_usn['__split1']:
                logger.debug("[USN] Split:                              2 -> \"1B\"")

                ugs[0].setpoint = sp * 4 * ugs[0].setpoint_maximo
                ugs[1].setpoint = 0

            else:
                for ug in ugs: ug.setpoint = 0

            logger.debug("")
            for ug in ugs: logger.debug(f"[UG{ug.id}] SP    <-                            {int(ug.setpoint)}")

        elif len(ugs) == 1:
            logger.debug("[USN] Split:                              1")

            ugs[0].setpoint = sp * 4 * ugs[0].setpoint_maximo

            logger.debug("")
            logger.debug(f"[UG{ugs[0].id}] SP    <-                            {int(ugs[0].setpoint)}")


    def verificar_ugs_disponiveis(self) -> "list[ug.UnidadeGeracao]":
        """
        Função para verificar leituras/condições específicas e determinar a Prioridade das Unidades.
        """

        ls = [ug for ug in self.ugs if ug.disponivel and not ug.etapa == UG_PARANDO]

        if dct_usn['modo_prioridade_ugs'] in (UG_PRIORIDADE_1, UG_PRIORIDADE_2, UG_PRIORIDADE_3, UG_PRIORIDADE_4):
            return sorted(ls, key=lambda y: (-1 * y.prioridade, -1 * y.etapa_atual, -1 * y.leitura_potencia, -1 * y.setpoint))
        else:
            return sorted(ls, key=lambda y: (-1 * y.etapa_atual, y.leitura_horimetro, -1 * y.leitura_potencia, -1 * y.setpoint))


    # FUNÇÕES DE CONTROLE DE DADOS

    def ler_valores(self) -> "None":
        """
        Função para leitura e atualização de parâmetros de operação através de
        Banco de Dados da Interface WEB.
        """

        serv.Servidores.ping_clients()
        tda.TomadaAgua.atualizar_montante()

        parametros = dct_usn['BD'].get_parametros_usina()

        self.atualizar_valores_cfg(parametros)
        self.atualizar_valores_banco(parametros)

        for ug in self.ugs:
            ug.atualizar_limites(parametros)


    def atualizar_valores_banco(self, parametros: "dict") -> "None":
        """
        Função para atualização de valores de Banco de Dados.
        """

        try:
            if int(parametros["emergencia_acionada"]) == 1 and not dct_usn['bd_emergencia']:
                dct_usn['bd_emergencia'] = True
                logger.info(f"[USN] Emergência:                         \"{'Ativada'}\"")

            elif int(parametros["emergencia_acionada"]) == 0 and dct_usn['bd_emergencia']:
                dct_usn['bd_emergencia'] = False
                logger.info(f"[USN] Emergência:                         \"{'Desativada'}\"")

            if int(parametros["modo_autonomo"]) == 1 and not self.modo_autonomo:
                self.modo_autonomo = True
                logger.info(f"[USN] Modo autônomo:                      \"{'Ativado'}\"")

            elif int(parametros["modo_autonomo"]) == 0 and self.modo_autonomo:
                self.modo_autonomo = False
                logger.info(f"[USN] Modo autônomo:                      \"{'Desativado'}\"")

            if dct_usn['modo_prioridade_ugs'] != int(parametros["modo_de_escolha_das_ugs"]):
                dct_usn['modo_prioridade_ugs'] = int(parametros["modo_de_escolha_das_ugs"])
                logger.info(f"[USN] Modo de prioridade das UGs:         \"{UG_STR_DCT_PRIORIDADE[dct_usn['modo_prioridade_ugs']]}\"")

        except Exception:
            logger.error(f"[USN] Houve um erro ao ler e atualizar os parâmetros do Banco de Dados.")
            logger.debug(traceback.format_exc())


    def atualizar_valores_cfg(self, parametros: "dict") -> "None":
        """
        Função para atualização de valores de operação do arquivo cfg.json.
        """

        try:
            dct_usn['CFG']["kp"] = float(parametros["kp"])
            dct_usn['CFG']["ki"] = float(parametros["ki"])
            dct_usn['CFG']["kd"] = float(parametros["kd"])
            dct_usn['CFG']["kie"] = float(parametros["kie"])

            dct_usn['CFG']["ad_kp"] = float(parametros["ad_kp"])
            dct_usn['CFG']["ad_ki"] = float(parametros["ad_ki"])

            dct_usn['CFG']["nv_alvo"] = float(parametros["nv_alvo"])
            dct_usn['CFG']["nv_minimo"] = float(parametros["nv_minimo"])
            dct_usn['CFG']["nv_maximo"] = float(parametros["nv_maximo"])
            dct_usn['CFG']["ad_nv_alvo"] = float(parametros["ad_nv_alvo"])

            dct_usn['CFG']["pot_minima_ugs"] = float(parametros["pot_minima_ugs"])
            dct_usn['CFG']["pot_maxima_ugs"] = float(parametros["pot_maxima_ugs"])
            dct_usn['CFG']["pot_maxima_usina"] = float(parametros["pot_maxima_usina"])
            dct_usn['CFG']["margem_pot_critica"] = float(parametros["margem_pot_critica"])

            with open(os.path.join(os.path.dirname("/opt/operacao-autonoma/src/dicionarios/"), 'cfg.json'), 'w') as file:
                json.dump(dct_usn['CFG'], file)

        except Exception:
            logger.error(f"[USN] Houve um erro ao atualizar o arquivo de configuração \"cfg.json\".")
            logger.debug(traceback.format_exc())


    def escrever_valores(self) -> "None":
        """
        Função para escrita de valores de operação nos Bancos do módulo do Django
        e Debug.
        """

        try:
            dct_usn['BD'].update_valores_usina([
                self.get_time().strftime("%Y-%m-%d %H:%M:%S"),
                1 if dct_tda['aguardando_reservatorio'] else 0,
                dct_tda['nivel_montante'].valor,
                self.ug1.leitura_potencia,
                self.ug1.setpoint,
                self.ug1.etapa_atual,
                self.ug2.leitura_potencia,
                self.ug2.setpoint,
                self.ug2.etapa_atual,
                self.ug3.leitura_potencia,
                self.ug3.setpoint,
                self.ug3.etapa_atual,
                self.ug4.leitura_potencia,
                self.ug4.setpoint,
                self.ug4.etapa_atual
            ])

        except Exception:
            logger.error(f"[USN] Houve um erro ao atualizar os valores de controle de operação no Banco de Dados.")
            logger.debug(traceback.format_exc())

        try:
            dct_usn['BD'].update_debug([
                time(),
                1 if self.modo_autonomo else 0,
                dct_tda['nivel_montante'].valor,
                dct_tda['erro_nivel'],
                self.ug1.setpoint,
                self.ug1.leitura_potencia,
                self.ug1.codigo_state,
                self.ug2.setpoint,
                self.ug2.leitura_potencia,
                self.ug2.codigo_state,
                self.ug3.setpoint,
                self.ug3.leitura_potencia,
                self.ug3.codigo_state,
                self.ug4.setpoint,
                self.ug4.leitura_potencia,
                self.ug4.codigo_state,
                ad.Adufas.cp1.setpoint,
                ad.Adufas.cp1.posicao,
                ad.Adufas.cp2.setpoint,
                ad.Adufas.cp2.posicao,
                ad.Adufas.cp1.controle_p,
                ad.Adufas.cp1.controle_i,
                ad.Adufas.cp2.controle_p,
                ad.Adufas.cp2.controle_i,
                dct_usn['controle_p'],
                dct_usn['controle_i'],
                dct_usn['controle_d'],
                dct_usn['controle_ie'],
                dct_usn['CFG']["kp"],
                dct_usn['CFG']["ki"],
                dct_usn['CFG']["kd"],
                dct_usn['CFG']["kie"],
            ])

        except Exception:
            logger.error(f"[USN] Houve um erro ao atualizar valores DEBUG do controle de potência no Banco de Dados.")
            logger.debug(traceback.format_exc())


    def heartbeat(self) -> "None":
        """
        Função para controle do CLP - MOA.

        Esta função tem como objetivo enviar comandos de controle/bloqueio para
        os CLPs da Usina e também, ativação/desativação do MOA através de chaves
        seletoras no painel do Sistema Auxiliar.
        """
        return

        try:
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["PAINEL_LIDO"], 1)
            self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["MOA_OUT_MODE"], 1 if self.modo_autonomo else 0)
            self.clp["MOA"].write_single_register(REG_CLP["MOA"]["MOA_OUT_STATUS"], dct_usn['estado_moa'])

            if self.modo_autonomo:
                self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_EMERG"], 1 if dct_usn['clp_emergencia'] else 0)
                self.clp["MOA"].write_multiple_registers(REG_CLP["MOA"]["OUT_SETPOINT"], int(sum(ug.setpoint for ug in self.ugs)))
                self.clp["MOA"].write_multiple_registers(REG_CLP["MOA"]["OUT_TARGET_LEVEL"], int((dct_usn['CFG']["nv_alvo"] - 800) * 1000))

                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_HABILITA_AUTO"])[0] == 1:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_HABILITA_AUTO"], 1)
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_DESABILITA_AUTO"], 0)
                    self.modo_autonomo = True

                elif self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_DESABILITA_AUTO"])[0] == 1:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_HABILITA_AUTO"], 0)
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_DESABILITA_AUTO"], 1)
                    self.modo_autonomo = False

                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_EMERG"])[0] == 1 and not dct_usn['borda_emergencia']:
                    for ug in self.ugs:
                        ug.verificar_condicionadores()

                elif self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_EMERG"])[0] == 0 and dct_usn['borda_emergencia']:
                    dct_usn['borda_emergencia'] = False

                for ug in self.ugs:
                    if self.clp["MOA"].read_coils(REG_CLP["MOA"][f"IN_EMERG_UG{ug.id}"])[0] == 1:
                        ug.verificar_condicionadores()

                    if self.clp["MOA"].read_coils(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"])[0] == 1:
                        self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"], 1)

                    elif self.clp["MOA"].read_coils(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"])[0] == 0:
                        self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"], 0)

            elif not self.modo_autonomo:
                if self.clp["MOA"].read_coils(REG_CLP["MOA"]["IN_HABILITA_AUTO"])[0] == 1:
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_HABILITA_AUTO"], 1)
                    self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["IN_DESABILITA_AUTO"], 0)
                    self.modo_autonomo = True

                self.clp["MOA"].write_single_coil(REG_CLP["MOA"]["OUT_EMERG"], 0)
                self.clp["MOA"].write_single_register(REG_CLP["MOA"]["OUT_SETPOINT"], 0)
                self.clp["MOA"].write_single_register(REG_CLP["MOA"]["OUT_TARGET_LEVEL"], 0)
                [self.clp["MOA"].write_single_coil(REG_CLP["MOA"][f"OUT_BLOCK_UG{ug.id}"], 0) for ug in self.ugs]

        except Exception:
            logger.error(f"[USN] Houve um erro ao tentar escrever valores modbus no CLP MOA.")
            logger.debug(traceback.format_exc())
