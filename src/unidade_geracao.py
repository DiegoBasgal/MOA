__version__ = "0.2"
__author__ = "Lucas Lavratti", "Henrique Pfeifer", "Diego Basgal"
__description__ = "Este módulo corresponde a implementação das Unidades de Geração."

import pytz
import logging
import traceback
import threading

import src.subestacao as se
import src.dicionarios.dict as d
import src.funcoes.leitura as lei
import src.funcoes.escrita as esc
import src.funcoes.condicionadores as c
import src.conectores.servidores as serv

from time import time, sleep
from datetime import datetime

from src.dicionarios.comp import *
from src.dicionarios.reg import *
from src.maquinas_estado.ug import *


logger = logging.getLogger("logger")
debug_log = logging.getLogger("debug")


class UnidadeGeracao:
    def __init__(self, id: "int"):

        # VERIFICAÇÃO DE ARGUMENTOS
        if id <= 0:
            logger.error(f"[UG{self.id}] A Unidade não pode ser instanciada com o ID menor que \"0\" ou vazio.")
            raise ValueError
        else:
            self.__id = id

        self.clp = serv.Servidores.clp

        # LEITURAS MB
        dct_ug[f'UG{self.id}']['potencia'] = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["POT_ATIVA_MEDIA"],
            descricao=f"[UG{self.id}] Leitura Potência"
        )
        dct_ug[f'UG{self.id}']['etapa_atual'] = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["OPER_ETAPA_ATUAL"],
            descricao=f"[UG{self.id}] Leitura Etapa"
        )
        dct_ug[f'UG{self.id}']['etapa_alvo'] = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["OPER_ETAPA_ALVO"],
            descricao=f"[UG{self.id}] Leitura Etapa"
        )
        dct_ug[f'UG{self.id}']['horimetro'] = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["HORIM_ELETR_LOW"],
            descricao=f"[UG{self.id}] Leitura Horímetro"
        )
        dct_ug[f'UG{self.id}']['posicao_distribuidor'] = lei.LeituraModbus(
            self.clp[f"UG{self.id}"],
            REG_UG[f"UG{self.id}"]["REG_V_DISTRIBUIDOR"],
            escala=0.001,
            descricao=f"[UG{self.id}] Leitura Posição Distribuidor"
        )
        dct_ug[f'UG{self.id}']['uhta'][f'UHTA0{1 if self.id in (1,2) else 2}'] = lei.LeituraModbusBit(
            self.clp['TDA'],
            REG_TDA[f'UHTA0{1 if self.id in (1,2) else 2}_OPERACIONAL'],
            descricao=f'[TDA] UHTA0{1 if self.id in (1,2) else 2} Disponível'
        )

        # VARIÁVEIS
        dct_ug[f'UG{self.id}']['setpoint_minimo'] = dct_usn['CFG']["pot_minima_ugs"]
        dct_ug[f'UG{self.id}']['setpoint_maximo'] = dct_usn['CFG'][f"pot_maxima_ug{self.id}"]

        dct_ug[f'UG{self.id}']['ts_auxiliar'] = self.get_time()

        dct_ug[f'UG{self.id}']['next_state'] = StateDisponivel(self)

        # FINALIZAÇÃO DO __INIT__
        self.carregar_leituras()


    @property
    def id(self) -> "int":
        # PROPRIEDADE -> Retrona o ID da Unidade.

        return self.__id

    @property
    def potencia(self) -> "int":
        # PROPRIEDADE -> Retorna a Leitura de Potência da Unidade.

        return dct_ug[f'UG{self.id}']['potencia'].valor

    @property
    def manual(self) -> "bool":
        # PROPRIEDADE -> Verifica se a Unidade está em modo Manual.

        return isinstance(dct_ug[f'UG{self.id}']['next_state'], StateManual)

    @property
    def restrito(self) -> "bool":
        # PROPRIEDADE -> Verifica se a Unidade está em modo Restrito.

        return isinstance(dct_ug[f'UG{self.id}']['next_state'], StateRestrito)

    @property
    def disponivel(self) -> "bool":
        # PROPRIEDADE -> Verifica se a Unidade está em modo Disponível.

        return isinstance(dct_ug[f'UG{self.id}']['next_state'], StateDisponivel)

    @property
    def indisponivel(self) -> "bool":
        # PROPRIEDADE -> Verifica se a Unidade está em modo Indisponível.

        return isinstance(dct_ug[f'UG{self.id}']['next_state'], StateIndisponivel)

    @property
    def uhta_disponivel(self) -> "bool":
        # PROPRIEDADE -> Retorna se a Unidade Hidráulica da Comporta está Disponível

        return dct_ug[f'UG{self.id}']['uhta'][f'UHTA0{1 if self.id in (1,2) else 2}'].valor

    @property
    def etapa(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de etapa tratado

        if dct_ug[f'UG{self.id}']['etapa_atual'].valor == 0 and dct_ug[f'UG{self.id}']['etapa_alvo'].valor == 0:
            return UG_PARADA

        elif dct_ug[f'UG{self.id}']['etapa_atual'].valor == 5 and dct_ug[f'UG{self.id}']['etapa_alvo'].valor == 5:
            return UG_SINCRONIZADA

        elif dct_ug[f'UG{self.id}']['etapa_atual'].valor >= 0 and dct_ug[f'UG{self.id}']['etapa_alvo'].valor == 5:
            return UG_SINCRONIZANDO

        elif dct_ug[f'UG{self.id}']['etapa_atual'].valor <= 5 and dct_ug[f'UG{self.id}']['etapa_alvo'].valor == 0:
            return UG_PARANDO

    @property
    def setpoint(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de setpoint da Unidade.

        return dct_ug[f'UG{self.id}']['setpoint']

    @setpoint.setter
    def setpoint(self, var: "int") -> "None":
        # SETTER -> Atribui o novo valor de setpoint da Unidade.

        if var < dct_usn['CFG']["pot_minima_ugs"]:
            dct_ug[f'UG{self.id}']['setpoint'] = dct_usn['CFG']["pot_minima_ugs"] if dct_ug[f'UG{self.id}']['manter_unidade'] else 0

        elif var > dct_usn['CFG'][f"pot_maxima_ug{self.id}"]:
            dct_ug[f'UG{self.id}']['setpoint'] = dct_usn['CFG'][f"pot_maxima_ug{self.id}"]

        else:
            dct_ug[f'UG{self.id}']['setpoint'] = int(var)

    @property
    def tentativas_normalizacao(self) -> "int":
        # PROPRIEDADE -> Retorna o valor de tentativas de normalização da Unidade.

        return dct_ug[f'UG{self.id}']['tentativas_normalizacao']

    @tentativas_normalizacao.setter
    def tentativas_normalizacao(self, var: "int") -> "None":
        # SETTER -> Atribui o novo valor de tentativas de normalização da Unidade.

        if 0 <= var and var == int(var):
            self._tentativas_de_normalizacao = int(var)


    # FUNÇÕES
    @staticmethod
    def get_time() -> "datetime":
        """
        Função para obter data e hora atual.
        """

        return datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)


    def forcar_estado_manual(self) -> "None":
        """
        Função para forçar o estado manual na Unidade.
        """

        dct_ug[f'UG{self.id}']['next_state'] = StateManual(self)


    def forcar_estado_restrito(self) -> "None":
        """
        Função para forçar o estado restrito na Unidade.
        """

        dct_ug[f'UG{self.id}']['next_state'] = StateRestrito(self)


    def forcar_estado_indisponivel(self) -> "None":
        """
        Função para forçar o estado indisponível na Unidade.
        """

        dct_ug[f'UG{self.id}']['next_state'] = StateIndisponivel(self)


    def forcar_estado_disponivel(self) -> "None":
        """
        Função para forçar o estado disponível na Unidade.
        """

        self.reconhece_reset_alarmes()
        dct_ug[f'UG{self.id}']['next_state'] = StateDisponivel(self)


    def iniciar_ultimo_estado(self) -> "None":
        """
        Função para verificar e atribuir o último estado da Unidade, antes
        da interrupção da última execução do MOA.

        Realiza a consulta no Banco de Dados e atribui o último estado comparando
        com o valor das constantes de Estado.
        """

        estado = dct_usn['BD'].get_ultimo_estado_ug(self.id)[0]

        if estado == None:
            dct_ug[f'UG{self.id}']['next_state'] = StateDisponivel(self)
        else:
            if estado == UG_SM_MANUAL:
                dct_ug[f'UG{self.id}']['next_state'] = StateManual(self)
            elif estado == UG_SM_DISPONIVEL:
                dct_ug[f'UG{self.id}']['next_state'] = StateDisponivel(self)
            elif estado == UG_SM_RESTRITA:
                dct_ug[f'UG{self.id}']['next_state'] = StateRestrito(self)
            elif estado == UG_SM_INDISPONIVEL:
                dct_ug[f'UG{self.id}']['next_state'] = StateIndisponivel(self)
            else:
                logger.debug("")
                logger.error(f"[UG{self.id}] Não foi possível ler o último estado da Unidade")
                logger.info(f"[UG{self.id}] Acionando estado \"Manual\".")
                dct_ug[f'UG{self.id}']['next_state'] = StateManual(self)


    def step(self) -> "None":
        """
        Função principal de passo da Unidade.

        Serve como principal chamada para controle das Unidades da máquina de estados.
        """

        try:
            logger.debug("")
            logger.debug(f"[UG{self.id}] Step  -> Unidade:                   \"{UG_SM_STR_DCT[dct_ug[f'UG{self.id}']['codigo_state']]}\"")
            logger.debug(f"[UG{self.id}]          Etapa:                     \"{UG_STR_DCT_ETAPAS[self.etapa]}\" (Atual: {dct_ug[f'UG{self.id}']['etapa_atual'].valor} | Alvo: {dct_ug[f'UG{self.id}']['etapa_alvo'].valor})")

            if self.etapa == UG_SINCRONIZADA:
                logger.debug(f"[UG{self.id}]          Leituras de Potência:")
                logger.debug(f"[UG{self.id}]          - \"Ativa\":                 {dct_ug[f'UG{self.id}']['potencia'].valor} kW")

            # self.atualizar_modbus_moa()
            dct_ug[f'UG{self.id}']['next_state'] = dct_ug[f'UG{self.id}']['next_state'].step()

        except Exception:
            logger.error(f"[UG{self.id}] Erro na execução da máquina de estados da Unidade -> \"step\".")
            logger.debug(traceback.format_exc())


    def atualizar_modbus_moa(self) -> "None":
        """
        Função para atualização do estado da Unidade no CLP - MOA.
        """

        try:
            self.clp["MOA"].write_single_coil(REG_MOA["MOA"][f"OUT_ETAPA_UG{self.id}"], dct_ug[f"UG{self.id}"]["etapa_atual"])
            self.clp["MOA"].write_single_coil(REG_MOA["MOA"][f"OUT_STATE_UG{self.id}"], dct_ug[f'UG{self.id}']['codigo_state'])

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível escrever os valores no CLP MOA.")
            logger.debug(traceback.format_exc())


    def partir(self) -> "None":
        """
        Função para acionamento do comando de partida da Unidade.
        """

        try:
            if not self.uhta_disponivel:
                logger.debug("")
                logger.info(f"[UG{self.id}] A Unidade Hidráulica da Comporta está em Operação.")
                return

            elif self.etapa == UG_PARADA:
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARTIDA\"")

                self.clp[f'UG{self.id}'].write_single_register(REG_UG[f'UG{self.id}']['CMD_OPER_US'], 1)
                self.enviar_setpoint(dct_ug[f'UG{self.id}']['setpoint'])

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível partir a Unidade.")
            logger.debug(traceback.format_exc())


    def parar(self) -> "None":
        """
        Função para acionamento do comando de Parada da Unidade.

        Verifica se a unidade está sincronizada ou sincronizando. Caso esteja, aciona os comandos
        de parada e reconhecimento de alarmes.
        """

        try:
            if self.etapa in (UG_SINCRONIZADA, UG_SINCRONIZANDO):
                logger.info(f"[UG{self.id}]          Enviando comando:          \"PARADA\"")

                self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["CMD_OPER_UP"], 1)
                self.enviar_setpoint(0)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possível parar a Unidade.")
            logger.debug(traceback.format_exc())


    def enviar_setpoint(self, setpoint_kw: "int") -> "bool":
        """
        Função para envio do valor de setpoint para o controle de potência das
        Unidades.

        Controla os limites máximo e mínimo e logo em seguida, envia o valor calculado para a
        Unidade.
        """

        self.popular_listas_sp_pot()

        cont_mppt = 0
        for pot in dct_ug[f'UG{self.id}']['potencias_anteriores']:
            if pot + 300 < setpoint_kw:
                cont_mppt += 1

        debug_log.debug("")
        debug_log.debug("------------------------------------------------------------------------------")
        debug_log.debug(f"\"UG{self.id}\" Setpoint \"Calculado\":             {setpoint_kw:0.0f}")
        debug_log.debug(f"      Lista de Potências Anteriores:    {dct_ug[f'UG{self.id}']['potencias_anteriores']}")
        debug_log.debug("")

        if cont_mppt == dct_ug[f'UG{self.id}']['amostras_pot_mppt'] and dct_usn['CFG']['pot_minima_ugs'] <= setpoint_kw <= dct_usn['CFG']["pot_maxima_ugs"]:

            debug_log.debug(f"      Potência Atual:                   {dct_ug[f'UG{self.id}']['potencia'].valor:0.0f}")
            debug_log.debug(f"      Potência Anterior:                {dct_ug[f'UG{self.id}']['potencias_anteriores'][-1]:0.0f}")
            debug_log.debug("")
            debug_log.debug(f"      Setpoint Anterior:                {dct_ug[f'UG{self.id}']['setpoints_anteriores'][-1]:0.0f}")
            debug_log.debug("")

            setpoint_kw = self.ajustar_mppt(
                [dct_ug[f"UG{self.id}"]["potencia"].valor, dct_ug[f'UG{self.id}']['potencias_anteriores'][-1]],
                [dct_ug[f'UG{self.id}']['setpoints_anteriores'][-1], dct_ug[f'UG{self.id}']['setpoints_anteriores'][-2]],
                [dct_ug[f'UG{self.id}']['posicao_distribuidor'].valor, dct_ug[f'UG{self.id}']['pos_dist_anterior']],
            )

            setpoint_kw = dct_usn['CFG']['pot_minima_ugs'] if setpoint_kw <= dct_usn['CFG']['pot_minima_ugs'] else setpoint_kw

            logger.debug(f"[UG{self.id}]          Enviando setpoint:")
            logger.debug(f"[UG{self.id}]          - \"MPPT\":                  {setpoint_kw:0.0f} kW")

        else:
            logger.debug(f"[UG{self.id}]          Enviando setpoint:         {int(setpoint_kw)} kW")

        dct_ug[f'UG{self.id}']['setpoint'] = int(setpoint_kw)
        dct_ug[f'UG{self.id}']['pos_dist_anterior'] = dct_ug[f'UG{self.id}']['posicao_distribuidor']

        try:
            # res = self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["CMD_SINC_MODO_AUTO_LIGAR"], 1)
            # res = self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["CMD_RT_MTVC_HABILITAR"], 1)
            # res = self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["CMD_RV_CONJUGADO_AUTO_HABILITAR"], 1)
            # res = self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["CMD_CTRL_REATIVO_MODO_VArLIGAR"], 1)
            # res = self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["CMD_CTRL_REATIVO_MODO_FPDESLIGAR"], 1)
            # res = self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["CMD_CTRL_POT_MODO_NIVEL_LIGAR"], 1)
            # res = self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["CMD_CTRL_POT_MODO_NIVEL_DESLIGAR"], 1)
            # res = esc.EscritaModBusBit.escrever_bit(REG_UG[f"UG{self.id}"]["CTRL_POT_MODO_POT"], valor=1)

            # res = esc.EscritaModBusBit.escrever_bit(REG_UG[f"UG{self.id}"]["CTRL_REAT_MODO_VAR"], valor=0)
            # res = esc.EscritaModBusBit.escrever_bit(REG_UG[f"UG{self.id}"]["CRTL_REATIVO_SP_REATIVO"], valor=0)

            res = self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["CRTL_POT_ALVO"], int(dct_ug[f'UG{self.id}']['setpoint']))
            return res

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o setpoint para a Unidade.")
            logger.debug(traceback.format_exc())
            return False


    def reconhece_reset_alarmes(self) -> "None":
        """
        Função para reset e reconhecimento de TRIPs.

        Realiza três tentativas de executar as funções de remoção de TRIP elétrico e lógico.
        """

        try:
            logger.debug("")
            logger.info(f"[UG{self.id}]          Enviando comando:          \"RECONHECE E RESET\"")
            # self.clp["MOA"].write_single_coil(REG_UG["MOA"]["PAINEL_LIDO"], 0)

            passo = 0
            for x in range(2):
                passo += 1
                logger.debug("")
                logger.debug(f"[UG{self.id}]          Passo: {passo}/3")
                self.remover_trip_eletrico()
                sleep(1)
                self.remover_trip_logico()
                sleep(1)

            # self.clp["MOA"].write_single_coil(REG_UG["MOA"]["PAINEL_LIDO"], 1)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel enviar o comando de reconhecer e resetar alarmes.")
            logger.debug(traceback.format_exc())


    def acionar_trip_logico(self) -> "None":
        """
        Função para acionamento de TRIP lógico.

        Aciona o comando de parada de emergência da Unidade.
        """

        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP LÓGICO\"")
            self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["CMD_OPER_EMERGENCIA_LIGAR"], valor=1)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel acionar o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())


    def remover_trip_logico(self) -> "None":
        """
        Função para remoção de TRIP lógico.

        Aciona os comandos de Reset e Rearmes de Relés, Unidades Hidráulicas, Bloqueios e Falhas.
        """

        try:
            logger.debug(f"[UG{self.id}]          Removendo comando:         \"TRIP LÓGICO\"")
            # self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"][""], 0)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Lógico\".")
            logger.debug(traceback.format_exc())


    def acionar_trip_eletrico(self) -> "None":
        """
        Função para acionamento de TRIP elétrico.

        Aciona o comando de bloqueio da Unidade através do CLP - MOA.
        """

        try:
            logger.debug(f"[UG{self.id}]          Enviando comando:          \"TRIP ELÉTRICO\"")
            # self.clp["MOA"].write_single_coil(REG_UG["MOA"][f"OUT_BLOCK_UG{self.id}"], 1)

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel acionar o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())


    def remover_trip_eletrico(self) -> "None":
        """
        Função para remoção de TRIP elétrico.

        Remove o comando de bloqueio da Unidade através do CLP - MOA e fecha o
        Disjuntor 52L (Linha) caso esteja aberto.
        """

        try:
            logger.debug(f"[UG{self.id}]          Removendo comando:         \"TRIP ELÉTRICO\"")
            # self.clp["MOA"].write_single_coil(REG_UG["MOA"]["PAINEL_LIDO"], 0)
            # self.clp["MOA"].write_single_coil(REG_UG["MOA"][f"OUT_BLOCK_UG{self.id}"], 0)
            se.Subestacao.fechar_dj_linha()

        except Exception:
            logger.error(f"[UG{self.id}] Não foi possivel remover o comando de TRIP: \"Elétrico\".")
            logger.debug(traceback.format_exc())


    def aguardar_normalizacao(self, delay: "int") -> "None":
        """
        Função de temporizador para espera de normalização da Unidade restrita,
        por tempo pré-definido por agendamento na Interface.
        """

        while not self.temporizar_normalizacao:
            sleep(max(0, time() + delay - time()))
            self.temporizar_normalizacao = True
            return


    def normalizar_unidade(self) -> "bool":
        """
        Função para normalização de ocorrências da Unidade de Geração.

        Primeiramente verifica se a Unidade passou do número de tentativas. Caso
        tenha passado, será chamada a função de forçar estado indisponível, senão
        aciona a função de reconhecimento e reset de alarmes da Unidade.
        """

        if self.tentativas_normalizacao > self.limite_tentativas_normalizacao:
            logger.warning(f"[UG{self.id}] A UG estourou as tentativas de normalização, indisponibilizando Unidade.")
            return False

        elif ([self.ts_auxiliar] - self.get_time()).seconds > dct_ug[f'UG{self.id}']['tempo_entre_tentativas']:
            self.tentativas_normalizacao += 1
            [self.ts_auxiliar] = self.get_time()
            logger.info(f"[UG{self.id}] Normalizando Unidade (Tentativa {self.tentativas_normalizacao}/{self.limite_tentativas_normalizacao})")
            self.reconhece_reset_alarmes()
            return True


    def bloquear_unidade(self) -> "None":
        """
        Função para Bloqueio da Unidade nos estados Restrito e Indisponível.

        Verfica se a Unidade está parada e caso não esteja, aciona o comando de parar para logo
        em seguida verificar a comporta. Após a parada total da Unidade, verifica se a comporta
        está aberta ou em cracking. Caso esteja, aciona o comando de fechamento da comporta, mas
        caso já esteja fechada, aciona os comandos de TRIP lógico e elétrico. Caso a comporta
        esteja operando, avisa o operador e aguarda o fechamento completo.
        """

        dct_ug[f'UG{self.id}']['temporizar_partida'] = False

        if dct_ug[f"UG{self.id}"]["etapa_atual"] == UG_PARADA:
            self.acionar_trip_eletrico()
            self.acionar_trip_logico()

        elif not self.borda_parar and self.parar():
            self.borda_parar = True


    def verificar_sincronismo(self) -> "None":
        """
        Função de verificação de partida da Unidade.

        Caso a unidade seja totalmente sincronizada, o timer é encerrado e avisado,
        senão, é enviado o comando de parada de emergência para a Unidade.
        """

        logger.debug(f"[UG{self.id}]          Verificação MOA:           \"Temporização de Sincronismo\"")
        while time() < time() + 600:
            if not dct_ug[f'UG{self.id}']['temporizar_partida']:
                return

        logger.warning(f"[UG{self.id}]          Verificação MOA:          \"Acionar emergência por timeout de Sincronismo\"")
        self.clp[f"UG{self.id}"].write_single_register(REG_UG[f"UG{self.id}"]["CMD_OPER_EMERGENCIA_LIGAR"], 1)
        dct_ug[f'UG{self.id}']['temporizar_partida'] = False
        sleep(1)


    def popular_listas_sp_pot(self) -> "None":
        """
        FUnção para popular listas com leituras e cálculos de potência e setpoint,
        para controle do MPPT.
        """
        if self.etapa == UG_PARADA:
            dct_ug[f'UG{self.id}']['potencias_anteriores'] = []

        elif self.etapa == UG_SINCRONIZADA:
            if len(dct_ug[f'UG{self.id}']['potencias_anteriores']) == dct_ug[f'UG{self.id}']['amostras_pot_mppt'] + 1: # Verificar
                dct_ug[f'UG{self.id}']['potencias_anteriores'].pop(-1)

            if len(dct_ug[f'UG{self.id}']['setpoints_anteriores']) == dct_ug[f'UG{self.id}']['amostras_sp_mppt'] + 1: # Verificar
                dct_ug[f'UG{self.id}']['setpoints_anteriores'].pop(-1)


            if len(dct_ug[f'UG{self.id}']['potencias_anteriores']) == dct_ug[f'UG{self.id}']['amostras_pot_mppt'] and dct_usn['CFG']['pot_minima_ugs'] <= dct_ug[f"UG{self.id}"]["potencia"].valor <= dct_usn['CFG']['pot_maxima_ugs']:
                dct_ug[f'UG{self.id}']['potencias_anteriores'].pop(0)
                dct_ug[f'UG{self.id}']['potencias_anteriores'].append(dct_ug[f"UG{self.id}"]["potencia"].valor)

            elif dct_usn['CFG']['pot_minima_ugs'] <= dct_ug[f"UG{self.id}"]["potencia"].valor <= dct_usn['CFG']['pot_maxima_ugs']:
                dct_ug[f'UG{self.id}']['potencias_anteriores'].append(dct_ug[f"UG{self.id}"]["potencia"].valor)

            if len(dct_ug[f'UG{self.id}']['setpoints_anteriores']) == dct_ug[f'UG{self.id}']['amostras_sp_mppt'] and dct_usn['CFG']['pot_minima_ugs'] <= dct_ug[f'UG{self.id}']['setpoint'] <= dct_usn['CFG']['pot_maxima_ugs']:
                dct_ug[f'UG{self.id}']['setpoints_anteriores'].pop(0)
                dct_ug[f'UG{self.id}']['setpoints_anteriores'].append(dct_ug[f'UG{self.id}']['setpoint'])

            elif dct_usn['CFG']['pot_minima_ugs'] <= dct_ug[f'UG{self.id}']['setpoint'] <= dct_usn['CFG']['pot_maxima_ugs']:
                dct_ug[f'UG{self.id}']['setpoints_anteriores'].append(dct_ug[f'UG{self.id}']['setpoint'])


    def ajustar_mppt(self, potencia, setpoint, abertura_dist) -> "float":
        """
        Função para ajuste de setpoint, baseado na entrega máxima de potência,
        por MPPT (Maximum Power Point Tracking)
        """

        setpoint_saida = setpoint[0]
        delta = 35

        if potencia[0] < potencia[1]:
            if abertura_dist[0] < abertura_dist[1]:
                setpoint_saida += delta
            else:
                setpoint_saida -= delta

        elif potencia[0] == potencia[1]:
                setpoint_saida -= delta

        else:
            if abertura_dist[0] < abertura_dist[1]:
                setpoint_saida -= delta
            else:
                setpoint_saida += delta

        return setpoint_saida


    def atenuar_carga(self) -> "None":
        """
        Função para atenuação de carga através de leitura de Pressão na Entrada da Turbina.

        Calcula o ganho e verifica os limites máximo e mínimo para deteminar se
        deve atenuar ou não.
        """

        atenuacao = 0
        for condic in dct_ug[f'UG{self.id}']['condicionadores_atenuadores']:
            atenuacao = max(atenuacao, condic.valor)
            logger.debug(f"[UG{self.id}]          Verificando Atenuadores:")
            logger.debug(f"[UG{self.id}]          - \"{condic.descricao}\":   Leitura: {condic.leitura} | Atenuação: {atenuacao}")

        ganho = 1 - atenuacao
        aux = dct_ug[f'UG{self.id}']['setpoint']
        if (dct_ug[f'UG{self.id}']['setpoint'] > dct_ug[f'UG{self.id}']['setpoint_minimo']) and dct_ug[f'UG{self.id}']['setpoint'] * ganho > dct_ug[f'UG{self.id}']['setpoint_minimo']:
            dct_ug[f'UG{self.id}']['setpoint'] = dct_ug[f'UG{self.id}']['setpoint'] * ganho

        elif (dct_ug[f'UG{self.id}']['setpoint'] * ganho < dct_ug[f'UG{self.id}']['setpoint_minimo']) and (dct_ug[f'UG{self.id}']['setpoint'] > dct_ug[f'UG{self.id}']['setpoint_minimo']):
            dct_ug[f'UG{self.id}']['setpoint'] =  dct_ug[f'UG{self.id}']['setpoint_minimo']

        logger.debug(f"[UG{self.id}]                                     SP {aux} * GANHO {ganho} = {dct_ug[f'UG{self.id}']['setpoint']} kW")


    def controlar_etapas(self) -> "None":
        """
        Função para controle de etapas da Unidade.

        PARANDO -> Chama a função de controle de comporta caso seja atribuído um valor
        de setpoint, senão aciona o comando de fechamento da Comporta caso o valor da
        potência caia abaixo de 300 kW.
        PARADA -> Chama a função de controle de comporta caso seja atribuído um valor
        de setpoint, senão apenas envia o setpoint (boa prática).
        SINCRONIZANDO -> Chama o comando de enviar setpoint, senão caiona o comando de
        parada caso o setpoint retorne 0.
        SINCRONIZADA -> Controla a variável de tempo sincronizada e envia o comando
        de parada caso seja atribuído o setpoint 0 para a Unidade.
        """

        if self.etapa == UG_PARADA:
            if dct_ug[f'UG{self.id}']['setpoint'] >= dct_usn['CFG']["pot_minima_ugs"]:
                self.partir()

        elif self.etapa == UG_PARANDO:
            if dct_ug[f'UG{self.id}']['setpoint'] >= dct_usn['CFG']["pot_minima_ugs"]:
                self.enviar_setpoint(dct_ug[f'UG{self.id}']['setpoint'])

        elif self.etapa == UG_SINCRONIZANDO:
            if not dct_ug[f'UG{self.id}']['temporizar_partida']:
                dct_ug[f'UG{self.id}']['temporizar_partida'] = True
                threading.Thread(target=lambda: self.verificar_sincronismo()).start()

            self.parar() if dct_ug[f'UG{self.id}']['setpoint'] == 0 else self.enviar_setpoint(dct_ug[f'UG{self.id}']['setpoint'])

        elif self.etapa == UG_SINCRONIZADA:
            dct_ug[f'UG{self.id}']['temporizar_partida'] = False

            if not dct_ug[f'UG{self.id}']['aux_tempo_sincronizada']:
                dct_ug[f'UG{self.id}']['aux_tempo_sincronizada'] = self.get_time()

            elif (self.get_time() - dct_ug[f'UG{self.id}']['aux_tempo_sincronizada']).seconds >= 300:
                self.tentativas_normalizacao = 0

            self.parar() if dct_ug[f'UG{self.id}']['setpoint'] == 0 else self.enviar_setpoint(dct_ug[f'UG{self.id}']['setpoint'])

        if not dct_ug[f"UG{self.id}"]["etapa_atual"] == UG_SINCRONIZADA:
            dct_ug[f'UG{self.id}']['aux_tempo_sincronizada'] = None


    def verificar_condicionadores(self) -> "int":
        """
        Função para a verificação de acionamento de condicionadores e determinação
        de gravidade.

        Itera sobre a lista de condicionadores da Unidade e verifica se algum está
        ativo. Caso esteja, verifica o nível de gravidade e retorna o valor para
        a determinação do passo seguinte.
        Caso não haja nenhum condicionador ativo, apenas retorna o valor de ignorar.
        """

        autor_i = 0
        autor_a = 0
        autor_n = 0
        flag = CONDIC_IGNORAR

        if True in (condic.ativo for condic in dct_ug[f'UG{self.id}']['condicionadores_essenciais']):
            condics_ativos = [condic for condics in dct_ug[f'UG{self.id}'][['condicionadores_essenciais'], dct_ug[f'UG{self.id}']['condicionadores']] for condic in condics if condic.ativo]

            logger.debug("")
            if dct_ug[f'UG{self.id}']['condicionadores_ativos'] == []:
                logger.warning(f"[UG{self.id}] Foram detectados condicionadores ativos na Unidade!")
            else:
                logger.info(f"[UG{self.id}] Ainda há condicionadores ativos na Unidade!")

            for condic in condics_ativos:
                if condic in dct_ug[f'UG{self.id}']['condicionadores_ativos']:
                    logger.debug(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    flag = condic.gravidade
                    continue

                elif condic.gravidade == CONDIC_INDISPONIBILIZAR:
                    logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    dct_ug[f'UG{self.id}']['condicionadores_ativos'].append(condic)
                    flag = CONDIC_INDISPONIBILIZAR
                    dct_usn['BD'].update_alarmes([
                        self.get_time(),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor_i == 0 else ""
                    ])

                elif condic.gravidade == CONDIC_AGUARDAR:
                    logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    dct_ug[f'UG{self.id}']['condicionadores_ativos'].append(condic)
                    flag = CONDIC_NORMALIZAR
                    dct_usn['BD'].update_alarmes([
                        self.get_time(),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor_i == 0 and autor_a == 0 else ""
                    ])

                elif condic.gravidade == CONDIC_NORMALIZAR:
                    logger.warning(f"[UG{self.id}] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    dct_ug[f'UG{self.id}']['condicionadores_ativos'].append(condic)
                    flag = CONDIC_NORMALIZAR
                    dct_usn['BD'].update_alarmes([
                        self.get_time(),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor_i == 0 and autor_a == 0 and autor_n == 0 else ""
                    ])

            logger.debug("")
            return flag

        else:
            dct_ug[f'UG{self.id}']['condicionadores_ativos'] = []
            return flag


    def atualizar_limites(self, parametros: "dict") -> "None":
        """
        Função para extração de valores do Banco de Dados da Interface WEB e atribuição
        de novos limites de operação de condicionadores.
        """

        try:
            self.prioridade = int(parametros[f"ug{self.id}_prioridade"])

            self.c_temp_fase_r_ug.valor_base = float(parametros[f"alerta_temperatura_fase_r_ug{self.id}"])
            self.c_temp_fase_s_ug.valor_base = float(parametros[f"alerta_temperatura_fase_s_ug{self.id}"])
            self.c_temp_fase_t_ug.valor_base = float(parametros[f"alerta_temperatura_fase_t_ug{self.id}"])
            self.c_temp_mancal_gerador_la_1_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_gerador_la_1_ug{self.id}"])
            self.c_temp_mancal_gerador_la_2_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_gerador_la_2_ug{self.id}"])
            self.c_temp_mancal_gerador_lna_1_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_gerador_lna_1_ug{self.id}"])
            self.c_temp_mancal_gerador_lna_2_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_gerador_lna_2_ug{self.id}"])
            self.c_temp_mancal_turbina_radial_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_turbina_radial_ug{self.id}"])
            self.c_temp_mancal_turbina_escora_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_turbina_escora_ug{self.id}"])
            self.c_temp_mancal_turbina_contra_escora_ug.valor_base = float(parametros[f"alerta_temperatura_mancal_turbina_contra_escora_ug{self.id}"])
            self.c_pressao_turbina_ug.valor_base = float(parametros[f"alerta_pressao_turbina_ug{self.id}"])

            self.c_temp_fase_r_ug.valor_limite = float(parametros[f"limite_temperatura_fase_r_ug{self.id}"])
            self.c_temp_fase_s_ug.valor_limite = float(parametros[f"limite_temperatura_fase_s_ug{self.id}"])
            self.c_temp_fase_t_ug.valor_limite = float(parametros[f"limite_temperatura_fase_t_ug{self.id}"])
            self.c_temp_mancal_gerador_la_1_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_gerador_la_1_ug{self.id}"])
            self.c_temp_mancal_gerador_la_2_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_gerador_la_2_ug{self.id}"])
            self.c_temp_mancal_gerador_lna_1_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_gerador_lna_1_ug{self.id}"])
            self.c_temp_mancal_gerador_lna_2_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_gerador_lna_2_ug{self.id}"])
            self.c_temp_mancal_turbina_radial_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_turbina_radial_ug{self.id}"])
            self.c_temp_mancal_turbina_escora_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_turbina_escora_ug{self.id}"])
            self.c_temp_mancal_turbina_contra_escora_ug.valor_limite = float(parametros[f"limite_temperatura_mancal_turbina_contra_escora_ug{self.id}"])
            self.c_pressao_turbina_ug.valor_limite = float(parametros[f"limite_pressao_turbina_ug{self.id}"])

        except Exception:
            logger.error(f"[UG{self.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores.")
            logger.debug(traceback.format_exc())


    def verificar_limites(self) -> "None":
        """
        Função para verificação de limites de operação da Unidade.

        Verifica os valores base e limite da Unidade, pré-determinados na interface
        WEB, e avisa o operador caso algum valor ultrapasse o estipulado.
        """

        if self.l_temp_fase_r.valor >= self.c_temp_fase_r_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase R da UG passou do valor base! ({self.c_temp_fase_r_ug.valor_base}C) | Leitura: {self.l_temp_fase_r.valor}C")
        if self.l_temp_fase_r.valor >= 0.9*(self.c_temp_fase_r_ug.valor_limite - self.c_temp_fase_r_ug.valor_base) + self.c_temp_fase_r_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase R da UG está muito próxima do limite! ({self.c_temp_fase_r_ug.valor_limite}C) | Leitura: {self.l_temp_fase_r.valor}C")

        if self.l_temp_fase_s.valor >= self.c_temp_fase_s_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase S da UG passou do valor base! ({self.c_temp_fase_s_ug.valor_base}C) | Leitura: {self.l_temp_fase_s.valor}C")
        if self.l_temp_fase_s.valor >= 0.9*(self.c_temp_fase_s_ug.valor_limite - self.c_temp_fase_s_ug.valor_base) + self.c_temp_fase_s_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase S da UG está muito próxima do limite! ({self.c_temp_fase_s_ug.valor_limite}C) | Leitura: {self.l_temp_fase_s.valor}C")

        if self.l_temp_fase_t.valor >= self.c_temp_fase_t_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura de Fase T da UG passou do valor base! ({self.c_temp_fase_t_ug.valor_base}C) | Leitura: {self.l_temp_fase_t.valor}C")
        if self.l_temp_fase_t.valor >= 0.9*(self.c_temp_fase_t_ug.valor_limite - self.c_temp_fase_t_ug.valor_base) + self.c_temp_fase_t_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura de Fase T da UG está muito próxima do limite! ({self.c_temp_fase_t_ug.valor_limite}C) | Leitura: {self.l_temp_fase_t.valor}C")

        if self.l_temp_mancal_gerador_la_1.valor >= self.c_temp_mancal_gerador_la_1_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Gerador LA 1 da UG passou do valor base! ({self.c_temp_mancal_gerador_la_1_ug.valor_base}C) | Leitura: {self.l_temp_mancal_gerador_la_1.valor}C")
        if self.l_temp_mancal_gerador_la_1.valor >= 0.9*(self.c_temp_mancal_gerador_la_1_ug.valor_limite - self.c_temp_mancal_gerador_la_1_ug.valor_base) + self.c_temp_mancal_gerador_la_1_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Gerador LA 1 da UG está muito próxima do limite! ({self.c_temp_mancal_gerador_la_1_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_gerador_la_1.valor}C")

        if self.l_temp_mancal_gerador_la_2.valor >= self.c_temp_mancal_gerador_la_2_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Gerador LA 2 da UG passou do valor base! ({self.c_temp_mancal_gerador_la_2_ug.valor_base}C) | Leitura: {self.l_temp_mancal_gerador_la_2.valor}C")
        if self.l_temp_mancal_gerador_la_2.valor >= 0.9*(self.c_temp_mancal_gerador_la_2_ug.valor_limite - self.c_temp_mancal_gerador_la_2_ug.valor_base) + self.c_temp_mancal_gerador_la_2_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Gerador LA 2 da UG está muito próxima do limite! ({self.c_temp_mancal_gerador_la_2_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_gerador_la_2.valor}C")

        if self.l_temp_mancal_gerador_lna_1.valor >= self.c_temp_mancal_gerador_lna_1_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Gerador LNA 1 da UG passou do valor base! ({self.c_temp_mancal_gerador_lna_1_ug.valor_base}C) | Leitura: {self.l_temp_mancal_gerador_lna_1.valor}C")
        if self.l_temp_mancal_gerador_lna_1.valor >= 0.9*(self.c_temp_mancal_gerador_lna_1_ug.valor_limite - self.c_temp_mancal_gerador_lna_1_ug.valor_base) + self.c_temp_mancal_gerador_lna_1_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Gerador LNA 1 da UG está muito próxima do limite! ({self.c_temp_mancal_gerador_lna_1_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_gerador_lna_1.valor}C")

        if self.l_temp_mancal_gerador_lna_2.valor >= self.c_temp_mancal_gerador_lna_2_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Gerador LNA 2 da UG passou do valor base! ({self.c_temp_mancal_gerador_lna_2_ug.valor_base}C) | Leitura: {self.l_temp_mancal_gerador_lna_2.valor}C")
        if self.l_temp_mancal_gerador_lna_2.valor >= 0.9*(self.c_temp_mancal_gerador_lna_2_ug.valor_limite - self.c_temp_mancal_gerador_lna_2_ug.valor_base) + self.c_temp_mancal_gerador_lna_2_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Gerador LNA 2 da UG está muito próxima do limite! ({self.c_temp_mancal_gerador_lna_2_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_gerador_lna_2.valor}C")

        if self.l_temp_mancal_turbina_radial.valor >= self.c_temp_mancal_turbina_radial_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura dos Patins do Mancal Gerador LNA 2 da UG passou do valor base! ({self.c_temp_mancal_turbina_radial_ug.valor_base}C) | Leitura: {self.l_temp_mancal_turbina_radial.valor}C")
        if self.l_temp_mancal_turbina_radial.valor >= 0.9*(self.c_temp_mancal_turbina_radial_ug.valor_limite - self.c_temp_mancal_turbina_radial_ug.valor_base) + self.c_temp_mancal_turbina_radial_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura dos Patins do Mancal Gerador LNA 2 da UG está muito próxima do limite! ({self.c_temp_mancal_turbina_radial_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_turbina_radial.valor}C")

        if self.l_temp_mancal_turbina_radial.valor >= self.c_temp_mancal_turbina_radial_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura dos Mancal Turbina Radial da UG passou do valor base! ({self.c_temp_mancal_turbina_radial_ug.valor_base}C) | Leitura: {self.l_temp_mancal_turbina_radial.valor}C")
        if self.l_temp_mancal_turbina_radial.valor >= 0.9*(self.c_temp_mancal_turbina_radial_ug.valor_limite - self.c_temp_mancal_turbina_radial_ug.valor_base) + self.c_temp_mancal_turbina_radial_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura dos Mancal Turbina Radial da UG está muito próxima do limite! ({self.c_temp_mancal_turbina_radial_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_turbina_radial.valor}C")

        if self.l_temp_mancal_turbina_escora.valor >= self.c_temp_mancal_turbina_escora_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Turbina Escora da UG passou do valor base! ({self.c_temp_mancal_turbina_escora_ug.valor_base}C) | Leitura: {self.l_temp_mancal_turbina_escora.valor}C")
        if self.l_temp_mancal_turbina_escora.valor >= 0.9*(self.c_temp_mancal_turbina_escora_ug.valor_limite - self.c_temp_mancal_turbina_escora_ug.valor_base) + self.c_temp_mancal_turbina_escora_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Turbina Escora da UG está muito próxima do limite! ({self.c_temp_mancal_turbina_escora_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_turbina_escora.valor}C")

        if self.l_temp_mancal_turbina_contra_escora.valor >= self.c_temp_mancal_turbina_contra_escora_ug.valor_base:
            logger.warning(f"[UG{self.id}] A temperatura do Mancal Turbina Contra Escora da UG passou do valor base! ({self.c_temp_mancal_turbina_contra_escora_ug.valor_base}C) | Leitura: {self.l_temp_mancal_turbina_contra_escora.valor}C")
        if self.l_temp_mancal_turbina_contra_escora.valor >= 0.9*(self.c_temp_mancal_turbina_contra_escora_ug.valor_limite - self.c_temp_mancal_turbina_contra_escora_ug.valor_base) + self.c_temp_mancal_turbina_contra_escora_ug.valor_base:
            logger.critical(f"[UG{self.id}] A temperatura do Mancal Turbina Contra Escora da UG está muito próxima do limite! ({self.c_temp_mancal_turbina_contra_escora_ug.valor_limite}C) | Leitura: {self.l_temp_mancal_turbina_contra_escora.valor}C")

        if self.l_pressao_turbina.valor <= self.c_pressao_turbina_ug.valor_base and self.l_pressao_turbina.valor != 0 and dct_ug[f"UG{self.id}"]["etapa_atual"] == UG_SINCRONIZADA:
            logger.warning(f"[UG{self.id}] A pressão na entrada da turbina da UG passou do valor base! ({self.c_pressao_turbina_ug.valor_base:03.2f} KGf/m2) | Leitura: {self.l_pressao_turbina.valor:03.2f}")
        if self.l_pressao_turbina.valor <= self.c_pressao_turbina_ug.valor_limite+0.9*(self.c_pressao_turbina_ug.valor_base - self.c_pressao_turbina_ug.valor_limite) and self.l_pressao_turbina.valor != 0 and dct_ug[f"UG{self.id}"]["etapa_atual"] == UG_SINCRONIZADA:
            logger.critical(f"[UG{self.id}] A pressão na entrada da turbina da UG está muito próxima do limite! ({self.c_pressao_turbina_ug.valor_limite:03.2f} KGf/m2) | Leitura: {self.l_pressao_turbina.valor:03.2f} KGf/m2")


    def verificar_leituras(self) -> "None":
        """
        Função para consulta de acionamentos da Unidade e avisos através do mecanismo
        de acionamento temporizado.
        """

        if self.l_alm_04_b_10.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o a Pastilha de Ferio da Unidade está Gasta. Favor verificar.")

        if self.l_alm_07_b_06.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura de Fase R do Gerador. Favor verificar.")

        if self.l_alm_07_b_07.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura de Fase S do Gerador. Favor verificar.")

        if self.l_alm_07_b_08.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura de Fase T do Gerador. Favor verificar.")

        if self.l_alm_07_b_09.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura do Casquilho 01 do Mancal LA. Favor verificar.")

        if self.l_alm_07_b_10.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura do Casquilho 02 do Mancal LA. Favor verificar.")

        if self.l_alm_07_b_11.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura do Casquilho 01 do Mancal LNA. Favor verificar.")

        if self.l_alm_07_b_12.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura do Casquilho 02 do Mancal LNA. Favor verificar.")

        if self.l_alm_07_b_13.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura do Gaxeteiro Lado Montante. Favor verificar.")

        if self.l_alm_07_b_14.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura do Gaxeteiro Lado Jusante. Favor verificar.")

        if self.l_alm_07_b_15.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura da Bucha Radial do Mancal Combinado. Favor verificar.")

        if self.l_alm_08_b_00.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura das Sapatas Axiais Escora do Mancal Combiando. Favor verificar.")

        if self.l_alm_08_b_01.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura das Sapatas Axiais Contra Escora do Mancal Combiando. Favor verificar.")

        if self.l_alm_08_b_02.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura do Óleo da UHCT. Favor verificar.")

        if self.l_alm_08_b_03.valor:
            logger.warning(f"[UG{self.id}] Foi identificada uma Falha no Sensor de Temperatura do Óleo da UHLM. Favor verificar.")

        if self.l_alm_08_b_07.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura de Fase R do Gerador via CLP. Favor verificar.")

        if self.l_alm_08_b_08.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura de Fase S do Gerador via CLP. Favor verificar.")

        if self.l_alm_08_b_09.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura de Fase T do Gerador via CLP. Favor verificar.")

        if self.l_alm_08_b_10.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura do Casquilho 01 do Mancal LA via CLP. Favor verificar.")

        if self.l_alm_08_b_11.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura do Casquilho 02 do Mancal LA via CLP. Favor verificar.")

        if self.l_alm_08_b_12.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura do Casquilho 01 do Mancal LNA via CLP. Favor verificar.")

        if self.l_alm_08_b_13.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura do Casquilho 02 do Mancal LNA via CLP. Favor verificar.")

        if self.l_alm_08_b_14.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura do Gaxeteiro Lado Jusante via CLP. Favor verificar.")

        if self.l_alm_08_b_15.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura do Gaxeteiro Lado Montante via CLP. Favor verificar.")

        if self.l_alm_09_b_00.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura da Bucha Radial do Mancal Combinado via CLP. Favor verificar.")

        if self.l_alm_09_b_01.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura das Sapatas Axiais Escora do Mancal Combinado via CLP. Favor verificar.")

        if self.l_alm_09_b_02.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura das Sapatas Axiais Contra Escora do Mancal Combinado via CLP. Favor verificar.")

        if self.l_alm_09_b_03.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura do Óleo da UHCT via CLP. Favor verificar.")

        if self.l_alm_09_b_04.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Sobretemperatura do Óleo da UHLM via CLP. Favor verificar.")

        if self.l_alm_15_b_00.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Vibração Vertical Excessiva do Mancal Combinado da Turbina. Favor verificar.")

        if self.l_alm_15_b_02.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Vibração Horizontal Excessiva do Mancal Combinado da Turbina. Favor verificar.")

        if self.l_alm_15_b_04.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Vibração Axial Excessiva do Mancal Combinado da Turbina. Favor verificar.")

        if self.l_alm_15_b_06.valor:
            logger.warning(f"[UG{self.id}] Foi identificado um Alarme de Vibração Excessiva do Mancal Lado Acoplado da Turbina. Favor verificar.")

        if self.l_alm_15_b_12.valor:
            logger.warning(f"[UG{self.id}] Foi identificado uma Falha de RTD´s ou Falha de Comunicação com o módulo SEL-2600 (Bloqueio 86M T). Favor verificar.")


        if self.l_dj_07.valor:
            logger.warning(f"[UG{self.id}] Foi identificado que o Disjuntor Q125.0 UG1 de Alimentação do SEL2600 foi Desligado/Aberto. Favor verificar.")


        if self.l_modo_local.valor and not d.voip[f"UG{self.id}_OPER_MODO_LOCAL"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado que a Unidade {self.id} entrou em Modo de Operação Local. Favor verificar.")
            d.voip[f"UG{self.id}_OPER_MODO_LOCAL"][0] = True
        elif not self.l_modo_local.valor and d.voip[f"UG{self.id}_OPER_MODO_LOCAL"][0]:
            d.voip[f"UG{self.id}_OPER_MODO_LOCAL"][0] = False

        if self.l_uhct_nv_oleo_l.valor and not d.voip[f"UG{self.id}_UHCT_NIVEL_OLEO_L"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado que o nível do Óleo da UHCT está na faixa \"Baixo\". Favor verificar.")
            d.voip[f"UG{self.id}_UHCT_NIVEL_OLEO_L"][0] = True
        elif not self.l_uhct_nv_oleo_l.valor and d.voip[f"UG{self.id}_UHCT_NIVEL_OLEO_L"][0]:
            d.voip[f"UG{self.id}_UHCT_NIVEL_OLEO_L"][0] = False

        if self.l_uhct_nv_oleo_h.valor and not d.voip[f"UG{self.id}_UHCT_NIVEL_OLEO_H"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado que o nível do Óleo da UHCT está na faixa \"Alto\". Favor monitorar.")
            d.voip[f"UG{self.id}_UHCT_NIVEL_OLEO_H"][0] = True
        elif not self.l_uhct_nv_oleo_h.valor and d.voip[f"UG{self.id}_UHCT_NIVEL_OLEO_H"][0]:
            d.voip[f"UG{self.id}_UHCT_NIVEL_OLEO_H"][0] = False

        if self.l_uhct_nv_oleo_hh.valor and not d.voip[f"UG{self.id}_UHCT_NIVEL_OLEO_HH"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado que o nível do Óleo da UHCT está na faixa \"Muito Alto\". Favor monitorar.")
            d.voip[f"UG{self.id}_UHCT_NIVEL_OLEO_HH"][0] = True
        elif not self.l_uhct_nv_oleo_hh.valor and d.voip[f"UG{self.id}_UHCT_NIVEL_OLEO_HH"][0]:
            d.voip[f"UG{self.id}_UHCT_NIVEL_OLEO_HH"][0] = False

        if self.l_uhlm_modo_local.valor and not d.voip[f"UG{self.id}_UHLM_MODO_LOCAL"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado que a UHLM entrou em Modo de Operação Local. Favor verificar.")
            d.voip[f"UG{self.id}_UHLM_MODO_LOCAL"][0] = True
        elif not self.l_uhlm_modo_local.valor and d.voip[f"UG{self.id}_UHLM_MODO_LOCAL"][0]:
            d.voip[f"UG{self.id}_UHLM_MODO_LOCAL"][0] = False

        if self.l_uhlm_nv_oleo_l.valor and not d.voip[f"UG{self.id}_UHLM_NIVEL_OLEO_L"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado que o nível do Óleo da UHLM está na faixa \"Baixo\". Favor monitorar.")
            d.voip[f"UG{self.id}_UHLM_NIVEL_OLEO_L"][0] = True
        elif not self.l_uhlm_nv_oleo_l.valor and d.voip[f"UG{self.id}_UHLM_NIVEL_OLEO_L"][0]:
            d.voip[f"UG{self.id}_UHLM_NIVEL_OLEO_L"][0] = False

        if self.l_uhlm_nv_oleo_h.valor and not d.voip[f"UG{self.id}_UHLM_NIVEL_OLEO_H"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado que o nível do Óleo da UHLM está na faixa \"Alto\". Favor monitorar.")
            d.voip[f"UG{self.id}_UHLM_NIVEL_OLEO_H"][0] = True
        elif not self.l_uhlm_nv_oleo_h.valor and d.voip[f"UG{self.id}_UHLM_NIVEL_OLEO_H"][0]:
            d.voip[f"UG{self.id}_UHLM_NIVEL_OLEO_H"][0] = False

        if self.l_uhlm_nv_oleo_hh.valor and not d.voip[f"UG{self.id}_UHLM_NIVEL_OLEO_HH"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado que o nível do Óleo da UHLM está na faixa \"Muito Alto\". Favor monitorar.")
            d.voip[f"UG{self.id}_UHLM_NIVEL_OLEO_HH"][0] = True
        elif not self.l_uhlm_nv_oleo_hh.valor and d.voip[f"UG{self.id}_UHLM_NIVEL_OLEO_HH"][0]:
            d.voip[f"UG{self.id}_UHLM_NIVEL_OLEO_HH"][0] = False

        if self.l_turb_sens_desati.valor and not d.voip[f"UG{self.id}_TURB_SENS_DESATIVADO"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado que o Sensor da Turbina foi Desativado. Favor verificar.")
            d.voip[f"UG{self.id}_TURB_SENS_DESATIVADO"][0] = True
        elif not self.l_turb_sens_desati.valor and d.voip[f"UG{self.id}_TURB_SENS_DESATIVADO"][0]:
            d.voip[f"UG{self.id}_TURB_SENS_DESATIVADO"][0] = False

        if self.l_turb_fren_manual.valor and not d.voip[f"UG{self.id}_TURB_FRENA_MANUAL"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado que a Turbina entrou em Modo de Frenagem Manual. Favor verificar.")
            d.voip[f"UG{self.id}_TURB_FRENA_MANUAL"][0] = True
        elif not self.l_turb_fren_manual.valor and d.voip[f"UG{self.id}_TURB_FRENA_MANUAL"][0]:
            d.voip[f"UG{self.id}_TURB_FRENA_MANUAL"][0] = False

        if self.l_rv_ctrl_man_distr.valor and not d.voip[f"UG{self.id}_REG_V_CTRL_MANUAL_DISTRI"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado que o Distribuidor do RV entrou em Modo de Controle Manual. Favor verificar.")
            d.voip[f"UG{self.id}_REG_V_CTRL_MANUAL_DISTRI"][0] = True
        elif not self.l_rv_ctrl_man_distr.valor and d.voip[f"UG{self.id}_REG_V_CTRL_MANUAL_DISTRI"][0]:
            d.voip[f"UG{self.id}_REG_V_CTRL_MANUAL_DISTRI"][0] = False

        if self.l_rv_ctrl_man_valv.valor and not d.voip[f"UG{self.id}_REG_V_CTRL_MANUAL_VALV"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado que a Válvula do RV entrou em Modo de Controle Manual. Favor verificar.")
            d.voip[f"UG{self.id}_REG_V_CTRL_MANUAL_VALV"][0] = True
        elif not self.l_rv_ctrl_man_valv.valor and d.voip[f"UG{self.id}_REG_V_CTRL_MANUAL_VALV"][0]:
            d.voip[f"UG{self.id}_REG_V_CTRL_MANUAL_VALV"][0] = False

        if self.l_sinc_modo_manual.valor and not d.voip[f"UG{self.id}_SINC_MODO_MANUAL"][0]:
            logger.warning(f"[UG{self.id}] Foi identificado que o Sincronoscópio da Unidade {self.id} entrou em Modo Manual. Favor verificar.")
            d.voip[f"UG{self.id}_SINC_MODO_MANUAL"][0] = True
        elif not self.l_sinc_modo_manual.valor and d.voip[f"UG{self.id}_SINC_MODO_MANUAL"][0]:
            d.voip[f"UG{self.id}_SINC_MODO_MANUAL"][0] = False


    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """

        # CONDICIONADORES ESSENCIAIS
        # Temperaturas
            # Fase R
        self.l_temp_fase_r = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_01"], descricao=f"[UG{self.id}] Temperatura Fase R")
        self.c_temp_fase_r_ug = c.CondicionadorExponencial(self.l_temp_fase_r)
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(self.c_temp_fase_r_ug)

            # Fase S
        self.l_temp_fase_s = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_02"], descricao=f"[UG{self.id}] Temperatura Fase S")
        self.c_temp_fase_s_ug = c.CondicionadorExponencial(self.l_temp_fase_s)
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(self.c_temp_fase_s_ug)

            # Fase T
        self.l_temp_fase_t = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_03"], descricao=f"[UG{self.id}] Temperatura Fase T")
        self.c_temp_fase_t_ug = c.CondicionadorExponencial(self.l_temp_fase_t)
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(self.c_temp_fase_t_ug)

            # Mancal Gerador LA 1
        self.l_temp_mancal_gerador_la_1 = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_04"], descricao=f"[UG{self.id}] Temperatura Mancal Gerador LA 1")
        self.c_temp_mancal_gerador_la_1_ug = c.CondicionadorExponencial(self.l_temp_mancal_gerador_la_1)
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(self.c_temp_mancal_gerador_la_1_ug)

            # Mancal Gerador LA 2
        self.l_temp_mancal_gerador_la_2 = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_05"], descricao=f"[UG{self.id}] Temperatura Mancal Gerador LA 2")
        self.c_temp_mancal_gerador_la_2_ug = c.CondicionadorExponencial(self.l_temp_mancal_gerador_la_2)
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(self.c_temp_mancal_gerador_la_2_ug)

            # Mancal Gerador LNA 1
        self.l_temp_mancal_gerador_lna_1 = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_06"], descricao=f"[UG{self.id}] Temperatura Mancal Gerador LNA 1")
        self.c_temp_mancal_gerador_lna_1_ug = c.CondicionadorExponencial(self.l_temp_mancal_gerador_lna_1)
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(self.c_temp_mancal_gerador_lna_1_ug)

            #  Mancal Gerador LNA 2
        self.l_temp_mancal_gerador_lna_2 = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_07"], descricao=f"[UG{self.id}] Temperatura Mancal Gerador LNA 2")
        self.c_temp_mancal_gerador_lna_2_ug = c.CondicionadorExponencial(self.l_temp_mancal_gerador_lna_2)
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(self.c_temp_mancal_gerador_lna_2_ug)

            # Mancal Turbina Radial
        self.l_temp_mancal_turbina_radial = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_10"], descricao=f"[UG{self.id}] Temperatura Mancal Turbina Radial")
        self.c_temp_mancal_turbina_radial_ug = c.CondicionadorExponencial(self.l_temp_mancal_turbina_radial)
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(self.c_temp_mancal_turbina_radial_ug)

            # Mancal Turbina Escora
        self.l_temp_mancal_turbina_escora = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_11"], descricao=f"[UG{self.id}] Temperatura Mancal Turbina Escora")
        self.c_temp_mancal_turbina_escora_ug = c.CondicionadorExponencial(self.l_temp_mancal_turbina_escora)
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(self.c_temp_mancal_turbina_escora_ug)

            # Mancal Turbina Radial Contra Escora
        self.l_temp_mancal_turbina_contra_escora = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_12"], descricao=f"[UG{self.id}] Temperatura Mancal Turbina Contra Escora")
        self.c_temp_mancal_turbina_contra_escora_ug = c.CondicionadorExponencial(self.l_temp_mancal_turbina_contra_escora)
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(self.c_temp_mancal_turbina_contra_escora_ug)

            # Óleo UHRV
        self.l_temp_oleo_uhrv = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_13"], descricao=f"[UG{self.id}] Temperatura Óleo UHRV")
        self.c_temp_oleo_uhrv_ug = c.CondicionadorExponencial(self.l_temp_oleo_uhrv)
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(self.c_temp_oleo_uhrv_ug)

            # Óleo ULHM
        self.l_temp_oleo_uhlm = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TEMPERATURA_14"], descricao=f"[UG{self.id}] Temperatura Óleo ULHM")
        self.c_temp_oleo_uhlm_ug = c.CondicionadorExponencial(self.l_temp_oleo_uhlm)
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(self.c_temp_oleo_uhlm_ug)

        # CONDICIONCADORES ATENUADORES
            # Pressão Entrada Turbina
        self.l_pressao_turbina = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TURB_PRESSAO_CONDUTO"], escala=0.1, descricao=f"[UG{self.id}] Pressão Entrada Turbina")
        self.c_pressao_turbina_ug = c.CondicionadorExponencialReverso(self.l_pressao_turbina, CONDIC_INDISPONIBILIZAR, 1.6, 1.3)
        dct_ug[f'UG{self.id}']['condicionadores_atenuadores'].append(self.c_pressao_turbina_ug)


        self.l_oper_parada_emerg = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["OPER_INFO_PARADA_EMERG"], descricao=f"[UG{self.id}] Operação Parada Emergência")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_oper_parada_emerg, CONDIC_NORMALIZAR))

        self.l_oper_parada_trip_e = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["OPER_INFO_PARADA_TRIP_E"], descricao=f"[UG{self.id}] Operação Parada TRIP Elétrico")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_oper_parada_trip_e, CONDIC_NORMALIZAR))

        self.l_oper_parada_trip_h = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["OPER_INFO_PARADA_TRIP_H"], descricao=f"[UG{self.id}] Operação Parada TRIP Hidráulico")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_oper_parada_trip_h, CONDIC_NORMALIZAR))

        self.l_alm_01_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_01"], descricao=f"[UG{self.id}] Botão de Emergência Pressionado (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_alm_01_b_01, CONDIC_NORMALIZAR))

        self.l_alm_02_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_03"], descricao=f"[UG{self.id}] UHLM - Botão de Emergência Pressionado (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_alm_02_b_03, CONDIC_NORMALIZAR))

        self.l_alm_03_b_08 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_08"], descricao=f"[UG{self.id}] UHCT - Botão de Emergência Pressionado (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_alm_03_b_08, CONDIC_NORMALIZAR))

        self.l_alm_05_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_02"], descricao=f"[UG{self.id}] Reg Tensão - TRIP (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_alm_05_b_02, CONDIC_NORMALIZAR))

        self.l_alm_05_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_09"], descricao=f"[UG{self.id}] Relé de Bloqueio 86M Trip Atuado ")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_alm_05_b_09, CONDIC_NORMALIZAR))

        self.l_alm_05_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_10"], descricao=f"[UG{self.id}] Relé de Bloqueio 86M Trip Atuado Temporizado")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_alm_05_b_10, CONDIC_NORMALIZAR))

        self.l_alm_05_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_11"], descricao=f"[UG{self.id}] Relé de Bloqueio 86M Trip Atuado pelo CLP")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_alm_05_b_11, CONDIC_NORMALIZAR))

        self.l_alm_05_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_12"], descricao=f"[UG{self.id}] Relé de Bloqueio 86E Trip Atuado ")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_alm_05_b_12, CONDIC_NORMALIZAR))

        self.l_alm_05_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_13"], descricao=f"[UG{self.id}] Relé de Bloqueio 86E Trip Atuado Temporizado")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_alm_05_b_13, CONDIC_NORMALIZAR))

        self.l_alm_05_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_14"], descricao=f"[UG{self.id}] Relé de Bloqueio 86E Trip Atuado pelo CLP")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_alm_05_b_14, CONDIC_NORMALIZAR))

        self.l_alm_05_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_15"], descricao=f"[UG{self.id}] Relé de Bloqueio 86H Trip Atuado")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_alm_05_b_15, CONDIC_NORMALIZAR))

        self.l_alm_06_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme06_00"], descricao=f"[UG{self.id}] Relé de Bloqueio 86H Trip Atuado pelo CLP")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_alm_06_b_00, CONDIC_NORMALIZAR))

        self.l_alm_06_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme06_03"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - TRIP")
        dct_ug[f'UG{self.id}']['condicionadores_essenciais'].append(c.CondicionadorBase(self.l_alm_06_b_03, CONDIC_NORMALIZAR))


        self.l_emergencia = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["OPER_EMERGENCIA"], descricao=f"[UG{self.id}] Operação Emergência Ligada")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_emergencia, CONDIC_INDISPONIBILIZAR))

        self.l_oper_parada_trip_agua = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["OPER_INFO_PARADA_TRIP_AGUA"], descricao=f"[UG{self.id}] Operação Parada TRIP Água")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_oper_parada_trip_agua, CONDIC_INDISPONIBILIZAR))

        self.l_oper_parada_trip_m = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["OPER_INFO_PARADA_TRIP_M"], descricao=f"[UG{self.id}] Operação Parada TRIP Mecânico")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_oper_parada_trip_m, CONDIC_INDISPONIBILIZAR))

        self.l_uhct_nv_oleo_ll = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHCT_NIVEL_OLEO_LL"], descricao=f"[UG{self.id}] UHCT Nível Óleo Muito Baixo")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_uhct_nv_oleo_ll, CONDIC_INDISPONIBILIZAR))

        self.l_uhlm_nv_oleo_ll = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_NIVEL_OLEO_LL"], descricao=f"[UG{self.id}] UHLM Nível Óleo Muito Baixo")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_uhlm_nv_oleo_ll, CONDIC_INDISPONIBILIZAR))

        self.l_dj52G_inserido = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Dj52G_INSERIDO"], descricao=f"[UG{self.id}] Disjuntor 52G Inserido")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_dj52G_inserido, CONDIC_INDISPONIBILIZAR))

        self.l_dj52G_falta_vcc = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Dj52G_FALTA_VCC"], descricao=f"[UG{self.id}] Disjuntor 52G Falta VCC")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_dj52G_inserido, CONDIC_INDISPONIBILIZAR))

        self.l_alm_01_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_00"], descricao=f"[UG{self.id}] Emergência Supervisório Pressionada (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_01_b_00, CONDIC_INDISPONIBILIZAR))

        self.l_alm_01_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_02"], descricao=f"[UG{self.id}] Botão de Emergência Quadro Q49-U1 Pressionado (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_01_b_02, CONDIC_INDISPONIBILIZAR))

        self.l_alm_01_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_03"], descricao=f"[UG{self.id}] PCP-U1 - Falta de Fase CA Atuado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_01_b_03, CONDIC_NORMALIZAR))

        self.l_alm_01_b_06 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_06"], descricao=f"[UG{self.id}] Falha na Transição de UP para UPGM")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_01_b_06, CONDIC_NORMALIZAR))

        self.l_alm_01_b_07 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_07"], descricao=f"[UG{self.id}] Falha na Transição de UPGM para UMD ")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_01_b_07, CONDIC_NORMALIZAR))

        self.l_alm_01_b_08 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_08"], descricao=f"[UG{self.id}] Falha na Transição de UMD para UPS ")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_01_b_08, CONDIC_NORMALIZAR))

        self.l_alm_01_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_09"], descricao=f"[UG{self.id}] Falha na Transição de UPS para US")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_01_b_09, CONDIC_NORMALIZAR))

        self.l_alm_01_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_10"], descricao=f"[UG{self.id}] Falha na Transição de US para UPS")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_01_b_10, CONDIC_NORMALIZAR))

        self.l_alm_01_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_11"], descricao=f"[UG{self.id}] Falha na Transição de UPS para UMD")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_01_b_11, CONDIC_NORMALIZAR))

        self.l_alm_01_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_12"], descricao=f"[UG{self.id}] Falha na Transição de UMD para UPGM")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_01_b_12, CONDIC_NORMALIZAR))

        self.l_alm_01_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_13"], descricao=f"[UG{self.id}] Falha na Transição de UPGM para UP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_01_b_13, CONDIC_NORMALIZAR))

        self.l_alm_01_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_14"], descricao=f"[UG{self.id}] UHLM - Falha no Inversor da Bomba de Emergência (PINV)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_01_b_14, CONDIC_INDISPONIBILIZAR))

        self.l_alm_01_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme01_15"], descricao=f"[UG{self.id}] UHLM - Falta Fluxo de Água na Saída do Trocador de Calor")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_01_b_15, CONDIC_NORMALIZAR))

        self.l_alm_02_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_00"], descricao=f"[UG{self.id}] UHLM - Nível de Óleo Baixo")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_00, CONDIC_NORMALIZAR))

        self.l_alm_02_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_01"], descricao=f"[UG{self.id}] UHLM - Nível de Óleo Crítico (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_01, CONDIC_INDISPONIBILIZAR))

        self.l_alm_02_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_02"], descricao=f"[UG{self.id}] UHLM - Filtro de Pressão Sujo")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_02, CONDIC_NORMALIZAR))

        self.l_alm_02_b_04 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_04"], descricao=f"[UG{self.id}] UHLM - Falta Fluxo de Óleo na Bucha Radial do Mancal Combinado - Analógico")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_04, CONDIC_INDISPONIBILIZAR))

        self.l_alm_02_b_05 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_05"], descricao=f"[UG{self.id}] UHLM - Falta Fluxo de Óleo na Bomba Mecânica")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_05, CONDIC_INDISPONIBILIZAR))

        self.l_alm_02_b_06 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_06"], descricao=f"[UG{self.id}] UHLM - Pressão de Óleo Baixa na Linha do Mancal Combinado (Bloqueio 86M Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_06, CONDIC_INDISPONIBILIZAR))

        self.l_alm_02_b_07 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_07"], descricao=f"[UG{self.id}] UHLM - Partida da Maquina Bloqueada pelo Filtro Sujo (Bloqueio 86M Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_07, CONDIC_INDISPONIBILIZAR))

        self.l_alm_02_b_08 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_08"], descricao=f"[UG{self.id}] UHLM - Falha no Acionamento da Bomba 01 (CA) de Óleo")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_08, CONDIC_INDISPONIBILIZAR))

        self.l_alm_02_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_09"], descricao=f"[UG{self.id}] UHLM - Falha no Acionamento da Válvula Direcional da Bomba Mecânica")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_09, CONDIC_NORMALIZAR))

        self.l_alm_02_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_10"], descricao=f"[UG{self.id}] UHLM - Falha na Abertura da Válvula de Entrada de Água no Trocador de Calor")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_10, CONDIC_NORMALIZAR))

        self.l_alm_02_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_11"], descricao=f"[UG{self.id}] UHLM - Falha no Fechamento da Válvula de Entrada de Água no Trocador de Calor")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_11, CONDIC_INDISPONIBILIZAR))

        self.l_alm_02_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_12"], descricao=f"[UG{self.id}] UHLM - Falha na Abertura da Válvula de Saída de Água no Trocador de Calor")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_12, CONDIC_INDISPONIBILIZAR))

        self.l_alm_02_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_13"], descricao=f"[UG{self.id}] UHLM - Falha no Fechamento da Válvula de Saída de Água no Trocador de Calor")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_13, CONDIC_NORMALIZAR))

        self.l_alm_02_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_14"], descricao=f"[UG{self.id}] UHLM - Falta Fluxo de Óleo na Bomba 01 (CA) - Analógico")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_14, CONDIC_INDISPONIBILIZAR))

        self.l_alm_02_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme02_15"], descricao=f"[UG{self.id}] UHLM - Falta Fluxo de Óleo na Bomba 02 (Inversor) - Analógico")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_02_b_15, CONDIC_INDISPONIBILIZAR))

        self.l_alm_03_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_00"], descricao=f"[UG{self.id}] UHCT - Falha de Pressurização")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_00, CONDIC_INDISPONIBILIZAR))

        self.l_alm_03_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_01"], descricao=f"[UG{self.id}] UHCT - Pressão de Desligamento (Bloqueio 86M Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_01, CONDIC_INDISPONIBILIZAR))

        self.l_alm_03_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_02"], descricao=f"[UG{self.id}] UHCT - Nível de Óleo Baixo")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_02, CONDIC_NORMALIZAR))

        self.l_alm_03_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_03"], descricao=f"[UG{self.id}] UHCT - Nível de Óleo Crítico (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_03, CONDIC_INDISPONIBILIZAR))

        self.l_alm_03_b_04 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_04"], descricao=f"[UG{self.id}] UHCT - Filtro de Pressão Sujo")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_04, CONDIC_NORMALIZAR))

        self.l_alm_03_b_05 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_05"], descricao=f"[UG{self.id}] UHCT - Filtro de Retorno Sujo")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_05, CONDIC_NORMALIZAR))

        self.l_alm_03_b_06 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_06"], descricao=f"[UG{self.id}] UHCT - Pressão Crítica Mecânica (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_06, CONDIC_INDISPONIBILIZAR))

        self.l_alm_03_b_07 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_07"], descricao=f"[UG{self.id}] UHCT - Pressão Crítica Eletrônica (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_07, CONDIC_INDISPONIBILIZAR))

        self.l_alm_03_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_09"], descricao=f"[UG{self.id}] UHCT - Falha no Acionamento da Bomba de Óleo 01")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_09, CONDIC_NORMALIZAR))

        self.l_alm_03_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_10"], descricao=f"[UG{self.id}] UHCT - Falha no Acionamento da Bomba de Óleo 02")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_10, CONDIC_NORMALIZAR))

        self.l_alm_03_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_11"], descricao=f"[UG{self.id}] UHLM - Falha na Energização da Válvula Direcional da Bomba Mecânica com Turbina Rodando")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_11, CONDIC_INDISPONIBILIZAR))

        self.l_alm_03_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_12"], descricao=f"[UG{self.id}] Turbina - Falta Fluxo de Água na Vedação do Eixo - Lado Montante")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_12, CONDIC_NORMALIZAR))

        self.l_alm_03_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_13"], descricao=f"[UG{self.id}] Turbina - Falta Fluxo de Água na Vedação do Eixo - Lado Jusante")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_13, CONDIC_NORMALIZAR))

        self.l_alm_03_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_14"], descricao=f"[UG{self.id}] Turbina - Sem Pressão de Água na Vedação do Eixo - Lado Montante")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_14, CONDIC_NORMALIZAR))

        self.l_alm_03_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme03_15"], descricao=f"[UG{self.id}] Turbina - Sem Pressão de Água na Vedação do Eixo - Lado Jusante")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_03_b_15, CONDIC_NORMALIZAR))

        self.l_alm_04_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_00"], descricao=f"[UG{self.id}] Turbina - Falha no Fechamento do Distribuidor")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_00, CONDIC_NORMALIZAR))

        self.l_alm_04_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_01"], descricao=f"[UG{self.id}] Turbina - Pás do Distribuidor Desalinhadas (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_01, CONDIC_INDISPONIBILIZAR))

        self.l_alm_04_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_02"], descricao=f"[UG{self.id}] Turbina - Falta Fluxo ou Pressão de Água na Vedação do Eixo (Bloqueio 86M Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_02, CONDIC_NORMALIZAR))

        self.l_alm_04_b_04 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_04"], descricao=f"[UG{self.id}] Filtro de Água - Atenção! Filtro 01 em Modo Manual")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_04, CONDIC_NORMALIZAR))

        self.l_alm_04_b_05 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_05"], descricao=f"[UG{self.id}] Filtro de Água - Atenção! Filtro 02 em Modo Manual")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_05, CONDIC_NORMALIZAR))

        self.l_alm_04_b_06 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_06"], descricao=f"[UG{self.id}] Filtro de Água - Falha no Sistema")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_06, CONDIC_NORMALIZAR))

        self.l_alm_04_b_07 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_07"], descricao=f"[UG{self.id}] Filtro de Água - Falta de Alimentação CA")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_07, CONDIC_NORMALIZAR))

        self.l_alm_04_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_09"], descricao=f"[UG{self.id}] Freio - Falha na Desaplicação")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_09, CONDIC_NORMALIZAR))

        self.l_alm_04_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_10"], descricao=f"[UG{self.id}] Freio - Pastilha Gasta")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_10, CONDIC_NORMALIZAR))

        self.l_alm_04_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_11"], descricao=f"[UG{self.id}] Freio - Pressão Baixa")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_11, CONDIC_NORMALIZAR))

        self.l_alm_04_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_12"], descricao=f"[UG{self.id}] Reg Velocidade - TRIP (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_12, CONDIC_NORMALIZAR))

        self.l_alm_04_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_13"], descricao=f"[UG{self.id}] Reg Velocidade - Falha Watchdog (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_13, CONDIC_NORMALIZAR))

        self.l_alm_04_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_14"], descricao=f"[UG{self.id}] Reg Velocidade - Falha na Válvula de Segurança")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_14, CONDIC_NORMALIZAR))

        self.l_alm_04_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme04_15"], descricao=f"[UG{self.id}] Dispositivo de SobreVelocidade Mecânico Atuado (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_15, CONDIC_INDISPONIBILIZAR))

        self.l_alm_05_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_00"], descricao=f"[UG{self.id}] Reg Velocidade - Falha Sensor de Velocidade (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_05_b_00, CONDIC_NORMALIZAR))

        self.l_alm_05_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_03"], descricao=f"[UG{self.id}] Reg Tensão - Falha Watchdog (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_05_b_03, CONDIC_NORMALIZAR))

        self.l_alm_05_b_04 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_04"], descricao=f"[UG{self.id}] Reg Tensão - Falha no Contator de Campo ")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_05_b_04, CONDIC_NORMALIZAR))

        self.l_alm_05_b_05 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_05"], descricao=f"[UG{self.id}] Reg Tensão - Falha Painel PRT em Modo Local")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_05_b_05, CONDIC_NORMALIZAR))

        self.l_alm_05_b_06 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_06"], descricao=f"[UG{self.id}] Reg Tensão - Falha Painel PRT - Disjuntor dos TPs Aberto")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_05_b_06, CONDIC_INDISPONIBILIZAR))

        self.l_alm_05_b_07 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme05_07"], descricao=f"[UG{self.id}] GRTD 2000 - Falha no Sincronismo")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_05_b_07, CONDIC_NORMALIZAR))

        self.l_alm_06_b_04 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme06_04"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Falha no Disjuntor 50_62BF")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_06_b_04, CONDIC_INDISPONIBILIZAR))

        self.l_alm_06_b_05 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme06_05"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Falha de Hardware")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_06_b_05, CONDIC_NORMALIZAR))

        self.l_alm_06_b_08 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme06_08"], descricao=f"[UG{self.id}] Disjuntor 52G - Inconsistência Status Aberto/Fechado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_06_b_08, CONDIC_NORMALIZAR))

        self.l_alm_06_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme06_09"], descricao=f"[UG{self.id}] Disjuntor 52G - Falha no Carregamento da Mola")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_06_b_09, CONDIC_NORMALIZAR))

        self.l_alm_06_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme06_10"], descricao=f"[UG{self.id}] Disjuntor 52G - Falta Tensão de Comando Vcc")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_06_b_10, CONDIC_NORMALIZAR))

        self.l_alm_06_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme06_11"], descricao=f"[UG{self.id}] Disjuntor 52G - Falha na Abertura")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_06_b_11, CONDIC_INDISPONIBILIZAR))

        self.l_alm_06_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme06_12"], descricao=f"[UG{self.id}] Disjuntor 52G - Grade Frontal do CSG-U1 Aberta (Abertura 52L- SEL787)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_06_b_12, CONDIC_INDISPONIBILIZAR))

        self.l_alm_06_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme06_13"], descricao=f"[UG{self.id}] Disjuntor 52G - Grade Traseira do CSG-U1 Aberta (Abertura 52L - SEL787)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_06_b_13, CONDIC_INDISPONIBILIZAR))

        self.l_alm_06_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme06_14"], descricao=f"[UG{self.id}] Disjuntor 52G - Tampa Traseira do CSG-U1 Aberta (Abertura 52L - SEL787)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_06_b_14, CONDIC_INDISPONIBILIZAR))

        self.l_alm_06_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme06_15"], descricao=f"[UG{self.id}] Disjuntor 52G - Posição de Teste (Extraído)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_06_b_15, CONDIC_INDISPONIBILIZAR))

        self.l_alm_07_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_00"], descricao=f"[UG{self.id}] Controle de Potência - Falha Nível Minimo Alarme")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_00, CONDIC_NORMALIZAR))

        self.l_alm_07_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_01"], descricao=f"[UG{self.id}] Controle de Potência - Falha Nível Minimo Trip 86M")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_01, CONDIC_NORMALIZAR))

        self.l_alm_07_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_02"], descricao=f"[UG{self.id}] Controle de Potência - Falha Potência Minima Alarme")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_02, CONDIC_NORMALIZAR))

        self.l_alm_07_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_03"], descricao=f"[UG{self.id}] Controle de Potência - Falha Potência Minima Trip 86M")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_03, CONDIC_NORMALIZAR))

        self.l_alm_07_b_06 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_06"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura da Fase R do Gerador")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_06, CONDIC_NORMALIZAR))

        self.l_alm_07_b_07 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_07"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura da Fase S do Gerador")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_07, CONDIC_NORMALIZAR))

        self.l_alm_07_b_08 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_08"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura da Fase T do Gerador")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_08, CONDIC_NORMALIZAR))

        self.l_alm_07_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_09"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura do Casquilho 01 do Mancal LA")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_09, CONDIC_NORMALIZAR))

        self.l_alm_07_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_10"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura do Casquilho 02 do Mancal LA")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_10, CONDIC_NORMALIZAR))

        self.l_alm_07_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_11"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura do Casquilho 01 do Mancal LNA")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_11, CONDIC_NORMALIZAR))

        self.l_alm_07_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_12"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura do Casquilho 02 do Mancal LNA")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_12, CONDIC_NORMALIZAR))

        self.l_alm_07_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_13"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura do Gaxeteiro Lado Montante")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_13, CONDIC_NORMALIZAR))

        self.l_alm_07_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_14"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura do Gaxeteiro Lado Jusante")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_14, CONDIC_NORMALIZAR))

        self.l_alm_07_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme07_15"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura da Bucha Radial do Mancal Combinado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_07_b_15, CONDIC_NORMALIZAR))

        self.l_alm_08_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme08_00"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura das Sapatas Axiais Escora do Mancal Combinado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_08_b_00, CONDIC_NORMALIZAR))

        self.l_alm_08_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme08_01"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura das Sapatas Axiais Contra Escora do Mancal Combinado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_08_b_01, CONDIC_NORMALIZAR))

        self.l_alm_08_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme08_02"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura do Óleo da UHCT")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_08_b_02, CONDIC_NORMALIZAR))

        self.l_alm_08_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme08_03"], descricao=f"[UG{self.id}] Falha no Sensor de Temperatura do Óleo da UHLM")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_08_b_03, CONDIC_NORMALIZAR))

        self.l_alm_08_b_07 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme08_07"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura da Fase R do Gerador Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_08_b_07, CONDIC_NORMALIZAR))

        self.l_alm_08_b_08 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme08_08"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura da Fase S do Gerador Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_08_b_08, CONDIC_NORMALIZAR))

        self.l_alm_08_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme08_09"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura da Fase T do Gerador Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_08_b_09, CONDIC_NORMALIZAR))

        self.l_alm_08_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme08_10"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura do Casquilho 01 do Mancal LA Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_08_b_10, CONDIC_NORMALIZAR))

        self.l_alm_08_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme08_11"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura do Casquilho 02 do Mancal LA Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_08_b_11, CONDIC_NORMALIZAR))

        self.l_alm_08_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme08_12"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura do Casquilho 01 do Mancal LNA Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_08_b_12, CONDIC_NORMALIZAR))

        self.l_alm_08_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme08_13"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura do Casquilho 02 do Mancal LNA Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_08_b_13, CONDIC_NORMALIZAR))

        self.l_alm_08_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme08_14"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura do Gaxeteiro Lado Montante Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_08_b_14, CONDIC_NORMALIZAR))

        self.l_alm_08_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme08_15"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura do Gaxeteiro Lado Jusante Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_08_b_15, CONDIC_NORMALIZAR))

        self.l_alm_09_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_00"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura da Bucha Radial do Mancal Combinado Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_00, CONDIC_NORMALIZAR))

        self.l_alm_09_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_01"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura das Sapatas Axiais Escora do Mancal Combinado Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_01, CONDIC_NORMALIZAR))

        self.l_alm_09_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_02"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura das Sapatas Axiais Contra Escora do Mancal Combinado Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_02, CONDIC_NORMALIZAR))

        self.l_alm_09_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_03"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura do Óleo da UHCT Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_03, CONDIC_NORMALIZAR))

        self.l_alm_09_b_04 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_04"], descricao=f"[UG{self.id}] Alarme de Sobretemperatura do Óleo da UHLM Via CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_04, CONDIC_NORMALIZAR))

        self.l_alm_09_b_06 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_06"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura da Fase R do Gerador (Trip 86M)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_06, CONDIC_INDISPONIBILIZAR))

        self.l_alm_09_b_07 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_07"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura da Fase S do Gerador (Trip 86M)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_07, CONDIC_INDISPONIBILIZAR))

        self.l_alm_09_b_08 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_08"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura da Fase T do Gerador (Trip 86M)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_08, CONDIC_INDISPONIBILIZAR))

        self.l_alm_09_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_09"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura do Casquilho 01 do Mancal LA (Trip 86M)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_09, CONDIC_INDISPONIBILIZAR))

        self.l_alm_09_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_10"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura do Casquilho 02 do Mancal LA (Trip 86M)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_10, CONDIC_INDISPONIBILIZAR))

        self.l_alm_09_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_11"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura do Casquilho 01 do Mancal LNA (Trip 86M)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_11, CONDIC_INDISPONIBILIZAR))

        self.l_alm_09_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_12"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura do Casquilho 02 do Mancal LNA (Trip 86M)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_12, CONDIC_INDISPONIBILIZAR))

        self.l_alm_09_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_13"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura do Gaxeteiro Lado Montante (Trip 86M)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_13, CONDIC_INDISPONIBILIZAR))

        self.l_alm_09_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_14"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura do Gaxeteiro Lado Jusante (Trip 86M)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_14, CONDIC_INDISPONIBILIZAR))

        self.l_alm_09_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme09_15"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura da Bucha Radial do Mancal Combinado (Trip 86M)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_09_b_15, CONDIC_INDISPONIBILIZAR))

        self.l_alm_10_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_00"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura das Sapatas Axiais Escora do Mancal Combinado (Trip 86M)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_00, CONDIC_INDISPONIBILIZAR))

        self.l_alm_10_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_01"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura das Sapatas Axiais Contra Escora do Mancal Combinado (Trip 86M)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_01, CONDIC_INDISPONIBILIZAR))

        self.l_alm_10_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_02"], descricao=f"[UG{self.id}] Sobretemperatura do Óleo da UHCT (Trip 86M via CLP)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_02, CONDIC_INDISPONIBILIZAR))

        self.l_alm_10_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_03"], descricao=f"[UG{self.id}] Sobretemperatura do Óleo da UHLM (Trip 86M via CLP)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_03, CONDIC_INDISPONIBILIZAR))

        self.l_alm_10_b_05 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_05"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura da Fase R do Gerador (Trip 86E)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_05, CONDIC_INDISPONIBILIZAR))

        self.l_alm_10_b_06 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_06"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura da Fase S do Gerador (Trip 86E)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_06, CONDIC_INDISPONIBILIZAR))

        self.l_alm_10_b_07 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_07"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura da Fase T do Gerador (Trip 86E)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_07, CONDIC_INDISPONIBILIZAR))

        self.l_alm_10_b_08 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_08"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura do Casquilho 01 do Mancal LA (Trip 86H)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_08, CONDIC_INDISPONIBILIZAR))

        self.l_alm_10_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_09"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura do Casquilho 02 do Mancal LA (Trip 86H)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_09, CONDIC_INDISPONIBILIZAR))

        self.l_alm_10_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_10"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura do Casquilho 01 do Mancal LNA (Trip 86H)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_10, CONDIC_INDISPONIBILIZAR))

        self.l_alm_10_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_11"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura do Casquilho 02 do Mancal LNA (Trip 86H)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_11, CONDIC_INDISPONIBILIZAR))

        self.l_alm_10_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_12"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura do Gaxeteiro Lado Montante (Trip 86H)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_12, CONDIC_NORMALIZAR))

        self.l_alm_10_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_13"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura do Gaxeteiro Lado Jusante (Trip 86H)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_13, CONDIC_NORMALIZAR))

        self.l_alm_10_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_14"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura da Bucha Radial do Mancal Combinado (Trip 86H)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_14, CONDIC_INDISPONIBILIZAR))

        self.l_alm_10_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme10_15"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura das Sapatas Axiais Escora do Mancal Combinado (Trip 86H)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_15, CONDIC_INDISPONIBILIZAR))

        self.l_alm_11_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme11_00"], descricao=f"[UG{self.id}] Relé de Proteção - Sobretemperatura das Sapatas Axiais Contra Escora do Mancal Combinado (Trip 86H)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_11_b_00, CONDIC_INDISPONIBILIZAR))

        self.l_alm_11_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme11_01"], descricao=f"[UG{self.id}] Sobretemperatura do Óleo da UHCT (Trip 86H via CLP)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_11_b_01, CONDIC_INDISPONIBILIZAR))

        self.l_alm_11_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme11_02"], descricao=f"[UG{self.id}] Sobretemperatura do Óleo da UHLM (Trip 86H via CLP)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_11_b_02, CONDIC_INDISPONIBILIZAR))

        self.l_alm_11_b_06 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme11_06"], descricao=f"[UG{self.id}] GRTD2000 - Falha na Ponte de Excitação (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_11_b_06, CONDIC_NORMALIZAR))

        self.l_alm_11_b_07 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme11_07"], descricao=f"[UG{self.id}] GRTD2000 - Falha na Saída Analógica do Distribuidor (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_11_b_07, CONDIC_INDISPONIBILIZAR))

        self.l_alm_11_b_08 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme11_08"], descricao=f"[UG{self.id}] GRTD2000 - Falha na Saída Analógica do Rotor (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_11_b_08, CONDIC_INDISPONIBILIZAR))

        self.l_alm_11_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme11_09"], descricao=f"[UG{self.id}] GRTD2000 - Falha Realimentação de Tensão (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_11_b_09, CONDIC_NORMALIZAR))

        self.l_alm_11_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme11_10"], descricao=f"[UG{self.id}] GRTD2000 - Falha Sobretensão de Excitação (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_11_b_10, CONDIC_NORMALIZAR))

        self.l_alm_11_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme11_11"], descricao=f"[UG{self.id}] GRTD2000 - Falha Sobrecorrente de Excitação (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_11_b_11, CONDIC_INDISPONIBILIZAR))

        self.l_alm_11_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme11_12"], descricao=f"[UG{self.id}] GRTD2000 - Falha Sobrevelocidade Eletrônica (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_11_b_12, CONDIC_NORMALIZAR))

        self.l_alm_11_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme11_13"], descricao=f"[UG{self.id}] GRTD2000 - Falha na Realimentação de Velocidade (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_11_b_13, CONDIC_NORMALIZAR))

        self.l_alm_11_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme11_14"], descricao=f"[UG{self.id}] GRTD2000 - Falha na Realimentação do Distribuidor (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_11_b_14, CONDIC_INDISPONIBILIZAR))

        self.l_alm_11_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme11_15"], descricao=f"[UG{self.id}] GRTD2000 - Falha na Realimentação do Rotor (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_11_b_15, CONDIC_INDISPONIBILIZAR))

        self.l_alm_12_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_01"], descricao=f"[UG{self.id}] UHLM - Falta Fluxo de Óleo na Bucha Radial do Mancal Combinado - Digital")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_01, CONDIC_INDISPONIBILIZAR))

        self.l_alm_12_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_02"], descricao=f"[UG{self.id}] UHLM - Falta Fluxo de Óleo na Bomba 01 (CA) - Digital")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_02, CONDIC_INDISPONIBILIZAR))

        self.l_alm_12_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_03"], descricao=f"[UG{self.id}] UHLM - Falta Fluxo de Óleo na Bomba 02 (Inversor) - Digital")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_03, CONDIC_INDISPONIBILIZAR))

        self.l_alm_12_b_04 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_04"], descricao=f"[UG{self.id}] UHLM - ATENÇÃO! Tempo Excedido no Teste Bomba Retaguarda Operacional")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_04, CONDIC_INDISPONIBILIZAR))

        self.l_alm_12_b_05 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_05"], descricao=f"[UG{self.id}] GRTD2000 - Falha de Comunicação com o CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_05, CONDIC_NORMALIZAR))

        self.l_alm_12_b_06 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_06"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Falha de Comunicação com o CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_06, CONDIC_NORMALIZAR))

        self.l_alm_12_b_07 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_07"], descricao=f"[UG{self.id}] Regulador de Tensão WEG ECW500 - Falha de Comunicação com o CLP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_07, CONDIC_NORMALIZAR))

        self.l_alm_12_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_09"], descricao=f"[UG{self.id}] PCP-U1 - Alimentação Circuitos de Comando - Disjuntor Q125.0 Desligado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_09, CONDIC_INDISPONIBILIZAR))

        self.l_alm_12_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_10"], descricao=f"[UG{self.id}] PCP-U1 - Alimentação Regulador GRTD2000 - Disjuntor Q125.1 Desligado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_10, CONDIC_INDISPONIBILIZAR))

        self.l_alm_12_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_11"], descricao=f"[UG{self.id}] PCP-U1 - Alimentação Relés de Proteção - Disjuntor Q125.2 Desligado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_11, CONDIC_INDISPONIBILIZAR))

        self.l_alm_12_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_12"], descricao=f"[UG{self.id}] PCP-U1 - Alimentação Válvulas do Sistema de Água - Disjuntor Q125.4 Desligado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_12, CONDIC_NORMALIZAR))

        self.l_alm_12_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_13"], descricao=f"[UG{self.id}] PCP-U1 - Alimentação Válvulas Proporcionais e Transdutores de Posição - Disjuntor Q24.0 Desligado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_13, CONDIC_INDISPONIBILIZAR))

        self.l_alm_12_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_14"], descricao=f"[UG{self.id}] CSG-U1 - Alimentação Motor Carga Mola Disj 52G - Disjuntor Q220.1 Desligado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_14, CONDIC_INDISPONIBILIZAR))

        self.l_alm_12_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme12_15"], descricao=f"[UG{self.id}] CSG-U1 - Alimentação Circuito de Comando Disj 52G - Disjuntor Q125.0 Desligado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_15, CONDIC_INDISPONIBILIZAR))

        self.l_alm_13_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme13_00"], descricao=f"[UG{self.id}] Q49-U1 - Alimentação Módulo de Aquisição de Temperaturas SEL2600 - Disjuntor Q125.0 Desligado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_00, CONDIC_NORMALIZAR))

        self.l_alm_13_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme13_01"], descricao=f"[UG{self.id}] PCP-U1 - Bomba de Óleo 01 da UHCT - Disjuntor Motor QM1 Desligado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_01, CONDIC_INDISPONIBILIZAR))

        self.l_alm_13_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme13_02"], descricao=f"[UG{self.id}] PCP-U1 - Bomba de Óleo 02 da UHCT - Disjuntor Motor QM2 Desligado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_02, CONDIC_INDISPONIBILIZAR))

        self.l_alm_13_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme13_03"], descricao=f"[UG{self.id}] PCP-U1 - Bomba de Óleo da UHLM - Disjuntor Motor QM3 Desligado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_03, CONDIC_INDISPONIBILIZAR))

        self.l_alm_13_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme13_09"], descricao=f"[UG{self.id}] Falha na Entrada Analógica de Fluxo de Óleo na Bucha Radial do Mancal Combinado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_09, CONDIC_INDISPONIBILIZAR))

        self.l_alm_13_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme13_10"], descricao=f"[UG{self.id}] Falha na Entrada Analógica de Fluxo de Óleo da Bomba 01")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_10, CONDIC_INDISPONIBILIZAR))

        self.l_alm_13_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme13_11"], descricao=f"[UG{self.id}] Falha na Entrada Analógica de Fluxo de Óleo da Bomba 02")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_11, CONDIC_INDISPONIBILIZAR))

        self.l_alm_13_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme13_12"], descricao=f"[UG{self.id}] Falha na Entrada Analógica de Fluxo de Óleo na Bomba Mecânica")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_12, CONDIC_INDISPONIBILIZAR))

        self.l_alm_13_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme13_13"], descricao=f"[UG{self.id}] Falha na Entrada Analógica de Vibração Vertical do Mancal Combinado da Turbina")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_13, CONDIC_INDISPONIBILIZAR))

        self.l_alm_13_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme13_14"], descricao=f"[UG{self.id}] Falha na Entrada Analógica de Vibração Horizontal do Mancal Combinado da Turbina")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_14, CONDIC_INDISPONIBILIZAR))

        self.l_alm_13_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme13_15"], descricao=f"[UG{self.id}] Falha na Entrada Analógica de Vibração do Mancal Combinado Axial da Turbina")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_15, CONDIC_INDISPONIBILIZAR))

        self.l_alm_14_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme14_00"], descricao=f"[UG{self.id}] Falha na Entrada Analógica de Pressão do Conduto")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_00, CONDIC_NORMALIZAR))

        self.l_alm_14_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme14_01"], descricao=f"[UG{self.id}] Falha na Entrada Analógica de Pressão da Turbina")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_01, CONDIC_NORMALIZAR))

        self.l_alm_14_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme14_02"], descricao=f"[UG{self.id}] Falha na Entrada Analógica de Vibração do Mancal Lado Acoplado do Gerador")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_02, CONDIC_INDISPONIBILIZAR))

        self.l_alm_14_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme14_03"], descricao=f"[UG{self.id}] Falha na Entrada Analógica de Vibração do Mancal Lado Não Acoplado do Gerador")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_03, CONDIC_INDISPONIBILIZAR))

        self.l_alm_14_b_04 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme14_04"], descricao=f"[UG{self.id}] Falha na Entrada Analógica de Pressão de Óleo da UHCT")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_04, CONDIC_NORMALIZAR))

        self.l_alm_14_b_05 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme14_05"], descricao=f"[UG{self.id}] Falha na Entrada Analógica de Temperatura do Óleo da UHCT")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_05, CONDIC_NORMALIZAR))

        self.l_alm_14_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme14_10"], descricao=f"[UG{self.id}] PCP-U1 - Sensor de Fumaça Atuado ")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_10, CONDIC_NORMALIZAR))

        self.l_alm_14_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme14_11"], descricao=f"[UG{self.id}] PCP-U1 - Sensor de Fumaça Desconectado")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_11, CONDIC_NORMALIZAR))

        self.l_alm_14_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme14_12"], descricao=f"[UG{self.id}] PINV - Controlador Boost 01 - Falha Circuito de Potência/Falha Contator 1K1 ou 1K2/Falha Pré-Carga")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_12, CONDIC_NORMALIZAR))

        self.l_alm_14_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme14_13"], descricao=f"[UG{self.id}] PINV - Controlador Boost 01 - Sub_Sobretensão ou Sub_SobreCorrente Link 540Vcc/Sub_Sobre Disparo IGBT")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_13, CONDIC_NORMALIZAR))

        self.l_alm_14_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme14_14"], descricao=f"[UG{self.id}] PINV - Controlador Boost 02 - Falha Circuito de Potência/Falha Contator 1K1 ou 1K2/Falha Pré-Carga")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_14, CONDIC_NORMALIZAR))

        self.l_alm_14_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme14_15"], descricao=f"[UG{self.id}] PINV - Controlador Boost 02 - Sub_Sobretensão ou Sub_SobreCorrente Link 540Vcc/Sub_Sobre Disparo IGBT")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_15, CONDIC_NORMALIZAR))

        self.l_alm_15_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_00"], descricao=f"[UG{self.id}] Alarme Vibração Vertical Excessiva Mancal Combinado da Turbina")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_00, CONDIC_NORMALIZAR))

        self.l_alm_15_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_01"], descricao=f"[UG{self.id}] Trip Vibração Vertical Excessiva Mancal Combinado da Turbina (Bloqueio 86M Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_01, CONDIC_INDISPONIBILIZAR))

        self.l_alm_15_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_02"], descricao=f"[UG{self.id}] Alarme Vibração Horizontal Excessiva Mancal Combinado da Turbina")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_02, CONDIC_NORMALIZAR))

        self.l_alm_15_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_03"], descricao=f"[UG{self.id}] Trip Vibração Horizontal Excessiva Mancal Combinado da Turbina (Bloqueio 86M Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_03, CONDIC_INDISPONIBILIZAR))

        self.l_alm_15_b_04 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_04"], descricao=f"[UG{self.id}] Alarme Vibração Axial Excessiva Mancal Combinado da Turbina")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_04, CONDIC_NORMALIZAR))

        self.l_alm_15_b_05 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_05"], descricao=f"[UG{self.id}] Trip Vibração Axial Excessiva Mancal Combinado da Turbina (Bloqueio 86M Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_05, CONDIC_INDISPONIBILIZAR))

        self.l_alm_15_b_06 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_06"], descricao=f"[UG{self.id}] Alarme Vibração Excessiva Mancal Lado Acoplado do Gerador ")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_06, CONDIC_NORMALIZAR))

        self.l_alm_15_b_07 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_07"], descricao=f"[UG{self.id}] Trip Vibração Excessiva Mancal Lado Acoplado do Gerador (Bloqueio 86M Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_07, CONDIC_INDISPONIBILIZAR))

        self.l_alm_15_b_08 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_08"], descricao=f"[UG{self.id}] Alarme Vibração Excessiva Mancal Lado Não Acoplado do Gerador")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_08, CONDIC_NORMALIZAR))

        self.l_alm_15_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_09"], descricao=f"[UG{self.id}] Trip Vibração Excessiva Mancal Lado Não Acoplado do Gerador (Bloqueio 86M Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_09, CONDIC_INDISPONIBILIZAR))

        self.l_alm_15_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_10"], descricao=f"[UG{self.id}] Diferencial de Nível de Água - Grade Suja TRIP")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_10, CONDIC_NORMALIZAR))

        self.l_alm_15_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_12"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Proteção Diferencial Residual (87G) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_12, CONDIC_INDISPONIBILIZAR))

        self.l_alm_15_b_13 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_13"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Proteção Diferencial de Neutro (87N) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_13, CONDIC_INDISPONIBILIZAR))

        self.l_alm_15_b_14 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_14"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Sobrecorrente com Restrição de Tensão (51V) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_14, CONDIC_INDISPONIBILIZAR))

        self.l_alm_15_b_15 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme15_15"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Sobrecorrente Instantânea de Fase (50P) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_15, CONDIC_INDISPONIBILIZAR))

        self.l_alm_16_b_00 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme16_00"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Energização Indevida (50M) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_00, CONDIC_NORMALIZAR))

        self.l_alm_16_b_01 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme16_01"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Sobrecorrente de Sequência Negativa (46Q) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_01, CONDIC_INDISPONIBILIZAR))

        self.l_alm_16_b_02 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme16_02"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Sobrecarga Térmica (49T) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_02, CONDIC_INDISPONIBILIZAR))

        self.l_alm_16_b_03 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme16_03"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Sobre Excitação Volts/Hertz (24) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_03, CONDIC_NORMALIZAR))

        self.l_alm_16_b_04 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme16_04"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Sobrecorrente Residual Instantânea (50G) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_04, CONDIC_INDISPONIBILIZAR))

        self.l_alm_16_b_05 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme16_05"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Perda de Excitação (40Q) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_05, CONDIC_INDISPONIBILIZAR))

        self.l_alm_16_b_06 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme16_06"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Sobrecorrente Instantânea de Neutro (50N) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_06, CONDIC_INDISPONIBILIZAR))

        self.l_alm_16_b_07 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme16_07"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Potência Reversa (32P) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_07, CONDIC_INDISPONIBILIZAR))

        self.l_alm_16_b_08 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme16_08"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Sobretensão de Fase (59P) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_08, CONDIC_NORMALIZAR))

        self.l_alm_16_b_09 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme16_09"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Sobretensão Residual (59G) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_09, CONDIC_INDISPONIBILIZAR))

        self.l_alm_16_b_10 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme16_10"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Sobrefrequência (81O) (Bloqueio 86E Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_10, CONDIC_NORMALIZAR))

        self.l_alm_16_b_11 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme16_11"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Falha do Disjuntor (50_62BF) (Bloqueio 86H Trip)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_11, CONDIC_INDISPONIBILIZAR))

        self.l_alm_16_b_12 = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["Alarme16_12"], descricao=f"[UG{self.id}] Relé de Proteção SEL700G - Falha RTD's ou Falha de Comunicação com o Módulo SEL-2600 (Bloqueio 86M T)")
        dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_12, CONDIC_NORMALIZAR))


        ## MENSAGEIRO
        self.l_modo_local = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["OPER_MODO_LOCAL"], descricao=f"[UG{self.id}] Operação Modo Local Acionado")
        self.l_dj_07 = lei.LeituraModbus(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["DJ_07"], descricao=f"[UG{self.id}] Q49 - Disjuntor Q125.0 UG1 - Alimentação SEL2600")
        self.l_uhct_nv_oleo_l = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHCT_NIVEL_OLEO_L"], descricao=f"[UG{self.id}] UHCT Nível Óleo Baixo")
        self.l_uhct_nv_oleo_h = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHCT_NIVEL_OLEO_H"], descricao=f"[UG{self.id}] UHCT Nível Óleo Alto")
        self.l_uhct_nv_oleo_hh = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHCT_NIVEL_OLEO_HH"], descricao=f"[UG{self.id}] UHCT Nível Óleo Muito Alto")
        self.l_uhlm_modo_local = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_MODO_LOCAL"], descricao=f"[UG{self.id}] UHLM Modo Local Acionado")
        self.l_uhlm_nv_oleo_l = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_NIVEL_OLEO_L"], descricao=f"[UG{self.id}] UHLM Nível Óleo Baixo")
        self.l_uhlm_nv_oleo_h = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_NIVEL_OLEO_H"], descricao=f"[UG{self.id}] UHLM Nível Óleo Alto")
        self.l_uhlm_nv_oleo_hh = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["UHLM_NIVEL_OLEO_HH"], descricao=f"[UG{self.id}] UHLM Nível Óleo Muito Alto")
        self.l_turb_sens_desati = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TURB_SENS_DESATIVADO"], descricao=f"[UG{self.id}] Turbina Sensor Desativado")
        self.l_turb_fren_manual = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["TURB_FRENA_MANUAL"], descricao=f"[UG{self.id}] Turbina Frenagem Manual")
        self.l_rv_ctrl_man_distr = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["REG_V_CTRL_MANUAL_DISTRI"], descricao=f"[UG{self.id}] RV Controle Manual Distribuidor")
        self.l_rv_ctrl_man_valv = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["REG_V_CTRL_MANUAL_VALV"], descricao=f"[UG{self.id}] RV Controle Manual Válvula")
        self.l_sinc_modo_manual = lei.LeituraModbusBit(self.clp[f"UG{self.id}"], REG_UG[f"UG{self.id}"]["SINC_MODO_MANUAL"], descricao=f"[UG{self.id}] Sincronoscópio Modo Manual")


        ## CONDICIONADORES ESPECÍFICOS POR UNIDADE
        # UG1
        if self.id == 1:
            self.l_se_dj_32 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_32"], descricao="[UG1][SE] PDSA-CC - Alimentação das Cargas da UG01 - Disj. 1Q125.0")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_32, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_33 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_33"], descricao="[UG1][SE] PDSA-CC - Alimentação do Painel PCP-U1 - Disj. 1Q125.1")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_33, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_35 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_35"], descricao="[UG1][SE] PDSA-CC - Alimentação do Cubículo CSG-U1 - Disj. 1Q125.3")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_35, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_36 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_36"], descricao="[UG1][SE] PDSA-CC - Alimentação Painel do Regulador de Tensão UG01 - Disj. 1Q125.4")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_36, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_77 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_77"], descricao="[UG1][SE] PDSA-CC - Alimentação Painel do Regulador de Tensão UG01 - Disj. 1Q125.4")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_77, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_78 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_78"], descricao="[UG1][SE] PDSA-CA - Alimentação das Cargas Não Essenciais da UG01 - Disj. 1Q380.1")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_78, CONDIC_INDISPONIBILIZAR))

            self.l_alm_04_b_10 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme04_10"], descricao="[UG1] Cubículo CSA-U1 - Fusível Queimado ")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_10, CONDIC_INDISPONIBILIZAR))

            self.l_alm_04_b_11 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme04_11"], descricao="[UG1] Cubículo CSA-U1 - Grade Frontal Aberta  (Abertura 52L- SEL787 - TRIP)")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_11, CONDIC_INDISPONIBILIZAR))

            self.l_alm_04_b_12 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme04_12"], descricao="[UG1] Cubículo CSA-U1 - Grade Traseira Aberta (Abertura 52L- SEL787 - TRIP)")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_12, CONDIC_INDISPONIBILIZAR))

            self.l_alm_10_b_08 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme10_08"], descricao="[UG1] PCP-U1 - Alimentação Fonte 125/24Vcc - Disj. Q125.3 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_08, CONDIC_INDISPONIBILIZAR))

            self.l_alm_10_b_09 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme10_09"], descricao="[UG1] PCP-U1 - Alimentação Circuitos de Comando - Disj. Q24.1 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_09, CONDIC_INDISPONIBILIZAR))

            self.l_alm_12_b_01 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme12_01"], descricao="[UG1] PDSA-CC - Alimentação do Cubículo CSA-U1 - Disj. Q125.5 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_01, CONDIC_INDISPONIBILIZAR))

            self.l_alm_12_b_07 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme12_07"], descricao="[UG1] PDSA-CC - Alimentação das Cargas da Disj. 1Q125.0 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_07, CONDIC_INDISPONIBILIZAR))

            self.l_alm_12_b_08 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme12_08"], descricao="[UG1] PDSA-CC - Alimentação do Painel PCP-U1 - Disj. 1Q125.1 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_08, CONDIC_INDISPONIBILIZAR))

            self.l_alm_12_b_09 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme12_09"], descricao="[UG1] PDSA-CC - Alimentação do Quadro Q49-U1 - Disj. 1Q125.2 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_09, CONDIC_INDISPONIBILIZAR))

            self.l_alm_12_b_10 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme12_10"], descricao="[UG1] PDSA-CC - Alimentação do Cubículo CSG-U1 - Disj. 1Q125.3 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_10, CONDIC_INDISPONIBILIZAR))

            self.l_alm_12_b_11 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme12_11"], descricao="[UG1] PDSA-CC - Alimentação Painel do Regulador de Tensão Disj. 1Q125.4 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_11, CONDIC_INDISPONIBILIZAR))

            self.l_alm_12_b_12 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme12_12"], descricao="[UG1] PDSA-CC - Alimentação do Filtro Duplo Disj. 1Q125.5 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_12, CONDIC_INDISPONIBILIZAR))

            self.l_alm_12_b_13 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme12_13"], descricao="[UG1] PDSA-CC - Alimentação Reserva - Disj. 1Q125.6 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_13, CONDIC_NORMALIZAR))

            self.l_alm_15_b_12 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme15_12"], descricao="[UG1] PDSA-CA - Alimentação das Cargas Essenciais da Disj. 1Q380.0 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_12, CONDIC_INDISPONIBILIZAR))

            self.l_alm_15_b_13 = lei.LeituraModbusBit(self.clp["UG1"], REG_UG["UG1"]["Alarme15_13"], descricao="[UG1] PDSA-CA - Alimentação das Cargas Não Essenciais da Disj. 1Q380.1 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_13, CONDIC_INDISPONIBILIZAR))

            self.l_alm_22_b_10 = lei.LeituraModbusBit(self.clp["UG1"], REG_TDA["Alarme22_10"], descricao="[TDA] UHTA01 - Sobretemperatura do Óleo - Trip")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_22_b_10, CONDIC_INDISPONIBILIZAR))

            self.l_alm_22_b_11 = lei.LeituraModbusBit(self.clp["UG1"], REG_TDA["Alarme22_11"], descricao="[TDA] UHTA01 - Botão de Emergência Acionado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_22_b_11, CONDIC_NORMALIZAR))


        # UG2
        if self.id == 2:
            self.l_se_dj_39 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_39"], descricao="[UG2][SE] PDSA-CC - Alimentação das Cargas da UG02 - Disj. 2Q125.0")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_39, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_40 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_40"], descricao="[UG2][SE] PDSA-CC - Alimentação do Painel PCP-U2 - Disj. 2Q125.1")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_40, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_42 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_42"], descricao="[UG2][SE] PDSA-CC - Alimentação do Cubículo CSG-U2 - Disj. 2Q125.3")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_42, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_43 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_43"], descricao="[UG2][SE] PDSA-CC - Alimentação Painel do Regulador de Tensão UG02 - Disj. 2Q125.4")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_43, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_79 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_79"], descricao="[UG2][SE] PDSA-CA - Alimentação das Cargas Essenciais da UG02 - Disj. 2Q380.0")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_79, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_80 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_80"], descricao="[UG2][SE] PDSA-CA - Alimentação das Cargas Não Essenciais da UG02 - Disj. 2Q380.1")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_80, CONDIC_INDISPONIBILIZAR))

            self.l_alm_04_b_13 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme04_13"], descricao="[UG2] Cubículo CSA-U2 - Fusível Queimado ")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_13, CONDIC_INDISPONIBILIZAR))

            self.l_alm_04_b_14 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme04_14"], descricao="[UG2] Cubículo CSA-U2 - Grade Frontal Aberta  (Abertura 52L- SEL787 - TRIP)")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_14, CONDIC_INDISPONIBILIZAR))

            self.l_alm_04_b_15 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme04_15"], descricao="[UG2] Cubículo CSA-U2 - Grade Traseira Aberta  (Abertura 52L- SEL787 - TRIP)")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_04_b_15, CONDIC_INDISPONIBILIZAR))

            self.l_alm_10_b_10 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme10_10"], descricao="[UG2] PCP-U2 - Alimentação Fonte 125/24Vcc - Disj. Q125.3 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_10, CONDIC_INDISPONIBILIZAR))

            self.l_alm_10_b_11 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme10_11"], descricao="[UG2] PCP-U2 - Alimentação Circuitos de Comando - Disj. Q24.1 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_11, CONDIC_INDISPONIBILIZAR))

            self.l_alm_12_b_02 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme12_02"], descricao="[UG2] PDSA-CC - Alimentação do Cubículo CSA-U2 - Disj. Q125.6 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_02, CONDIC_INDISPONIBILIZAR))

            self.l_alm_12_b_14 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme12_14"], descricao="[UG2] PDSA-CC - Alimentação das Cargas da Disj. 2Q125.0 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_14, CONDIC_INDISPONIBILIZAR))

            self.l_alm_12_b_15 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme12_15"], descricao="[UG2] PDSA-CC - Alimentação do Painel PCP-U2 - Disj. 2Q125.1 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_12_b_15, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_00 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme13_00"], descricao="[UG2] PDSA-CC - Alimentação do Quadro Q49-U2 - Disj. 2Q125.2 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_00, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_01 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme13_01"], descricao="[UG2] PDSA-CC - Alimentação do Cubículo CSG-U2 - Disj. 2Q125.3 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_01, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_02 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme13_02"], descricao="[UG2] PDSA-CC - Alimentação Painel do Regulador de Tensão Disj. 2Q125.4 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_02, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_03 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme13_03"], descricao="[UG2] PDSA-CC - Alimentação do Filtro Duplo Disj. 2Q125.5 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_03, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_04 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme13_04"], descricao="[UG2] PDSA-CC - Alimentação Reserva - Disj. 2Q125.6 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_04, CONDIC_NORMALIZAR))

            self.l_alm_15_b_14 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme15_14"], descricao="[UG2] PDSA-CA - Alimentação das Cargas Essenciais da Disj. 2Q380.0 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_14, CONDIC_INDISPONIBILIZAR))

            self.l_alm_15_b_15 = lei.LeituraModbusBit(self.clp["UG2"], REG_UG["UG2"]["Alarme15_15"], descricao="[UG2] PDSA-CA - Alimentação das Cargas Não Essenciais da Disj. 2Q380.1 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_15_b_15, CONDIC_INDISPONIBILIZAR))

            self.l_alm_22_b_10 = lei.LeituraModbusBit(self.clp["UG2"], REG_TDA["Alarme22_10"], descricao="[TDA] UHTA01 - Sobretemperatura do Óleo - Trip")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_22_b_10, CONDIC_INDISPONIBILIZAR))

            self.l_alm_22_b_11 = lei.LeituraModbusBit(self.clp["UG2"], REG_TDA["Alarme22_11"], descricao="[TDA] UHTA01 - Botão de Emergência Acionado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_22_b_11, CONDIC_NORMALIZAR))


        # UG3
        if self.id == 3:
            self.l_se_dj_46 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_46"], descricao="[UG3][SE] PDSA-CC - Alimentação das Cargas da UG03 - Disj. 3Q125.0")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_46, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_47 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_47"], descricao="[UG3][SE] PDSA-CC - Alimentação do Painel PCP-U3 - Disj. 3Q125.1")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_47, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_49 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_49"], descricao="[UG3][SE] PDSA-CC - Alimentação do Cubículo CSG-U3 - Disj. 3Q125.3")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_49, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_50 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_50"], descricao="[UG3][SE] PDSA-CC - Alimentação Painel do Regulador de Tensão UG03 - Disj. 3Q125.4")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_50, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_81 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_81"], descricao="[UG3][SE] PDSA-CA - Alimentação das Cargas Essenciais da UG03 - Disj. 3Q380.0")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_81, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_82 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_82"], descricao="[UG3][SE] PDSA-CA - Alimentação das Cargas Não Essenciais da UG03 - Disj. 3Q380.1")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_82, CONDIC_INDISPONIBILIZAR))

            self.l_alm_10_b_12 = lei.LeituraModbusBit(self.clp["UG3"], REG_UG["UG3"]["Alarme10_12"], descricao="[UG3] PCP-U3 - Alimentação Fonte 125/24Vcc - Disj. Q125.3 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_12, CONDIC_INDISPONIBILIZAR))

            self.l_alm_10_b_13 = lei.LeituraModbusBit(self.clp["UG3"], REG_UG["UG3"]["Alarme10_13"], descricao="[UG3] PCP-U3 - Alimentação Circuitos de Comando - Disj. Q24.1 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_13, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_05 = lei.LeituraModbusBit(self.clp["UG3"], REG_UG["UG3"]["Alarme13_05"], descricao="[UG3] PDSA-CC - Alimentação das Cargas da Disj. 3Q125.0 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_05, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_06 = lei.LeituraModbusBit(self.clp["UG3"], REG_UG["UG3"]["Alarme13_06"], descricao="[UG3] PDSA-CC - Alimentação do Painel PCP-U3 - Disj. 3Q125.1 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_06, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_07 = lei.LeituraModbusBit(self.clp["UG3"], REG_UG["UG3"]["Alarme13_07"], descricao="[UG3] PDSA-CC - Alimentação do Quadro Q49-U3 - Disj. 3Q125.2 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_07, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_08 = lei.LeituraModbusBit(self.clp["UG3"], REG_UG["UG3"]["Alarme13_08"], descricao="[UG3] PDSA-CC - Alimentação do Cubículo CSG-U3 - Disj. 3Q125.3 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_08, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_09 = lei.LeituraModbusBit(self.clp["UG3"], REG_UG["UG3"]["Alarme13_09"], descricao="[UG3] PDSA-CC - Alimentação Painel do Regulador de Tensão Disj. 3Q125.4 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_09, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_10 = lei.LeituraModbusBit(self.clp["UG3"], REG_UG["UG3"]["Alarme13_10"], descricao="[UG3] PDSA-CC - Alimentação do Filtro Duplo Disj. 3Q125.5 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_10, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_11 = lei.LeituraModbusBit(self.clp["UG3"], REG_UG["UG3"]["Alarme13_11"], descricao="[UG3] PDSA-CC - Alimentação Reserva - Disj. 3Q125.6 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_11, CONDIC_NORMALIZAR))

            self.l_alm_16_b_00 = lei.LeituraModbusBit(self.clp["UG3"], REG_UG["UG3"]["Alarme16_00"], descricao="[UG3] PDSA-CA - Alimentação das Cargas Essenciais da Disj. 3Q380.0 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_00, CONDIC_INDISPONIBILIZAR))

            self.l_alm_16_b_01 = lei.LeituraModbusBit(self.clp["UG3"], REG_UG["UG3"]["Alarme16_01"], descricao="[UG3] PDSA-CA - Alimentação das Cargas Não Essenciais da Disj. 3Q380.1 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_01, CONDIC_INDISPONIBILIZAR))

            self.l_alm_24_b_09 = lei.LeituraModbusBit(self.clp["UG3"], REG_TDA["Alarme24_09"], descricao="[TDA] UHTA02 - Sobretemperatura do Óleo - Trip")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_24_b_09, CONDIC_NORMALIZAR))

            self.l_alm_24_b_10 = lei.LeituraModbusBit(self.clp["UG3"], REG_TDA["Alarme24_10"], descricao="[TDA] UHTA02 - Botão de Emergência Acionado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_24_b_10, CONDIC_NORMALIZAR))


        # UG4
        if self.id == 4:
            self.l_se_dj_53 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_53"], descricao="[UG4][SE] PDSA-CC - Alimentação das Cargas da UG04 - Disj. 4Q125.0")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_53, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_54 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_54"], descricao="[UG4][SE] PDSA-CC - Alimentação do Painel PCP-U4 - Disj. 4Q125.1")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_54, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_56 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_56"], descricao="[UG4][SE] PDSA-CC - Alimentação do Cubículo CSG-U4 - Disj. 4Q125.3")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_56, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_57 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_57"], descricao="[UG4][SE] PDSA-CC - Alimentação Painel do Regulador de Tensão UG04 - Disj. 4Q125.4")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_57, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_83 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_83"], descricao="[UG4][SE] PDSA-CA - Alimentação das Cargas Essenciais da UG04 - Disj. 4Q380.0")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_83, CONDIC_INDISPONIBILIZAR))

            self.l_se_dj_84 = lei.LeituraModbus(self.clp["SA"], REG_SE["DJ_84"], descricao="[UG4][SE] PDSA-CA - Alimentação das Cargas Não Essenciais da UG04 - Disj. 4Q380.1")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_se_dj_84, CONDIC_INDISPONIBILIZAR))

            self.l_alm_10_b_14 = lei.LeituraModbusBit(self.clp["UG4"], REG_UG["UG4"]["Alarme10_14"], descricao="[UG4] PCP-U4 - Alimentação Fonte 125/24Vcc - Disj. Q125.3 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_14, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_12 = lei.LeituraModbusBit(self.clp["UG4"], REG_UG["UG4"]["Alarme13_12"], descricao="[UG4] PDSA-CC - Alimentação das Cargas da Disj. 4Q125.0 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_12, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_13 = lei.LeituraModbusBit(self.clp["UG4"], REG_UG["UG4"]["Alarme13_13"], descricao="[UG4] PDSA-CC - Alimentação do Painel PCP-U4 - Disj. 4Q125.1 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_13, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_14 = lei.LeituraModbusBit(self.clp["UG4"], REG_UG["UG4"]["Alarme13_14"], descricao="[UG4] PDSA-CC - Alimentação do Quadro Q49-U4 - Disj. 4Q125.2 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_14, CONDIC_INDISPONIBILIZAR))

            self.l_alm_13_b_15 = lei.LeituraModbusBit(self.clp["UG4"], REG_UG["UG4"]["Alarme13_15"], descricao="[UG4] PDSA-CC - Alimentação do Cubículo CSG-U4 - Disj. 4Q125.3 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_13_b_15, CONDIC_INDISPONIBILIZAR))

            self.l_alm_14_b_00 = lei.LeituraModbusBit(self.clp["UG4"], REG_UG["UG4"]["Alarme14_00"], descricao="[UG4] PDSA-CC - Alimentação Painel do Regulador de Tensão Disj. 4Q125.4 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_00, CONDIC_INDISPONIBILIZAR))

            self.l_alm_14_b_01 = lei.LeituraModbusBit(self.clp["UG4"], REG_UG["UG4"]["Alarme14_01"], descricao="[UG4] PDSA-CC - Alimentação do Filtro Duplo Disj. 4Q125.5 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_01, CONDIC_INDISPONIBILIZAR))

            self.l_alm_14_b_02 = lei.LeituraModbusBit(self.clp["UG4"], REG_UG["UG4"]["Alarme14_02"], descricao="[UG4] PDSA-CC - Alimentação Reserva - Disj. 4Q125.6 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_14_b_02, CONDIC_NORMALIZAR))

            self.l_alm_16_b_02 = lei.LeituraModbusBit(self.clp["UG4"], REG_UG["UG4"]["Alarme16_02"], descricao="[UG4] PDSA-CA - Alimentação das Cargas Essenciais da Disj. 4Q380.0 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_02, CONDIC_INDISPONIBILIZAR))

            self.l_alm_16_b_03 = lei.LeituraModbusBit(self.clp["UG4"], REG_UG["UG4"]["Alarme16_03"], descricao="[UG4] PDSA-CA - Alimentação das Cargas Não Essenciais da Disj. 4Q380.1 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_16_b_03, CONDIC_INDISPONIBILIZAR))

            self.l_alm_10_b_15 = lei.LeituraModbusBit(self.clp["UG4"], REG_UG["UG4"]["Alarme10_15"], descricao="[UG4] PCP-U4 - Alimentação Circuitos de Comando - Disj. Q24.1 Desligado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_10_b_15, CONDIC_INDISPONIBILIZAR))

            self.l_alm_24_b_09 = lei.LeituraModbusBit(self.clp["UG4"], REG_TDA["Alarme24_09"], descricao="[TDA] UHTA02 - Sobretemperatura do Óleo - Trip")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_24_b_09, CONDIC_NORMALIZAR))

            self.l_alm_24_b_10 = lei.LeituraModbusBit(self.clp["UG4"], REG_TDA["Alarme24_10"], descricao="[TDA] UHTA02 - Botão de Emergência Acionado")
            dct_ug[f'UG{self.id}']['condicionadores'].append(c.CondicionadorBase(self.l_alm_24_b_10, CONDIC_NORMALIZAR))