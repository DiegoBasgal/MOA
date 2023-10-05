__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

import logging
import traceback

import src.comporta as cp

import src.dicionarios.dict as dct
import src.funcoes.condicionadores as c

from src.funcoes.leitura import *
from src.dicionarios.const import *

from src.conectores.servidores import Servidores
from src.funcoes.escrita import EscritaModBusBit as EMB

logger = logging.getLogger("logger")

class TomadaAgua:
    def __init__(self, cfg: "dict"=None, serv: "Servidores"=None) -> "None":

        # ATRIBUIÇÃO DE VARIÁVEIS

        self.clp = serv.clp

        self.cfg = cfg
        self.aguardando_reservatorio: "int" = 0

        self.cp: "dict[str, cp.Comporta]" = {}
        self.cp["CP1"] = cp.Comporta(1, serv, self)
        self.cp["CP2"] = cp.Comporta(2, serv, self)

        self.cp["CP1"].comporta_adjacente = self.cp["CP2"]
        self.cp["CP2"].comporta_adjacente = self.cp["CP1"]

        self.nivel_montante = LeituraModbusFloat(
            self.clp['TDA'],
            REG_CLP["TDA"]["NV_MONTANTE"],
            descricao="[TDA] Leitura Nível Montante"
        )
        self.status_limpa_grades = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"]["LG_OPE_MANUAL"],
            descricao="[TDA] Status Limpa Grades",
        )
        self.status_valvula_borboleta = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"]["VB_FECHANDO"],
            descricao="[TDA] Status Válvula Borboleta",
        )
        self.status_unidade_hidraulica = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"]["UH_DISPONIVEL"],
            descricao="[TDA] Status Unidade Hidáulica",
        )

        self.erro_nivel: "float" = 0
        self.erro_nivel_anterior: "float" = 0
        self.nivel_montante_anterior: "float" = 0

        self.condicionadores: "list[c.CondicionadorBase]" = []
        self.condicionadores_essenciais: "list[c.CondicionadorBase]" = []


    def resetar_emergencia(self) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            res = EMB.escrever_bit(self.clp["TDA"], REG_CLP["TDA"]["VB_CMD_RST_FLH"], valor=1)
            return res

        except Exception:
            logger.error("[TDA] Houve um erro ao realizar o Reset de Emergência.")
            logger.debug(f"[TDA] Traceback: {traceback.format_exc()}")

        return False


    def atualizar_montante(self) -> "None":
        """
        Função para atualizar valores anteriores de nível montante e erro de cálculo para
        cálculos futuros de ajuste de potência.
        """

        self.nivel_montante_anterior = self.nivel_montante.valor
        self.erro_nivel_anterior = self.erro_nivel
        self.erro_nivel = self.nivel_montante_anterior - self.cfg["nv_alvo"]


    def verificar_condicionadores(self) -> "list[c.CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        if True in (condic.ativo for condic in self.condicionadores_essenciais):
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.warning(f"[TDA] Foram detectados Condicionadores ativos na Tomada da Água!")

            else:
                logger.info(f"[TDA] Ainda há Condicionadores ativos na Tomada da Água!")

            for condic in condics_ativos:
                if condic in self.condicionadores_ativos:
                    logger.debug(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue
                else:
                    logger.warning(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)

            logger.debug("")
            return condics_ativos

        else:
            self.condicionadores_ativos = []
            return []


    def verificar_leituras(self) -> "None":
        """
        Função para verificação de leituras por acionamento temporizado.

        Verifica leituras específcas para acionamento da manuteção. As leituras são disparadas
        em períodos separados por um tempo pré-definido.
        """
        return

        if not self.l_filtro_limpo_uh.valor:
            logger.warning("[TDA] O filtro da UH da TDA está sujo. Favor realizar limpeza/troca.")

        if self.l_nvl_jusante_cp1.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 1. Favor verificar.")

        if self.l_nv_jusante_cp2.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 2. Favor verificar.")

        if not self.l_ca_tensao.valor:
            logger.warning("[TDA] Foi dentificado que o CA da tomada da água está sem tensão. Favor verificar.")

        if self.l_lg_manual.valor:
            logger.warning("[TDA] Foi identificado que o Limpa Grades entrou em operação manual. Favor verificar.")

        if self.l_nv_jusante_grade_cp1.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 1. Favor verificar.")

        if self.l_nv_jusante_grade_cp2.valor:
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 2. Favor verificar.")

        if self.l_falha_atuada_lg.valor and not dct.voip["LG_FALHA_ATUADA"][0]:
            logger.warning("[TDA] Foi identificado que o limpa grades está em falha. Favor verificar.")
            dct.voip["LG_FALHA_ATUADA"][0] = True
        elif not self.l_falha_atuada_lg.valor and dct.voip["LG_FALHA_ATUADA"][0]:
            dct.voip["LG_FALHA_ATUADA"][0] = False

        if self.l_falha_ler_nv_montante.valor and not dct.voip["FALHA_NIVEL_MONTANTE"][0]:
            logger.warning("[TDA] Houve uma falha na leitura de nível montante. Favor verificar.")
            dct.voip["FALHA_NIVEL_MONTANTE"][0] = True
        elif not self.l_falha_ler_nv_montante.valor and dct.voip["FALHA_NIVEL_MONTANTE"][0]:
            dct.voip["FALHA_NIVEL_MONTANTE"][0] = False


    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """
        return
        # CONDICIONADORES ESSENCIAIS
        # Normalizar
        self.l_sem_emergencia = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["SEM_EMERGENCIA"], invertido=True, descricao="[TDA] Emergência")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_sem_emergencia, CONDIC_NORMALIZAR))

        # CONDICIONADORES
        # Normalizar
        self.l_ca_tensao = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["CA_COM_TENSAO"], invertido=True, descricao="[TDA] Tensão CA Status ")
        self.condicionadores.append(c.CondicionadorBase(self.l_ca_tensao, CONDIC_NORMALIZAR))

        self.l_falha_ligar_bomba_uh = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["UH_FLH_LIGAR_BOMBA"], descricao="[TDA] UHTDA Falha Ligar Bomba")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_ligar_bomba_uh, CONDIC_NORMALIZAR))

        # LEITURA PERIÓDICA
        self.l_falha_atuada_lg = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["LG_FLH_ATUADA"], descricao="[TDA] Limpa Grades Falha")
        self.l_falha_ler_nv_montante = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["NV_MONTANTE_LER_FLH"], descricao="[TDA] Nível Montante Falha")
        self.l_filtro_limpo_uh = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["UH_FILTRO_LIMPO"], invertido=True, descricao="[TDA] UHTDA Filtro Sujo")
        self.l_lg_manual = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["LG_OPE_MANUAL"], descricao="[TDA] Limpa Grades Operação Manual")
        self.l_nvl_jusante_cp1 = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_CP1"], descricao="[TDA] Nível Justante Comporta 1")
        self.l_nv_jusante_cp2 = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_CP2"], descricao="[TDA] Nível Justante Comporta 2")
        self.l_nv_jusante_grade_cp1 = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP1_LER_FLH"], descricao="[TDA] Nível Justante Comporta 1 Falha")
        self.l_nv_jusante_grade_cp2 = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP2_LER_FLH"], descricao="[TDA] Nível Justante Comporta 2 Falha")
