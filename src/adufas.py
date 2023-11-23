__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__description__ = "Este módulo corresponde a implementação da operação das Adufas."

import logging
import traceback

import src.tomada_agua as tda
import src.funcoes.leitura as lei
import src.conectores.servidores as serv

from src.dicionarios.reg import *
from src.dicionarios.const import *


logger = logging.getLogger("logger")


class Adufas:

    __split1: "bool" = False
    __split2: "bool" = False

    clp = serv.Servidores.clp

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


        def verificar_operacao(self) -> "bool":
            try:
                self.clp["AD"].write_single_register(REG_AD[f"CP_0{self.id}_POSICAO"], 1)

            except Exception:
                logger.error(f"[AD][CP{self.id}] Não foi possível verificar a operação da Comporta.")
                logger.debug(traceback.format_exc())
                return False


        def enviar_setpoint(self, setpoint: "int") -> "None":
            try:
                logger.debug(f"[AD][CP{self.id}]      Enviando setpoint:         {int(setpoint)}")

                if setpoint > 1:
                    self.setpoint = int(setpoint)
                    res = self.clp["AD"].write_single_register(REG_AD[f"CP_0{self.id}_SP_POS"], int(self.setpoint))
                    return res

            except Exception:
                logger.error(f"[AD][CP{self.id}] Não foi possivel enviar o setpoint para a Comporta.")
                logger.debug(traceback.format_exc())
                return False


    cp1 = Comporta(1)
    cp2 = Comporta(2)

    cps: "list[Comporta]" = [cp1, cp2]


    @classmethod
    def verificar_reservatorio(cls) -> "int":
        tda.TomadaAgua.nivel_montante.valor
        return

    @classmethod
    def calcular_setpoint(cls) -> "float":
        return

    @classmethod
    def distribuir_setpoint(cls, sp_alvo: "int") -> "None":

        cls.__split1 = True if sp > 0 else cls.__split1
        cls.__split2 = True if sp > 0.5 else cls.__split2

        cls.__split2 = False if sp < 0.5 else cls.__split2
        cls.__split1 = False if sp == 0 else cls.__split1

        if len(cls.cps) == 2:
            if cls.__split2:
                cls.cps[0].setpoint = sp * cls.cps[0].setpoint_maximo
                cls.cps[1].setpoint = sp * cls.cps[1].setpoint_maximo

            elif cls.__split1:
                sp = sp * 2 / 1
                cls.cps[0].setpoint = sp * cls.cps[0].setpoint_maximo
                cls.cps[1].setpoint = 0

            else:
                cls.cps[0].setpoint = 0
                cls.cps[1].setpoint = 0

        elif len(cls.cps) == 1:
            if cls.__split1 or cls.__split2:

                sp = sp * 2 / 1
                cls.cps[0].setpoint = sp * cls.cps[0].setpoint_maximo

            else:
                cls.cps[0].setpoint = 0

        return
