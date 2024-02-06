__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__description__ = "Este módulo corresponde a implementação da operação das Adufas."

import pytz
import logging
import traceback

import src.tomada_agua as tda
import src.dicionarios.dict as d
import src.funcoes.leitura as lei
import src.funcoes.condicionadores as c
import src.conectores.banco_dados as bd
import src.conectores.servidores as serv

from time import sleep
from datetime import datetime

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class Adufas:

    clp = serv.Servidores.clp
    bd: "bd.BancoDados" = None
    cfg = {}


    class Comporta:
        def __init__(self, id: "int") -> "None":

            self.clp = serv.Servidores.clp

            self.__id = id
            self.cfg = {}

            self.__manual = lei.LeituraModbusBit(
                self.clp["AD"],
                REG_AD[f"CP_0{self.id}_ACION_LOCAL"],
                descricao=f"[AD][CP{self.id}] Comporta Manual"
            )
            self.__posicao = lei.LeituraModbus(
                self.clp["AD"],
                REG_AD[f"CP_0{self.id}_POSICAO"],
                descricao=f"[AD][CP{self.id}] Posição Atual"
            )

            self._estado: "int" = 0

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
        def posicao(self) -> "int":
        # PROPRIEDADE -> Retorna a posição da Comporta
        
            return self.__posicao.valor

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
        def estado(self) -> "int":
        # PROPRIEDADE -> Retorna o estado atual da Comporta

            return self._estado

        @estado.setter
        def estado(self, var: "int") -> "None":
        # SETTER -> Adiciona o novo valor de estado da Comporta

            self._estado = var


        def calcular_setpoint(self) -> "None":
            """
            Função para calcular o valor de setpoint por Comporta, a partir da
            leitura de nível Montante da Tomada da Água
            """

            logger.debug(f"[AD][CP{self.id}]      Comporta:                  \"{ADCP_STR_DCT_ESTADO[self.estado]}\"")
            logger.debug(f"[AD][CP{self.id}]      Etapa:                     \"{ADCP_STR_DCT_ETAPA[self.etapa]}\"")
            logger.debug(f"[AD][CP{self.id}]      Leituras:")
            logger.debug(f"[AD][CP{self.id}]      - \"Posição\":               {self.posicao}")
            logger.debug("")

            if self.manual or self._estado == ADCP_MANUAL:
                self.estado == ADCP_MANUAL
                return

            elif self.estado == ADCP_INDISPONIVEL:
                return

            else:
                self.estado = ADCP_DISPONIVEL

                if not self.verificar_permissivos():
                    return

                erro = tda.TomadaAgua.nivel_montante.valor - self.cfg["ad_nv_alvo"]

                self.controle_p = self.cfg["ad_kp"] * erro
                self.controle_i = min(max(0, self.cfg["ad_ki"] * erro + self.controle_i), 6000)

                sp = min(max(0, self.k * (self.controle_p + self.controle_i)), 6000)

                logger.debug(f"[AD][CP{self.id}]      P:                         {self.controle_p:1.4f}")
                logger.debug(f"[AD][CP{self.id}]      I:                         {self.controle_i:1.4f}")
                logger.debug(f"[AD][CP{self.id}]      ERRO:                      {erro}")

                self.setpoint = sp

                self.enviar_setpoint(self.setpoint)


        def enviar_setpoint(self, setpoint: "int") -> "None":
            """
            Função para enviar o setpoint para cada Comporta
            """

            try:
                # if not self.clp["AD"].read_holding_registers(REG_AD["PCAD_MODO_SETPOT_HAB"])[0]:
                #     logger.info(f"[AD]  O modo de setpoint das Comportas das Adufas não está Habilitado.")
                #     return

                if self.uhcd_operando.valor:
                    logger.debug(f"[AD][CP{self.id}]      Aguardando disponibilização da UHCD.")
                    return

                else:
                    logger.debug("")
                    logger.debug(f"[AD][CP{self.id}]      Enviando setpoint:         {round(setpoint)} mm")
                    self.clp["AD"].write_single_register(REG_AD[f"CP_0{self.id}_SP_POS"], int(setpoint))
                    sleep(1)
                    self.clp["AD"].write_single_register(REG_AD[f"CMD_CP_0{self.id}_BUSCAR"], 1)

            except Exception:
                logger.error(f"[AD][CP{self.id}] Não foi possível enviar o setpoint para a Comporta.")
                logger.debug(traceback.format_exc())


        def verificar_permissivos(self) -> "bool":
            """
            Função para a verificação de Permissivos de controle das Comportas das Adufas.

            Verifica se alguma das condições abaixo está acionada. Se estiver, aciona o modo manual
            da Comporta e inicia o disparo do Mensageiro para os Operadores.

            CONDIÇÕES:
            - Relé Atuado por Falta de Fase CA;
            - Nível de Óleo Crítico da UHCD;
            - Trip de Temperatura do óleo da UHCD;
            - Sensor de Fumaça Atuado;
            - Erro de Leitura de Entrada Analógica da Posição da Comporta 1;
            - Erro de Leitura de Entrada Analógica da Posição da Comporta 2;
            - Desligamento do Disjuntor de Alimentação 380Vca Principal;
            - Inconsistência do Disjuntor de Alimentação 380Vca Principal;
            - Trip do Disjuntor de Alimentação 380Vca Principal;
            - Desligamento do Disjuntor de Alimentação dos Circuitos de Comando;
            """

            flags = 0
            logger.debug(f"[AD][CP{self.id}]      Verificando Permissivos...")

            try:
                if self.rele_falta_fase.valor:
                    logger.warning(f"[AD][CP{self.id}]      Relé Atuado por Falta de Fase CA.")
                    flags += 1

                if self.oleo_uhcd_nv_crit.valor:
                    logger.warning(f"[AD][CP{self.id}]      Nível de Óleo Crítico da UHCD.")
                    flags += 1

                if self.oleo_uhcd_sobretemp.valor:
                    logger.warning(f"[AD][CP{self.id}]      Trip de Temperatura do óleo da UHCD.")
                    flags += 1

                if self.sens_fuma_atuado.valor:
                    logger.warning(f"[AD][CP{self.id}]      Sensor de Fumaça Atuado.")
                    flags += 1

                if self.erro_analog_pos_cp1.valor:
                    logger.warning(f"[AD][CP{self.id}]      Erro de Leitura de Entrada Analógica da Posição da Comporta 1.")
                    flags += 1

                if self.erro_analog_pos_cp2.valor:
                    logger.warning(f"[AD][CP{self.id}]      Erro de Leitura de Entrada Analógica da Posição da Comporta 2.")
                    flags += 1

                if self.disj_al_380vca_desl.valor:
                    logger.warning(f"[AD][CP{self.id}]      Desligamento do Disjuntor de Alimentação 380Vca Principal.")
                    flags += 1

                if self.disj_al_380vca_incosis.valor:
                    logger.warning(f"[AD][CP{self.id}]      Inconsistência do Disjuntor de Alimentação 380Vca Principal.")
                    flags += 1

                if self.disj_al_380vca_trip.valor:
                    logger.warning(f"[AD][CP{self.id}]      Trip do Disjuntor de Alimentação 380Vca Principal.")
                    flags += 1

                if self.disj_al_cirq_cmd_desl.valor:
                    logger.warning(f"[AD][CP{self.id}]      Desligamento do Disjuntor de Alimentação dos Circuitos de Comando.")
                    flags += 1


                if flags > 0:
                    logger.warning(f"[AD][CP{self.id}]      Sem Permissão para Operar a Comporta {self.id}. Passando para o Modo Manual.")
                    self._cmd_manual = True
                    return False
                else:
                    return True

            except Exception:
                logger.exception(f"[AD][CP{self.id}]      Houve um erro ao verificar os Permissivos da Comporta {self.id}.")
                logger.debug(traceback.format_exc())
                return False


        def verificar_leituras(self) -> "None":
            """
            Função para verificação de leituras por acionamento temporizado.

            Verifica leituras específcas para acionamento da manuteção. As leituras são disparadas
            em períodos separados por um tempo pré-definido.
            """

            if self.cp_acion_local.valor and not d.voip[f"AD_CP{self.id}_ACION_LOCAL"]:
                logger.warning(f"[AD][CP{self.id}] Foi identificado que a Comporta {self.id} das Adufas passou para o modo de Acionamento Local. Favor verificar.")
                d.voip[f"AD_CP{self.id}_ACION_LOCAL"] = True
            if not self.cp_acion_local.valor and d.voip[f"AD_CP{self.id}_ACION_LOCAL"]:
                d.voip[f"AD_CP{self.id}_ACION_LOCAL"] = False


        def carregar_leituras(self) -> "None":
            """
            Função para carregar as leituras de cada Comporta
            """

            ## STATUS
            self.parada = lei.LeituraModbusBit(self.clp["AD"], REG_AD[f"CP_0{self.id}_PARADA"], descricao=f"[AD][CP{self.id}] Comporta Parada")
            self.aberta = lei.LeituraModbusBit(self.clp["AD"], REG_AD[f"CP_0{self.id}_ABERTA"], descricao=f"[AD][CP{self.id}] Comporta Aberta")
            self.fechada = lei.LeituraModbusBit(self.clp["AD"], REG_AD[f"CP_0{self.id}_FECHADA"], descricao=f"[AD][CP{self.id}] Comporta Fechada")
            self.abrindo = lei.LeituraModbusBit(self.clp["AD"], REG_AD[f"CP_0{self.id}_ABRINDO"], descricao=f"[AD][CP{self.id}] Comporta Abrindo")
            self.fechando = lei.LeituraModbusBit(self.clp["AD"], REG_AD[f"CP_0{self.id}_FECHANDO"], descricao=f"[AD][CP{self.id}] Comporta Fechando")
            self.uhcd_operando = lei.LeituraModbusBit(self.clp["AD"], REG_AD["UHCD_OPERACIONAL"], descricao=f"[AD][CP{self.id}] UHCD Disponível")


            ## PERMISSIVOS
            self.rele_falta_fase = lei.LeituraModbusBit(self.clp["AD"], REG_AD["Alarme28_01"], descricao="[AD]  Relé Falta de Fase CA Atuado")
            self.oleo_uhcd_nv_crit = lei.LeituraModbusBit(self.clp["AD"], REG_AD["Alarme28_08"], descricao="[AD]  UHCD - Nível de Óleo Crítico")
            self.oleo_uhcd_sobretemp = lei.LeituraModbusBit(self.clp["AD"], REG_AD["Alarme28_11"], descricao="[AD]  UHCD - Sobretemperatura do Óleo - Trip")
            self.sens_fuma_atuado = lei.LeituraModbusBit(self.clp["AD"], REG_AD["Alarme30_00"], descricao="[AD]  Sensor de Fumaça Atuado")
            self.erro_analog_pos_cp1 = lei.LeituraModbusBit(self.clp["AD"], REG_AD["Alarme30_10"], descricao="[AD]  Erro de Leitura na entrada analógica da posição da comporta 01")
            self.erro_analog_pos_cp2 = lei.LeituraModbusBit(self.clp["AD"], REG_AD["Alarme30_11"], descricao="[AD]  Erro de Leitura na entrada analógica da posição da comporta 02")
            self.disj_al_380vca_desl = lei.LeituraModbusBit(self.clp["AD"], REG_AD["Alarme31_00"], descricao="[AD]  Alimentação 380Vca Principal - Disj. Q380.0 Desligado")
            self.disj_al_380vca_incosis = lei.LeituraModbusBit(self.clp["AD"], REG_AD["Alarme31_01"], descricao="[AD]  Alimentação 380Vca Principal - Disj. Q380.0 Inconsistência")
            self.disj_al_380vca_trip = lei.LeituraModbusBit(self.clp["AD"], REG_AD["Alarme31_02"], descricao="[AD]  Alimentação 380Vca Principal - Disj. Q380.0 Trip")
            self.disj_al_cirq_cmd_desl = lei.LeituraModbusBit(self.clp["AD"], REG_AD["Alarme31_05"], descricao="[AD]  Alimentação Circuitos de Comando - Disj. Q24.3 Desligado")


            ## MENSAGEIRO
            self.cp_acion_local = lei.LeituraModbusBit(self.clp["AD"], REG_AD[f"CP_0{self.id}_ACION_LOCAL"], descricao=f"[AD][CP{self.id}] Comporta Acionamento Local")


    cp1 = Comporta(1)
    cp2 = Comporta(2)
    cps: "list[Comporta]" = [cp1, cp2]

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []


    @classmethod
    def controlar_comportas(cls) -> "None":
        """
        Função para verificação de nível e acionamento do controle de Comportas
        Taipa do Canal de Adução.
        """


        logger.debug("")
        logger.debug(f"[AD]  Controlando Comportas...")
        logger.debug(f"[AD]  NÍVEL -> Alvo:                      {cls.cfg['ad_nv_alvo']:0.3f}")
        logger.debug(f"[TDA]          Leitura:                   {tda.TomadaAgua.nivel_montante.valor:0.3f}")
        logger.debug("")

        cls.clp["AD"].write_single_register(REG_AD["CMD_MODO_SP_HABILITAR"], 1)

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
    def verificar_leituras(cls) -> "None":
        """
        Função para verificação de leituras por acionamento temporizado.

        Verifica leituras específcas para acionamento da manuteção. As leituras são disparadas
        em períodos separados por um tempo pré-definido.
        """

        if cls.l_alm_28_b_01.valor:
            logger.warning(f"[AD]  Foi identificada uma Atuação do Relé por Falta de Fase CA. Favor Verificar.")

        if cls.l_alm_28_b_04.valor:
            logger.warning(f"[AD]  Foi identificado que a Pressão do Óleo da UHCD está Baixa. Favor Verificar.")

        if cls.l_alm_28_b_07.valor:
            logger.warning(f"[AD]  Foi identificado que o Filtro de Retorno da UHCD está Sujo. Favor Verificar.")

        if cls.l_alm_28_b_08.valor:
            logger.warning(f"[AD]  Foi identificado que o Nível de Óleo da UHCD está Crítico. Favor Verificar.")

        if cls.l_alm_28_b_10.valor:
            logger.warning(f"[AD]  Foi identificado um Alarme de Sobretemperatura do Óleo da UHCD. Favor Verificar.")

        if cls.l_alm_28_b_11.valor:
            logger.warning(f"[AD]  Foi identificado um Trip de Sobretemperatura do Óleo da UHCD. Favor Verificar.")

        if cls.l_alm_29_b_00.valor:
            logger.warning(f"[AD]  Foi identificado uma Falha no acionamento da Bomba de Óleo 01 da UHCD. Favor Verificar.")

        if cls.l_alm_29_b_01.valor:
            logger.warning(f"[AD]  Foi identificado que o Disjuntor QM1 da Bomba de Óleo 01 da UHCD. Favor Verificar.")

        if cls.l_alm_29_b_02.valor:
            logger.warning(f"[AD]  Foi identificado uma Falha no acionamento da Bomba de Óleo 02 da UHCD. Favor Verificar.")

        if cls.l_alm_29_b_03.valor:
            logger.warning(f"[AD]  Foi identificado que o Disjuntor QM2 da Bomba de Óleo 02 da UHCD. Favor Verificar.")

        if cls.l_alm_29_b_05.valor:
            logger.warning(f"[AD]  Foi identificada uma Falha na Abertura da Comporta 1. Favor Verificar.")

        if cls.l_alm_29_b_06.valor:
            logger.warning(f"[AD]  Foi identificada uma Falha no Fechamento da Comporta 1. Favor Verificar.")

        if cls.l_alm_29_b_09.valor:
            logger.warning(f"[AD]  Foi identificada uma Falha na Abertura da Comporta 2. Favor Verificar.")

        if cls.l_alm_29_b_10.valor:
            logger.warning(f"[AD]  Foi identificada uma Falha na Fechamento da Comporta 2. Favor Verificar.")

        if cls.l_alm_29_b_13.valor:
            logger.warning(f"[AD]  Foi identificada uma Falha no Carregador de Baterias. Favor Verificar.")

        if cls.l_alm_30_b_00.valor:
            logger.warning(f"[AD]  Foi identificada uma Atuação do Sensor de Fumaça. Favor Verificar.")

        if cls.l_alm_30_b_08.valor:
            logger.warning(f"[AD]  Foi identificado um Erro de Leitura na Entrada Analógica da Temperatura do Óleo da UHCD. Favor Verificar.")

        if cls.l_alm_30_b_09.valor:
            logger.warning(f"[AD]  Foi identificado um Erro de Leitura na Entrada Analógica do Nível do Óleo da UHCD. Favor Verificar.")

        if cls.l_alm_30_b_10.valor:
            logger.warning(f"[AD]  Foi identificado um Erro de Leitura na Entrada Analógica da Posição da Comporta 1. Favor Verificar.")

        if cls.l_alm_30_b_11.valor:
            logger.warning(f"[AD]  Foi identificado um Erro de Leitura na Entrada Analógica da Posição da Comporta 2. Favor Verificar.")

        if cls.l_alm_30_b_00.valor:
            logger.warning(f"[AD]  Foi identificado que o Disjuntor de Alimentação 380Vca Principal foi Desligado. Favor Verificar.")

        if cls.l_alm_30_b_01.valor:
            logger.warning(f"[AD]  Foi identificada uma Inconsistência com o Disjuntor de Alimentação 380Vca Principal. Favor Verificar.")

        if cls.l_alm_31_b_02.valor:
            logger.warning(f"[AD]  Foi identificado um Trip no Disjuntor de Alimentação 380Vca Principal. Favor Verificar.")

        if cls.l_alm_31_b_03.valor:
            logger.warning(f"[AD]  Foi identificado que o Disjuntor de Alimentação do Carregador de Baterias foi Desligado. Favor Verificar.")

        if cls.l_alm_31_b_04.valor:
            logger.warning(f"[AD]  Foi identificado que o Disjuntor de Alimentação do Banco de Baterias foi Desligado. Favor Verificar.")

        if cls.l_alm_31_b_05.valor:
            logger.warning(f"[AD]  Foi identificado que o Disjuntor de Alimentação dos Circuitos de Comando foi Desligado. Favor Verificar.")


        if cls.l_uhcd_temp_oleo_h.valor and not d.voip["UHCD_TEMPE_OLEO_H"][0]:
            logger.warning("[AD]  Foi identificado que a temperatura do Óleo da UHCD está Alta. Favor verificar.")
            d.voip["UHCD_TEMPE_OLEO_H"][0] = True
        if not cls.l_uhcd_temp_oleo_h.valor and d.voip["UHCD_TEMPE_OLEO_H"][0]:
            d.voip["UHCD_TEMPE_OLEO_H"][0] = False

        if cls.l_uhcd_temp_oleo_hh.valor and not d.voip["UHCD_TEMPE_OLEO_HH"][0]:
            logger.warning("[AD]  Foi identificado que a temperatura do Óleo da UHCD está Muito Alta. Favor verificar.")
            d.voip["UHCD_TEMPE_OLEO_HH"][0] = True
        if not cls.l_uhcd_temp_oleo_hh.valor and d.voip["UHCD_TEMPE_OLEO_HH"][0]:
            d.voip["UHCD_TEMPE_OLEO_HH"][0] = False

        # if cls.l_uhcd_temp_oleo.valor and not d.voip["UHCD_TEMPERATURA_OLEO"][0]:
        #     logger.warning("[AD]  . Favor verificar.")
        #     d.voip["UHCD_TEMPERATURA_OLEO"][0] = True
        # if not cls.l_uhcd_temp_oleo.valor and d.voip["UHCD_TEMPERATURA_OLEO"][0]:
        #     d.voip["UHCD_TEMPERATURA_OLEO"][0] = False

        # if cls.l_uhcd_nv_oleo.valor and not d.voip["UHCD_NIVEL_OLEO"][0]:
        #     logger.warning("[AD]  . Favor verificar.")
        #     d.voip["UHCD_NIVEL_OLEO"][0] = True
        # if not cls.l_uhcd_nv_oleo.valor and d.voip["UHCD_NIVEL_OLEO"][0]:
        #     d.voip["UHCD_NIVEL_OLEO"][0] = False


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


        cls.l_uhcd_operacional = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["UHCD_OPERACIONAL"], descricao="[AD]  UHCD - Operacional")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_uhcd_operacional, CONDIC_INDISPONIBILIZAR))

        cls.l_pcad_falta_fase = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["PCAD_FALTA_FASE"], descricao="[AD]  PCAD - Falta Fase")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_pcad_falta_fase, CONDIC_INDISPONIBILIZAR))

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


        ## MENSAGEIRO
        cls.l_uhcd_temp_oleo_h = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["UHCD_TEMPE_OLEO_H"], descricao="[AD]  UHCD - Temperatura Óleo Alta")
        cls.l_uhcd_temp_oleo_hh = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["UHCD_TEMPE_OLEO_HH"], descricao="[AD]  UHCD - Temperatura Óleo Muito Alta")
        cls.l_uhcd_temp_oleo = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["UHCD_TEMPERATURA_OLEO"], descricao="[AD]  UHCD - Temperatura Óleo")
        cls.l_uhcd_nv_oleo = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["UHCD_NIVEL_OLEO"], descricao="[AD]  UHCD - Nível Óleo")
