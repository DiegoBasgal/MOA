import pytz
import logging
import traceback

import src.mensageiro.dict as vd
import src.dicionarios.dict as d

from time import time
from datetime import datetime

from src.funcoes.leitura import *
from src.Condicionadores import *
from src.dicionarios.reg import *
from src.dicionarios.const import *

from src.banco_dados import BancoDados


logger = logging.getLogger("logger")

class OcorrenciasUsn:
    def __init__(self, clp: "dict[str, ModbusClient]"=None, db: "BancoDados"=None) -> "None":

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__db = db
        self.__clp = clp


        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS

        self._condicionadores: "list[CondicionadorBase]" = []
        self._condicionadores_essenciais: "list[CondicionadorBase]" = []


        # FINALIZAÇÃO DO __INIT__

        self.carregar_leituras()

    @property
    def condicionadores(self) -> "list[CondicionadorBase]":
        # PROPRIEDADE -> Retrona a lista de condicionadores da Usina.

        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[CondicionadorBase]") -> None:
        # SETTER -> Atrubui a nova lista de condicionadores da Usina.

        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        # PROPRIEDADE -> Retrona a lista de condicionadores essenciais da Usina.

        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]") -> None:
        # SETTER -> Atrubui a nova lista de condicionadores essenciais da Usina.

        self._condicionadores_essenciais = var

    def verificar_condicionadores(self) -> int:
        """
        Função para a verificação de acionamento de condicionadores e determinação
        de gravidade.

        Itera sobre a lista de condicionadores da Usina e verifica se algum está
        ativo. Caso esteja, verifica o nível de gravidade e retorna o valor para
        a determinação do passo seguinte.
        Caso não haja nenhum condicionador ativo, apenas retorna o valor de ignorar.
        """

        flag = CONDIC_IGNORAR
        v = []

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condicionadores_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            for condic in condicionadores_ativos:
                if condic.gravidade == CONDIC_NORMALIZAR:
                    flag = CONDIC_NORMALIZAR
                elif condic.gravidade == CONDIC_INDISPONIBILIZAR:
                    flag = CONDIC_INDISPONIBILIZAR

            logger.debug("")
            logger.warning(f"[OCO-USN] Foram detectados condicionadores ativos na Usina:")
            [logger.warning(f"[OCO-USN] Descrição: \"{condic.descr}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"") for condic in condicionadores_ativos]
            logger.debug("")

            for condic in condicionadores_ativos:
                v = [datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr]
                self.__db.update_alarmes(v)

            return flag
        return flag

    def leitura_temporizada(self) -> None:
        """
        Função para consulta de acionamentos da usina e avisos através do mecanismo
        de acionamento temporizado.
        """

        return

    def carregar_leituras(self) -> None:
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Usina.
        """
        return


class OcorrenciasUg:
    def __init__(self, ug, clp: "dict[str, ModbusClient]"=None, db: BancoDados=None):

        # ATRIBUIÇÃO DE VARIÁVEIS PRIVADAS

        self.__ug = ug
        self.__db = db
        self.__clp = clp

        # ATRIBUIÇÃO DE VARIÁVEIS PROTEGIDAS

        self._temperatura_base: int = 100
        self._temperatura_limite: int = 200

        self._condicionadores: "list[CondicionadorBase]" = []
        self._condicionadores_essenciais: "list[CondicionadorBase]" = []

        self._leitura_dict: "dict[str, LeituraModbus]" = {}
        self._condic_dict: "dict[str, CondicionadorBase]" = {}


        # ATRIBUIÇÃO DE VARIÁVEIS PÚBLICAS

        self.leitura_voip: "dict[str, LeituraModbus]" = {}


        # FINALIZAÇÃO DO __INIT__

        self.carregar_leituras()

    @property
    def temperatura_base(self) -> "int":
        # PROPRIEDADE -> Retrona o valor de temperaturas base da Unidade.

        return self._temperatura_base

    @temperatura_base.setter
    def temperatura_base(self, var: "int") -> None:
        # SETTER -> Atrubui o novo valor de temperaturas base da Unidade.

        self._temperatura_base = var

    @property
    def temperatura_limite(self) -> "int":
        # PROPRIEDADE -> Retrona o valor de temperaturas limite da Unidade.

        return self._temperatura_limite

    @temperatura_limite.setter
    def temperatura_limite(self, var: "int") -> None:
        # SETTER -> Atrubui o novo valor de temperaturas limite da Unidade.

        self._temperatura_limite = var

    @property
    def condic_dict(self) -> "dict[str, CondicionadorExponencial]":
        # PROPRIEDADE -> Retrona o dicionário de condicionadores da Unidade.

        return self._condic_dict

    @condic_dict.setter
    def condic_dict(self, var: "dict[str, CondicionadorExponencial]") -> None:
        # SETTER -> Atrubui o novo dicionário de condicionadores da Unidade.

        self._condic_dict = var

    @property
    def leitura_dict(self) -> "dict[str, LeituraModbus]":
        # PROPRIEDADE -> Retrona o dicionário de leituras da Unidade.

        return self._leitura_dict

    @leitura_dict.setter
    def leitura_dict(self, var: "dict[str, LeituraModbus]") -> None:
        # SETTER -> Atrubui o novo dicionário de leituras da Unidade.

        self._leitura_dict = var

    @property
    def condicionadores(self) -> "list[CondicionadorBase]":
        # PROPRIEDADE -> Retrona a lista de condicionadores da Unidade.

        return self._condicionadores

    @condicionadores.setter
    def condicionadores(self, var: "list[CondicionadorBase]") -> None:
        # SETTER -> Atrubui a nova lista de condicionadores da Unidade.

        self._condicionadores = var

    @property
    def condicionadores_essenciais(self) -> "list[CondicionadorBase]":
        # PROPRIEDADE -> Retrona a lista de condicionadores essenciais da Unidade.

        return self._condicionadores_essenciais

    @condicionadores_essenciais.setter
    def condicionadores_essenciais(self, var: "list[CondicionadorBase]") -> None:
        # SETTER -> Atrubui a nova lista de condicionadores essenciais da Unidade.

        self._condicionadores_essenciais = var

    def verificar_condicionadores(self) -> "int":
        """
        Função para a verificação de acionamento de condicionadores e determinação
        de gravidade.

        Itera sobre a lista de condicionadores da Unidade e verifica se algum está
        ativo. Caso esteja, verifica o nível de gravidade e retorna o valor para
        a determinação do passo seguinte.
        Caso não haja nenhum condicionador ativo, apenas retorna o valor de ignorar.
        """

        flag = CONDIC_IGNORAR
        v = []

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condicionadores_ativos = [x for y in [self.condicionadores_essenciais, self.condicionadores] for x in y if x.ativo]

            for condic in condicionadores_ativos:
                if condic.gravidade == CONDIC_NORMALIZAR:
                    flag = CONDIC_NORMALIZAR
                elif condic.gravidade == CONDIC_AGUARDAR:
                    flag = CONDIC_AGUARDAR
                elif condic.gravidade == CONDIC_INDISPONIBILIZAR:
                    flag = CONDIC_INDISPONIBILIZAR

            logger.debug("")
            logger.warning(f"[OCO-UG{self.__ug.id}] Foram detectados condicionadores ativos na UG:")
            [logger.warning(f"[OCO-UG{self.__ug.id}] Descrição: \"{condic.descr}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"") for condic in condicionadores_ativos]
            logger.debug("")

            for condic in condicionadores_ativos:
                v = [datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None), condic.gravidade, condic.descr]
                self.__db.update_alarmes(v)

            return flag
        return flag

    def atualizar_limites_condicionadores(self, parametros) -> "None":
        """
        Função para extração de valores do Banco de Dados da Interface WEB e atribuição
        de novos limites de operação de condicionadores.
        """

        try:
            self.condic_dict[f"pressao_cx_espiral_ug{self.__ug.id}"].valor_base = float(parametros[f"alerta_caixa_espiral_ug{self.__ug.id}"])
            self.condic_dict[f"pressao_cx_espiral_ug{self.__ug.id}"].valor_limite = float(parametros[f"limite_caixa_espiral_ug{self.__ug.id}"])

        except Exception:
            logger.error(f"[OCO-UG{self.__ug.id}] Houve um erro ao atualizar os limites de temperaturas dos condicionadores.")
            logger.debug(f"[OCO-UG{self.__ug.id}] Traceback: {traceback.format_exc()}")

    def controle_limites_operacao(self) -> "None":
        """
        Função para verificação de limites de operação da Unidade.

        Verifica os valores base e limite da Unidade, pré-determinados na interface
        WEB, e avisa o operador caso algum valor ultrapasse o estipulado.
        """

        ld = self.leitura_dict
        cd = self.condic_dict

        if ld[f"pressao_cx_espiral_ug{self.__ug.id}"].valor <= cd[f"pressao_cx_espiral_ug{self.__ug.id}"].valor_base and ld[f"pressao_cx_espiral_ug{self.__ug.id}"].valor != 0 and self.__ug.etapa_atual == UG_SINCRONIZADA:
            logger.debug(f"[OCO-UG{self.__ug.id}] A pressão Caixa Espiral da UG passou do valor base! ({cd[f'pressao_cx_espiral_ug{self.__ug.id}'].valor_base:03.2f} KGf/m2) | Leitura: {ld[f'pressao_cx_espiral_ug{self.__ug.id}'].valor:03.2f}")

        if ld[f"pressao_cx_espiral_ug{self.__ug.id}"].valor <= cd[f"pressao_cx_espiral_ug{self.__ug.id}"].valor_limite and ld[f"pressao_cx_espiral_ug{self.__ug.id}"].valor != 0 and self.__ug.etapa_atual == UG_SINCRONIZADA:
            logger.debug(f"[OCO-UG{self.__ug.id}] A pressão Caixa Espiral da UG está muito próxima do limite! ({cd[f'pressao_cx_espiral_ug{self.__ug.id}'].valor_limite:03.2f} KGf/m2) | Leitura: {ld[f'pressao_cx_espiral_ug{self.__ug.id}'].valor:03.2f} KGf/m2")


    def leitura_temporizada(self) -> "None":
        """
        Função para consulta de acionamentos da Unidade e avisos através do mecanismo
        de acionamento temporizado.
        """

        return

    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de todas as leituras para acionamentos de avisos
        e emergências da Unidade.
        """

        ### CONDICIONADORES ESSENCIAIS
        self.leitura_dict[f"pressao_cx_espiral_ug{self.__ug.id}"] = LeituraModbus(f"[UG{self.__ug.id}] Caixa Espiral", self.__clp[f"UG{self.__ug.id}"], REG[f"UG{self.__ug.id}_EA_PressK1CaixaExpiral_MaisCasas"], escala=0.01, op=4)
        self.condic_dict[f"pressao_cx_espiral_ug{self.__ug.id}"] = CondicionadorExponencialReverso(self.leitura_dict[f"pressao_cx_espiral_ug{self.__ug.id}"].descr, CONDIC_INDISPONIBILIZAR, self.leitura_dict[f"pressao_cx_espiral_ug{self.__ug.id}"], valor_base=16.5, valor_limite=14)

        return