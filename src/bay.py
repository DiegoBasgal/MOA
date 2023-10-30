__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__description__ = "Este módulo corresponde a implementação da operação do BAY de comunicação."

import logging
import traceback
import threading

from time import time, sleep

from src.funcoes.leitura import *
from src.dicionarios.const import *
from src.funcoes.condicionadores import *

from src.conectores.servidores import Servidores
from src.funcoes.escrita import EscritaModBusBit as EMB


logger = logging.getLogger("logger")


class Bay:
    def __init__(self, serv: "Servidores"=None) -> "None":

        # ATRIBUIÇÃO DE VARIÁVEIS

        self.mp = serv.mp
        self.mr = serv.mr
        self.clp = serv.clp
        self.rele = serv.rele

        self.status_tensao: "int" = TENSAO_VERIFICAR

        self.tensao_vs = LeituraModbus(
            self.rele["BAY"],
            REG_RELE["BAY"]["LT_VS"],
            descricao="[BAY][RELE] Leitura Tensão VS"
        )
        self.tensao_vab = LeituraModbus(
            self.rele["BAY"],
            REG_RELE["BAY"]["LT_FASE_A"],
            descricao="[BAY][RELE] Leitura Tensão Fase A"
        )
        self.tensao_vbc = LeituraModbus(
            self.rele["BAY"],
            REG_RELE["BAY"]["LT_FASE_B"],
            descricao="[BAY][RELE] Leitura Tensão Fase B"
        )
        self.tensao_vca = LeituraModbus(
            self.rele["BAY"],
            REG_RELE["BAY"]["LT_FASE_C"],
            descricao="[BAY][RELE] Leitura Tensão Fase C"
        )
        self.dj_linha_bay = LeituraModbusBit(
            self.rele["BAY"],
            REG_RELE["BAY"]["DJL_FECHADO"],
            descricao="[BAY][RELE] Disjuntor Bay Status"
        )
        self.dj_linha_se = LeituraModbusBit(
            self.rele["SE"],
            REG_RELE["SE"]["DJL_FECHADO"],
            descricao="[SE][RELE] Disjuntor Linha Status"
        )
        self.potencia_mp = LeituraModbusFloat(
            self.clp["SA"], # Mudar para -> self.mp
            REG_CLP["SE"]["P"], # Mudar para -> REG_MEDIDOR["LT_P_MP"]
            op=3,
            descricao="[BAY][MP] Leitura Medidor Principal"
        )
        self.potencia_mr = LeituraModbus(
            self.mr,
            REG_MEDIDOR["LT_P_MR"],
            escala=0.001,
            op=3,
            descricao="[BAY][MP] Leitura Medidor Retaguarda"
        )

        self.condicionadores: "list[CondicionadorBase]" = []
        self.condicionadores_ativos: "list[CondicionadorBase]" = []
        self.condicionadores_essenciais: "list[CondicionadorBase]" = []


    def resetar_emergencia(self) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = self.rele["BAY"].write_single_coil(REG_RELE["BAY"]["RELE_RST_TRP"], [1])
            return res

        except Exception:
            logger.exception(f"[BAY] Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False


    def fechar_dj_linha(self) -> "int":
        """
        Função para acionar comando de fechamento do Disjuntor do BAY de comunicação.

        Verifica se o disjuntor do BAY está aberto. Caso esteja, chama o método de verificação
        de condições de fechamento. Caso não haja nenhum problema com a verificação, aciona o
        comando de fechamento, senão, avisa o operador da falha.
        Caso o Disjuntor já estja fechado, apenas registra nos LOGs e retorna.
        """

        try:
            if not self.dj_linha_bay.valor:
                logger.info("[BAY] O Disjuntor do Bay está Aberto!")

                if self.verificar_dj_linha():
                    logger.debug(f"[BAY] Enviando comando:                   \"FECHAR DISJUNTOR\"")
                    logger.debug("")
                    self.rele["BAY"].write_single_coil(REG_RELE["BAY"]["DJL_CMD_FECHAR"], [1])
                    return True

                else:
                    logger.warning("[BAY] Não foi possível fechar do Disjuntor do BAY.")
                    logger.debug("")
                    return False

            else:
                return True

        except Exception:
            logger.exception(f"[BAY] Houve um erro ao realizar a leitura do status do Disjuntor do Bay.")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False


    def verificar_dj_linha(self) -> "bool":
        """
        Função para verificação de condições de fechamento do Disjuntor do BAY.

        Verifica se o Disjuntor da Subestação está fechado e caso esteja, aciona o comando de abertura.
        Logo em seguida, verifica as seguintes condições:
        - Se há ausência de tensão trifásica;
        - Se há presença de tensão VS;
        - Se a mola do Disjuntor está carregada;
        - Se a Seccionadora está fechada;
        - Se há qualquer leitura de corrente na barra (Barra Morta = False & Barra Viva = True);
        - Se há qualquer leitura de corrente na linha (Linha Morta = False & Linha Viva = True).
        Caso qualquer das condições acima retornar diferente do esperado, avisa o operador e impede o
        comando de fechamento do Disjuntor.
        """

        flags = 0
        logger.info("[BAY] Verificando Condições do Disjuntor BAY...")

        try:
            if self.secc_fechada.valor:
                logger.warning("[BAY] A Seccionadora está Aberta!")
                flags += 1

            if self.dj_linha_se.valor:
                logger.info("[BAY] Disjuntor da Subestação Fechado!")
                logger.debug(f"[BAY] Enviando comando:                   \"ABRIR DISJUNTOR SE\"")
                res = EMB.escrever_bit(self.clp["SA"], REG_CLP["SE"]["DJL_CMD_ABRIR"], valor=1)

                if not res:
                    logger.warning("[BAY] Não foi possível realizar a abertura do Disjuntor de Linha da Subestação!")
                    flags += 1

            if not self.barra_morta.valor and self.barra_viva.valor:
                logger.warning(f"[BAY] Foi identificada uma Leitura de Tensão na Barra! Tensão VS -> {self.tensao_vs.valor}")
                flags += 1

            if not self.linha_morta.valor and self.linha_viva.valor:
                logger.warning("[BAY] Foi identificada uma leitura de Tensão na linha!")
                flags += 1

            if not self.mola_carregada.valor:
                logger.warning("[BAY] A mola do Disjuntor está descarregada!")
                flags += 1

            logger.warning(f"[BAY] Foram identificadas \"{flags}\" condições de bloqueio ao realizar fechamento do Disjuntor do BAY. Favor normalizar.") \
                if flags > 0 else logger.debug("[BAY] Condições de Fechamento Validadas.")

            return False if flags > 0 else True

        except Exception:
            logger.exception(f"[BAY] Houve um erro ao verificar as pré-condições de fechameto do Disjuntor do Bay.")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False


    def verificar_tensao_trifasica(self) -> "bool":
        """
        Função para verificação de Tensão trifásica na linha do BAY.
        """

        try:
            if (TENSAO_FASE_BAY_BAIXA < self.tensao_vab.valor < TENSAO_FASE_BAY_ALTA) \
                and (TENSAO_FASE_BAY_BAIXA < self.tensao_vbc.valor < TENSAO_FASE_BAY_ALTA) \
                and (TENSAO_FASE_BAY_BAIXA < self.tensao_vca.valor < TENSAO_FASE_BAY_ALTA):
                return True
            else:
                return False

        except Exception:
            logger.exception(f"[BAY] Houve um erro ao realizar a verificação da tensão trifásica.")
            logger.debug(f"[BAY] Traceback: {traceback.format_exc()}")
            return False


    def aguardar_tensao(self) -> "bool":
        """
        Função para normalização após a queda de tensão da linha de transmissão.

        Primeiramente, caso haja uma queda, será chamada a função com o temporizador de
        espera com tempo pré-definido. Caso a tensão seja reestabelecida dentro do limite
        de tempo, é chamada a funcão de normalização da Usina. Se o temporizador passar do
        tempo, é chamada a função de acionamento de emergência e acionado tropedo de emergência
        por Voip.
        """

        if self.status_tensao == TENSAO_VERIFICAR:
            self.status_tensao = TENSAO_AGUARDO
            logger.debug("[BAY] Iniciando o temporizador de normalização da tensão na linha.")
            threading.Thread(target=lambda: self.temporizar_tensao(30)).start()

        elif self.status_tensao == TENSAO_REESTABELECIDA:
            logger.info("[BAY] Tensão na linha reestabelecida.")
            self.status_tensao = TENSAO_VERIFICAR
            return True

        elif self.status_tensao == TENSAO_FORA:
            logger.critical("[BAY] Não foi possível reestabelecer a tensão na linha. Acionando emergência")
            self.status_tensao = TENSAO_VERIFICAR
            return False

        else:
            logger.debug("[BAY] A tensão na linha ainda está fora.")


    def temporizar_tensao(self, seg: "int") -> "None":
        """
        Função de temporizador para espera de normalização de tensão da linha de transmissão.
        """

        delay = time() + seg

        while time() <= delay:
            if self.verificar_tensao_trifasica():
                self.status_tensao = TENSAO_REESTABELECIDA
                return
            sleep(time() - (time() - 15))
        self.status_tensao = TENSAO_FORA


    def verificar_condicionadores(self) -> "list[CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.warning(f"[BAY] Foram detectados Condicionadores ativos no Bay!")

            else:
                logger.info(f"[BAY] Ainda há Condicionadores ativos no Bay!")

            for condic in condics_ativos:
                if condic in self.condicionadores_ativos:
                    logger.debug(f"[BAY] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                else:
                    logger.warning(f"[BAY] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)

            logger.debug("")
            return condics_ativos

        else:
            self.condicionadores_ativos = []
            return []


    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de leituras necesárias para a operação.
        """

        # CONDIÇÕES DE FECHAMENTO Dj52l
        self.linha_viva = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["ID_LINHA_VIVA"], descricao="[BAY][RELE] Identificação Linha Viva")
        self.barra_viva = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["ID_BARRA_VIVA"], descricao="[BAY][RELE] Identificação Barra Viva")
        self.linha_morta = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["ID_LINHA_MORTA"], descricao="[BAY][RELE] Identificação Linha Morta")
        self.barra_morta = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["ID_BARRA_MORTA"], descricao="[BAY][RELE] Identificação Barra Morta")
        self.mola_carregada = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["DJL_MOLA_CARREGADA"], descricao="[BAY][RELE] Disjuntor Mola Carregada")
        self.secc_fechada = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["SECC_FECHADA"], invertido=True, descricao="[BAY][RELE] Seccionadora Fechada")
        self.condicionadores_essenciais.append(CondicionadorBase(self.secc_fechada, CONDIC_INDISPONIBILIZAR))

        self.l_falha_abertura_dj = LeituraModbusBit(self.rele["BAY"], REG_RELE["BAY"]["DJL_FLH_ABERTURA"], descricao="[BAY][RELE] Disjuntor Linha Falha Abertura")
        self.condicionadores_essenciais.append(CondicionadorBase(self.l_falha_abertura_dj, CONDIC_INDISPONIBILIZAR))