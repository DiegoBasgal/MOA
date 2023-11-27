__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__description__ = "Este módulo corresponde a implementação da operação das Adufas."

import logging
import traceback

import src.tomada_agua as tda
import src.funcoes.leitura as lei
import src.funcoes.condicionadores as c
import src.conectores.servidores as serv

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class Adufas:

    __split1: "bool" = False
    __split2: "bool" = False

    clp = serv.Servidores.clp

    condicionadores: "list[c.CondicionadorBase]" = []
    condicionadores_essenciais: "list[c.CondicionadorBase]" = []

    class Comporta:
        def __init__(self, id: "int") -> "None":

            self.__id: "int" = id

            self.clp = serv.Servidores.clp

            self.__leitura_info = lei.LeituraModbus(
                self.clp["AD"],
                REG_AD["CP_01_INFO"],
                op=3,
                descricao=f"[AD][CP{self.id}] Informação"
            )
            self.__leitura_posicao = lei.LeituraModbus(
                self.clp["AD"],
                REG_AD[f"CP_0{self.id}_POSICAO"],
                op=3,
                descricao=f"[AD][CP{self.id}] Leitura Posição"
            )

            self.setpoint: "int" = 0
            self.setpoint_anterior: "int" = 0

            self.espera: "bool" = False
            self.operando: "bool" = False


        @property
        def id(self) -> "int":
            return self.__id

        @property
        def leitura_info(self) -> "float":
            return self.__leitura_info.valor

        @property
        def leitura_posicao(self) -> "int":
            return self.__leitura_posicao.valor


        def enviar_setpoint(self, setpoint: "int") -> "None":
            try:
                logger.debug(f"[AD][CP{self.id}]      Enviando setpoint:         {int(setpoint)}")

                if setpoint > 1:
                    self.setpoint = int(setpoint)
                    self.clp["AD"].write_single_register(REG_AD[f"CP_0{self.id}_SP_POS"], int(self.setpoint))

            except Exception:
                logger.error(f"[AD][CP{self.id}] Não foi possivel enviar o setpoint para a Comporta.")
                logger.debug(traceback.format_exc())


    cp1 = Comporta(1)
    cp2 = Comporta(2)
    cps: "list[Comporta]" = [cp1, cp2]


    @classmethod
    def calcular_setpoint(cls) -> "int":
        tda.TomadaAgua.nivel_montante.valor
        return

    @classmethod
    def distribuir_setpoint(cls, sp_alvo: "int") -> "None":

        cls.__split1 = True if sp > 0 else cls.__split1
        cls.__split2 = True if sp > 0.5 else cls.__split2

        cls.__split2 = False if sp < 0.5 else cls.__split2
        cls.__split1 = False if sp == 0 else cls.__split1

        if len(cls.cps) == 2:
            if cls.__split2:
                cls.cps[0].setpoint = sp * cls.cps[0]
                cls.cps[1].setpoint = sp * cls.cps[1]

            elif cls.__split1:
                sp = sp * 2 / 1
                cls.cps[0].setpoint = sp * cls.cps[0]
                cls.cps[1].setpoint = 0

            else:
                cls.cps[0].setpoint = 0
                cls.cps[1].setpoint = 0

        elif len(cls.cps) == 1:
            if cls.__split1:

                sp = sp * 2 / 1
                cls.cps[0].setpoint = sp * cls.cps[0]

            else:
                cls.cps[0].setpoint = 0


    @classmethod
    def carregar_leituras(cls) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """

        cls.l_alm_28_b_00 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme28_00"], descricao="[AD]  Botão de Emergência Pressionado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_28_b_00, CONDIC_NORMALIZAR))

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

        cls.l_alm_28_b_12 = lei.LeituraModbusBit(cls.clp["AD"], REG_AD["Alarme28_12"], descricao="[AD]  UHCD - Botão de Emergência Pressionado")
        cls.condicionadores.append(c.CondicionadorBase(cls.l_alm_28_b_12, CONDIC_NORMALIZAR))

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

        return