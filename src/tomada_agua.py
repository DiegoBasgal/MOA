__version__ = "0.1"
__author__ = "Diego Basgal", "Henrique Pfeifer"
__credits__ = ["Lucas Lavratti", ...]
__description__ = "Este módulo corresponde a implementação da operação da Tomada da Água."

import pytz
import logging
import traceback

import src.comporta as cp

import src.dicionarios.dict as dct
import src.funcoes.condicionadores as c

from datetime import datetime, timedelta

from src.dicionarios.const import *
from src.funcoes.leitura import *
from src.funcoes.escrita import EscritaModBusBit as ESC

from src.conectores.servidores import Servidores
from src.conectores.banco_dados import BancoDados
from src.funcoes.escrita import EscritaModBusBit as EMB


logger = logging.getLogger("logger")


class TomadaAgua:
    def __init__(self, cfg: "dict"=None, serv: "Servidores"=None, bd: "BancoDados"=None) -> "None":

        # ATRIBUIÇÃO DE VARIÁVEIS

        self.__bd = bd

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
            wordorder=False,
            descricao="[TDA] Leitura Nível Montante"
        )
        self.perda_grade_1 = LeituraModbusFloat(
            self.clp["TDA"],
            REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP1"],
            descricao="[TDA] Leitura Perda Grade CP1"
        )
        self.perda_grade_2 = LeituraModbusFloat(
            self.clp["TDA"],
            REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP2"],
            descricao="[TDA] Leitura Perda Grade CP2"
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
        self.status_limpa_grades = LeituraModbusBit(
            self.clp["TDA"],
            REG_CLP["TDA"]["LG_OPE_MANUAL"],
            descricao="[TDA] Limpa Grades Manual",
        )

        self._modo_lg: "int" = 1

        self.erro_nivel: "float" = 0
        self.erro_nivel_anterior: "float" = 0
        self.nivel_montante_anterior: "float" = 0

        self.condicionadores: "list[c.CondicionadorBase]" = []
        self.condicionadores_essenciais: "list[c.CondicionadorBase]" = []

        # FINALIZAÇÃO __INIT__

        self.iniciar_ultimo_estado_lg()


    def resetar_emergencia(self) -> "bool":
        """
        Função para acionar comandos de reset de TRIPS/Alarmes
        """

        try:
            # res = EMB.escrever_bit(self.clp["TDA"], REG_CLP["TDA"]["VB_CMD_RST_FLH"], valor=1)
            # return res
            return True

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


    def iniciar_ultimo_estado_lg(self) -> "None":
        """
        Função para extrair do banco de dados o último estado registrado do Limpa Grades
        """

        self._modo_lg = self.__bd.get_ultimo_estado_lg()[0]


    def forcar_estado_disponivel_lg(self) -> "None":
        """
        Função para forçar o estado disponível no Limpa Grades.
        """

        self._modo_lg = LG_DISPONIVEL
        self.__bd.update_estado_lg(LG_DISPONIVEL)


    def forcar_estado_indisponivel_lg(self) -> "None":
        """
        Função para forçar o estado indisponível no Limpa Grades.
        """

        self._modo_lg = LG_INDISPONIVEL
        self.__bd.update_estado_lg(LG_INDISPONIVEL)


    def operar_limpa_grades(self) -> "None":
        """
        Função para operar o Limpa Grades.

        Verifica se o Limpa Grades está em modo Manual ou Indisponível e caso esteja,
        avisa o operador e segue com a operação normal.
        Se o Limpa Grades estiver Disponível, extrai o dado com período de acionamento
        do Banco, para comparar com o horário atual. Se a comparação dos horários estiver
        dentro da faixa, inicia a operação.
        """

        perda = self.__bd.get_disparo_perda_lg()
        perda_1 = perda[0]
        perda_2 = perda[1]

        horario = self.__bd.get_horario_operar_lg()
        agora = datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None)

        if perda_1 >= self.perda_grade_1.valor or perda_2 >= self.perda_grade_2.valor:
            logger.debug("")
            logger.debug(f"[TDA] Atenção! Foi identificado um valor de perda nas grades para disparo de Limpeza!")

        elif agora <= horario[0] <= agora + timedelta(minutes=5):
            logger.debug("")
            logger.debug(f"[TDA] Atenção! Enviando comando de Limpeza de Grades por período pré definido!")

            prox_horario = agora + timedelta(days=horario[1], hours=horario[2])
            self.__bd.update_horario_operar_lg([prox_horario.strftime('%Y-%m-%d %H:%M:%S')])

        elif agora + timedelta(minutes=6) > horario[0]:
            logger.debug("")
            logger.debug(f"[TDA] Atenção! Foi identificado que o horário para a limpeza de grades passou do período estipulado.")
            logger.debug(f"[TDA] Reagendando limpeza para o próximo horário...")

            prox_horario = agora + timedelta(days=horario[1], hours=horario[2])
            self.__bd.update_horario_operar_lg([prox_horario.strftime('%Y-%m-%d %H:%M:%S')])
            return

        else:
            return

        if self.verificar_condicoes_lg() and self._modo_lg == LG_DISPONIVEL:
            logger.debug(f"[LG]           Enviando comando:          \"OPERAR LIMPA GRADES\"")
            # ESC.escrever_bit(self.clp["TDA"], REG_CLP["TDA"]["LG_CMD_RST_FLH"], valor=1)
            # ESC.escrever_bit(self.clp["TDA"], REG_CLP["TDA"]["LG_CMD_LIMPEZA"], valor=1)
            return


    def verificar_condicoes_lg(self) -> "bool":
        """
        Função para verificar as pré-condições de operação do Limpa Grades.
        """

        flags = 0

        try:
            if self.l_lg_manual.valor:
                logger.debug("[LG]  Não é possível operar o Limpa Grades em modo \"MANUAL\"")
                flags += 1

            elif self._modo_lg == LG_INDISPONIVEL:
                logger.debug("[LG]  Não é possível operar o Limpa Grades no estado \"INDISPONÍVEL\"")
                flags += 1

            elif not self.l_lg_parado.valor:
                logger.debug("[LG]  O Limpa Grades já está em operação.")
                flags += 1

            elif not self.l_lg_permissao.valor:
                logger.debug("[LG]  Sem Permissão para operar o Limpa Grades.")
                flags += 1


            logger.warning(f"[LG]  Foram identificadas \"{flags}\" condições de bloqueio para operação do Limpa Grades. Favor normalizar.") \
                if flags > 0 else logger.debug("[LG]  Condições de operação validadas.")

            return False if flags > 0 else True

        except Exception:
            logger.exception(f"[LG]  Houve um erro ao verificar as pré-condições do Limpa Grades.")
            logger.debug(f"[LG]  Traceback: {traceback.format_exc()}")
            return False


    def verificar_condicionadores(self) -> "list[c.CondicionadorBase]":
        """
        Função para verificação de TRIPS/Alarmes.

        Verifica os condicionadores ativos e retorna lista com os mesmos para a função de verificação
        da Classe da Usina determinar as ações necessárias.
        """

        autor = 0

        leituras = self.clp["TDA"].read_holding_registers(0, 55)

        if True in (condic.status(leituras) for condic in self.condicionadores_essenciais):
            condics_ativos = [condic for condics in [self.condicionadores_essenciais, self.condicionadores] for condic in condics if condic.ativo]

            logger.debug("")
            if self.condicionadores_ativos == []:
                logger.debug(f"[TDA] Foram detectados Condicionadores ativos na Tomada da Água!")
            else:
                logger.debug(f"[TDA] Ainda há Condicionadores ativos na Tomada da Água!")

            for condic in condics_ativos:
                if condic.teste:
                    logger.debug(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\", Obs.: \"TESTE\"")
                    continue

                elif condic in self.condicionadores_ativos:
                    logger.debug(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    continue

                else:
                    logger.warning(f"[TDA] Descrição: \"{condic.descricao}\", Gravidade: \"{CONDIC_STR_DCT[condic.gravidade] if condic.gravidade in CONDIC_STR_DCT else 'Desconhecida'}\"")
                    self.condicionadores_ativos.append(condic)
                    self.__bd.update_alarmes([
                        datetime.now(pytz.timezone("Brazil/East")).replace(tzinfo=None),
                        condic.gravidade,
                        condic.descricao,
                        "X" if autor == 0 else ""
                    ])
                    sleep(1)
                    autor += 1

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

        leituras = self.clp["TDA"].read_holding_registers(0, 55)

        if not self.l_filtro_limpo_uh.ler(leituras):
            logger.warning("[TDA] O filtro da UH da TDA está sujo. Favor realizar limpeza/troca.")

        if self.l_nv_jusante_cp1.ler(leituras):
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 1. Favor verificar.")

        if self.l_nv_jusante_cp2.ler(leituras):
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante da comporta 2. Favor verificar.")

        if not self.l_ca_tensao.ler(leituras):
            logger.warning("[TDA] Foi dentificado que o CA da tomada da água está sem tensão. Favor verificar.")

        if self.l_lg_manual.ler(leituras):
            logger.warning("[TDA] Foi identificado que o Limpa Grades entrou em operação manual. Favor verificar.")

        if self.l_nv_jusante_grade_cp1.ler(leituras):
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 1. Favor verificar.")

        if self.l_nv_jusante_grade_cp2.ler(leituras):
            logger.warning("[TDA] Houve uma falha no sensor de nível jusante grade da comporta 2. Favor verificar.")

        if self.l_falha_atuada_lg.ler(leituras) and not dct.voip["LG_FALHA_ATUADA"][0]:
            logger.warning("[TDA] Foi identificado que o limpa grades está em falha. Favor verificar.")
            dct.voip["LG_FALHA_ATUADA"][0] = True
        elif not self.l_falha_atuada_lg.ler(leituras) and dct.voip["LG_FALHA_ATUADA"][0]:
            dct.voip["LG_FALHA_ATUADA"][0] = False

        if self.l_falha_ler_nv_montante.ler(leituras) and not dct.voip["FALHA_NIVEL_MONTANTE"][0]:
            logger.warning("[TDA] Houve uma falha na leitura de nível montante. Favor verificar.")
            dct.voip["FALHA_NIVEL_MONTANTE"][0] = True
        elif not self.l_falha_ler_nv_montante.ler(leituras) and dct.voip["FALHA_NIVEL_MONTANTE"][0]:
            dct.voip["FALHA_NIVEL_MONTANTE"][0] = False


    def carregar_leituras(self) -> "None":
        """
        Função para carregamento de leituras necessárias para a operação.
        """

        # CONDICIONADORES ESSENCIAIS
        self.l_sem_emergencia = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["SEM_EMERGENCIA"], invertido=True, descricao="[TDA] Emergência")
        self.condicionadores_essenciais.append(c.CondicionadorBase(self.l_sem_emergencia, CONDIC_NORMALIZAR))


        # CONDICIONADORES
        self.l_ca_tensao = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["CA_COM_TENSAO"], invertido=True, descricao="[TDA] Tensão CA Status ")
        self.condicionadores.append(c.CondicionadorBase(self.l_ca_tensao, CONDIC_NORMALIZAR))

        self.l_falha_ligar_bomba_uh = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["UH_FLH_LIGAR_BOMBA"], descricao="[TDA] UHTDA Falha Ligar Bomba")
        self.condicionadores.append(c.CondicionadorBase(self.l_falha_ligar_bomba_uh, CONDIC_NORMALIZAR))


        self.l_filtro_limpo_uh = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["UH_FILTRO_LIMPO"], invertido=True, descricao="[TDA] UHTDA Filtro Sujo") # 1
        self.l_falha_ler_nv_montante = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["NV_MONTANTE_LER_FLH"], descricao="[TDA] Nível Montante Falha") # 3
        self.l_nv_jusante_cp1 = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_CP1_LER_FLH"], descricao="[TDA] Falha Leitura Nível Justante Comporta 1")
        self.l_nv_jusante_cp2 = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_CP2_LER_FLH"], descricao="[TDA] Falha Leitura Nível Justante Comporta 2")
        self.l_nv_jusante_grade_cp1 = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP1_LER_FLH"], descricao="[TDA] Nível Leitura Justante Grade Comporta 1 Falha")
        self.l_nv_jusante_grade_cp2 = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["NV_JUSANTE_GRADE_CP2_LER_FLH"], descricao="[TDA] Nível Leitura Justante Grade Comporta 2 Falha")

        self.l_lg_permissao = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["LG_PERMISSAO"], descricao="[TDA] Limpa Grades Permissivos") # 24
        self.l_lg_parado = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["LG_PARADO"], descricao="[TDA] Limpa Grades Parado") # 25
        self.l_falha_atuada_lg = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["LG_FLH_ATUADA"], descricao="[TDA] Limpa Grades Falha") # 26
        self.l_lg_manual = LeituraModbusBit(self.clp["TDA"], REG_CLP["TDA"]["LG_OPE_MANUAL"], descricao="[TDA] Limpa Grades Operação Manual") # 27
        # LEITURA PERIÓDICA