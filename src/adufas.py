__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__description__ = "Este módulo corresponde a implementação da operação das Adufas."

import pytz
import logging
import traceback

import src.tomada_agua as tda
import src.funcoes.leitura as lei
import src.funcoes.condicionadores as c
import src.conectores.banco_dados as bd
import src.conectores.servidores as serv

from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class Adufas:

    clp = serv.Servidores.clp
    bd: "bd.BancoDados" = None
    cfg = {}

    class Comporta:
        def __init__(self, id: "int", cfg: "dict") -> "None":

            self.clp = serv.Servidores.clp

            self.__id = id
            self.__cfg = cfg

            self.__manual = lei.LeituraModbusBit(
                self.clp["AD"],
                REG_AD[f"CP_0{self.id}_ACION_LOCAL"],
                descricao=f"[AD][CP{self.id}] Comporta Manual"
            )

            self._estado: "int" = 1

            self.setpoint: "int" = 0
            self.setpoint_maximo: "int" = 0
            self.setpoint_anterior: "int" = 0

            self.k: "float" = 1000

            self.controle_i: "float" = 0.0
            self.controle_p: "float" = 0.0


            # FINALIZAÇÃO __INIT__
            self.carregar_leituras()


        @property
        def id(self) -> "int":
        # PROPRIEDADE -> Retorna o id da Comporta

            return self.__id

        @property
        def manual(self) -> "bool":
        # PROPRIEDADE -> Retorna se o modo manual da Comporta foi ativado

            return self.__manual.valor

        @property
        def etapa(self) -> "int":
        # PROPRIEDADE -> Retorna a etapa da Comporta

            if self.parada.valor:
                return ADCP_PARADA
            elif self.abrindo.valor:
                return ADCP_ABRINDO
            elif self.fechando.valor:
                return ADCP_FECHANDO

        @property
        def etapa_parada(self) -> "int":
        # PROPRIEDADE -> Retorna a etapa da Comporta enquanto está parada

            if self.aberta.valor:
                return ADCP_P_ABERTA
            elif self.fechada.valor:
                return ADCP_P_FECHADA

        @property
        def estado(self) -> "int":
        # PROPRIEDADE -> Retorna o estado atual da Comporta

            return self._estado

        @estado.setter
        def estado(self, var: "int") -> "None":
        # SETTER -> Adiciona o novo calor de estado da Comporta

            self._estado = var


        def calcular_setpoint(self) -> "None":
            """
            Função para calcular o valor de setpoint por Comporta, a partir da
            leitura de nível Montante da Tomada da Água
            """

            logger.debug(f"[AD][CP{self.id}]      Comporta:          \"{ADCP_STR_DCT_ESTADO[self._estado] if not self.manual else 'Manual'}\"")
            logger.debug(f"[AD][CP{self.id}]      Etapa:             \"{(ADCP_STR_DCT_ETAPA[self.etapa] + '->' + ADCP_STR_DCT_ETAPA_P[self.etapa_parada]) if self.parada.valor else ADCP_STR_DCT_ETAPA[self.etapa]}\"")

            erro = tda.TomadaAgua.nivel_montante.valor - self.__cfg["ad_nv_alvo"]

            self.controle_p = self.__cfg["ad_kp"] * erro
            self.controle_i = min(max(0, self.__cfg["ad_ki"] * erro + self.controle_i), 6000)

            sp = self.k * (self.controle_p + self.controle_i)
            sp = min(max(0, sp), 6000)

            logger.debug(f"[AD][CP{self.id}]      P:                 {self.controle_p}")
            logger.debug(f"[AD][CP{self.id}]      I:                 {self.controle_i}")
            logger.debug(f"[AD][CP{self.id}]      ERRO:              {erro}")
            logger.debug("")

            if self.manual and self.estado == ADCP_INDISPONIVEL:
                return

            self.enviar_setpoint(sp)


        def enviar_setpoint(self, setpoint: "int") -> "None":
            """
            Função para enviar o setpoint para cada Comporta
            """

            try:
                logger.debug(f"[AD][CP{self.id}]      Enviando setpoint:         {round(setpoint)} mm")

                self.clp["AD"].write_single_register(REG_AD[f"CP_0{self.id}_SP_POS"], round(self.setpoint))
                self.clp["AD"].write_single_register(REG_AD[f"CMD_CP_0{self.id}_BUSCAR"], 1)

            except Exception:
                logger.error(f"[AD][CP{self.id}] Não foi possível enviar o setpoint para a Comporta.")
                logger.debug(traceback.format_exc())


        def carregar_leituras(self) -> "None":
            """
            Função para carregar as leituras de cada Comporta
            """

            self.parada = lei.LeituraModbusBit(self.clp["AD"], REG_AD[f"CP_0{self.id}_PARADA"], descricao=f"[AD][CP{self.id}] Comporta Parada")
            self.aberta = lei.LeituraModbusBit(self.clp["AD"], REG_AD[f"CP_0{self.id}_ABERTA"], descricao=f"[AD][CP{self.id}] Comporta Aberta")
            self.fechada = lei.LeituraModbusBit(self.clp["AD"], REG_AD[f"CP_0{self.id}_FECHADA"], descricao=f"[AD][CP{self.id}] Comporta Fechada")
            self.abrindo = lei.LeituraModbusBit(self.clp["AD"], REG_AD[f"CP_0{self.id}_ABRINDO"], descricao=f"[AD][CP{self.id}] Comporta Abrindo")
            self.fechando = lei.LeituraModbusBit(self.clp["AD"], REG_AD[f"CP_0{self.id}_FECHANDO"], descricao=f"[AD][CP{self.id}] Comporta Fechando")


    cp1 = Comporta(1, cfg)
    cp2 = Comporta(2, cfg)
    cps: "list[Comporta]" = [cp1, cp2]

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []


    @classmethod
    def controlar_comportas(cls) -> "None":
        logger.debug(f"[AD]  Controlando Comportas...")
        logger.debug(f"[AD]  NÍVEL -> Alvo:                      {cls.cfg['nv_alvo']:0.3f}")
        logger.debug(f"[TDA]          Leitura:                   {tda.TomadaAgua.nivel_montante.valor:0.3f}")
        logger.debug("")

        for cp in cls.cps:
            cp.calcular_setpoint()
            logger.debug("")


    @classmethod
    def verificar_condicionadores(cls) -> "list[c.CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        autor = 0

        if True in (condic.ativo for condic in cls.condicionadores_essenciais):
            condics_ativos = [condic for condics in [cls.condicionadores_essenciais, cls.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if cls.condicionadores_ativos == []:
                logger.warning(f"[AD]  Foram detectados Condicionadores ativos no Serviço Auxiliar!")

            else:
                logger.info(f"[AD]  Ainda há Condicionadores ativos no Serviço Auxiliar!")

            for condic in condics_ativos:
                if condic in cls.condicionadores_ativos:
                    logger.debug(f"[AD]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                else:
                    logger.warning(f"[AD]  Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    cls.condicionadores_ativos.append(condic)
                    cls.bd.update_alarmes([
                        datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor == 0 else ""
                    ])

            logger.debug("")
            return condics_ativos

        else:
            cls.condicionadores_ativos = []
            return []


    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """

        ## CONDICINOADORES:
        cls.l_alm_28_b_00 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme28_00"], descricao="[AD]  Botão de Emergência Pressionado")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_alm_28_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_28_b_12 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme28_12"], descricao="[AD]  UHCD - Botão de Emergência Pressionado")
        cls.condicionadores_essenciais.append(c.CondicionadorBase(cls.l_alm_28_b_12, CONDIC_NORMALIZAR))

        cls.l_alm_28_b_01 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme28_01"], descricao="[AD]  Relé Falta de Fase CA Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_28_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_28_b_04 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme28_04"], descricao="[AD]  UHCD - Pressão de Óleo Baixa")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_28_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_28_b_05 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme28_05"], descricao="[AD]  UHCD - Pressão de Óleo Alta na Linha da Comporta 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_28_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_28_b_06 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme28_06"], descricao="[AD]  UHCD - Pressão de Óleo Alta na Linha da Comporta 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_28_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_28_b_07 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme28_07"], descricao="[AD]  UHCD - Filtro de Retorno Sujo")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_28_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_28_b_08 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme28_08"], descricao="[AD]  UHCD - Nível de Óleo Crítico")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_28_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_28_b_09 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme28_09"], descricao="[AD]  UHCD - Nível de Óleo Alto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_28_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_28_b_10 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme28_10"], descricao="[AD]  UHCD - Sobretemperatura do Óleo - Alarme")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_28_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_28_b_11 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme28_11"], descricao="[AD]  UHCD - Sobretemperatura do Óleo - Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_28_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_29_b_00 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme29_00"], descricao="[AD]  UHCD - Bomba de Óleo 01 - Falha no Acionamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_29_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_29_b_01 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme29_01"], descricao="[AD]  UHCD - Bomba de Óleo 01 - Disjuntor QM1 Aberto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_29_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_29_b_02 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme29_02"], descricao="[AD]  UHCD - Bomba de Óleo 02 - Falha no Acionamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_29_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_29_b_03 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme29_03"], descricao="[AD]  UHCD - Bomba de Óleo 02 - Disjuntor QM2 Aberto")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_29_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_29_b_05 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme29_05"], descricao="[AD]  Comporta 01 - Falha na Abertura")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_29_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_29_b_06 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme29_06"], descricao="[AD]  Comporta 01 - Falha no Fechamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_29_b_06, CONDIC_NORMALIZAR))

        cls.l_alm_29_b_07 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme29_07"], descricao="[AD]  Comporta 01 - Falha Tempo Abertura Step Excedido")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_29_b_07, CONDIC_NORMALIZAR))

        cls.l_alm_29_b_09 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme29_09"], descricao="[AD]  Comporta 02 - Falha na Abertura")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_29_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_29_b_10 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme29_10"], descricao="[AD]  Comporta 02 - Falha no Fechamento")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_29_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_29_b_11 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme29_11"], descricao="[AD]  Comporta 02 - Falha Tempo Abertura Step Excedido")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_29_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_29_b_13 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme29_13"], descricao="[AD]  Falha no Carregador de Baterias")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_29_b_13, CONDIC_NORMALIZAR))

        cls.l_alm_30_b_00 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme30_00"], descricao="[AD]  Sensor de Fumaça Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_30_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_30_b_01 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme30_01"], descricao="[AD]  Sensor de Fumaça Desconectado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_30_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_30_b_04 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme30_04"], descricao="[AD]  Sensor de Presença Atuado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_30_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_30_b_05 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme30_05"], descricao="[AD]  Sensor de Presença Inibido")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_30_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_30_b_08 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme30_08"], descricao="[AD]  Erro de Leitura na entrada analógica da temperatura do Óleo da UHCD")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_30_b_08, CONDIC_NORMALIZAR))

        cls.l_alm_30_b_09 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme30_09"], descricao="[AD]  Erro de Leitura na entrada analógica do nível de óleo da UHCD")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_30_b_09, CONDIC_NORMALIZAR))

        cls.l_alm_30_b_10 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme30_10"], descricao="[AD]  Erro de Leitura na entrada analógica da posição da comporta 01")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_30_b_10, CONDIC_NORMALIZAR))

        cls.l_alm_30_b_11 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme30_11"], descricao="[AD]  Erro de Leitura na entrada analógica da posição da comporta 02")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_30_b_11, CONDIC_NORMALIZAR))

        cls.l_alm_31_b_00 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme31_00"], descricao="[AD]  Alimentação 380Vca Principal - Disj. Q380.0 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_31_b_00, CONDIC_NORMALIZAR))

        cls.l_alm_31_b_01 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme31_01"], descricao="[AD]  Alimentação 380Vca Principal - Disj. Q380.0 Inconsistência")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_31_b_01, CONDIC_NORMALIZAR))

        cls.l_alm_31_b_02 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme31_02"], descricao="[AD]  Alimentação 380Vca Principal - Disj. Q380.0 Trip")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_31_b_02, CONDIC_NORMALIZAR))

        cls.l_alm_31_b_03 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme31_03"], descricao="[AD]  Alimentação Carregador de Baterias - Disj. Q220.0 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_31_b_03, CONDIC_NORMALIZAR))

        cls.l_alm_31_b_04 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme31_04"], descricao="[AD]  Alimentação Banco de Baterias - Disj. Q24.0 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_31_b_04, CONDIC_NORMALIZAR))

        cls.l_alm_31_b_05 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme31_05"], descricao="[AD]  Alimentação Circuitos de Comando - Disj. Q24.3 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_31_b_05, CONDIC_NORMALIZAR))

        cls.l_alm_31_b_06 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme31_06"], descricao="[AD]  Alimentação Inversor 24/220Vca - Disj. Q24.4 Desligado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_31_b_06, CONDIC_NORMALIZAR))